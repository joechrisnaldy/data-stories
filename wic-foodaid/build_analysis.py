"""Post 12 analysis: WIC, the benefit that costs less than it delivers.
USDA WIC administrative tables (Kaggle jpmiller/publicassistance), FY2013-2016. Reconciled against
USDA FNS national totals (see docs/). Key facts verified at sourcing:
  - the dataset's Food_Costs = NET (post-rebate) food cost; gross = net + rebates.
  - drop the 'Mountain Plains' REGIONAL SUBTOTAL row and blank rows (they double-count).
  - cleaned figures match USDA national (FY2016 participation 7.70M, net food cost $3.95B, rebate $1.72B).
Writes results.json. Prints full tables. All numbers are descriptive administrative data."""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
YEARS = ["2013", "2014", "2015", "2016"]
# The 7 USDA FNS regions appear as SUBTOTAL rows mixed into the state list; exclude them.
REGIONS = {"mountain plains", "midwest", "northeast", "southeast", "southwest", "western",
           "mid-atlantic", "mid atlantic"}


def load(fy, name):
    d = pd.read_csv(BASE / "data" / f"WICAgencies{fy}ytd" / f"{name}.csv")
    d = d.rename(columns={d.columns[0]: "agency"})
    summ = d.columns[-1]  # last column is the annual summary (Cumulative Cost / Average Participation)
    d["val"] = pd.to_numeric(d[summ], errors="coerce")
    isreg = d.agency.astype(str).str.strip().str.lower().isin(REGIONS)
    return d[~isreg & d.val.notna()]


# --- annual net/gross/rebate/share + participation ---
rows = []
for fy in YEARS:
    net = load(fy, "Food_Costs").val.sum()                 # dataset Food_Costs = NET (post-rebate)
    reb = load(fy, "Rebates_Received").val.sum()
    part = load(fy, "Total_Number_of_Participants").val.sum()   # avg monthly participation
    gross = net + reb
    rows.append({"fy": int(fy), "net": float(net), "rebates": float(reb), "gross": float(gross),
                 "rebate_share_of_gross": round(reb / gross, 4), "participation": float(part)})
by_year = pd.DataFrame(rows)
print("=== WIC food economics by fiscal year (cleaned, national) ===")
show = by_year.copy()
for c in ["net", "rebates", "gross"]:
    show[c] = (show[c] / 1e9).round(2)
show["participation"] = (show["participation"] / 1e6).round(2)
show["rebate_share_of_gross"] = (show["rebate_share_of_gross"] * 100).round(1)
print(show.to_string(index=False))

# --- FY2016 headline + per person ---
r16 = by_year[by_year.fy == 2016].iloc[0]
pp_net = r16.net / r16.participation / 12
pp_gross = r16.gross / r16.participation / 12
print(f"\nFY2016: gross ${r16.gross/1e9:.2f}B delivered | net ${r16.net/1e9:.2f}B paid | "
      f"rebate ${r16.rebates/1e9:.2f}B ({r16.rebate_share_of_gross*100:.1f}% of gross)")
print(f"FY2016 per person/month: gross ${pp_gross:.2f} delivered vs net ${pp_net:.2f} paid "
      f"(USDA published net = $42.77)")

# --- FY2016 breastfeeding split (dataset, cleaned; corroborates USDA FNS BF report 13.2/18.5) ---
bf = {n: load("2016", f)["val"].sum() for n, f in
      {"fully": "Infants_Fully_Breastfed", "partial": "Infants_Partially_Breastfed",
       "formula": "Infants_Fully_Formula-fed", "total": "Total_Infants"}.items()}
bf_pct = {k: round(bf[k] / bf["total"] * 100, 1) for k in ["fully", "partial", "formula"]}
print(f"\nFY2016 WIC infants: fully breastfed {bf_pct['fully']}%, partially {bf_pct['partial']}%, "
      f"formula-only {bf_pct['formula']}%  (USDA FNS BF report: 13.2 / 18.5 / 68.3)")

out = {
    "by_year": rows,
    "fy2016": {"net": float(r16.net), "rebates": float(r16.rebates), "gross": float(r16.gross),
               "rebate_share_of_gross": float(r16.rebate_share_of_gross),
               "participation": float(r16.participation),
               "per_person_gross_month": round(pp_gross, 2), "per_person_net_month": round(pp_net, 2)},
    # breastfeeding: USDA FNS FY2016 Breastfeeding Data Local Agency Report (authoritative) + dataset check
    "breastfeeding": {"fully_bf_pct": 13.2, "partial_bf_pct": 18.5, "formula_only_pct": 68.3,
                      "dataset_check": bf_pct},
    # verified external context (USDA FNS / GAO / ERS); see docs references
    "context": {"usda_fy2016_net_foodcost_m": 3949.6, "usda_fy2016_rebate_b": 1.72,
                "usda_fy2016_participation_m": 7.70, "usda_fy2016_pp_net_month": 42.77,
                "usda_fy2024_net_foodcost_b": 4.91, "usda_fy2024_rebate_b": 1.6,
                "usda_fy2024_participation_m": 6.70, "usda_fy2024_pp_net_month": 61.06,
                "rebate_share_of_wholesale_2023_pct": 90, "rebate_share_of_wholesale_2020_pct": 124,
                "rebate_funds_caseload_pct_2023": 19.3,
                "gao_rebate_share_of_foodcost_low_2023_pct": 27, "gao_rebate_share_high_2020_pct": 39,
                "wic_formula_market_share": "over half (57-68% in 2004-06)",
                "indonesia_mbg_launch": "2025-01-06", "indonesia_mbg_target_m": 82.9,
                "indonesia_mbg_firststage_budget_rp_t": 71, "indonesia_mbg_firststage_usd_b": 4.39},
}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("\nwrote results.json")
