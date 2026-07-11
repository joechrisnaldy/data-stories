"""Education ROI: total Master's cost per country, payback = cost / local average wage,
employment overlay. Restricted to the OECD destinations with wage + employment coverage.

total_cost = tuition * duration + rent * 12 * duration + visa + insurance (USD). This is a
lower bound on living cost (rent only, no food/transport); the same definition for every
country, so cross-country comparison is fair. payback = total_cost / average annual wage =
years of the local average salary to earn the degree back."""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
cost = pd.read_csv(BASE / "data" / "International_Education_Costs.csv")
wage = pd.read_csv(BASE / "external" / "oecd_avg_wages_2024.csv", comment="#")
emp = pd.read_csv(BASE / "external" / "employment_rate.csv", comment="#")

ALIAS = {"United States": "USA", "United Kingdom": "UK", "Korea": "South Korea",
         "Korea, Rep.": "South Korea", "Czechia": "Czech Republic", "Turkiye": "Turkey",
         "Türkiye": "Turkey", "Slovak Republic": "Slovakia"}
wage["country"] = wage.country.replace(ALIAS)
emp["country"] = emp.country.replace(ALIAS)

m = cost[cost.Level == "Master"].copy()
m["total_cost"] = (m.Tuition_USD * m.Duration_Years
                   + m.Rent_USD * 12 * m.Duration_Years
                   + m.Visa_Fee_USD + m.Insurance_USD)

agg = (m.groupby("Country")
       .agg(total_cost=("total_cost", "median"),
            tuition=("Tuition_USD", "median"),
            n_programs=("total_cost", "size"),
            avg_duration=("Duration_Years", "median")))
agg = agg[agg.n_programs >= 3]

w = wage.set_index("country").avg_annual_wage_usd_ppp
e = emp.set_index("country").employment_rate
agg = agg.join(w, how="inner").join(e, how="inner").rename(
    columns={"avg_annual_wage_usd_ppp": "avg_wage", "employment_rate": "employment"})
agg["payback_years"] = (agg.total_cost / agg.avg_wage).round(2)
agg["cost_rank"] = agg.total_cost.rank(ascending=False, method="min").astype(int)
agg["payback_rank"] = agg.payback_years.rank(ascending=False, method="min").astype(int)
agg["rank_shift"] = agg.cost_rank - agg.payback_rank  # positive = cheaper-looking than its payback

out = {
    "n_countries": int(len(agg)),
    "by_country": agg.reset_index().round(2).to_dict(orient="records"),
    "cheapest": str(agg.total_cost.idxmin()), "most_expensive": str(agg.total_cost.idxmax()),
    "best_payback": str(agg.payback_years.idxmin()), "worst_payback": str(agg.payback_years.idxmax()),
    "rank_corr": round(float(agg.cost_rank.corr(agg.payback_rank, method="spearman")), 3),
}
(BASE / "results.json").write_text(json.dumps(out, indent=2))

print("countries:", out["n_countries"], "| cost-vs-payback rank corr (Spearman):", out["rank_corr"])
print("cheapest total cost:", out["cheapest"], "| most expensive:", out["most_expensive"])
print("best payback:", out["best_payback"], "| worst payback:", out["worst_payback"])
print("\n--- sorted by payback (years of local salary to earn the degree back) ---")
show = agg.sort_values("payback_years")[["total_cost", "avg_wage", "payback_years", "employment", "cost_rank", "payback_rank"]]
print(show.to_string())
print("\n--- biggest movers (cost rank vs payback rank) ---")
print(agg.reindex(agg.rank_shift.abs().sort_values(ascending=False).index)[["total_cost","payback_years","cost_rank","payback_rank","rank_shift"]].head(8).to_string())
