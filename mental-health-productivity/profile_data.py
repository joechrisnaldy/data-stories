"""Profile the mental-health-prediction dataset: shape, dtypes, distributions,
correlations among lifestyle inputs and wellbeing scores, and a circularity check
(can the labels / scores be reconstructed from the lifestyle inputs?)."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.model_selection import cross_val_score

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "mental_health_prediction.csv")

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 30)

print("shape:", df.shape)
print("\ndtypes:\n", df.dtypes.to_string())

cat = ["gender", "occupation", "mental_health_condition", "severity", "treatment"]
for c in cat:
    print(f"\n--- {c} ({df[c].nunique()} unique) ---")
    print(df[c].value_counts(dropna=False).to_string())

num = df.select_dtypes(include=[np.number]).columns.tolist()
print("\n=== numeric describe ===")
print(df[num].describe().round(2).T.to_string())

# wellbeing scores vs lifestyle inputs: correlation block
wellbeing = ["stress_level", "anxiety_score", "depression_score", "mood_score",
             "concentration_level"]
lifestyle = ["sleep_hours", "sleep_quality", "social_media_hours",
             "academic_work_pressure", "physical_activity_days",
             "work_life_balance", "social_support"]
present_w = [c for c in wellbeing if c in df.columns]
present_l = [c for c in lifestyle if c in df.columns]
print("\n=== Pearson corr: lifestyle inputs (rows) vs wellbeing scores (cols) ===")
print(df[present_l + present_w].corr().loc[present_l, present_w].round(2).to_string())

# circularity / reconstruction check: predict each score from the lifestyle inputs
# (HistGradientBoosting handles NaN natively, so no imputation needed)
print("\n=== reconstruct each wellbeing score from the 7 lifestyle inputs (5-fold CV R^2) ===")
for target in present_w:
    mask = df[target].notna().values
    Xm = df.loc[mask, present_l].values
    ym = df.loc[mask, target].values
    r2 = cross_val_score(HistGradientBoostingRegressor(random_state=0), Xm, ym,
                         cv=5, scoring="r2").mean()
    print(f"  {target:20s} R^2 = {r2:.3f}  (n={mask.sum()})")

# label circularity: predict mental_health_condition from (a) lifestyle inputs and
# (b) the wellbeing scores. If (b) is near-perfect, the label is a rule on the scores.
print("\n=== reconstruct mental_health_condition (4-class, chance = 0.25) 5-fold CV accuracy ===")
yc = df["mental_health_condition"].values
for name, cols in [("from 7 lifestyle inputs", present_l),
                   ("from 5 wellbeing scores", present_w),
                   ("from lifestyle + scores", present_l + present_w)]:
    acc = cross_val_score(HistGradientBoostingClassifier(random_state=0),
                          df[cols].values, yc, cv=5, scoring="accuracy").mean()
    print(f"  {name:26s} acc = {acc:.3f}")

# is anxiety/depression basically a function of stress? pairwise among scores
print("\n=== corr among the wellbeing scores themselves ===")
print(df[present_w].corr().round(2).to_string())

# label vs scores: does mental_health_condition track the scores deterministically?
print("\n=== mean scores by mental_health_condition ===")
print(df.groupby("mental_health_condition")[present_w].mean().round(2).to_string())
print("\n=== mean scores by severity ===")
print(df.groupby("severity")[present_w].mean().round(2).to_string())
