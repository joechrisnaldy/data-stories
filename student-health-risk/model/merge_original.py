"""Test the 'original dataset' lever (College Student Health Behavior, 50k rows).

Two exploits, evaluated honestly:
  A. Exact-match probe: do any competition TEST rows share identical 13-feature
     vectors with original rows? If yes, their true labels are free.
  B. Training augmentation: within the shared 5-fold protocol, append the 50k
     original rows to each fold's TRAINING portion (never to validation, which
     stays pure competition data). Score the same HGBC-C1 + LGBM blend.

Reference: round-1 blend OOF 0.94982 (LB 0.95012).
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import CATEGORICAL, N_SPLITS, NUMERIC, SEED, load_raw, tune_class_priors
from final_push import make_hgbc, make_lgbm

DATA = Path(__file__).resolve().parent.parent / "data"
CLASSES = np.array(["at-risk", "fit", "unhealthy"])
FEATS = NUMERIC + CATEGORICAL


def load_original():
    df = pd.read_csv(DATA / "original" / "student_health_dataset_50k.csv")
    return df[FEATS + ["health_condition"]].copy()


def encode3(train, test, orig):
    """Encode all three frames with a shared category union."""
    out = []
    cats_by_col = {}
    for c in CATEGORICAL:
        cats_by_col[c] = pd.Categorical(
            pd.concat([train[c], test[c], orig[c]], ignore_index=True)).categories
    for src in (train, test, orig):
        X = src[NUMERIC].copy()
        for c in CATEGORICAL:
            codes = pd.Categorical(src[c], categories=cats_by_col[c]).codes.astype("float64")
            codes[codes == -1] = np.nan
            X[c] = codes
        out.append(X)
    return out


def main():
    train, test = load_raw()
    orig = load_original()
    y = train.health_condition.values
    y_orig = orig.health_condition.values
    print(f"original: {len(orig):,} rows; class mix "
          f"{orig.health_condition.value_counts(normalize=True).round(3).to_dict()}")

    print("\n=== A. exact-match probe (test rows vs original rows) ===")
    key = lambda df: pd.util.hash_pandas_object(
        df[FEATS].round(6), index=False)  # tolerant of float repr
    orig_keys = pd.DataFrame({"k": key(orig), "label": y_orig})
    test_keys = pd.DataFrame({"k": key(test)})
    matches = test_keys.merge(orig_keys, on="k", how="inner")
    print(f"test rows with an exact original match: {len(matches):,}")
    train_keys = pd.DataFrame({"k": key(train)})
    tr_matches = train_keys.merge(orig_keys, on="k", how="inner")
    print(f"train rows with an exact original match: {len(tr_matches):,}")

    print("\n=== B. training augmentation (shared 5-fold protocol) ===")
    X_h, Xt_h, Xo_h = encode3(train, test, orig)
    # LGBM native categories
    def cat3(src_train, src_test, src_orig):
        outs = []
        for src in (src_train, src_test, src_orig):
            X = src[NUMERIC].copy()
            for c in CATEGORICAL:
                cats = pd.Categorical(pd.concat(
                    [src_train[c], src_test[c], src_orig[c]], ignore_index=True)).categories
                X[c] = pd.Categorical(src[c], categories=cats)
            outs.append(X)
        return outs
    X_l, Xt_l, Xo_l = cat3(train, test, orig)

    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof_h = np.zeros((len(y), 3))
    oof_l = np.zeros((len(y), 3))
    for k, (tr, va) in enumerate(skf.split(X_h, y)):
        t0 = time.time()
        y_aug = np.concatenate([y[tr], y_orig])
        w_aug = compute_sample_weight("balanced", y_aug)
        Xh_aug = pd.concat([X_h.iloc[tr], Xo_h], ignore_index=True)
        m = make_hgbc(42).fit(Xh_aug, y_aug, sample_weight=w_aug)
        oof_h[va] = m.predict_proba(X_h.iloc[va])
        Xl_aug = pd.concat([X_l.iloc[tr], Xo_l], ignore_index=True)
        ml = make_lgbm(42).fit(Xl_aug, y_aug)
        oof_l[va] = ml.predict_proba(X_l.iloc[va])
        print(f"fold {k}: hgbc+orig "
              f"{balanced_accuracy_score(y[va], CLASSES[oof_h[va].argmax(1)]):.5f}  "
              f"lgbm+orig {balanced_accuracy_score(y[va], CLASSES[oof_l[va].argmax(1)]):.5f} "
              f"({time.time() - t0:.0f}s)", flush=True)

    for name, proba in (("hgbc_c1+orig", oof_h), ("lgbm+orig", oof_l),
                        ("blend(h+l)+orig", (oof_h + oof_l) / 2)):
        raw = balanced_accuracy_score(y, CLASSES[proba.argmax(1)])
        _, tuned = tune_class_priors(proba, y, CLASSES, n_iter=2)
        print(f"{name:20s} OOF {raw:.5f}  prior-tuned {tuned:.5f}")
    print("\nreference: round-1 blend OOF 0.94982 (members ~0.94953-0.94957)")
    np.savez_compressed(Path(__file__).parent / "merge_original_oof.npz",
                        oof_h=oof_h, oof_l=oof_l)


if __name__ == "__main__":
    main()
