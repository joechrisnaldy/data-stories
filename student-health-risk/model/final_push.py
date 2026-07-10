"""Final leaderboard push: evaluate the combined candidate on the shared protocol.

Members (chosen from the variant experiments):
  - HGBC "C1" (max_iter=1000, lr=0.05, leaves=63, min_samples_leaf=40, l2=1.0),
    the hyperparameter screen winner, seeds 42 and 7 (float-code encoding)
  - LightGBM small config (num_leaves=31, lr=0.08, 200 trees, colsample 0.8),
    native categorical encoding, which decorrelates it from the HGBC members

Reports, all on eval_common's stratified 5-fold protocol:
  each member's OOF balanced accuracy, the blend's, and prior-tuned versions.
Saves OOF probabilities and the tuned prior weights to final_push.npz/json.
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lightgbm import LGBMClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import (CATEGORICAL, N_SPLITS, NUMERIC, SEED, encode,
                         load_raw, tune_class_priors)

OUT = Path(__file__).resolve().parent


def encode_lgbm(train, test):
    """LightGBM-native encoding: categoricals as pandas 'category' dtype."""
    X_tr = train[NUMERIC].copy()
    X_te = test[NUMERIC].copy()
    for c in CATEGORICAL:
        cats = pd.Categorical(pd.concat([train[c], test[c]], ignore_index=True)).categories
        X_tr[c] = pd.Categorical(train[c], categories=cats)
        X_te[c] = pd.Categorical(test[c], categories=cats)
    return X_tr, X_te


def make_hgbc(seed):
    return HistGradientBoostingClassifier(
        max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
        min_samples_leaf=40, l2_regularization=1.0,
        early_stopping=True, validation_fraction=0.1, n_iter_no_change=15,
        random_state=seed)


def make_lgbm(seed):
    return LGBMClassifier(
        objective="multiclass", class_weight="balanced", num_leaves=31,
        learning_rate=0.08, n_estimators=200, colsample_bytree=0.8,
        min_child_samples=20, n_jobs=6, random_state=seed, verbosity=-1)


MEMBERS = [
    ("hgbc_c1_s42", "hgbc", 42),
    ("hgbc_c1_s7", "hgbc", 7),
    ("lgbm_s42", "lgbm", 42),
]


def main():
    train, test = load_raw()
    y = train.health_condition.values
    X_h, Xt_h = encode(train, test)
    X_l, Xt_l = encode_lgbm(train, test)

    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    splits = list(skf.split(X_h, y))

    oofs = {name: np.zeros((len(y), 3)) for name, _, _ in MEMBERS}
    classes = None
    for k, (tr, va) in enumerate(splits):
        w = compute_sample_weight("balanced", y[tr])
        for name, kind, seed in MEMBERS:
            t0 = time.time()
            if kind == "hgbc":
                m = make_hgbc(seed).fit(X_h.iloc[tr], y[tr], sample_weight=w)
                proba = m.predict_proba(X_h.iloc[va])
            else:
                m = make_lgbm(seed).fit(X_l.iloc[tr], y[tr])
                proba = m.predict_proba(X_l.iloc[va])
            if classes is None:
                classes = np.array(m.classes_)
            oofs[name][va] = proba
            print(f"fold {k} {name}: "
                  f"bal {balanced_accuracy_score(y[va], classes[proba.argmax(1)]):.5f} "
                  f"({time.time() - t0:.0f}s)", flush=True)

    def report(name, proba):
        raw = balanced_accuracy_score(y, classes[proba.argmax(1)])
        w, tuned = tune_class_priors(proba, y, classes)
        print(f"{name:28s} OOF {raw:.5f}   prior-tuned {tuned:.5f}  w={np.round(w, 3)}")
        return {"oof": raw, "tuned": tuned, "weights": w.tolist()}

    print("\n=== results (shared 5-fold protocol) ===")
    results = {}
    for name, _, _ in MEMBERS:
        results[name] = report(name, oofs[name])
    blend_all = np.mean([oofs[n] for n, _, _ in MEMBERS], axis=0)
    results["blend_all3"] = report("blend_all3", blend_all)
    blend_hgbc = np.mean([oofs["hgbc_c1_s42"], oofs["hgbc_c1_s7"]], axis=0)
    results["blend_hgbc2"] = report("blend_hgbc2", blend_hgbc)

    np.savez_compressed(OUT / "final_push_oof.npz", classes=classes,
                        **{n: oofs[n] for n, _, _ in MEMBERS})
    (OUT / "final_push.json").write_text(json.dumps(results, indent=2))
    print("\nsaved final_push.json / final_push_oof.npz")


if __name__ == "__main__":
    main()
