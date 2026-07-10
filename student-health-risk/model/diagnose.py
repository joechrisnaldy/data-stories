"""Error anatomy for the S6E7 push: what is actually missing, and is it fixable?

Uses the 7 saved member OOF matrices (final_push2_oof.npz). Reports:
  1. Where the round-1 blend's errors live (confusion, confidence anatomy):
     high-confidence errors are a label-noise proxy (unfixable); borderline
     errors are potentially fixable by a better combiner.
  2. Oracle ceiling: balanced accuracy if a perfect combiner picked the right
     member whenever ANY of the 7 is right. No combiner of these members can
     exceed this.
  3. Exact duplicate feature rows with conflicting labels (direct evidence of
     irreducible noise).
  4. Stacking: a meta-learner on the 21 member-probability columns, evaluated
     with the same 5-fold protocol (this is the strongest remaining lever).
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import N_SPLITS, SEED, load_raw, tune_class_priors

OUT = Path(__file__).resolve().parent
CLASSES = np.array(["at-risk", "fit", "unhealthy"])


def main():
    saved = np.load(OUT / "final_push2_oof.npz")
    members = [k for k in saved.files if k != "classes"]
    oofs = {k: saved[k] for k in members}
    train, _ = load_raw()
    y = train.health_condition.values
    y_idx = np.searchsorted(CLASSES, y)

    # Round-1 blend (the current LB best): equal mean of the 3 round-1 members
    blend = np.mean([oofs["hgbc_c1_s42"], oofs["hgbc_c1_s7"], oofs["lgbm_s42"]], axis=0)
    pred = blend.argmax(1)
    correct = pred == y_idx
    bal = balanced_accuracy_score(y, CLASSES[pred])
    print(f"round-1 blend OOF balanced accuracy: {bal:.5f}")
    print(f"total errors: {(~correct).sum():,} of {len(y):,}")

    print("\n=== 1. error anatomy ===")
    cm = confusion_matrix(y, CLASSES[pred], labels=list(CLASSES))
    print(pd.DataFrame(cm, index=[f"true_{c}" for c in CLASSES],
                       columns=[f"pred_{c}" for c in CLASSES]).to_string())
    conf = blend.max(1)
    margin = np.sort(blend, axis=1)
    margin = margin[:, -1] - margin[:, -2]
    for name, mask in (("errors", ~correct), ("correct", correct)):
        print(f"{name}: median confidence {np.median(conf[mask]):.3f}, "
              f"share with confidence>0.9: {(conf[mask] > 0.9).mean():.1%}, "
              f"share with top-2 margin<0.1: {(margin[mask] < 0.1).mean():.1%}")
    hc_err = ((~correct) & (conf > 0.9)).sum()
    print(f"high-confidence (>0.9) errors: {hc_err:,} "
          f"({hc_err / (~correct).sum():.1%} of errors) <- label-noise proxy, unfixable")

    print("\n=== 2. oracle ceiling over the 7 members ===")
    any_right = np.zeros(len(y), bool)
    for k in members:
        any_right |= (oofs[k].argmax(1) == y_idx)
    per_class = [any_right[y == c].mean() for c in CLASSES]
    print(f"any-member-correct balanced accuracy: {np.mean(per_class):.5f} "
          f"(per class: {dict(zip(CLASSES, np.round(per_class, 4)))})")
    print("(no combiner of these members can beat this; a realistic stacker gets a "
          "small fraction of the way there)")

    print("\n=== 3. duplicate feature rows with conflicting labels ===")
    feat_cols = [c for c in train.columns if c not in ("id", "health_condition")]
    grp = train.groupby(feat_cols, dropna=False).health_condition
    sizes = grp.size()
    nuniq = grp.nunique()
    dup_rows = int(sizes[sizes > 1].sum())
    conflict_groups = int((nuniq > 1).sum())
    conflict_rows = int(sizes[nuniq > 1].sum())
    print(f"duplicate-feature rows: {dup_rows:,}; groups with CONFLICTING labels: "
          f"{conflict_groups:,} ({conflict_rows:,} rows)")

    print("\n=== 4. stacking meta-learner on member probabilities ===")
    meta_X = np.hstack([oofs[k] for k in members])
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    for name, est in (
        ("logistic", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ("hgbc_small", HistGradientBoostingClassifier(
            max_iter=200, learning_rate=0.1, max_leaf_nodes=15, random_state=SEED)),
    ):
        fit_params = None
        if name == "hgbc_small":
            # class weights via sample_weight per fold using the params API
            proba = cross_val_predict(
                est, meta_X, y, cv=skf, method="predict_proba", n_jobs=1,
                params={"sample_weight": compute_sample_weight("balanced", y)})
        else:
            proba = cross_val_predict(est, meta_X, y, cv=skf,
                                      method="predict_proba", n_jobs=1)
        raw = balanced_accuracy_score(y, CLASSES[proba.argmax(1)])
        _, tuned = tune_class_priors(proba, y, CLASSES, n_iter=2)
        print(f"stacker[{name}]: OOF {raw:.5f}  prior-tuned {tuned:.5f}")

    print("\nreference: round-1 blend 0.94982 (LB 0.95012); LB #1 = 0.95158")


if __name__ == "__main__":
    main()
