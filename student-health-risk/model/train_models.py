"""Two models, identical except for what they are told to care about.

The whole argument of the post: same HistGradientBoostingClassifier, same features,
same hyperparameters, same data. The ONLY difference is the sample weights.

  - Model A (accuracy):  no weights. Leans on the 86% majority.
  - Model B (balanced):  'balanced' sample weights. Forced to care about the rare
                         classes, which is exactly what the competition metric
                         (balanced accuracy) rewards.

Prints validation accuracy, balanced accuracy, and per-class recall for each, writes
two Kaggle submissions, and saves results.json for the charts.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = BASE / "model"
RANDOM_STATE = 42

NUMERIC = ["sleep_duration", "heart_rate", "bmi", "calorie_expenditure",
           "step_count", "exercise_duration", "water_intake"]
CATEGORICAL = ["diet_type", "stress_level", "sleep_quality",
               "physical_activity_level", "smoking_alcohol", "gender"]


def encode(train, test):
    """Numeric columns pass through; categoricals become codes with NaN kept as NaN
    (categories learned from train+test together so codes align). HGBC handles NaN."""
    X_tr = train[NUMERIC].copy()
    X_te = test[NUMERIC].copy()
    for c in CATEGORICAL:
        cats = pd.Categorical(pd.concat([train[c], test[c]], ignore_index=True)).categories
        for src, dst in ((train, X_tr), (test, X_te)):
            codes = pd.Categorical(src[c], categories=cats).codes.astype("float64")
            codes[codes == -1] = np.nan  # let the model treat missing as missing
            dst[c] = codes
    return X_tr, X_te


def make_model():
    # Identical config for A and B; only the fit-time sample weights differ.
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
        early_stopping=True, validation_fraction=0.1, random_state=RANDOM_STATE)


def evaluate(name, y_true, y_pred, labels):
    acc = accuracy_score(y_true, y_pred)
    bal = balanced_accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    recall = cm.diagonal() / cm.sum(axis=1)
    print(f"\n{name}: accuracy={acc:.4f}  balanced_accuracy={bal:.4f}")
    for lab, r in zip(labels, recall):
        print(f"   recall[{lab:>9}] = {r:.3f}")
    return {"accuracy": acc, "balanced_accuracy": bal,
            "confusion": cm.tolist(), "recall": recall.tolist()}


def main():
    train = pd.read_csv(DATA / "train.csv")
    test = pd.read_csv(DATA / "test.csv")
    labels = ["fit", "at-risk", "unhealthy"]  # display order: good -> bad
    y = train.health_condition.values
    X, X_test = encode(train, test)
    print(f"train {X.shape}  test {X_test.shape}  classes {labels}")

    # all-at-risk baseline (the floor the essay opens on)
    base_pred = np.full(len(y), "at-risk")
    base = {"accuracy": accuracy_score(y, base_pred),
            "balanced_accuracy": balanced_accuracy_score(y, base_pred)}
    print(f"\nall-'at-risk' baseline: accuracy={base['accuracy']:.4f}  "
          f"balanced_accuracy={base['balanced_accuracy']:.4f}")

    # stratified validation split
    X_tr, X_va, y_tr, y_va = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE)
    w_tr = compute_sample_weight("balanced", y_tr)

    results = {"labels": labels, "baseline": base, "n_train": len(train),
               "n_test": len(test),
               "class_counts": train.health_condition.value_counts().to_dict()}

    model_a = make_model().fit(X_tr, y_tr)
    results["A"] = evaluate("Model A (accuracy)", y_va, model_a.predict(X_va), labels)

    model_b = make_model().fit(X_tr, y_tr, sample_weight=w_tr)
    results["B"] = evaluate("Model B (balanced)", y_va, model_b.predict(X_va), labels)

    # refit on all data and write the two submissions
    full_a = make_model().fit(X, y)
    full_b = make_model().fit(X, y, sample_weight=compute_sample_weight("balanced", y))
    for tag, model in (("A", full_a), ("B", full_b)):
        sub = pd.DataFrame({"id": test.id, "health_condition": model.predict(X_test)})
        sub.to_csv(OUT / f"submission_{tag}.csv", index=False)
        dist = sub.health_condition.value_counts(normalize=True).round(3).to_dict()
        print(f"\nsubmission_{tag}.csv written; predicted mix: {dist}")
        results[tag]["test_pred_dist"] = dist

    (OUT / "results.json").write_text(json.dumps(results, indent=2))
    print(f"\nsaved {(OUT / 'results.json').relative_to(BASE)}")


if __name__ == "__main__":
    main()
