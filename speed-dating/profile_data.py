"""Profile the Columbia speed dating dataset: shape, gender split, and the stated
preference and revealed rating columns the essay is built on."""
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Speed Dating Data.csv", encoding="latin-1")

print("rows:", len(df), "| subjects:", df.iid.nunique(), "| waves:", df.wave.nunique())
print("gender rows (0=F, 1=M):", df.gender.value_counts().to_dict())

STATED = ["attr1_1", "sinc1_1", "intel1_1", "fun1_1", "amb1_1", "shar1_1"]
RATE = ["attr", "sinc", "intel", "fun", "amb", "shar"]
print("stated cols present:", [c for c in STATED if c in df.columns])
print("rating cols present:", [c for c in RATE if c in df.columns])
print("dec present:", "dec" in df.columns, "| match present:", "match" in df.columns)
print("100-point-allocation waves rows (exclude 6-9):", int((~df.wave.isin([6, 7, 8, 9])).sum()))
