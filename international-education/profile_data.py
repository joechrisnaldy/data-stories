"""Profile the international education cost dataset: shape, levels, per-country
Master's program counts, cost columns."""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "International_Education_Costs.csv")
print("shape:", df.shape, "| countries:", df.Country.nunique())
print("levels:", df.Level.value_counts().to_dict())
m = df[df.Level == "Master"]
print("Master rows:", len(m), "| countries with Masters:", m.Country.nunique())
print("Master programs per country (top 15):")
print(m.Country.value_counts().head(15).to_string())
print("cost columns nulls:", df[["Tuition_USD", "Rent_USD", "Visa_Fee_USD",
                                 "Insurance_USD", "Duration_Years"]].isna().sum().to_dict())
