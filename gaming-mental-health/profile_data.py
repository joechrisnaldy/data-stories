"""Profile the gaming-addiction dataset to inform the article angle.
Small n (250), mental-health topic: profile carefully, flag construction artifacts."""
import numpy as np
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 60)

df = pd.read_csv("data/gaming_addiction.csv")
print(f"shape: {df.shape[0]} rows x {df.shape[1]} cols")

print("\n=== columns: dtype, missing, nunique ===")
info = pd.DataFrame({"dtype": df.dtypes.astype(str),
                     "missing": df.isna().sum(),
                     "nunique": df.nunique()})
print(info.to_string())

num = df.select_dtypes("number").columns.tolist()
cat = [c for c in df.columns if c not in num]

print("\n=== numeric summary ===")
print(df[num].describe().T[["mean", "std", "min", "50%", "max"]].round(2).to_string())

print("\n=== categorical value counts (<=12 levels) ===")
for c in cat:
    if df[c].nunique() <= 12:
        print(f"\n-- {c} --")
        print(df[c].value_counts(dropna=False).to_string())

# The key outcome-ish fields
print("\n=== target-like fields ===")
for c in ["addiction_score", "addiction_binary", "addiction_severity",
          "behavioral_cluster", "mental_health_risk_score", "burnout_probability",
          "churn_probability", "depression_indicator"]:
    if c in df.columns:
        if df[c].dtype == object:
            print(f"{c}: {df[c].value_counts().to_dict()}")
        else:
            print(f"{c}: min={df[c].min()} max={df[c].max()} mean={df[c].mean():.2f}")

# Construction check: is addiction_score a deterministic function of the features?
# Correlate everything numeric with addiction_score to spot near-perfect drivers.
print("\n=== top correlations with addiction_score ===")
if "addiction_score" in num:
    corr = df[num].corr()["addiction_score"].drop("addiction_score").sort_values(
        key=abs, ascending=False)
    print(corr.head(15).round(3).to_string())
