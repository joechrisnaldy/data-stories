"""Profile the Food Nutrition dataset (5 group CSVs, ~2,395 foods, per 100g).
Data-quality read + two story probes: (1) do calories add up from macros (Atwater)?
(2) what is the black-box 'Nutrition Density' metric actually made of?"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

BASE = Path(__file__).resolve().parent
paths = sorted((BASE / "data").glob("FOOD-DATA-GROUP*.csv"))
frames = []
for i, p in enumerate(paths, 1):
    d = pd.read_csv(p)
    d["group"] = i
    frames.append(d)
df = pd.concat(frames, ignore_index=True)
# drop the two unnamed index columns
df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed") or c == ""],
             errors="ignore")

print("shape:", df.shape, "| rows per group:", [len(f) for f in frames])
print("unique foods:", df.food.nunique(), "| exact-dup rows:", df.duplicated().sum())
print("\ncolumns:", [c for c in df.columns if c not in ("food", "group")])

num = df.select_dtypes(include=[np.number]).columns.tolist()
print("\n=== value ranges (min / max / #negative / #NaN) ===")
for c in num:
    neg = int((df[c] < 0).sum())
    print(f"  {c:22s} min={df[c].min():10.3f} max={df[c].max():12.3f} neg={neg} nan={int(df[c].isna().sum())}")

# (1) ATWATER: do calories = 4*carb + 4*protein + 9*fat ?
atw = 4 * df.Carbohydrates + 4 * df.Protein + 9 * df.Fat
resid = df["Caloric Value"] - atw
print("\n=== Atwater calorie check (4*carb + 4*protein + 9*fat vs Caloric Value) ===")
print(f"  corr={df['Caloric Value'].corr(atw):.4f}")
print(f"  median abs residual={resid.abs().median():.2f} kcal  mean abs={resid.abs().mean():.2f}")
print(f"  within 5 kcal: {(resid.abs() <= 5).mean():.1%}  | within 20 kcal: {(resid.abs() <= 20).mean():.1%}")
# try including fiber (2 kcal/g) and subtracting nothing
atw2 = 4 * df.Carbohydrates + 4 * df.Protein + 9 * df.Fat - 4 * df["Dietary Fiber"] + 2 * df["Dietary Fiber"]
print(f"  with fiber at 2 kcal/g: median abs={ (df['Caloric Value'] - atw2).abs().median():.2f}")

# (2) NUTRITION DENSITY: reverse-engineer. Is it a simple formula?
feats = [c for c in num if c not in ("Nutrition Density", "group")]
X = df[feats].fillna(0).values
y = df["Nutrition Density"].values
lin = LinearRegression().fit(X, y)
print("\n=== reverse-engineer 'Nutrition Density' ===")
print(f"  linear R^2 (all {len(feats)} nutrients): {lin.score(X, y):.4f}")
r2_cv = cross_val_score(HistGradientBoostingRegressor(random_state=0), X, y, cv=5, scoring="r2").mean()
print(f"  gradient-boosting 5-fold CV R^2: {r2_cv:.4f}")
coef = pd.Series(lin.coef_, index=feats).sort_values(key=abs, ascending=False)
print("  top standardized-ish linear drivers (raw coef):")
print(coef.head(10).round(4).to_string())
# correlation of density with each nutrient
corr = df[feats].corrwith(df["Nutrition Density"]).sort_values(key=abs, ascending=False)
print("\n  top |correlation| with Nutrition Density:")
print(corr.head(10).round(3).to_string())

# (3) energy density story: water vs calories
print("\n=== energy density: correlation of Caloric Value with water & fat ===")
for c in ["Water", "Fat", "Sugars", "Protein", "Carbohydrates"]:
    print(f"  {c:16s} corr with Caloric Value = {df['Caloric Value'].corr(df[c]):+.3f}")

# what are the groups? mean caloric value + a couple markers by group
print("\n=== group profiles (are they food categories?) ===")
print(df.groupby("group")[["Caloric Value", "Sugars", "Protein", "Fat", "Water"]].mean().round(1).to_string())
print("\nsample foods per group:")
for g, gdf in df.groupby("group"):
    print(f"  group {g}: {', '.join(gdf.food.head(6).tolist())}")
