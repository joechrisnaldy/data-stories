"""Post 07 analysis: rank the lifestyle levers of mental health (raw vs adjusted),
bridge to concentration (a productivity proxy). Writes results.json.
Data is synthetic (500 rows); associational only, no causal claims."""
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "mental_health_prediction.csv")

LEVERS = ["work_life_balance", "social_support", "sleep_quality", "sleep_hours",
          "physical_activity_days", "academic_work_pressure", "social_media_hours"]


def z(s):
    return (s - s.mean()) / s.std()


df["distress"] = (z(df.stress_level) + z(df.anxiety_score) + z(df.depression_score)) / 3.0


def rank_levers(target):
    """raw corr, standardized OLS beta (adjusted), permutation importance for one target."""
    raw = df[LEVERS].corrwith(df[target])  # pairwise-complete correlations
    sub = df[LEVERS + [target]].dropna()   # listwise-complete for the regression
    Xz = (sub[LEVERS] - sub[LEVERS].mean()) / sub[LEVERS].std()
    ols = LinearRegression().fit(Xz, sub[target])
    beta = pd.Series(ols.coef_, index=LEVERS)
    r2 = ols.score(Xz, sub[target])
    m = df[target].notna()                 # HGB handles NaN in X, needs complete y
    hgb = HistGradientBoostingRegressor(random_state=0).fit(df.loc[m, LEVERS], df.loc[m, target])
    pim = permutation_importance(hgb, df.loc[m, LEVERS], df.loc[m, target],
                                 n_repeats=30, random_state=0)
    perm = pd.Series(pim.importances_mean, index=LEVERS)
    rows = [{"lever": L, "raw_corr": round(float(raw[L]), 3),
             "std_beta": round(float(beta[L]), 3),
             "perm_imp": round(float(perm[L]), 4)} for L in LEVERS]
    rows.sort(key=lambda r: abs(r["std_beta"]), reverse=True)
    return {"levers": rows, "ols_r2": round(float(r2), 3),
            "n_listwise": int(len(sub)), "n_perm": int(m.sum())}


distress = rank_levers("distress")
concentration = rank_levers("concentration_level")

b = df[["distress", "concentration_level", "mental_health_condition"]].dropna()
bridge_corr = float(b["distress"].corr(b["concentration_level"]))
scatter = [{"d": round(float(r.distress), 3), "c": float(r.concentration_level),
            "cond": r.mental_health_condition} for r in b.itertuples()]

out = {"n_rows": int(len(df)), "distress": distress, "concentration": concentration,
       "bridge_corr": round(bridge_corr, 3), "bridge_n": int(len(b)), "scatter": scatter}
(BASE / "results.json").write_text(json.dumps(out, indent=2))

print("distress ranking (by |adjusted beta|):")
for r in distress["levers"]:
    print(f"  {r['lever']:24s} raw={r['raw_corr']:+.2f}  adj={r['std_beta']:+.2f}  perm={r['perm_imp']:.3f}")
print(f"OLS R^2={distress['ols_r2']}  n_listwise={distress['n_listwise']}  n_perm={distress['n_perm']}")
print(f"bridge distress~concentration r={bridge_corr:.3f}  n={len(b)}")
