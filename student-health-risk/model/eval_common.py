"""Shared evaluation protocol for the S6E7 leaderboard push.

Every experiment MUST report scores from this exact protocol so numbers are
comparable: stratified 5-fold CV (seed 42), scored as balanced accuracy of the
out-of-fold argmax predictions. The single 80/20 holdout used for the essay is
too noisy to rank changes worth ~0.0005.

Usage from a variant script:

    from eval_common import load_data, oof_evaluate
    X, y, X_test, test_id, classes = load_data()          # baseline features
    result = oof_evaluate(make_model, X, y)               # model factory
    # result: {"balanced_accuracy", "oof_proba", "classes"}

`oof_evaluate` also returns OOF probabilities so post-hoc decision rules
(per-class thresholds/priors) can be tuned without refitting.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold

DATA = Path(__file__).resolve().parent.parent / "data"
N_SPLITS = 5
SEED = 42

NUMERIC = ["sleep_duration", "heart_rate", "bmi", "calorie_expenditure",
           "step_count", "exercise_duration", "water_intake"]
CATEGORICAL = ["diet_type", "stress_level", "sleep_quality",
               "physical_activity_level", "smoking_alcohol", "gender"]


def load_raw():
    train = pd.read_csv(DATA / "train.csv")
    test = pd.read_csv(DATA / "test.csv")
    return train, test


def encode(train, test):
    """Baseline encoding: numerics pass through, categoricals -> codes, NaN kept."""
    X_tr = train[NUMERIC].copy()
    X_te = test[NUMERIC].copy()
    for c in CATEGORICAL:
        cats = pd.Categorical(pd.concat([train[c], test[c]], ignore_index=True)).categories
        for src, dst in ((train, X_tr), (test, X_te)):
            codes = pd.Categorical(src[c], categories=cats).codes.astype("float64")
            codes[codes == -1] = np.nan
            dst[c] = codes
    return X_tr, X_te


def load_data():
    train, test = load_raw()
    X, X_test = encode(train, test)
    return X, train.health_condition.values, X_test, test.id.values, None


def oof_evaluate(make_model, X, y, sample_weight_fn=None, verbose=True):
    """Stratified 5-fold OOF evaluation. `make_model()` returns a fresh estimator
    with predict_proba. `sample_weight_fn(y_fold)` optionally returns fit weights.
    Returns dict with balanced_accuracy (of argmax), oof_proba, classes."""
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof = None
    classes = None
    for k, (tr, va) in enumerate(skf.split(X, y)):
        m = make_model()
        kw = {}
        if sample_weight_fn is not None:
            kw["sample_weight"] = sample_weight_fn(y[tr])
        m.fit(X.iloc[tr], y[tr], **kw)
        proba = m.predict_proba(X.iloc[va])
        if oof is None:
            classes = np.array(m.classes_)
            oof = np.zeros((len(y), len(classes)))
        oof[va] = proba
        if verbose:
            fold_bal = balanced_accuracy_score(y[va], classes[proba.argmax(1)])
            print(f"  fold {k}: balanced_acc {fold_bal:.5f}")
    bal = balanced_accuracy_score(y, classes[oof.argmax(1)])
    if verbose:
        print(f"OOF balanced accuracy (argmax): {bal:.5f}")
    return {"balanced_accuracy": bal, "oof_proba": oof, "classes": classes}


def tune_class_priors(oof_proba, y, classes, n_iter=3, grid=None):
    """Coordinate-ascent search over per-class probability multipliers to maximize
    balanced accuracy of argmax(w * proba). Legitimate post-hoc decision rule:
    tuned on OOF predictions only. Returns (weights, tuned_balanced_accuracy)."""
    if grid is None:
        grid = np.linspace(0.6, 1.8, 25)
    w = np.ones(len(classes))
    best = balanced_accuracy_score(y, classes[(oof_proba * w).argmax(1)])
    for _ in range(n_iter):
        for j in range(len(classes)):
            for g in grid:
                w_try = w.copy()
                w_try[j] = g
                s = balanced_accuracy_score(y, classes[(oof_proba * w_try).argmax(1)])
                if s > best:
                    best, w = s, w_try
    return w, best
