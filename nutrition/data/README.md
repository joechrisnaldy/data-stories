# Data

The dataset is not committed here. Download it from Kaggle.

## Source

[Food Nutrition Dataset](https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset)
(Utsav Dey, 2024), CC0 Public Domain. Five group files, `FOOD-DATA-GROUP1.csv` through
`FOOD-DATA-GROUP5.csv`, 2,395 foods combined, with per-100g nutrient columns (macros, vitamins,
minerals) plus a `Nutrition Density` column that is the uploader's own derived metric.

## Download

```bash
kaggle datasets download -d utsavdey1410/food-nutrition-dataset -p .
unzip food-nutrition-dataset.zip
# the five FOOD-DATA-GROUP*.csv files live under "FINAL FOOD DATASET/"
```

## Important: this is an unofficial dataset with data-quality problems

It is a popular, user-uploaded convenience dataset, not an authoritative government nutrient
database, and it has no stated provenance for its values. The numbers are not reliably per
100 g: 821 foods list water above 100 g per 100 g, and about 48 percent of rows have
fat + carbohydrate + protein + water summing above 105 g per 100 g (physically impossible),
though the median row (93.3 g) is fine.

Because of this, the essay uses only the parts that are robust to bad individual rows: the
FORMULAS behind the derived columns (which are exact) and broad relationships. It does NOT rank
foods or quote absolute nutrient amounts, since those would be corrupted by the bad rows.
