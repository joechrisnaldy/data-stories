# Data

The dataset is not committed here. Download it from Kaggle.

## Source

[Mental Health Prediction Dataset](https://www.kaggle.com/datasets/harpartapsingh13/mental-health-prediction-dataset)
(Harpartap Singh), one file, `mental_health_prediction.csv`: 500 records of students and
working professionals, 18 columns, CC0 Public Domain.

Columns: age, gender, occupation, and twelve 0-to-12 or 1-to-10 lifestyle and wellbeing
scales (sleep_hours, sleep_quality, social_media_hours, academic_work_pressure,
physical_activity_days, stress_level, anxiety_score, depression_score, work_life_balance,
mood_score, concentration_level, social_support), plus three label columns
(mental_health_condition, severity, treatment).

## Download

```bash
kaggle datasets download -d harpartapsingh13/mental-health-prediction-dataset -p .
unzip mental-health-prediction-dataset.zip
```

## Important: this data is simulated

The creator describes it as "real-world inspired" lifestyle data. It behaves like a generated
teaching dataset, not a survey: the four conditions are perfectly balanced (exactly 125 rows
each of Normal, Anxiety, Burnout, Depression), and the condition label is about 86 percent
reconstructable from the lifestyle inputs alone. So the relationships in it are clean partly
because they were built in. Treat the analysis as a hypothesis made visible, not as evidence
from the field.

It is also cross-sectional (one snapshot per person, no time dimension) and has NO productivity,
income, or economic column. The essay uses `concentration_level` as an in-data proxy for
"can you actually work," and brings the productivity and economic payoff from external sources
(see `../docs/2026-07-12-mental-health-productivity-references-verified.md`).
