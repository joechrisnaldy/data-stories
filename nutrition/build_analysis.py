"""Post 08 analysis: reverse-engineer the 'Nutrition Density' score (an exact sum of 8
nutrients), decompose its contribution shares to expose unit-mixing, and confirm calories
are Atwater 4/4/9 arithmetic. Writes results.json. Descriptive/associational only."""
import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
frames = [pd.read_csv(p) for p in sorted((BASE / "data").glob("FOOD-DATA-GROUP*.csv"))]
df = pd.concat(frames, ignore_index=True)
df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed") or c == ""],
             errors="ignore")

NUTRIENTS = [c for c in df.select_dtypes("number").columns if c != "Nutrition Density"]
UNIT = {"Fat": "g", "Carbohydrates": "g", "Protein": "g", "Dietary Fiber": "g",
        "Vitamin A": "ug", "Vitamin C": "mg", "Calcium": "mg", "Iron": "mg"}

# (1) recover the formula: regress the score on the 33 nutrient columns
lin = LinearRegression().fit(df[NUTRIENTS], df["Nutrition Density"])
w = pd.Series(lin.coef_, index=NUTRIENTS)
ingredients = [c for c in NUTRIENTS if w[c] >= 0.5]
raw_sum = df[ingredients].sum(axis=1)
max_abs_diff = float((df["Nutrition Density"] - raw_sum).abs().max())
r2 = float(lin.score(df[NUTRIENTS], df["Nutrition Density"]))

# (2) decompose contribution shares (mean value of each ingredient / total)
mean_contrib = df[ingredients].mean()
share = mean_contrib / mean_contrib.sum() * 100
contribution = sorted(
    [{"term": t, "unit": UNIT.get(t, "?"), "mean": round(float(mean_contrib[t]), 2),
      "share_pct": round(float(share[t]), 1)} for t in ingredients],
    key=lambda r: r["share_pct"], reverse=True)

density_calorie_corr = float(df["Nutrition Density"].corr(df["Caloric Value"]))
density_calcium_corr = float(df["Nutrition Density"].corr(df["Calcium"]))

# (3) calories = Atwater 4/4/9
pred = 4 * df.Carbohydrates + 4 * df.Protein + 9 * df.Fat
resid = df["Caloric Value"] - pred
macro_sum = df.Fat + df.Carbohydrates + df.Protein + df.Water
clean = df["Caloric Value"].between(1, 900) & (macro_sum <= 105)  # physically plausible
water_over_100 = int((df.Water > 100).sum())
mass_violation_pct = round(float((macro_sum > 105).mean() * 100), 1)
corr_all = float(df["Caloric Value"].corr(pred))
corr_clean = float(df.loc[clean, "Caloric Value"].corr(pred[clean]))
scatter = [{"pred": round(float(pred[i]), 1), "actual": round(float(df["Caloric Value"][i]), 1)}
           for i in df.index[clean]]
mdf = df.assign(pred=pred, resid=resid)
mdf = mdf.reindex(resid.abs().sort_values(ascending=False).index).head(6)
misses = [{"food": r["food"], "actual": round(float(r["Caloric Value"]), 1),
           "pred": round(float(r["pred"]), 1), "resid": round(float(r["resid"]), 1)}
          for _, r in mdf.iterrows()]

out = {
    "n_foods": int(len(df)),
    "recipe": {"r2": round(r2, 4), "ingredients": ingredients,
               "max_abs_diff": round(max_abs_diff, 3),
               "weights_all": [{"nutrient": c, "weight": round(float(w[c]), 3)}
                               for c in w.sort_values(ascending=False).index]},
    "contribution": contribution,
    "density_calorie_corr": round(density_calorie_corr, 3),
    "density_calcium_corr": round(density_calcium_corr, 3),
    "atwater": {"corr_all": round(corr_all, 4), "corr_clean": round(corr_clean, 4),
                "median_abs_err_clean": round(float(resid[clean].abs().median()), 2),
                "within20_clean_pct": round(float((resid[clean].abs() <= 20).mean() * 100), 1),
                "n_clean": int(clean.sum()), "n_all": int(len(df))},
    "atwater_scatter": scatter,
    "atwater_misses": misses,
    "data_quality": {"water_over_100g": water_over_100,
                     "mass_violation_pct": mass_violation_pct,
                     "clean_calorie_bounds": [1, 900], "clean_mass_max_g": 105,
                     "n_clean": int(clean.sum())},
}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("recipe R^2:", out["recipe"]["r2"], "| ingredients:", ingredients)
print("max abs diff (density - raw sum):", out["recipe"]["max_abs_diff"])
for c in contribution:
    print(f"  {c['term']:16s} ({c['unit']}) {c['share_pct']:5.1f}%")
print("density~calories r:", out["density_calorie_corr"], "density~calcium r:", out["density_calcium_corr"])
print("Atwater corr_clean:", out["atwater"]["corr_clean"],
      "median_abs_err:", out["atwater"]["median_abs_err_clean"],
      "within20%:", out["atwater"]["within20_clean_pct"], "n_clean:", out["atwater"]["n_clean"])
print("biggest misses:", [(m["food"], m["actual"], m["resid"]) for m in misses[:4]])
