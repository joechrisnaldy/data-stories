"""feature_eng variant: same HGBC config + balanced weights as baseline, only the
feature matrix changes.

v2 strategy: fits are cheap (~5s, early stopping at ~65-90 iters), and fold-0
deltas of ~0.0001 are inside single-fold noise (SE ~0.001). So every candidate
feature set is scored on the FULL shared protocol (stratified 5-fold, seed 42,
OOF balanced accuracy) — the only comparison that is actually trustworthy here.

Blocks (all functions of feature columns only, computed row-wise -> fold-safe):
  miss  : per-column isna flags + row-wise missing count
  ratio : steps/exercise_min, calorie/step, calorie/exercise_min, water/calorie,
          bmi * (8 - sleep_duration). Pure monotone transforms (8 - sleep, sleep/8)
          are no-ops for trees and skipped.
  inter : extra products/ratios: bmi*heart_rate, step_count*exercise_duration,
          calorie/bmi, heart_rate/sleep_duration
  bins  : 10-quantile bins of sleep_duration and step_count (coarser view than
          HGBC's internal 255 bins; a regularization bet)

Candidates: baseline, each block alone, and combinations of any block that beats
baseline OOF. Final report = best candidate's OOF balanced accuracy + prior-tuned
OOF (tune_class_priors on its OOF probabilities).
"""
import os

os.environ["OMP_NUM_THREADS"] = "4"

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

MODEL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODEL_DIR))

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import SEED, load_data, oof_evaluate, tune_class_priors


def make_model():
    # EXACT baseline config (train_models.py); only features differ in this variant.
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
        early_stopping=True, validation_fraction=0.1, random_state=SEED)


def balanced_weights(y_fold):
    return compute_sample_weight("balanced", y_fold)


# ---------------------------------------------------------------- feature blocks
def add_missing_flags(X):
    """Per-column missingness flags + row-wise missing count (fold-safe)."""
    out = X.copy()
    for c in X.columns:
        out[f"{c}_miss"] = X[c].isna().astype(np.float64)
    out["n_missing"] = X.isna().sum(axis=1).astype(np.float64)
    return out


def add_ratios(X):
    """Ratios/interactions trees cannot express with axis-aligned splits."""
    out = X.copy()
    with np.errstate(divide="ignore", invalid="ignore"):
        out["steps_per_exmin"] = X["step_count"] / X["exercise_duration"]
        out["cal_per_step"] = X["calorie_expenditure"] / X["step_count"]
        out["cal_per_exmin"] = X["calorie_expenditure"] / X["exercise_duration"]
        out["water_per_cal"] = X["water_intake"] / X["calorie_expenditure"]
        out["bmi_sleep_deficit"] = X["bmi"] * (8.0 - X["sleep_duration"])
    return out.replace([np.inf, -np.inf], np.nan)


def add_interactions(X):
    """Additional products/ratios of the physiological columns."""
    out = X.copy()
    with np.errstate(divide="ignore", invalid="ignore"):
        out["bmi_x_hr"] = X["bmi"] * X["heart_rate"]
        out["steps_x_exmin"] = X["step_count"] * X["exercise_duration"]
        out["cal_per_bmi"] = X["calorie_expenditure"] / X["bmi"]
        out["hr_per_sleep"] = X["heart_rate"] / X["sleep_duration"]
    return out.replace([np.inf, -np.inf], np.nan)


def add_bins(X, cols=("sleep_duration", "step_count"), q=10):
    """Coarse quantile bins of the strongest separators (feature-only, fold-safe)."""
    out = X.copy()
    for c in cols:
        out[f"{c}_bin"] = pd.qcut(X[c], q=q, labels=False, duplicates="drop").astype("float64")
    return out


BLOCKS = {"miss": add_missing_flags, "ratio": add_ratios,
          "inter": add_interactions, "bins": add_bins}


def apply_blocks(X, names):
    out = X
    for n in names:
        out = BLOCKS[n](out)
    return out


def full_oof(name, X, y):
    t0 = time.time()
    res = oof_evaluate(make_model, X, y, sample_weight_fn=balanced_weights, verbose=False)
    print(f"[oof] {name:<24} bal_acc={res['balanced_accuracy']:.5f}  "
          f"({time.time() - t0:.0f}s, {X.shape[1]} feats)", flush=True)
    return res


def main():
    t_start = time.time()
    X, y, X_test, test_id, _ = load_data()
    print(f"data: train {X.shape}, test {X_test.shape}", flush=True)

    results = {}
    results[()] = full_oof("baseline", X, y)
    for name in BLOCKS:
        key = (name,)
        results[key] = full_oof("+".join(key), apply_blocks(X, key), y)

    base = results[()]["balanced_accuracy"]
    winners = [n for n in BLOCKS
               if results[(n,)]["balanced_accuracy"] > base]
    print(f"\nOOF deltas vs baseline ({base:.5f}): "
          + ", ".join(f"{n}: {results[(n,)]['balanced_accuracy'] - base:+.5f}"
                      for n in BLOCKS), flush=True)
    print(f"blocks above baseline: {winners or 'none'}", flush=True)

    # combo of all winning blocks, evaluated on the same full protocol
    if len(winners) >= 2:
        key = tuple(winners)
        results[key] = full_oof("+".join(key), apply_blocks(X, key), y)

    best_key = max(results, key=lambda k: results[k]["balanced_accuracy"])
    best = results[best_key]
    w, tuned = tune_class_priors(best["oof_proba"], y, best["classes"])

    print(f"\n=== feature_eng RESULTS (full 5-fold protocol) ===")
    print(f"baseline OOF        : {base:.5f}")
    print(f"best feature set    : baseline"
          + "".join(f" + {n}" for n in best_key) or "")
    print(f"OOF balanced acc    : {best['balanced_accuracy']:.5f}")
    print(f"prior-tuned OOF     : {tuned:.5f}  (weights {np.round(w, 3).tolist()}, "
          f"classes {best['classes'].tolist()})")
    print(f"total runtime       : {(time.time() - t_start) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
