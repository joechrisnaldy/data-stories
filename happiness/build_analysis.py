"""Post 09 analysis: Indonesia's generosity paradox and the gap between evaluated (ladder) and
experienced (affect) happiness. World Happiness Report 2024 + 2005-2024 panel. Writes
results.json. Descriptive/associational only."""
import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
cross = pd.read_csv(BASE / "data" / "world-happiness-2024.csv", encoding="latin-1")
panel = pd.read_csv(BASE / "data" / "world-happiness-panel-2005-2024.csv", encoding="latin-1")

region = dict(zip(cross["Country name"], cross["Regional indicator"]))
latest = panel.sort_values("year").groupby("Country name").tail(1).copy()
L = latest.dropna(subset=["Life Ladder", "Positive affect", "Negative affect",
                          "Generosity", "Social support", "Log GDP per capita"]).copy()
L["region"] = L["Country name"].map(region).fillna("Other")
L["ladder_rank"] = L["Life Ladder"].rank(ascending=False).astype(int)
L["posaff_rank"] = L["Positive affect"].rank(ascending=False).astype(int)


def rank_desc(series, country):
    v = series[L["Country name"] == country].iloc[0]
    return int((series > v).sum()) + 1


ic = cross[cross["Country name"] == "Indonesia"].iloc[0]
ladder_rank_2024 = int((cross["Ladder score"] > ic["Ladder score"]).sum()) + 1
il = L[L["Country name"] == "Indonesia"].iloc[0]
indonesia = {
    "ladder_2024": round(float(ic["Ladder score"]), 2), "n_2024": int(len(cross)),
    "ladder_rank_2024": ladder_rank_2024,
    "generosity": round(float(il["Generosity"]), 3),
    "generosity_rank": rank_desc(L["Generosity"], "Indonesia"),
    "positive_affect": round(float(il["Positive affect"]), 3),
    "positive_affect_rank": rank_desc(L["Positive affect"], "Indonesia"),
    "ladder_panel": round(float(il["Life Ladder"]), 2),
    "ladder_rank_panel": rank_desc(L["Life Ladder"], "Indonesia"), "n_panel": int(len(L)),
}
corr = {
    "generosity_ladder": round(float(L["Generosity"].corr(L["Life Ladder"])), 3),
    "posaff_ladder": round(float(L["Positive affect"].corr(L["Life Ladder"])), 3),
    "negaff_ladder": round(float(L["Negative affect"].corr(L["Life Ladder"])), 3),
    "social_ladder": round(float(L["Social support"].corr(L["Life Ladder"])), 3),
}
lin = LinearRegression().fit(L[["Log GDP per capita"]], L["Life Ladder"])
corr["loggdp_ladder_r2"] = round(float(lin.score(L[["Log GDP per capita"]], L["Life Ladder"])), 3)

scatter = [{"country": r["Country name"], "ladder": round(float(r["Life Ladder"]), 2),
            "posaff": round(float(r["Positive affect"]), 3), "region": r["region"]}
           for _, r in L.iterrows()]
generosity_top = [{"country": r["Country name"], "generosity": round(float(r["Generosity"]), 3),
                   "ladder": round(float(r["Life Ladder"]), 2)}
                  for _, r in L.nlargest(10, "Generosity").iterrows()]
curated = []
for cty in ["Indonesia", "Finland", "Costa Rica", "Poland"]:
    row = L[L["Country name"] == cty]
    if len(row):
        r = row.iloc[0]
        curated.append({"country": cty, "ladder_rank": int(r["ladder_rank"]),
                        "posaff_rank": int(r["posaff_rank"]),
                        "ladder": round(float(r["Life Ladder"]), 2),
                        "posaff": round(float(r["Positive affect"]), 3)})
L["gap"] = L["ladder_rank"] - L["posaff_rank"]  # positive => feel more than they rate
feel_more = [r["Country name"] for _, r in L.nlargest(6, "gap").iterrows()]
rate_more = [r["Country name"] for _, r in L.nsmallest(6, "gap").iterrows()]

out = {"indonesia": indonesia, "corr": corr, "n_panel": int(len(L)), "scatter": scatter,
       "generosity_top": generosity_top, "curated": curated,
       "feel_more": feel_more, "rate_more": rate_more}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("Indonesia:", indonesia)
print("corr:", corr)
print("feel_more:", feel_more)
print("rate_more:", rate_more)
print("curated:", [(c["country"], "ladder#" + str(c["ladder_rank"]), "feel#" + str(c["posaff_rank"])) for c in curated])
