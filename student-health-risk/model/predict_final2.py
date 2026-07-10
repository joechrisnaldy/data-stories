"""Refit the round-2 seven-member blend on ALL training data and write
submissions for the two chosen candidates:

  1. w40_priors : hgbc_weight=0.40, prior weights [0.95, 1.2, 1.0] (grid best)
  2. w50_plain  : hgbc_weight=0.50, no prior adjustment (robust flat-grid pick)

Members: HGBC-C1 seeds 42/7/123, HGBC-A0 seed 42, LGBM31 seeds 42/7, LGBM63 seed 42.
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sklearn.utils.class_weight import compute_sample_weight

from eval_common import encode, load_raw
from final_push import encode_lgbm, make_hgbc, make_lgbm
from final_push2 import make_hgbc_a0, make_lgbm63

OUT = Path(__file__).resolve().parent
CLASSES = np.array(["at-risk", "fit", "unhealthy"])

HGBC_MEMBERS = [lambda: make_hgbc(42), lambda: make_hgbc(7),
                lambda: make_hgbc(123), lambda: make_hgbc_a0(42)]
LGBM_MEMBERS = [lambda: make_lgbm(42), lambda: make_lgbm(7),
                lambda: make_lgbm63(42)]

CANDIDATES = {
    "w40_priors": {"hgbc_w": 0.40, "priors": np.array([0.95, 1.2, 1.0])},
    "w50_plain": {"hgbc_w": 0.50, "priors": np.ones(3)},
}


def main():
    train, test = load_raw()
    y = train.health_condition.values
    X_h, Xt_h = encode(train, test)
    X_l, Xt_l = encode_lgbm(train, test)
    w = compute_sample_weight("balanced", y)

    def fit_group(factories, X, Xt, use_weights):
        probas = []
        for i, factory in enumerate(factories):
            t0 = time.time()
            m = factory().fit(X, y, sample_weight=w) if use_weights else factory().fit(X, y)
            assert list(m.classes_) == CLASSES.tolist()
            probas.append(m.predict_proba(Xt))
            print(f"  member {i}: fit+predict {time.time() - t0:.0f}s", flush=True)
        return np.mean(probas, axis=0)

    print("HGBC group (4 members):")
    hgbc_avg = fit_group(HGBC_MEMBERS, X_h, Xt_h, use_weights=True)
    print("LGBM group (3 members):")
    lgbm_avg = fit_group(LGBM_MEMBERS, X_l, Xt_l, use_weights=False)

    for name, cfg in CANDIDATES.items():
        proba = cfg["hgbc_w"] * hgbc_avg + (1 - cfg["hgbc_w"]) * lgbm_avg
        pred = CLASSES[(proba * cfg["priors"]).argmax(1)]
        sub = pd.DataFrame({"id": test.id, "health_condition": pred})
        path = OUT / f"submission_{name}.csv"
        sub.to_csv(path, index=False)
        print(f"wrote {path.name}; mix "
              f"{sub.health_condition.value_counts(normalize=True).round(3).to_dict()}")


if __name__ == "__main__":
    main()
