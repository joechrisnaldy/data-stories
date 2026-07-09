"""Model for the Sberbank Russian Housing Market competition (metric: RMSLE).

Goal: predict `price_doc` for the 7,662 test rows.

Design:
  - Target is log1p(price_doc): RMSLE on prices == RMSE on log1p, so a squared-error
    learner in log space optimizes the competition metric directly.
  - Model is sklearn's HistGradientBoostingRegressor: strong on tabular data and it
    handles this dataset's heavy missingness natively (no imputation to get wrong).
  - Validation is time-based (train on earlier sales, hold out the newest ~15%),
    because the test set is the future. A random split would flatter the score.

This is the tuned model. It started as a plain baseline (RMSLE 0.2709) and folds in
four improvements, each validated in isolation on the same time-based holdout before
being combined (see model/variants/ for the individual experiments and ablations):

  1. Robust cleaning + one-sided target de-noising  (0.2709 -> 0.2665 alone)
     Fix swapped life_sq/full_sq, blank more impossible attributes, and drop the
     cheapest ~1% price-per-m2 rows from TRAINING only (residual mislabeled sales,
     the same failure mode as the 1M/2M declared prices). One-sided on purpose:
     dropping the expensive-per-m2 tail removes genuine luxury flats and hurts.
  2. Leak-free sub_area encodings                   (0.2709 -> 0.2678 alone)
     Frequency (count) encoding plus a smoothed mean-log-price encoding fit on the
     training slice only, then mapped onto the holdout and test.
  3. Property feature engineering                    (0.2709 -> 0.2688 alone)
     11 deterministic ratios from existing size/floor/room/year columns.
  4. Hyperparameter tuning                           (0.2709 -> 0.2695 alone)
     max_features=0.8 (per-split column subsampling) and max_iter=1000.

Leakage control when combined: the time split is taken before any row is dropped, so
the holdout is byte-identical to the baseline and the CV stays comparable; de-noising
and the target encoding are both fit on the training slice only and mapped outward.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = BASE / "model" / "submission.csv"

MACRO_COLS = ["usdrub", "cpi", "oil_urals", "mortgage_rate", "salary", "deposits_rate"]
RANDOM_STATE = 42
PSQM_LO_Q = 0.01     # drop the cheapest 1% price-per-m2 rows from TRAIN (one-sided)
TE_SMOOTHING = 200   # target-encoding shrinkage toward the global mean
BASELINE_RMSLE = 0.2709


def rmsle_from_log(y_true_log, y_pred_log):
    """Both inputs are already log1p-transformed, so this is RMSE in log space."""
    return np.sqrt(mean_squared_error(y_true_log, y_pred_log))


def clean(df):
    """Robust size/attribute fixes applied identically to train and test."""
    df = df.copy()
    # Swapped life_sq/full_sq: both plausible areas but life_sq > full_sq means the
    # columns were entered in the wrong order. Swap them back.
    swap = (df.life_sq > df.full_sq) & df.full_sq.notna() & df.life_sq.notna() \
        & df.full_sq.between(1, 1000) & df.life_sq.between(1, 1000)
    tmp = df.loc[swap, "full_sq"].to_numpy()
    df.loc[swap, "full_sq"] = df.loc[swap, "life_sq"].to_numpy()
    df.loc[swap, "life_sq"] = tmp
    # full_sq==0/tiny are data errors: fall back to life_sq, else mark missing.
    bad_full = df.full_sq < 5
    df.loc[bad_full, "full_sq"] = df.loc[bad_full, "life_sq"]
    df.loc[df.full_sq < 5, "full_sq"] = np.nan
    df.loc[df.full_sq > 400, "full_sq"] = np.nan
    # life_sq sanity: tiny junk or (still) larger than full_sq -> missing.
    df.loc[df.life_sq < 2, "life_sq"] = np.nan
    df.loc[df.life_sq > df.full_sq * 1.5, "life_sq"] = np.nan
    # Blank impossible categorical / count / year attributes.
    df.loc[~df.build_year.between(1860, 2020), "build_year"] = np.nan
    df.loc[~df.state.between(1, 4), "state"] = np.nan
    df.loc[(df.num_room < 1) | (df.num_room > 15), "num_room"] = np.nan
    df.loc[df.kitch_sq >= df.full_sq, "kitch_sq"] = np.nan
    df.loc[df.kitch_sq > 400, "kitch_sq"] = np.nan
    return df


def add_date_and_macro(df, macro):
    """Baseline date parts + six macro series by month. (Month-level macro deltas
    and rent series were tested and hurt the holdout, so they are left out.)"""
    df = df.copy()
    df["year"] = df.timestamp.dt.year
    df["month"] = df.timestamp.dt.month
    df["month_key"] = df.timestamp.dt.to_period("M").dt.to_timestamp()
    m = macro.set_index("timestamp")[MACRO_COLS].resample("MS").mean().reset_index()
    m = m.rename(columns={"timestamp": "month_key"})
    return df.merge(m, on="month_key", how="left").drop(columns=["month_key"])


def add_property_features(df):
    """Cheap deterministic features from existing columns (no macro, no target)."""
    df = df.copy()
    full, life, kitch = df["full_sq"], df["life_sq"], df["kitch_sq"]
    floor, max_floor, num_room = df["floor"], df["max_floor"], df["num_room"]

    def safe_div(numer, denom):
        out = numer / denom.replace(0, np.nan)
        return out.replace([np.inf, -np.inf], np.nan)

    df["apartment_age"] = (df["year"] - df["build_year"]).clip(lower=0, upper=150)
    df["extra_sq"] = full - life
    df["life_ratio"] = safe_div(life, full)
    df["kitch_ratio"] = safe_div(kitch, full)
    df["kitch_to_life"] = safe_div(kitch, life)
    df["room_size"] = safe_div(full, num_room)
    df["living_room_size"] = safe_div(life, num_room)
    df["floor_ratio"] = safe_div(floor, max_floor)
    df["floors_from_top"] = max_floor - floor
    top = (floor == max_floor).astype(float)
    top[floor.isna() | max_floor.isna()] = np.nan
    df["is_top_floor"] = top
    ground = (floor <= 1).astype(float)
    ground[floor.isna()] = np.nan
    df["is_ground_floor"] = ground
    return df


def add_freq_encoding(train, test):
    """sub_area frequency (count) encoding. Target-free, so no leakage."""
    freq = train["sub_area"].value_counts()
    train["sub_area_freq"] = train["sub_area"].map(freq).astype("float64")
    test["sub_area_freq"] = test["sub_area"].map(freq).fillna(0.0).astype("float64")


def psqm_keep_mask(price_doc, full_sq, lo_q=PSQM_LO_Q):
    """Rows to KEEP by price-per-m2 (one-sided low-tail drop). Rows with unknown
    psqm (full_sq missing) are always kept. The bound is learned from the data
    passed in, so callers pass the training slice only (never test/holdout)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        psqm = np.asarray(price_doc, float) / np.asarray(full_sq, float)
    finite = np.isfinite(psqm)
    lo = float(np.quantile(psqm[finite], lo_q))
    keep = (~finite) | (finite & (psqm >= lo))
    return keep, lo


def build_features(train, test):
    """Ordinal-encode every non-numeric column (categories from train+test together)
    and return aligned numeric matrices. pandas 3.0 reads text as `str`, not
    `object`, so we test with is_numeric_dtype."""
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


def make_xy(train, test, y, fit_idx):
    """Build model matrices, adding a leak-free sub_area target encoding fit on
    `fit_idx` only. Works on copies so it can be called per split without state."""
    tr, te = train.copy(), test.copy()
    global_mean = float(y[fit_idx].mean())
    fdf = pd.DataFrame({"sub_area": train["sub_area"].to_numpy()[fit_idx], "y": y[fit_idx]})
    agg = fdf.groupby("sub_area")["y"].agg(["mean", "count"])
    smooth = (agg["count"] * agg["mean"] + TE_SMOOTHING * global_mean) / \
             (agg["count"] + TE_SMOOTHING)
    tr["sub_area_te"] = tr["sub_area"].map(smooth).fillna(global_mean).astype("float64")
    te["sub_area_te"] = te["sub_area"].map(smooth).fillna(global_mean).astype("float64")
    return build_features(tr, te)


def make_model():
    return HistGradientBoostingRegressor(
        loss="squared_error", learning_rate=0.05, max_iter=1000,
        max_leaf_nodes=31, min_samples_leaf=40, l2_regularization=1.0,
        max_features=0.8, early_stopping=True, validation_fraction=0.1,
        random_state=RANDOM_STATE)


def main():
    train = pd.read_csv(DATA / "train.csv", parse_dates=["timestamp"])
    test = pd.read_csv(DATA / "test.csv", parse_dates=["timestamp"])
    macro = pd.read_csv(DATA / "macro.csv", parse_dates=["timestamp"])

    n0 = len(train)
    train = train[~train.price_doc.isin([1_000_000, 2_000_000])].reset_index(drop=True)
    print(f"train rows: {n0:,} -> {len(train):,} after dropping 1M/2M declared prices")

    train = add_property_features(add_date_and_macro(clean(train), macro))
    test = add_property_features(add_date_and_macro(clean(test), macro))
    add_freq_encoding(train, test)

    y = np.log1p(train.price_doc.values)
    price, full_sq = train.price_doc.values, train.full_sq.values

    # Time split first (before any row drop) so the holdout matches the baseline.
    order = train.timestamp.argsort().values
    cut = int(len(order) * 0.85)
    tr_idx, va_idx = order[:cut], order[cut:]

    # De-noise the TRAINING portion only; the holdout is never touched.
    keep_tr, lo = psqm_keep_mask(price[tr_idx], full_sq[tr_idx])
    tr_idx_dn = tr_idx[keep_tr]
    print(f"psqm de-noise: drop psqm < {lo:,.0f} RUB/m2, "
          f"{len(tr_idx) - len(tr_idx_dn):,} of {len(tr_idx):,} train rows; "
          f"holdout intact ({len(va_idx):,})")

    # Validation: target encoding fit on the de-noised training slice only.
    X, _, feat_cols = make_xy(train, test, y, fit_idx=tr_idx_dn)
    print(f"features: {len(feat_cols)}")
    va_pred = make_model().fit(X.iloc[tr_idx_dn], y[tr_idx_dn]).predict(X.iloc[va_idx])
    cv = rmsle_from_log(y[va_idx], va_pred)
    print(f"\nvalidation RMSLE (time-based holdout): {cv:.4f}")
    print(f"baseline: {BASELINE_RMSLE}  |  delta: {cv - BASELINE_RMSLE:+.4f} "
          f"({'IMPROVED' if cv < BASELINE_RMSLE else 'no improvement'})")

    # Final refit: de-noise on the full train, target-encode on the survivors, predict.
    keep_all, _ = psqm_keep_mask(price, full_sq)
    Xf, Xf_test, _ = make_xy(train, test, y, fit_idx=np.where(keep_all)[0])
    model = make_model().fit(Xf.iloc[keep_all], y[keep_all])
    pred = np.clip(np.expm1(model.predict(Xf_test)), 1e5, None)

    sub = pd.DataFrame({"id": test.id, "price_doc": pred})
    sub.to_csv(OUT, index=False)
    print(f"\nwrote {OUT.relative_to(BASE)}  ({len(sub):,} rows)")
    print(sub.price_doc.describe().apply(lambda v: f"{v:,.0f}").to_string())


if __name__ == "__main__":
    main()
