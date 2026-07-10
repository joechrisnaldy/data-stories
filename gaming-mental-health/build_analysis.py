"""Analysis for 'the conclusion was in the definition'.

Central claim (revised for honesty after adversarial review): addiction_score is a
CONSTRUCTED COMPOSITE built from the columns in the file, so it is circular by
construction. Playtime is its single biggest input, but it also loads on
impulse-control and functional-impairment columns, which is what makes it look like
a legitimate behavioral-addiction construct rather than an obvious relabeling.

We test reconstruction with cross-validated R2 on a LEAKAGE-CLEAN feature set that
excludes the other engineered sibling indices (mental_health_risk_score,
burnout_probability, churn_probability, dopamine_dependency_index), so the number is
raw inputs rebuilding the score, not composite-predicts-composite.

Outputs results.json and oof_pred.csv (out-of-fold reconstruction for the scatter).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_predict, cross_val_score

BASE = Path(__file__).resolve().parent
SEED = 42
KF = KFold(5, shuffle=True, random_state=SEED)

PLAYTIME = ["daily_playtime_hours", "screen_time_total_hours", "consecutive_hours_max",
            "late_night_sessions_hours", "weekly_play_sessions", "weekend_playtime_hours"]
# engineered sibling indices excluded from the leakage-clean reconstruction
SIBLINGS = ["addiction_score", "addiction_binary", "mental_health_risk_score",
            "burnout_probability", "churn_probability", "dopamine_dependency_index"]
IMPAIRMENT = ["missed_deadlines", "impulsiveness_score", "self_control_score"]
MENTALHEALTH = ["anxiety_level", "depression_indicator", "loneliness_score",
                "emotional_stability"]
WELLBEING = ["sleep_hours", "stress_score", "anxiety_level", "emotional_stability",
             "depression_indicator", "loneliness_score", "self_control_score",
             "impulsiveness_score", "social_interaction_hours", "gpa_or_performance_score"]


def cv_r2(cols, y):
    X = df[cols].fillna(df[cols].median())
    return float(np.mean(cross_val_score(LinearRegression(), X, y, cv=KF, scoring="r2")))


def signif(a, b):
    d = df[[a, b]].dropna()
    r, p = stats.pearsonr(d[a], d[b])
    lo, hi = np.tanh(np.arctanh(r) + np.array([-1, 1]) * 1.96 / np.sqrt(len(d) - 3))
    return {"r": round(float(r), 3), "p": round(float(p), 4),
            "ci": [round(float(lo), 2), round(float(hi), 2)], "n": int(len(d))}


df = pd.read_csv(BASE / "data" / "gaming_addiction.csv")
y = df.addiction_score
num = df.select_dtypes("number").columns.tolist()
clean = [c for c in num if c not in SIBLINGS]


def main():
    res = {"n": len(df), "n_cols": df.shape[1]}

    # 1. reconstruction (leakage-clean headline)
    res["r2_clean_cv"] = round(cv_r2(clean, y), 3)          # 0.91
    res["r2_all_cv"] = round(cv_r2([c for c in num if c not in
                                    ("addiction_score", "addiction_binary")], y), 3)  # 0.94
    res["r2_playtime_cv"] = round(cv_r2(PLAYTIME, y), 3)     # 0.75
    res["r2_daily_playtime_cv"] = round(cv_r2(["daily_playtime_hours"], y), 3)  # 0.74
    res["r2_nonplaytime_clean_cv"] = round(
        cv_r2([c for c in clean if c not in PLAYTIME], y), 3)  # 0.60
    oof = cross_val_predict(LinearRegression(),
                            df[clean].fillna(df[clean].median()), y, cv=KF)
    pd.DataFrame({"actual": y, "predicted": oof}).to_csv(BASE / "oof_pred.csv", index=False)
    print(f"reconstruction CV R2: clean {res['r2_clean_cv']}, all {res['r2_all_cv']}, "
          f"playtime6 {res['r2_playtime_cv']}, daily-playtime {res['r2_daily_playtime_cv']}, "
          f"non-playtime {res['r2_nonplaytime_clean_cv']}")

    # 2. what the score is built from: three tiers
    corr = df[num].corr()["addiction_score"].drop("addiction_score")
    res["corr_playtime"] = {c: round(float(corr[c]), 2) for c in PLAYTIME}
    res["corr_impairment"] = {c: round(float(corr[c]), 2) for c in IMPAIRMENT}
    res["corr_mentalhealth"] = {c: round(float(corr[c]), 2) for c in MENTALHEALTH}
    # impulse-control columns are ~orthogonal to hours (key to 'not just hours')
    res["impulse_vs_playtime"] = {
        c: round(float(df[c].corr(df.daily_playtime_hours)), 2)
        for c in ["impulsiveness_score", "self_control_score"]}

    # 3. the harm the name promises: small, mixed, mostly mundane (with significance)
    res["playtime_vs_wellbeing"] = {c: signif("daily_playtime_hours", c) for c in WELLBEING}

    # 4. the tells
    res["tells"] = {
        "burnout_prob_eq_1_share": round(float((df.burnout_probability == 1.0).mean()), 3),
        "gpa_eq_4_share": round(float((df.gpa_or_performance_score == 4.0).mean()), 3),
    }
    res["cluster_score_means"] = (df.groupby("behavioral_cluster").addiction_score.mean()
                                  .round(1).to_dict())

    (BASE / "results.json").write_text(json.dumps(res, indent=2))
    print("\n" + json.dumps(res, indent=2))
    print("\nsaved results.json, oof_pred.csv")


if __name__ == "__main__":
    main()
