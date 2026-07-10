"""Variant: LightGBM with native categorical handling.

Axis: swap HGBC for LGBMClassifier(objective='multiclass', class_weight='balanced')
and feed the 6 categorical columns as pandas 'category' dtype so LightGBM uses its
native categorical splits (instead of treating float codes as ordinal).

Protocol: eval_common.oof_evaluate (stratified 5-fold, seed 42, OOF balanced
accuracy of argmax) + tune_class_priors on the OOF probabilities.

Usage:
    python lgbm_native.py            # full 5-fold protocol with the chosen config
    python lgbm_native.py --screen   # single-fold screen of candidate configs
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "4")  # before sklearn/lightgbm imports

MODEL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODEL_DIR))


def _ensure_lightgbm():
    """lightgbm needs libomp; if brew's copy is absent, re-exec with
    DYLD_LIBRARY_PATH pointing at sklearn's bundled libomp (same venv)."""
    try:
        import lightgbm  # noqa: F401
        return
    except OSError:
        if os.environ.get("_LGBM_REEXEC") == "1":
            raise
        import sklearn
        dylibs = Path(sklearn.__file__).resolve().parent / ".dylibs"
        if not (dylibs / "libomp.dylib").exists():
            raise
        env = dict(os.environ)
        env["DYLD_LIBRARY_PATH"] = f"{dylibs}:{env.get('DYLD_LIBRARY_PATH', '')}"
        env["_LGBM_REEXEC"] = "1"
        os.execve(sys.executable, [sys.executable] + sys.argv, env)


_ensure_lightgbm()

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, early_stopping, log_evaluation
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold

from eval_common import (CATEGORICAL, N_SPLITS, NUMERIC, SEED, load_raw,
                         oof_evaluate, tune_class_priors)


def encode_native(train, test):
    """Numerics pass through; categoricals become pandas 'category' dtype with
    categories aligned across train+test (values only; no target involved).
    NaN stays NaN -> LightGBM's native missing handling."""
    X_tr = train[NUMERIC].copy()
    X_te = test[NUMERIC].copy()
    for c in CATEGORICAL:
        cats = pd.Categorical(
            pd.concat([train[c], test[c]], ignore_index=True)).categories
        X_tr[c] = pd.Categorical(train[c], categories=cats)
        X_te[c] = pd.Categorical(test[c], categories=cats)
    return X_tr, X_te


BASE_PARAMS = dict(
    objective="multiclass",
    class_weight="balanced",   # per-fold balanced weights, computed by sklearn API
    colsample_bytree=0.8,
    n_jobs=4,
    random_state=SEED,
    verbose=-1,
)

# Chosen after fold-0 screening. Key finding: deep trees (127-255 leaves) with
# logloss early stopping collapse balanced accuracy to ~0.925; modest capacity
# with a fixed, small iteration count is what works. Fold-0 peaks:
#   leaves31/lr.08: 0.95063 @ 150 | leaves63/lr.05/bag.8/mcs200: 0.95068 @ 400
# (HGBC baseline fold 0: 0.94977.)
# Full-protocol results: FINAL 0.94953 (prior-tuned 0.94966);
# ALT (63 leaves, bagged) 0.94950 (prior-tuned 0.94962). Both tie the baseline.
FINAL_PARAMS = dict(
    BASE_PARAMS,
    learning_rate=0.08,
    num_leaves=31,
    min_child_samples=20,
    n_estimators=200,
)

# Second candidate (fold-0 winner, slightly worse on the full protocol); --alt.
ALT_PARAMS = dict(
    BASE_PARAMS,
    learning_rate=0.05,
    num_leaves=63,
    min_child_samples=200,
    subsample=0.8,
    subsample_freq=1,
    n_estimators=400,
)

SCREEN_CONFIGS = [
    ("lr.05_leaves127_mcs100", dict(learning_rate=0.05, num_leaves=127,
                                    min_child_samples=100)),
    ("lr.03_leaves255_mcs200", dict(learning_rate=0.03, num_leaves=255,
                                    min_child_samples=200)),
    ("lr.08_leaves63_mcs50", dict(learning_rate=0.08, num_leaves=63,
                                  min_child_samples=50)),
]


def screen(X, y):
    """Fit candidate configs on fold 0 with early stopping on the fold's
    validation split; report balanced accuracy and best iteration."""
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    tr, va = next(iter(skf.split(X, y)))
    X_tr, X_va, y_tr, y_va = X.iloc[tr], X.iloc[va], y[tr], y[va]
    for name, cfg in SCREEN_CONFIGS:
        import time
        t0 = time.time()
        m = LGBMClassifier(**BASE_PARAMS, **cfg, n_estimators=2000)
        m.fit(X_tr, y_tr, eval_set=[(X_va, y_va)],
              callbacks=[early_stopping(50, verbose=False), log_evaluation(0)])
        pred = np.array(m.classes_)[m.predict_proba(X_va).argmax(1)]
        bal = balanced_accuracy_score(y_va, pred)
        print(f"[screen] {name}: fold0 balanced_acc={bal:.5f} "
              f"best_iter={m.best_iteration_} ({time.time() - t0:.0f}s)",
              flush=True)


def main():
    train, test = load_raw()
    X, X_test = encode_native(train, test)
    y = train.health_condition.values
    print(f"train {X.shape}  dtypes: "
          f"{dict(X.dtypes.astype(str).value_counts())}", flush=True)

    if "--screen" in sys.argv:
        screen(X, y)
        return

    params = ALT_PARAMS if "--alt" in sys.argv else FINAL_PARAMS
    print(f"params: {params}", flush=True)
    result = oof_evaluate(lambda: LGBMClassifier(**params), X, y)
    w, tuned = tune_class_priors(result["oof_proba"], y, result["classes"])
    print(f"OOF balanced accuracy (argmax): {result['balanced_accuracy']:.5f}")
    print(f"prior-tuned OOF balanced accuracy: {tuned:.5f}  weights={np.round(w, 3)}")


if __name__ == "__main__":
    main()
