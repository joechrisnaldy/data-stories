"""Variant: seed_ensemble — variance reduction by seed averaging.

Same HGBC config as the baseline (max_iter=300, lr=0.08, leaves=31, early
stopping, balanced sample weights), but within each fold of the shared
protocol we fit K=5 copies that differ ONLY in random_state
(42, 7, 123, 2024, 31337) and average their predict_proba. The CV loop
mirrors eval_common.oof_evaluate exactly: StratifiedKFold(5, shuffle=True,
random_state=42), scored as balanced accuracy of the OOF argmax, plus
tune_class_priors on the averaged OOF probabilities.

The seed-42 member IS the baseline model, so its OOF is tracked too as a
free within-script baseline comparison.
"""
import os

os.environ["OMP_NUM_THREADS"] = "4"  # must precede sklearn import

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import N_SPLITS, SEED, load_data, tune_class_priors

SEEDS = [42, 7, 123, 2024, 31337]


def make_model(seed):
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
        early_stopping=True, validation_fraction=0.1, random_state=seed)


def main():
    X, y, _X_test, _test_id, _ = load_data()
    print(f"seed_ensemble: K={len(SEEDS)} HGBC seeds {SEEDS}, "
          f"shared {N_SPLITS}-fold protocol, n={len(y)}", flush=True)

    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof_avg = None       # averaged over seeds
    oof_seed42 = None    # baseline member alone
    classes = None
    t0 = time.time()

    for k, (tr, va) in enumerate(skf.split(X, y)):
        sw = compute_sample_weight("balanced", y[tr])
        proba_sum = None
        for seed in SEEDS:
            t_fit = time.time()
            m = make_model(seed).fit(X.iloc[tr], y[tr], sample_weight=sw)
            proba = m.predict_proba(X.iloc[va])
            if classes is None:
                classes = np.array(m.classes_)
                oof_avg = np.zeros((len(y), len(classes)))
                oof_seed42 = np.zeros((len(y), len(classes)))
            assert list(m.classes_) == list(classes)
            proba_sum = proba if proba_sum is None else proba_sum + proba
            if seed == 42:
                oof_seed42[va] = proba
            print(f"  fold {k} seed {seed}: n_iter={m.n_iter_} "
                  f"fit+pred {time.time() - t_fit:.1f}s", flush=True)
        oof_avg[va] = proba_sum / len(SEEDS)
        fold_bal = balanced_accuracy_score(y[va], classes[oof_avg[va].argmax(1)])
        fold_bal_42 = balanced_accuracy_score(y[va], classes[oof_seed42[va].argmax(1)])
        print(f"  fold {k}: ensemble balanced_acc {fold_bal:.5f} "
              f"(seed-42 alone {fold_bal_42:.5f})  "
              f"elapsed {time.time() - t0:.0f}s", flush=True)

    bal = balanced_accuracy_score(y, classes[oof_avg.argmax(1)])
    bal_42 = balanced_accuracy_score(y, classes[oof_seed42.argmax(1)])
    print(f"\nOOF balanced accuracy (argmax, 5-seed avg): {bal:.5f}")
    print(f"OOF balanced accuracy (seed-42 member = baseline): {bal_42:.5f}")

    w, tuned = tune_class_priors(oof_avg, y, classes)
    print(f"tuned class priors {w.round(3).tolist()} -> {tuned:.5f}")
    w42, tuned_42 = tune_class_priors(oof_seed42, y, classes)
    print(f"(baseline member tuned priors {w42.round(3).tolist()} -> {tuned_42:.5f})")

    out = {"seeds": SEEDS,
           "oof_balanced_accuracy": bal,
           "prior_tuned_oof": tuned,
           "prior_weights": w.tolist(),
           "baseline_member_oof": bal_42,
           "baseline_member_tuned": tuned_42,
           "classes": classes.tolist(),
           "runtime_s": round(time.time() - t0, 1)}
    Path(__file__).with_name("seed_ensemble.json").write_text(json.dumps(out, indent=2))
    print(f"wrote seed_ensemble.json  (total {out['runtime_s']}s)")


if __name__ == "__main__":
    main()
