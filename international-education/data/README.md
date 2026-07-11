# Data

The primary cost data is not committed here (download it from Kaggle). The salary and
employment tables are external and live in `../external/` (committed, with provenance).

## Source (cost)

[Cost of International Education](https://www.kaggle.com/datasets/adilshamim8/cost-of-international-education)
(adilshamim8), one file, `International_Education_Costs.csv`: 907 programs at universities in
71 countries, with tuition, rent, visa, insurance, duration, and living-cost index.

## Download

```bash
kaggle datasets download -d adilshamim8/cost-of-international-education -p .
unzip cost-of-international-education.zip
```

## Note

This dataset has study costs only. It does NOT include average salary or employment rate.
Those come from OECD data in `../external/` (average annual wages 2024 PPP-USD; employment
rate 15-64), joined by country. The analysis is restricted to the ~30 OECD destinations
where a clean average wage exists.
