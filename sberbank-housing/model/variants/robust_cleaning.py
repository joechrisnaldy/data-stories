"""Variant: robust_cleaning.

Axis: better data cleaning + TRAIN-only target de-noising. No new features, no
macro changes, same model, same time-based split protocol as the baseline.

Changes vs model/train_predict.py (all inside `clean` + one de-noising step):
  1. Detect and fix swapped life_sq/full_sq. When life_sq > full_sq and both look
     like plausible areas, the columns were entered in the wrong order -> swap them.
  2. full_sq==0/tiny -> life_sq fallback else missing (kept from baseline), plus a
     small-life_sq blank so life_sq=0/1 junk does not leak in.
  3. Blank impossible build_year / state / num_room / kitch_sq (baseline only did
     build_year/state/kitch_sq; num_room==0 and year-like kitch_sq are now blanked).
  4. De-noise the TRAIN target: drop rows in the bottom 1% of price-per-square-metre.
     These are residual underpriced / mislabelled sales (the same failure mode as the
     1M/2M declared prices the baseline already drops). The drop is ONE-SIDED on
     purpose: an ablation across 3 seeds showed dropping the LOW psqm tail helps
     (~-0.005 RMSLE) while dropping the HIGH tail hurts (it discards genuine luxury
     flats the model needs), so a symmetric 0.5/99.5 clip is a net regression.

LEAKAGE CONTROL: no rows are dropped before the split, so the timestamp `order`
and the newest-15% holdout (`va_idx`, its rows AND targets) are byte-identical to
the baseline -> the CV number stays comparable. The psqm percentile bound is
computed on the TRAINING PORTION only and the row-drop is applied to that portion
only; the holdout is never de-noised (that would flatter the score by discarding
hard rows). Size fixes in `clean` are applied to both train and test.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

BASE = Path(__file__).resolve().parent.parent.parent
DATA = BASE / "data"
OUT = BASE / "model" / "variants" / "robust_cleaning_submission.csv"

MACRO_COLS = ["usdrub", "cpi", "oil_urals", "mortgage_rate", "salary", "deposits_rate"]
RANDOM_STATE = 42

# price-per-square-metre de-noising (TRAIN only): drop the cheapest 1% per m^2.
# One-sided (low tail only) - see module docstring for the ablation rationale.
PSQM_LO_Q = 0.01


def rmsle_from_log(y_true_log, y_pred_log):
    """Both inputs are already log1p-transformed, so this is RMSE in log space."""
    return np.sqrt(mean_squared_error(y_true_log, y_pred_log))


def clean(df):
    """Robust size/attribute fixes applied identically to train and test."""
    df = df.copy()

    # 1) Swapped life_sq/full_sq: both plausible areas but life_sq > full_sq means
    #    the two columns were entered in the wrong order. Swap them back.
    swap = (df.life_sq > df.full_sq) & df.full_sq.notna() & df.life_sq.notna() \
        & df.full_sq.between(1, 1000) & df.life_sq.between(1, 1000)
    tmp = df.loc[swap, "full_sq"].to_numpy()
    df.loc[swap, "full_sq"] = df.loc[swap, "life_sq"].to_numpy()
    df.loc[swap, "life_sq"] = tmp

    # 2) full_sq==0/tiny are data errors: fall back to life_sq, else mark missing.
    bad_full = df.full_sq < 5
    df.loc[bad_full, "full_sq"] = df.loc[bad_full, "life_sq"]
    df.loc[df.full_sq < 5, "full_sq"] = np.nan
    df.loc[df.full_sq > 400, "full_sq"] = np.nan

    # 3) life_sq sanity: tiny junk or (still) larger than full_sq -> missing.
    df.loc[df.life_sq < 2, "life_sq"] = np.nan
    df.loc[df.life_sq > df.full_sq * 1.5, "life_sq"] = np.nan

    # 4) Blank impossible categorical / count / year attributes.
    df.loc[~df.build_year.between(1860, 2020), "build_year"] = np.nan
    df.loc[~df.state.between(1, 4), "state"] = np.nan
    df.loc[(df.num_room < 1) | (df.num_room > 15), "num_room"] = np.nan
    # kitchen can't be as big as (or bigger than) the whole flat; year-like values
    # (e.g. 1970, 2014) are junk that survive when full_sq is missing.
    df.loc[df.kitch_sq >= df.full_sq, "kitch_sq"] = np.nan
    df.loc[df.kitch_sq > 400, "kitch_sq"] = np.nan
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


def psqm_keep_mask(price_doc, full_sq, lo_q=PSQM_LO_Q, lo=None):
    """Rows to KEEP based on price-per-square-metre (one-sided low-tail drop).

    Rows with unknown psqm (full_sq missing) are always kept - we can't judge them.
    If `lo` is None the lower bound is learned from the given data (used for the
    training portion); otherwise the pre-computed bound is applied. Returns
    (mask, lo).
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        psqm = np.asarray(price_doc, float) / np.asarray(full_sq, float)
    finite = np.isfinite(psqm)
    if lo is None:
        lo = float(np.quantile(psqm[finite], lo_q))
    keep = (~finite) | (finite & (psqm >= lo))
    return keep, lo


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

    # Time-based validation: newest ~15% of sales as the holdout. Identical to the
    # baseline because no rows are dropped before this split.
    order = train.timestamp.argsort().values
    cut = int(len(order) * 0.85)
    tr_idx, va_idx = order[:cut], order[cut:]

    # TRAIN-only target de-noising: drop the cheapest-per-m^2 rows from the TRAINING
    # portion only. The bound is learned on tr_idx alone; the holdout is untouched.
    price = train.price_doc.values
    full_sq = train.full_sq.values
    keep_tr, lo = psqm_keep_mask(price[tr_idx], full_sq[tr_idx])
    tr_idx_dn = tr_idx[keep_tr]
    dropped = len(tr_idx) - len(tr_idx_dn)
    print(f"psqm de-noise (train portion): drop psqm < {lo:,.0f} RUB/m^2, "
          f"dropped {dropped:,} / {len(tr_idx):,} rows "
          f"({dropped / len(tr_idx):.2%}); holdout kept intact ({len(va_idx):,} rows)")

    def make_model():
        return HistGradientBoostingRegressor(
            loss="squared_error", learning_rate=0.05, max_iter=700,
            max_leaf_nodes=31, min_samples_leaf=40, l2_regularization=1.0,
            early_stopping=True, validation_fraction=0.1, random_state=RANDOM_STATE)

    val_model = make_model().fit(X.iloc[tr_idx_dn], y[tr_idx_dn])
    va_pred = val_model.predict(X.iloc[va_idx])
    cv = rmsle_from_log(y[va_idx], va_pred)
    print(f"\nvalidation RMSLE (time-based holdout): {cv:.4f}")
    print("baseline RMSLE: 0.2709  |  delta: "
          f"{cv - 0.2709:+.4f} ({'IMPROVED' if cv < 0.2709 else 'no improvement'})")

    # Final refit for submission: de-noise on the FULL train (computed on train
    # only, no test involvement), then refit on the survivors and predict test.
    keep_all, _ = psqm_keep_mask(price, full_sq)  # bound learned on full train only
    Xf, yf = X.iloc[keep_all], y[keep_all]
    model = make_model().fit(Xf, yf)
    pred = np.expm1(model.predict(X_test))
    pred = np.clip(pred, 1e5, None)  # prices are positive; floor at 100k RUB

    sub = pd.DataFrame({"id": test.id, "price_doc": pred})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sub.to_csv(OUT, index=False)
    print(f"\nwrote {OUT.relative_to(BASE)}  ({len(sub):,} rows)")


if __name__ == "__main__":
    main()
