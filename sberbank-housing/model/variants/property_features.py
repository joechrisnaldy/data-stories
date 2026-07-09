"""Variant: property_features.

Copy of the baseline pipeline (model/train_predict.py) with ONE change: engineer
extra property features from EXISTING columns only (no macro, no target). Everything
else -- data loading, dropping 1M/2M declared-price rows from TRAIN, log1p target,
and the time-based validation (sort by timestamp, newest ~15% holdout) -- is byte-for-
byte identical to the baseline so the CV number stays comparable.

The new features are cheap deterministic transforms of size/floor/room/year columns.
None of them touch price_doc, so there is no target-leakage risk (they are pure
functions of input columns and can safely be computed on train and test alike).

Divide-by-zero and out-of-range results are replaced with NaN, which
HistGradientBoostingRegressor handles natively.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

BASE = Path(__file__).resolve().parent.parent.parent
DATA = BASE / "data"
OUT = BASE / "model" / "submission.csv"  # NOTE: not written in this variant.

MACRO_COLS = ["usdrub", "cpi", "oil_urals", "mortgage_rate", "salary", "deposits_rate"]
RANDOM_STATE = 42


def rmsle_from_log(y_true_log, y_pred_log):
    """Both inputs are already log1p-transformed, so this is RMSE in log space."""
    return np.sqrt(mean_squared_error(y_true_log, y_pred_log))


def clean(df):
    """Light, defensible fixes applied identically to train and test."""
    df = df.copy()
    bad_full = df.full_sq < 5
    df.loc[bad_full, "full_sq"] = df.loc[bad_full, "life_sq"]
    df.loc[df.full_sq < 5, "full_sq"] = np.nan
    df.loc[df.full_sq > 400, "full_sq"] = np.nan
    df.loc[df.life_sq > df.full_sq * 1.5, "life_sq"] = np.nan
    df.loc[~df.build_year.between(1860, 2020), "build_year"] = np.nan
    df.loc[df.kitch_sq > df.full_sq, "kitch_sq"] = np.nan
    df.loc[~df.state.between(1, 4), "state"] = np.nan
    return df


def add_date_and_macro(df, macro):
    df = df.copy()
    df["year"] = df.timestamp.dt.year
    df["month"] = df.timestamp.dt.month
    df["month_key"] = df.timestamp.dt.to_period("M").dt.to_timestamp()
    m = macro.set_index("timestamp")[MACRO_COLS].resample("MS").mean().reset_index()
    m = m.rename(columns={"timestamp": "month_key"})
    return df.merge(m, on="month_key", how="left").drop(columns=["month_key"])


def add_property_features(df):
    """Derive cheap property features from existing columns (no macro, no target).

    All ratios are computed as float and any inf produced by a zero denominator is
    turned into NaN. Boolean flags are computed as float so that rows with a missing
    input become NaN rather than a misleading False.
    """
    df = df.copy()

    full = df["full_sq"]
    life = df["life_sq"]
    kitch = df["kitch_sq"]
    floor = df["floor"]
    max_floor = df["max_floor"]
    num_room = df["num_room"]

    def safe_div(numer, denom):
        # Guard divide-by-zero: 0-denominators yield inf/-inf, which we map to NaN.
        out = numer / denom.replace(0, np.nan)
        return out.replace([np.inf, -np.inf], np.nan)

    # Apartment age at sale time; clip to a sane range, keep NaN where build_year unknown.
    df["apartment_age"] = (df["year"] - df["build_year"]).clip(lower=0, upper=150)

    # Size-derived features.
    df["extra_sq"] = full - life                      # non-living area (halls, walls, etc.)
    df["life_ratio"] = safe_div(life, full)           # share of area that is living space
    df["kitch_ratio"] = safe_div(kitch, full)         # kitchen share of total area
    df["kitch_to_life"] = safe_div(kitch, life)       # kitchen relative to living space
    df["room_size"] = safe_div(full, num_room)        # avg area per room
    df["living_room_size"] = safe_div(life, num_room)  # avg living area per room

    # Floor-derived features.
    df["floor_ratio"] = safe_div(floor, max_floor)    # relative height in the building
    df["floors_from_top"] = max_floor - floor         # how many floors above this unit

    # Boolean position flags, kept as float so missing inputs propagate to NaN.
    top = (floor == max_floor).astype(float)
    top[floor.isna() | max_floor.isna()] = np.nan
    df["is_top_floor"] = top

    ground = (floor <= 1).astype(float)
    ground[floor.isna()] = np.nan
    df["is_ground_floor"] = ground

    return df


def build_features(train, test):
    """Return X_train, X_test with identical, model-ready columns."""
    drop = {"id", "price_doc", "timestamp"}
    cat_cols = [c for c in train.columns
                if c not in drop and not pd.api.types.is_numeric_dtype(train[c])]
    for c in cat_cols:
        cats = pd.Categorical(pd.concat([train[c], test[c]], ignore_index=True)).categories
        train[c] = pd.Categorical(train[c], categories=cats).codes  # unseen/NaN -> -1
        test[c] = pd.Categorical(test[c], categories=cats).codes

    feat_cols = [c for c in train.columns if c not in drop and c in test.columns
                 and pd.api.types.is_numeric_dtype(train[c])]
    return train[feat_cols], test[feat_cols], feat_cols


def main():
    train = pd.read_csv(DATA / "train.csv", parse_dates=["timestamp"])
    test = pd.read_csv(DATA / "test.csv", parse_dates=["timestamp"])
    macro = pd.read_csv(DATA / "macro.csv", parse_dates=["timestamp"])

    # Drop the declared-price fakes from training only (mislabeled targets).
    n0 = len(train)
    train = train[~train.price_doc.isin([1_000_000, 2_000_000])].reset_index(drop=True)
    print(f"train rows: {n0:,} -> {len(train):,} after dropping 1M/2M declared prices")

    train = add_property_features(add_date_and_macro(clean(train), macro))
    test = add_property_features(add_date_and_macro(clean(test), macro))

    y = np.log1p(train.price_doc.values)
    X, X_test, feat_cols = build_features(train, test)
    print(f"features: {len(feat_cols)}  |  test rows: {len(X_test):,}")

    # Time-based validation: newest ~15% of sales as the holdout (identical to baseline).
    order = train.timestamp.argsort().values
    cut = int(len(order) * 0.85)
    tr_idx, va_idx = order[:cut], order[cut:]

    def make_model():
        return HistGradientBoostingRegressor(
            loss="squared_error", learning_rate=0.05, max_iter=700,
            max_leaf_nodes=31, min_samples_leaf=40, l2_regularization=1.0,
            early_stopping=True, validation_fraction=0.1, random_state=RANDOM_STATE)

    val_model = make_model().fit(X.iloc[tr_idx], y[tr_idx])
    va_pred = val_model.predict(X.iloc[va_idx])
    rmsle = rmsle_from_log(y[va_idx], va_pred)
    print(f"\nvalidation RMSLE (time-based holdout): {rmsle:.4f}")
    print(f"baseline RMSLE: 0.2709  |  delta: {rmsle - 0.2709:+.4f}")


if __name__ == "__main__":
    main()
