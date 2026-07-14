# Data

The data is not committed here. Download it from Kaggle.

## Source

[World Happiness Report - 2024](https://www.kaggle.com/datasets/jainaru/world-happiness-report-2024-yearly-updated)
(jaina, 2024), CC0. A third-party re-upload of the World Happiness Report. The authority for any
statistic is the report itself: Helliwell, Layard, Sachs, De Neve, Aknin & Wang (Eds.), *World
Happiness Report 2024*, University of Oxford, Wellbeing Research Centre.

## Download

```bash
kaggle datasets download -d jainaru/world-happiness-report-2024-yearly-updated -p .
unzip world-happiness-report-2024-yearly-updated.zip
```

## The two files (they are different)

- `World-happiness-report-2024.csv` (renamed here `world-happiness-2024.csv`): the 2024
  cross-section of 143 countries. Its factor columns are the "explained-by" CONTRIBUTIONS: the
  six factors plus Dystopia+residual sum exactly to the ladder score. Used only for the official
  2024 ladder ranking.
- `World-happiness-report-updated_2024.csv` (renamed here `world-happiness-panel-2005-2024.csv`):
  the 2005-2024 panel. Its columns are the RAW factor values, plus positive and negative affect.
  Used for all correlations and the affect analysis (latest year per country, ~150 countries).

Both files must be read with `encoding="latin-1"` (accented country names).

## Note

"Ladder score" is the Cantril life-evaluation (rate your life 0 = worst possible to 10 = best
possible). "Generosity" is the residual of the charity-donation question regressed on log GDP
per capita, so it is income-adjusted giving, not raw dollars. All analysis here is descriptive
and associational.
