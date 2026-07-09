"""Variant: hyperparam_tuning.

Same pipeline / cleaning / features / time-based validation as the baseline
(model/train_predict.py). The ONLY change is the model step: instead of a single
fixed HistGradientBoostingRegressor config, we run a small search over
learning_rate, max_iter (with early stopping), max_leaf_nodes, min_samples_leaf,
l2_regularization, and max_features, scoring EACH config on the identical
time-based holdout (newest ~15% of sales). Baseline features and cleaning are
untouched.

Leakage note: every config is fit ONLY on the training slice (tr_idx) and scored
on the held-out newest slice (va_idx). Early stopping uses HGBR's internal
validation split carved from the training slice, so the time-based holdout is
never seen during fitting.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

BASE = Path(__file__).resolve().parent.parent.parent
DATA = BASE / "data"

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


def build_features(train, test):
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


# Small curated search grid (~12 configs) around the baseline. Every config keeps
# early_stopping=True so max_iter is an upper bound; low-lr/high-max_iter configs
# rely on early stopping to pick the effective number of trees.
# Fields: learning_rate, max_iter, max_leaf_nodes, min_samples_leaf,
#         l2_regularization, max_features
SEARCH_CONFIGS = [
    # baseline reference (matches model/train_predict.py)
    dict(learning_rate=0.05, max_iter=700,  max_leaf_nodes=31, min_samples_leaf=40,  l2_regularization=1.0, max_features=1.0),
    dict(learning_rate=0.03, max_iter=1200, max_leaf_nodes=31, min_samples_leaf=40,  l2_regularization=1.0, max_features=1.0),
    dict(learning_rate=0.03, max_iter=1500, max_leaf_nodes=63, min_samples_leaf=60,  l2_regularization=1.0, max_features=0.8),
    dict(learning_rate=0.02, max_iter=2000, max_leaf_nodes=31, min_samples_leaf=50,  l2_regularization=2.0, max_features=0.7),
    dict(learning_rate=0.05, max_iter=1000, max_leaf_nodes=63, min_samples_leaf=80,  l2_regularization=2.0, max_features=0.7),
    dict(learning_rate=0.05, max_iter=800,  max_leaf_nodes=15, min_samples_leaf=40,  l2_regularization=1.0, max_features=1.0),
    dict(learning_rate=0.05, max_iter=1000, max_leaf_nodes=31, min_samples_leaf=100, l2_regularization=5.0, max_features=0.6),
    dict(learning_rate=0.04, max_iter=1200, max_leaf_nodes=45, min_samples_leaf=60,  l2_regularization=3.0, max_features=0.8),
    dict(learning_rate=0.02, max_iter=2500, max_leaf_nodes=63, min_samples_leaf=100, l2_regularization=2.0, max_features=0.6),
    dict(learning_rate=0.08, max_iter=500,  max_leaf_nodes=31, min_samples_leaf=40,  l2_regularization=1.0, max_features=1.0),
    dict(learning_rate=0.03, max_iter=1500, max_leaf_nodes=31, min_samples_leaf=60,  l2_regularization=1.0, max_features=0.9),
    dict(learning_rate=0.05, max_iter=1000, max_leaf_nodes=31, min_samples_leaf=40,  l2_regularization=1.0, max_features=0.8),
]


def make_model(cfg):
    return HistGradientBoostingRegressor(
        loss="squared_error",
        early_stopping=True, validation_fraction=0.1, random_state=RANDOM_STATE,
        **cfg)


def main():
    train = pd.read_csv(DATA / "train.csv", parse_dates=["timestamp"])
    test = pd.read_csv(DATA / "test.csv", parse_dates=["timestamp"])
    macro = pd.read_csv(DATA / "macro.csv", parse_dates=["timestamp"])

    n0 = len(train)
    train = train[~train.price_doc.isin([1_000_000, 2_000_000])].reset_index(drop=True)
    print(f"train rows: {n0:,} -> {len(train):,} after dropping 1M/2M declared prices")

    train = add_date_and_macro(clean(train), macro)
    test = add_date_and_macro(clean(test), macro)

    y = np.log1p(train.price_doc.values)
    X, X_test, feat_cols = build_features(train, test)
    print(f"features: {len(feat_cols)}  |  test rows: {len(X_test):,}")

    # Time-based validation: newest ~15% of sales as the holdout (IDENTICAL to baseline).
    order = train.timestamp.argsort().values
    cut = int(len(order) * 0.85)
    tr_idx, va_idx = order[:cut], order[cut:]
    print(f"train slice: {len(tr_idx):,}  |  holdout slice: {len(va_idx):,}\n")

    results = []
    for i, cfg in enumerate(SEARCH_CONFIGS):
        model = make_model(cfg).fit(X.iloc[tr_idx], y[tr_idx])
        va_pred = model.predict(X.iloc[va_idx])
        score = rmsle_from_log(y[va_idx], va_pred)
        n_trees = model.n_iter_
        results.append((score, cfg, n_trees))
        tag = " (baseline config)" if i == 0 else ""
        print(f"cfg {i:2d}: RMSLE={score:.4f}  trees={n_trees:4d}  {cfg}{tag}")

    results.sort(key=lambda r: r[0])
    best_score, best_cfg, best_trees = results[0]

    print("\n" + "=" * 70)
    print(f"BASELINE time-based holdout RMSLE: 0.2709")
    print(f"BEST config trees (early-stopped): {best_trees}")
    print(f"BEST config: {best_cfg}")
    print(f"\nvalidation RMSLE (time-based holdout): {best_score:.4f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
