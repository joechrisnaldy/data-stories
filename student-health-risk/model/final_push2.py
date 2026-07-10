"""Leaderboard push, round 2: widen the blend and tune group weights on OOF.

Round 1 (final_push.py): 2x HGBC-C1 + LGBM equal blend -> OOF 0.94981, LB 0.95012.
Round 2 adds diversity members, reusing round-1 OOFs from final_push_oof.npz:
  new: hgbc_c1_s123, hgbc_a0_s42 (baseline 31-leaf capacity), lgbm_s7,
       lgbm63_s42 (63 leaves, bagging like the variant agent's alt config)
Then evaluates structured combinations with a small HGBC-vs-LGBM group-weight
grid and prior tuning. Selection is on OOF only.
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import json
import time
from pathlib import Path
import sys

import numpy as np
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_sample_weight

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lightgbm import LGBMClassifier
from sklearn.ensemble import HistGradientBoostingClassifier

from eval_common import N_SPLITS, SEED, encode, load_raw, tune_class_priors
from final_push import encode_lgbm, make_hgbc, make_lgbm

OUT = Path(__file__).resolve().parent


def make_hgbc_a0(seed):
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
        early_stopping=True, validation_fraction=0.1, random_state=seed)


def make_lgbm63(seed):
    return LGBMClassifier(
        objective="multiclass", class_weight="balanced", num_leaves=63,
        learning_rate=0.05, n_estimators=300, colsample_bytree=0.8,
        subsample=0.8, subsample_freq=1, min_child_samples=40, n_jobs=6,
        random_state=seed, verbosity=-1)


NEW_MEMBERS = [
    ("hgbc_c1_s123", "hgbc", lambda: make_hgbc(123)),
    ("hgbc_a0_s42", "hgbc", lambda: make_hgbc_a0(42)),
    ("lgbm_s7", "lgbm", lambda: make_lgbm(7)),
    ("lgbm63_s42", "lgbm", lambda: make_lgbm63(42)),
]


def main():
    # Read only the float OOF matrices; the stored 'classes' array is object-dtype
    # (would need pickle). Class order is sklearn's sorted order, fixed and known.
    classes = np.array(["at-risk", "fit", "unhealthy"])
    saved = np.load(OUT / "final_push_oof.npz")
    oofs = {k: saved[k] for k in saved.files if k != "classes"}

    train, test = load_raw()
    y = train.health_condition.values
    X_h, _ = encode(train, test)
    X_l, _ = encode_lgbm(train, test)

    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    for name, kind, factory in NEW_MEMBERS:
        oof = np.zeros((len(y), 3))
        for k, (tr, va) in enumerate(skf.split(X_h, y)):
            t0 = time.time()
            if kind == "hgbc":
                w = compute_sample_weight("balanced", y[tr])
                m = factory().fit(X_h.iloc[tr], y[tr], sample_weight=w)
                oof[va] = m.predict_proba(X_h.iloc[va])
            else:
                m = factory().fit(X_l.iloc[tr], y[tr])
                oof[va] = m.predict_proba(X_l.iloc[va])
            print(f"{name} fold {k}: "
                  f"{balanced_accuracy_score(y[va], classes[oof[va].argmax(1)]):.5f} "
                  f"({time.time() - t0:.0f}s)", flush=True)
        oofs[name] = oof
        print(f"{name} OOF: "
              f"{balanced_accuracy_score(y, classes[oof.argmax(1)]):.5f}", flush=True)

    hgbc_names = [n for n in oofs if n.startswith("hgbc")]
    lgbm_names = [n for n in oofs if n.startswith("lgbm")]
    hgbc_avg = np.mean([oofs[n] for n in hgbc_names], axis=0)
    lgbm_avg = np.mean([oofs[n] for n in lgbm_names], axis=0)

    print(f"\nmembers: hgbc={hgbc_names} lgbm={lgbm_names}")
    print("\n=== group-weight grid (w * hgbc_avg + (1-w) * lgbm_avg) ===")
    results = {}
    best = (None, -1)
    for w in np.round(np.arange(0.3, 0.75, 0.05), 2):
        proba = w * hgbc_avg + (1 - w) * lgbm_avg
        raw = balanced_accuracy_score(y, classes[proba.argmax(1)])
        pw, tuned = tune_class_priors(proba, y, classes, n_iter=2)
        print(f"w={w:.2f}: OOF {raw:.5f}  prior-tuned {tuned:.5f}")
        results[f"w{w:.2f}"] = {"oof": raw, "tuned": tuned, "prior_weights": pw.tolist()}
        if tuned > best[1]:
            best = ((w, pw), tuned)

    (w_best, pw_best), tuned_best = best
    print(f"\nBEST: hgbc_weight={w_best}  prior_weights={np.round(pw_best, 3).tolist()}  "
          f"OOF prior-tuned {tuned_best:.5f}")
    out = {"results": results, "best_hgbc_weight": float(w_best),
           "best_prior_weights": pw_best.tolist(), "best_tuned_oof": tuned_best,
           "hgbc_members": hgbc_names, "lgbm_members": lgbm_names}
    (OUT / "final_push2.json").write_text(json.dumps(out, indent=2))
    np.savez_compressed(OUT / "final_push2_oof.npz",
                        classes=np.asarray(classes, dtype="U16"), **oofs)
    print("saved final_push2.json / final_push2_oof.npz")


if __name__ == "__main__":
    main()
