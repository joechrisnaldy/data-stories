"""Profile the synthetic loan-approval dataset. The dataset ships its own generator
(CSV_Generation.py). Key checks: does a HIGHER credit score really lower approval odds in the
shipped data (the inverted-sign bug)? what drives approval? do the two targets (LoanApproved
vs RiskScore) disagree about credit? is there baked-in age preference?"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Loan.csv")

print("shape:", df.shape)
print("approval rate:", round(df.LoanApproved.mean(), 3))
print("RiskScore range:", round(df.RiskScore.min(), 1), "-", round(df.RiskScore.max(), 1))

print("\n=== correlation with LoanApproved (approve=1) ===")
for c in ["CreditScore", "AnnualIncome", "TotalDebtToIncomeRatio", "DebtToIncomeRatio",
          "Age", "LoanAmount", "InterestRate", "NetWorth", "PaymentHistory",
          "LengthOfCreditHistory", "PreviousLoanDefaults", "BankruptcyHistory"]:
    if c in df.columns:
        print(f"  {c:26s} {df[c].corr(df.LoanApproved):+.3f}")

print("\n=== approval rate by CREDIT SCORE band (the key check) ===")
df["cs_band"] = pd.cut(df.CreditScore, [300, 580, 640, 700, 750, 850],
                       labels=["300-580 (poor)", "580-640", "640-700", "700-750", "750-850 (great)"])
print(df.groupby("cs_band", observed=True).LoanApproved.agg(["mean", "size"]).round(3).to_string())

print("\n=== CreditScore vs RiskScore (expect NEGATIVE: higher credit = lower risk) ===")
print("  corr(CreditScore, RiskScore):", round(df.CreditScore.corr(df.RiskScore), 3))
print("  corr(CreditScore, LoanApproved):", round(df.CreditScore.corr(df.LoanApproved), 3),
      "<-- if negative, higher credit LOWERS approval odds (inverted)")

print("\n=== do the two targets disagree? RiskScore by approval; approval by credit within risk ===")
print("  mean RiskScore, approved vs denied:",
      round(df[df.LoanApproved == 1].RiskScore.mean(), 1), "vs",
      round(df[df.LoanApproved == 0].RiskScore.mean(), 1))

print("\n=== approval rate by AGE band (baked-in preference for ~40?) ===")
df["age_band"] = pd.cut(df.Age, [17, 25, 35, 45, 55, 65, 80])
print(df.groupby("age_band", observed=True).LoanApproved.agg(["mean", "size"]).round(3).to_string())

print("\n=== what the 'bank' leans on: permutation importance for LoanApproved ===")
num = df.select_dtypes("number").drop(columns=["LoanApproved", "RiskScore"], errors="ignore")
clf = HistGradientBoostingClassifier(random_state=0).fit(num, df.LoanApproved)
print("  in-sample accuracy:", round(clf.score(num, df.LoanApproved), 3))
pim = permutation_importance(clf, num, df.LoanApproved, n_repeats=5, random_state=0)
imp = pd.Series(pim.importances_mean, index=num.columns).sort_values(ascending=False)
print(imp.head(10).round(4).to_string())
