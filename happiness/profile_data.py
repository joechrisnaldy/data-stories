"""Profile the World Happiness Report data. Two files: the 2024 cross-section (ladder +
factor contributions + dystopia) and the 2005-2024 panel (raw factors + positive/negative
affect). Probe: is the 2024 file contributions or raw? experienced-vs-evaluated (ladder vs
affect), income residuals (happier than money predicts), and Indonesia's profile."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
c = pd.read_csv(BASE / "data" / "world-happiness-2024.csv", encoding="latin-1")
p = pd.read_csv(BASE / "data" / "world-happiness-panel-2005-2024.csv", encoding="latin-1")

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

print("=== 2024 cross-section ===")
print("shape:", c.shape, "| countries:", c["Country name"].nunique())
print("columns:", list(c.columns))
FAC = ["Log GDP per capita", "Social support", "Healthy life expectancy",
       "Freedom to make life choices", "Generosity", "Perceptions of corruption"]
# contributions? sum of 6 factors + dystopia vs ladder
csum = c[FAC].sum(axis=1) + c["Dystopia + residual"]
print("\nfactor columns look like CONTRIBUTIONS if sum(6)+dystopia == ladder:")
print("  mean |sum - ladder| =", round((csum - c["Ladder score"]).abs().mean(), 4))
print("  factor value ranges:", {f: (round(c[f].min(), 2), round(c[f].max(), 2)) for f in FAC})
print("\ntop 5 ladder:\n", c.nlargest(5, "Ladder score")[["Country name", "Ladder score"]].to_string(index=False))
print("bottom 5 ladder:\n", c.nsmallest(5, "Ladder score")[["Country name", "Ladder score"]].to_string(index=False))
ind = c[c["Country name"] == "Indonesia"]
if len(ind):
    rank = int((c["Ladder score"] > ind["Ladder score"].iloc[0]).sum()) + 1
    print(f"\nIndonesia ladder {ind['Ladder score'].iloc[0]:.2f}, rank {rank} of {len(c)}")
    print(ind[FAC + ["Dystopia + residual"]].round(3).to_string(index=False))

print("\n=== panel 2005-2024 ===")
print("shape:", p.shape, "| years:", p.year.min(), "-", p.year.max())
print("columns:", list(p.columns))
latest = p.sort_values("year").groupby("Country name").tail(1).copy()
print("latest-year rows:", len(latest), "| year distribution:", latest.year.value_counts().to_dict())

# experienced vs evaluated: ladder vs positive/negative affect
sub = latest.dropna(subset=["Life Ladder", "Positive affect", "Negative affect"])
print("\ncorr Life Ladder vs Positive affect:", round(sub["Life Ladder"].corr(sub["Positive affect"]), 3))
print("corr Life Ladder vs Negative affect:", round(sub["Life Ladder"].corr(sub["Negative affect"]), 3))
# rank divergence: who FEELS better than they EVALUATE (positive affect rank >> ladder rank)
sub = sub.copy()
sub["ladder_rank"] = sub["Life Ladder"].rank(ascending=False)
sub["posaff_rank"] = sub["Positive affect"].rank(ascending=False)
sub["gap"] = sub["ladder_rank"] - sub["posaff_rank"]  # positive => feels better than evaluates
print("\nFEEL much better than they EVALUATE (top 8 positive gap):")
print(sub.nlargest(8, "gap")[["Country name", "Life Ladder", "Positive affect", "ladder_rank", "posaff_rank"]].round(2).to_string(index=False))
print("\nEVALUATE much better than they FEEL (top 8 negative gap):")
print(sub.nsmallest(8, "gap")[["Country name", "Life Ladder", "Positive affect", "ladder_rank", "posaff_rank"]].round(2).to_string(index=False))

# income residual: happier than log-GDP predicts
r = latest.dropna(subset=["Life Ladder", "Log GDP per capita"]).copy()
lin = LinearRegression().fit(r[["Log GDP per capita"]], r["Life Ladder"])
r["pred"] = lin.predict(r[["Log GDP per capita"]])
r["resid"] = r["Life Ladder"] - r["pred"]
print("\nR^2 of ladder ~ log GDP alone:", round(lin.score(r[["Log GDP per capita"]], r["Life Ladder"]), 3))
print("HAPPIER than income predicts (top 8):")
print(r.nlargest(8, "resid")[["Country name", "Life Ladder", "Log GDP per capita", "resid"]].round(2).to_string(index=False))
print("SADDER than income predicts (top 8):")
print(r.nsmallest(8, "resid")[["Country name", "Life Ladder", "Log GDP per capita", "resid"]].round(2).to_string(index=False))

# Indonesia in panel: generosity rank + affect
indp = latest[latest["Country name"] == "Indonesia"]
if len(indp):
    gr = int((latest["Generosity"] > indp["Generosity"].iloc[0]).sum()) + 1
    print(f"\nIndonesia (latest {int(indp.year.iloc[0])}): ladder {indp['Life Ladder'].iloc[0]:.2f}, "
          f"generosity {indp['Generosity'].iloc[0]:.3f} (rank {gr} of {len(latest)}), "
          f"pos affect {indp['Positive affect'].iloc[0]:.3f}, neg affect {indp['Negative affect'].iloc[0]:.3f}")
