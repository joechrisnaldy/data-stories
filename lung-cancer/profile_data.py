"""Vet profile for Kaggle mysarahmadbhat/lung-cancer ('survey lung cancer.csv'), Post 13 go/no-go.
Central questions: is it real or synthetic; is the target usable (balance); and does SMOKING
actually predict LUNG_CANCER here, or does selection bias wash it out (the likely story)."""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "survey lung cancer.csv")
df.columns = [c.strip() for c in df.columns]

print("=== SHAPE / MISSING / DUPES ===")
print("shape:", df.shape)
print("missing:", int(df.isna().sum().sum()))
print("exact duplicate rows:", int(df.duplicated().sum()))

# recode: binary symptom cols are 1=NO / 2=YES -> 0/1; target YES/NO -> 1/0; gender M/F
sym = [c for c in df.columns if c not in ("GENDER", "AGE", "LUNG_CANCER")]
d = df.copy()
for c in sym:
    d[c] = d[c].map({1: 0, 2: 1})
d["CANCER"] = d["LUNG_CANCER"].str.strip().map({"YES": 1, "NO": 0})
d["MALE"] = (d["GENDER"].str.strip() == "M").astype(int)

print("\n=== TARGET BALANCE (a control-less, skewed target = can't answer 'does X cause cancer') ===")
print(df["LUNG_CANCER"].value_counts())
print(f"cancer rate = {d['CANCER'].mean():.3f}")
print("AGE:", df["AGE"].describe()[["min", "mean", "max"]].round(1).to_dict())

print("\n=== THE HEADLINE QUESTION: does SMOKING predict CANCER here? ===")
ct = pd.crosstab(d["SMOKING"].map({0: "non-smoker", 1: "smoker"}), d["LUNG_CANCER"].str.strip())
print(ct.to_string())
p_smoker = d[d.SMOKING == 1]["CANCER"].mean()
p_non = d[d.SMOKING == 0]["CANCER"].mean()
print(f"P(cancer | smoker)     = {p_smoker:.3f}  (n={int((d.SMOKING==1).sum())})")
print(f"P(cancer | non-smoker) = {p_non:.3f}  (n={int((d.SMOKING==0).sum())})")
# Fisher exact odds ratio + p
tab = pd.crosstab(d["SMOKING"], d["CANCER"]).reindex(index=[0, 1], columns=[0, 1]).fillna(0).values
orr, p = stats.fisher_exact(tab)
print(f"Fisher exact: odds ratio = {orr:.2f}, p = {p:.3f}  (smoking vs cancer)")

print("\n=== WHAT ACTUALLY CORRELATES WITH CANCER IN THIS DATA (phi / point-biserial, ranked) ===")
feats = sym + ["MALE", "AGE"]
rows = []
for c in feats:
    r = np.corrcoef(d[c], d["CANCER"])[0, 1]
    rows.append((c, r))
rank = pd.DataFrame(rows, columns=["feature", "corr_with_cancer"]).reindex(
    columns=["feature", "corr_with_cancer"]).sort_values("corr_with_cancer", key=abs, ascending=False)
print(rank.round(3).to_string(index=False))

print("\n=== is smoking even correlated with the SYMPTOMS? (yellow fingers should be, if real) ===")
for c in ["YELLOW_FINGERS", "COUGHING", "CHEST PAIN", "SHORTNESS OF BREATH"]:
    if c in d:
        print(f"corr(SMOKING, {c}) = {np.corrcoef(d['SMOKING'], d[c])[0,1]:.3f}")
