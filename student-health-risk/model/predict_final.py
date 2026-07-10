"""Refit the chosen final-push candidate on ALL training data and write the
submission. Reads the tuned prior weights for the candidate from final_push.json.

Usage: python model/predict_final.py blend_all3|blend_hgbc2|hgbc_c1_s42 [out.csv]
"""
import os

os.environ["OMP_NUM_THREADS"] = "6"

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sklearn.utils.class_weight import compute_sample_weight

from eval_common import encode, load_raw
from final_push import MEMBERS, encode_lgbm, make_hgbc, make_lgbm

CANDIDATE_MEMBERS = {
    "blend_all3": ["hgbc_c1_s42", "hgbc_c1_s7", "lgbm_s42"],
    "blend_hgbc2": ["hgbc_c1_s42", "hgbc_c1_s7"],
    "hgbc_c1_s42": ["hgbc_c1_s42"],
}


def main(candidate, out_name):
    results = json.loads((Path(__file__).parent / "final_push.json").read_text())
    prior_w = np.array(results[candidate]["weights"])
    member_names = CANDIDATE_MEMBERS[candidate]
    specs = {name: (kind, seed) for name, kind, seed in MEMBERS}

    train, test = load_raw()
    y = train.health_condition.values
    X_h, Xt_h = encode(train, test)
    X_l, Xt_l = encode_lgbm(train, test)
    w = compute_sample_weight("balanced", y)

    probas = []
    classes = None
    for name in member_names:
        kind, seed = specs[name]
        print(f"refit {name} on full train...", flush=True)
        if kind == "hgbc":
            m = make_hgbc(seed).fit(X_h, y, sample_weight=w)
            probas.append(m.predict_proba(Xt_h))
        else:
            m = make_lgbm(seed).fit(X_l, y)
            probas.append(m.predict_proba(Xt_l))
        classes = np.array(m.classes_)

    blend = np.mean(probas, axis=0) * prior_w
    pred = classes[blend.argmax(1)]
    sub = pd.DataFrame({"id": test.id, "health_condition": pred})
    out = Path(__file__).parent / out_name
    sub.to_csv(out, index=False)
    print(f"wrote {out}")
    print("predicted mix:", sub.health_condition.value_counts(normalize=True)
          .round(3).to_dict())
    print("prior weights applied:", prior_w.round(3).tolist(), "classes:", classes.tolist())


if __name__ == "__main__":
    cand = sys.argv[1] if len(sys.argv) > 1 else "blend_all3"
    out = sys.argv[2] if len(sys.argv) > 2 else f"submission_{cand}.csv"
    main(cand, out)
