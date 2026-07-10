"""Baseline under the shared protocol: Model B (HGBC, balanced weights) with
5-fold OOF evaluation, plus the post-hoc class-prior tuning as a free first
improvement candidate. Writes baseline_cv.json."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.utils.class_weight import compute_sample_weight

from eval_common import load_data, oof_evaluate, tune_class_priors


def make_model():
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
        early_stopping=True, validation_fraction=0.1, random_state=42)


if __name__ == "__main__":
    X, y, X_test, test_id, _ = load_data()
    print("baseline: HGBC balanced weights, shared 5-fold protocol")
    res = oof_evaluate(make_model, X, y,
                       sample_weight_fn=lambda yy: compute_sample_weight("balanced", yy))
    w, tuned = tune_class_priors(res["oof_proba"], y, res["classes"])
    print(f"with tuned class priors {w.round(3).tolist()}: {tuned:.5f}")
    out = {"baseline_oof": res["balanced_accuracy"], "prior_tuned_oof": tuned,
           "prior_weights": w.tolist(), "classes": res["classes"].tolist()}
    Path(__file__).with_name("baseline_cv.json").write_text(json.dumps(out, indent=2))
    print("wrote baseline_cv.json")
