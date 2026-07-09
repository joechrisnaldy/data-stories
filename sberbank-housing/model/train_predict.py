"""Clean baseline model for the Sberbank Russian Housing Market competition.

Goal: predict `price_doc` for the 7,662 test rows, scored on RMSLE.

Design choices (kept deliberately simple and readable):
  - Target is log1p(price_doc): RMSLE on prices == RMSE on log1p, so training a
    squared-error learner in log space optimizes the competition metric directly.
  - Model is sklearn's HistGradientBoostingRegressor: fast, strong on tabular data,
    and it handles this dataset's heavy missingness natively (no imputation needed).
  - Light, defensible cleaning only. Categoricals are ordinal-encoded. A few macro
    indicators are joined by month. No leaderboard tricks; this is a baseline.
  - Validation is time-based (train on earlier sales, validate on the latest slice),
    because the test set is the future. A random split would flatter the score.
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
    df = df.copy()
    df["year"] = df.timestamp.dt.year
    df["month"] = df.timestamp.dt.month
    df["month_key"] = df.timestamp.dt.to_period("M").dt.to_timestamp()
    m = macro.set_index("timestamp")[MACRO_COLS].resample("MS").mean().reset_index()
    m = m.rename(columns={"timestamp": "month_key"})
    return df.merge(m, on="month_key", how="left").drop(columns=["month_key"])


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
    X, X_test, feat_cols = build_features(train, test)
    print(f"features: {len(feat_cols)}  |  test rows: {len(X_test):,}")

    # Time-based validation: newest ~15% of sales as the holdout.
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
    print(f"\nvalidation RMSLE (time-based holdout): {rmsle_from_log(y[va_idx], va_pred):.4f}")

    # Refit on all training data for the final submission.
    model = make_model().fit(X, y)
    pred = np.expm1(model.predict(X_test))
    pred = np.clip(pred, 1e5, None)  # prices are positive; floor at 100k RUB

    sub = pd.DataFrame({"id": test.id, "price_doc": pred})
    sub.to_csv(OUT, index=False)
    print(f"\nwrote {OUT.relative_to(BASE)}  ({len(sub):,} rows)")
    print(sub.price_doc.describe().apply(lambda v: f"{v:,.0f}").to_string())

    print("\nsample predictions:")
    print(sub.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
