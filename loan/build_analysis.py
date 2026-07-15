"""Post 10 analysis: read the bank's rulebook. What actually drives loan approval (income and
debt, not credit score), how credit acts through the interest rate, the not-about-risk factors
(age), and the fact that everyone here is already banked. Writes results.json. Synthetic data."""
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Loan.csv")

NICE = {"AnnualIncome": "annual income", "TotalDebtToIncomeRatio": "debt-to-income",
        "InterestRate": "loan interest rate", "LoanAmount": "loan amount", "NetWorth": "net worth",
        "CreditScore": "credit score", "Age": "age",
        "LengthOfCreditHistory": "credit-history length", "PreviousLoanDefaults": "past defaults"}
FEATS = list(NICE.keys())

# chart 1: correlation with approval for a curated, non-redundant feature set
corr_approval = sorted(
    [{"feature": f, "nice": NICE[f], "corr": round(float(df[f].corr(df.LoanApproved)), 3)}
     for f in FEATS], key=lambda r: abs(r["corr"]), reverse=True)

# permutation importance (concurs; routes through derived features like InterestRate)
num = df.select_dtypes("number").drop(columns=["LoanApproved", "RiskScore"], errors="ignore")
clf = HistGradientBoostingClassifier(random_state=0).fit(num, df.LoanApproved)
pim = permutation_importance(clf, num, df.LoanApproved, n_repeats=5, random_state=0)
importance = sorted([{"feature": c, "imp": round(float(v), 4)}
                     for c, v in zip(num.columns, pim.importances_mean)],
                    key=lambda r: r["imp"], reverse=True)[:8]

# chart 2: credit score prices you (credit -> interest rate)
credit_rate_corr = float(df.CreditScore.corr(df.InterestRate))
credit_approval_corr = float(df.CreditScore.corr(df.LoanApproved))
samp = df.sample(2500, random_state=0)
credit_rate_scatter = [{"credit": int(r.CreditScore), "rate": round(float(r.InterestRate), 4)}
                       for r in samp.itertuples()]

# chart 3: approval by age band (not-about-risk); plus education + season secondary
df["age_band"] = pd.cut(df.Age, [17, 25, 35, 45, 55, 65, 80],
                        labels=["under 25", "25-35", "35-45", "45-55", "55-65", "65+"])
approval_by_age = [{"band": str(b), "rate": round(float(g.LoanApproved.mean()), 3), "n": int(len(g))}
                   for b, g in df.groupby("age_band", observed=True)]
approval_by_edu = [{"edu": e, "rate": round(float(g.LoanApproved.mean()), 3), "n": int(len(g))}
                   for e, g in df.groupby("EducationLevel")]
month = pd.to_datetime(df.ApplicationDate).dt.month
ss = month.between(3, 8)
season = {"spring_summer_rate": round(float(df.LoanApproved[ss].mean()), 3),
          "rest_rate": round(float(df.LoanApproved[~ss].mean()), 3)}
# approval by application month: the CLEANEST not-about-risk factor. Application dates are assigned
# independently of the applicant in the generator, so this gap is purely the seasonal rule (+bonus
# for months 3-8), not confounded by income/experience the way the age and education gradients are.
approval_by_month = [{"month": int(m), "rate": round(float(g.LoanApproved.mean()), 3), "n": int(len(g))}
                     for m, g in df.groupby(month)]

# chart 4: everyone here is already legible to the bank
legible = {"n": int(len(df)),
           "with_credit_score": int((df.CreditScore > 0).sum()),
           "with_accounts": int(((df.SavingsAccountBalance > 0) | (df.CheckingAccountBalance > 0)).sum())}

out = {"n": int(len(df)), "approval_rate": round(float(df.LoanApproved.mean()), 3),
       "corr_approval": corr_approval, "importance": importance,
       "credit_rate_corr": round(credit_rate_corr, 3),
       "credit_approval_corr": round(credit_approval_corr, 3),
       "credit_rate_scatter": credit_rate_scatter,
       "approval_by_age": approval_by_age, "approval_by_edu": approval_by_edu,
       "season": season, "approval_by_month": approval_by_month, "legible": legible,
       "findex_unbanked_millions": 1300}  # EXTERNAL; World Bank Global Findex 2025 (verified Task 3)
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("approval rate:", out["approval_rate"])
print("corr with approval:", [(r["nice"], r["corr"]) for r in corr_approval])
print("top importance:", [(r["feature"], r["imp"]) for r in importance[:6]])
print("credit->rate corr:", out["credit_rate_corr"], "| credit->approval corr:", out["credit_approval_corr"])
print("approval by age:", [(r["band"], r["rate"]) for r in approval_by_age])
print("season:", season, "| legible:", legible)
