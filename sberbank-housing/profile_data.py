"""Quick profile of the Sberbank housing dataset to inform blog-angle brainstorming."""
import pandas as pd

pd.set_option("display.width", 200)

train = pd.read_csv("data/train.csv", parse_dates=["timestamp"])
macro = pd.read_csv("data/macro.csv", parse_dates=["timestamp"])

print("=== TRAIN ===")
print(f"shape: {train.shape[0]:,} rows x {train.shape[1]} cols")
print(f"date range: {train.timestamp.min().date()} -> {train.timestamp.max().date()}")

p = train.price_doc
print("\n--- price_doc (RUB) ---")
print(p.describe().apply(lambda x: f"{x:,.0f}").to_string())
print(f"sales at exactly 1M RUB: {(p == 1_000_000).sum():,}  |  at 2M: {(p == 2_000_000).sum():,}")

print("\n--- key columns missingness (top 15) ---")
miss = train.isna().mean().sort_values(ascending=False)
print((miss.head(15) * 100).round(1).to_string())

print("\n--- fields of interest ---")
for col in ["full_sq", "life_sq", "num_room", "build_year", "kitch_sq", "state", "floor", "max_floor"]:
    s = train[col]
    print(f"{col:12s} missing={s.isna().mean()*100:4.1f}%  min={s.min()}  max={s.max()}")

print(f"\nproduct_type: {train.product_type.value_counts().to_dict()}")
print(f"sub_area (districts): {train.sub_area.nunique()} unique")
print(f"ecology: {train.ecology.value_counts().to_dict()}")

print("\n--- sales per year, median price, median price/sqm ---")
t = train[["timestamp", "price_doc", "full_sq"]].copy()
t["year"] = t.timestamp.dt.year
t["psqm"] = t.price_doc / t.full_sq.where(t.full_sq > 10)
print(t.groupby("year").agg(n=("price_doc", "size"),
                            med_price=("price_doc", "median"),
                            med_psqm=("psqm", "median")).round(0).to_string())

print("\n=== MACRO ===")
print(f"shape: {macro.shape[0]:,} rows x {macro.shape[1]} cols")
print(f"date range: {macro.timestamp.min().date()} -> {macro.timestamp.max().date()}")
econ = [c for c in ["oil_urals", "usdrub", "eurrub", "cpi", "mortgage_rate", "deposits_rate",
                    "salary", "gdp_annual_growth", "unemployment", "rent_price_2room_eco"] if c in macro.columns]
m = macro.set_index("timestamp")[econ]
print("\n--- macro snapshot: Jan of each year ---")
print(m.resample("YS").first().round(2).to_string())
