"""Profile the Playground S6E7 student-health data to inform the article angle."""
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 40)

train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

print(f"train: {train.shape[0]:,} x {train.shape[1]}   test: {test.shape[0]:,} x {test.shape[1]}")

print("\n=== TARGET: health_condition ===")
vc = train.health_condition.value_counts(dropna=False)
prop = (vc / len(train) * 100).round(2)
print(pd.DataFrame({"count": vc, "pct": prop}).to_string())
print(f"n classes: {train.health_condition.nunique()}")
print(f"majority-class baseline balanced accuracy = {1/train.health_condition.nunique():.4f} "
      "(balanced acc rewards getting rare classes right)")

print("\n=== COLUMNS: dtype, missing%, nunique ===")
info = pd.DataFrame({
    "dtype": train.dtypes.astype(str),
    "missing_pct": (train.isna().mean() * 100).round(2),
    "nunique": train.nunique(),
})
print(info.to_string())

num_cols = [c for c in train.columns if pd.api.types.is_numeric_dtype(train[c])
            and c != "id"]
cat_cols = [c for c in train.columns if not pd.api.types.is_numeric_dtype(train[c])
            and c != "health_condition"]

print("\n=== NUMERIC summary ===")
print(train[num_cols].describe().T.round(2).to_string())

print("\n=== CATEGORICAL / low-cardinality value counts ===")
for c in cat_cols + [x for x in num_cols if train[x].nunique() <= 12]:
    print(f"\n-- {c} (nunique={train[c].nunique()}) --")
    print(train[c].value_counts(dropna=False).head(12).to_string())

print("\n=== signal peek: mean of key numeric features by health_condition ===")
peek = [c for c in ["bmi", "heart_rate", "sleep_duration", "stress_level",
                    "step_count", "exercise_duration"] if c in train.columns
        and pd.api.types.is_numeric_dtype(train[c])]
print(train.groupby("health_condition")[peek].mean().round(2).to_string())
