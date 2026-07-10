"""Variant: hyperparams — tune HistGradientBoostingClassifier only.

Axis: same baseline features (eval_common.load_data), same balanced sample
weights; ONLY the HGBC hyperparameters change. The baseline (max_iter=300,
lr=0.08, leaves=31) is suspected undertrained for ~690k rows.

Usage:
    python variants/hyperparams.py --screen            # rank configs on fold 0
    python variants/hyperparams.py --final C1 [C2 ...] # shared 5-fold protocol
"""
import os

os.environ["OMP_NUM_THREADS"] = "4"  # must precede sklearn import

import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import N_SPLITS, SEED, load_data, oof_evaluate, tune_class_priors

# Screened configs. Baseline A0 is the reference point.
CONFIGS = {
    "A0": dict(max_iter=300, learning_rate=0.08, max_leaf_nodes=31),
    "C1": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0),
    "C2": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=127,
               min_samples_leaf=60, l2_regularization=2.0),
    "C3": dict(max_iter=1500, learning_rate=0.03, max_leaf_nodes=127,
               min_samples_leaf=60, l2_regularization=2.0),
    "C4": dict(max_iter=800, learning_rate=0.08, max_leaf_nodes=63,
               min_samples_leaf=30, l2_regularization=0.5),
    "C5": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=255,
               min_samples_leaf=100, l2_regularization=5.0),
    "C6": dict(max_iter=600, learning_rate=0.10, max_leaf_nodes=63,
               l2_regularization=1.0, max_features=0.8),
    "C7": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
               l2_regularization=1.0, max_features=0.7),
    "C8": dict(max_iter=1200, learning_rate=0.06, max_leaf_nodes=95,
               min_samples_leaf=50, l2_regularization=1.5),
    "C9": dict(max_iter=1500, learning_rate=0.04, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0),
    # Round 2: refinements around C1 (the round-1 winner).
    "D1": dict(max_iter=1500, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0, n_iter_no_change=40),
    "D2": dict(max_iter=1500, learning_rate=0.04, max_leaf_nodes=48,
               min_samples_leaf=40, l2_regularization=1.0),
    "D3": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=20, l2_regularization=0.5),
    "D4": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=80, l2_regularization=1.0),
    "D5": dict(max_iter=1000, learning_rate=0.06, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0),
    "D6": dict(max_iter=1000, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0, max_bins=128),
    "D7": dict(max_iter=1200, learning_rate=0.05, max_leaf_nodes=95,
               min_samples_leaf=40, l2_regularization=1.0),
    "D8": dict(max_iter=1500, learning_rate=0.05, max_leaf_nodes=63,
               min_samples_leaf=40, l2_regularization=1.0,
               validation_fraction=0.15, n_iter_no_change=25),
}


def make_factory(cfg):
    def make_model():
        params = dict(early_stopping=True, validation_fraction=0.1,
                      n_iter_no_change=15, random_state=SEED)
        params.update(cfg)
        return HistGradientBoostingClassifier(**params)
    return make_model


def balanced_weights(y_fold):
    return compute_sample_weight("balanced", y_fold)


def screen(names, folds=(0,)):
    """Rank configs on given fold(s) of the shared split (same seed/shuffle)."""
    X, y, _, _, _ = load_data()
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    splits = [s for k, s in enumerate(skf.split(X, y)) if k in set(folds)]
    print(f"screen: folds {list(folds)}")
    results = {}
    for name in names:
        cfg = CONFIGS[name]
        t0 = time.time()
        scores, iters = [], []
        for tr, va in splits:
            m = make_factory(cfg)().fit(X.iloc[tr], y[tr],
                                        sample_weight=balanced_weights(y[tr]))
            scores.append(balanced_accuracy_score(y[va], m.predict(X.iloc[va])))
            iters.append(m.n_iter_)
        results[name] = np.mean(scores)
        print(f"  {name}: mean_bal={np.mean(scores):.5f}  "
              f"per_fold={[round(s, 5) for s in scores]}  n_iter={iters}  "
              f"time={time.time() - t0:.0f}s  cfg={cfg}", flush=True)
    print("\nranking:")
    for name, bal in sorted(results.items(), key=lambda kv: -kv[1]):
        print(f"  {name}: {bal:.5f}")


def final(names):
    """Full shared 5-fold protocol + prior tuning for the chosen config(s)."""
    X, y, _, _, _ = load_data()
    for name in names:
        cfg = CONFIGS[name]
        print(f"\n=== FINAL {name}: {cfg} ===", flush=True)
        t0 = time.time()
        res = oof_evaluate(make_factory(cfg), X, y, sample_weight_fn=balanced_weights)
        w, tuned = tune_class_priors(res["oof_proba"], y, res["classes"])
        print(f"{name}: OOF balanced accuracy = {res['balanced_accuracy']:.5f}")
        print(f"{name}: prior-tuned OOF       = {tuned:.5f}  weights={np.round(w, 3)}")
        print(f"{name}: total time {time.time() - t0:.0f}s")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--screen", action="store_true")
    p.add_argument("--final", nargs="+", metavar="CONFIG")
    p.add_argument("--configs", nargs="+", default=list(CONFIGS), metavar="CONFIG")
    p.add_argument("--folds", nargs="+", type=int, default=[0])
    args = p.parse_args()
    if args.screen:
        screen(args.configs, folds=args.folds)
    if args.final:
        final(args.final)
    if not args.screen and not args.final:
        p.error("pass --screen and/or --final CONFIG ...")
