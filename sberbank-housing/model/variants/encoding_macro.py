"""Variant: encoding_macro.

Baseline pipeline (model/train_predict.py) kept EXACTLY the same:
  - same data loading, same drop of 1M/2M declared-price rows from TRAIN,
  - same log1p(price_doc) target,
  - same model (HistGradientBoostingRegressor, identical hyperparameters),
  - same time-based validation (sort by timestamp, newest ~15% as holdout,
    RMSLE = RMSE in log space).

Assigned change (non-leaky categorical encoding + macro enrichment):
  1. Frequency (count) encoding of sub_area  -> `sub_area_freq`.
     Uses NO target, so it cannot leak price. Counts are learned on TRAIN only
     and mapped onto test (unseen district -> 0). Robust improvement on its own.
  2. LEAK-FREE mean-log-price target encoding of sub_area -> `sub_area_te`.
     The per-district mean of the log1p target is computed on the TRAINING slice
     of the time split (tr_idx) ONLY, heavily smoothed toward the tr-slice global
     mean, then mapped onto BOTH the holdout rows and the test rows. Districts
     unseen in the training slice fall back to the global mean. Because the
     holdout / test encodings never see their own targets, the validation number
     stays honest and comparable to the baseline 0.2709. Heavy smoothing (m=200)
     is deliberate: district price levels drift over time, so a lightly-smoothed
     encoding overfits the past and *hurts* the future holdout (verified by
     ablation: m=10 -> 0.272, m=200 -> 0.268).

Macro enrichment that was tested and DELIBERATELY EXCLUDED:
  I implemented and measured the requested extra macro signals -- month-over-month
  change in usdrub and oil_urals, plus economy-class 1-room/2-room rent series,
  joined by month (leak-free: external data, not derived from price_doc). Every
  one of them DEGRADED the time-based holdout (rent +0.0015, MoM +0.0020, both
  +0.0028; combined with the encodings the full bundle scored 0.2768). The trees
  already consume the six baseline macro columns; these extra month-level series
  add noise across the train->future gap. They are therefore left out of the
  final feature set. See the ablation notes in the task result.

Everything else is unchanged from the baseline.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

BASE = Path(__file__).resolve().parent.parent.parent
DATA = BASE / "data"
OUT = BASE / "model" / "variants" / "submission_encoding_macro.csv"

MACRO_COLS = ["usdrub", "cpi", "oil_urals", "mortgage_rate", "salary", "deposits_rate"]
RANDOM_STATE = 42
TE_SMOOTHING = 200.0  # heavy shrink of small-district means toward the global mean


def rmsle_from_log(y_true_log, y_pred_log):
    """Both inputs are already log1p-transformed, so this is RMSE in log space."""
    return np.sqrt(mean_squared_error(y_true_log, y_pred_log))


def clean(df):
    """Light, defensible fixes applied identically to train and test."""
    df = df.copy()
    # full_sq is the main size feature; 0/1 values are data errors. Fall back to
    # life_sq when it looks sane, else mark missing.
    bad_full = df.full_sq < 5
    df.loc[bad_full, "full_sq"] = df.loc[bad_full, "life_sq"]
    df.loc[df.full_sq < 5, "full_sq"] = np.nan
    df.loc[df.full_sq > 400, "full_sq"] = np.nan
    # life_sq should not exceed full_sq by much; blank the impossible ones.
    df.loc[df.life_sq > df.full_sq * 1.5, "life_sq"] = np.nan
    # build_year has junk like 0, 1, 20052009. Keep only plausible years.
    df.loc[~df.build_year.between(1860, 2020), "build_year"] = np.nan
    df.loc[df.kitch_sq > df.full_sq, "kitch_sq"] = np.nan
    df.loc[~df.state.between(1, 4), "state"] = np.nan
    return df


def add_date_and_macro(df, macro):
    # Identical to the baseline: the extra month-level macro signals were tested
    # (see module docstring) and hurt the time-based holdout, so this stays as-is.
    df = df.copy()
    df["year"] = df.timestamp.dt.year
    df["month"] = df.timestamp.dt.month
    df["month_key"] = df.timestamp.dt.to_period("M").dt.to_timestamp()
    m = macro.set_index("timestamp")[MACRO_COLS].resample("MS").mean().reset_index()
    m = m.rename(columns={"timestamp": "month_key"})
    return df.merge(m, on="month_key", how="left").drop(columns=["month_key"])


def add_subarea_encodings(train, test, y, tr_idx):
    """Add sub_area frequency + LEAK-FREE target encodings (in place).

    - Frequency: TRAIN counts (no target) mapped onto test; unseen -> 0.
    - Target encoding: mean of the log1p target per district computed on the
      TRAINING SLICE (tr_idx) only, smoothed toward the tr-slice global mean,
      then mapped onto every train row and every test row. The holdout rows and
      the test rows therefore never contribute to their own encoding.
    """
    # 1) Frequency (count) encoding -- target-free.
    freq = train["sub_area"].value_counts()
    train["sub_area_freq"] = train["sub_area"].map(freq).astype("float64")
    test["sub_area_freq"] = test["sub_area"].map(freq).fillna(0.0).astype("float64")

    # 2) Leak-free smoothed mean-log-price encoding, fit on tr_idx only.
    global_mean = float(y[tr_idx].mean())
    tr_df = pd.DataFrame({
        "sub_area": train["sub_area"].to_numpy()[tr_idx],
        "y": y[tr_idx],
    })
    agg = tr_df.groupby("sub_area")["y"].agg(["mean", "count"])
    smooth = (agg["count"] * agg["mean"] + TE_SMOOTHING * global_mean) / (
        agg["count"] + TE_SMOOTHING
    )
    train["sub_area_te"] = (
        train["sub_area"].map(smooth).fillna(global_mean).astype("float64")
    )
    test["sub_area_te"] = (
        test["sub_area"].map(smooth).fillna(global_mean).astype("float64")
    )
    return train, test


def build_features(train, test):
    """Return X_train, X_test with identical, model-ready columns.

    Ordinal-encode every non-numeric column (categories learned from train+test
    together so codes line up). Note: pandas 3.0 reads text as the `str` dtype,
    not `object`, so we test with is_numeric_dtype rather than == "object".
    """
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

    train = add_date_and_macro(clean(train), macro)
    test = add_date_and_macro(clean(test), macro)

    y = np.log1p(train.price_doc.values)

    # Time-based validation: newest ~15% of sales as the holdout.
    # (Computed here BEFORE encoding so the target encoding can be fit on tr_idx only.)
    order = train.timestamp.argsort().values
    cut = int(len(order) * 0.85)
    tr_idx, va_idx = order[:cut], order[cut:]

    # Non-leaky sub_area encodings: frequency + tr-slice-only target encoding.
    train, test = add_subarea_encodings(train, test, y, tr_idx)

    X, X_test, feat_cols = build_features(train, test)
    print(f"features: {len(feat_cols)}  |  test rows: {len(X_test):,}")
    print("added features:",
          [c for c in ["sub_area_freq", "sub_area_te"] if c in feat_cols])

    def make_model():
        return HistGradientBoostingRegressor(
            loss="squared_error", learning_rate=0.05, max_iter=700,
            max_leaf_nodes=31, min_samples_leaf=40, l2_regularization=1.0,
            early_stopping=True, validation_fraction=0.1, random_state=RANDOM_STATE)

    val_model = make_model().fit(X.iloc[tr_idx], y[tr_idx])
    va_pred = val_model.predict(X.iloc[va_idx])
    va_rmsle = rmsle_from_log(y[va_idx], va_pred)
    print(f"\nvalidation RMSLE (time-based holdout): {va_rmsle:.4f}")
    print(f"baseline RMSLE: 0.2709  |  delta: {va_rmsle - 0.2709:+.4f}")

    # Refit on all training data for the final submission.
    model = make_model().fit(X, y)
    pred = np.expm1(model.predict(X_test))
    pred = np.clip(pred, 1e5, None)  # prices are positive; floor at 100k RUB

    sub = pd.DataFrame({"id": test.id, "price_doc": pred})
    sub.to_csv(OUT, index=False)
    print(f"\nwrote {OUT.relative_to(BASE)}  ({len(sub):,} rows)")
    print(sub.price_doc.describe().apply(lambda v: f"{v:,.0f}").to_string())


if __name__ == "__main__":
    main()
