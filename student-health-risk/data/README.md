# Data

Not committed to this repository (Kaggle competition data). Download it yourself.

## Source

[Kaggle Playground Series S6E7, "Predicting Student Health Risk"](https://www.kaggle.com/competitions/playground-series-s6e7).

## Download

With the [Kaggle CLI](https://github.com/Kaggle/kaggle-api) (`pip install kaggle`, then add your API token):

```bash
kaggle competitions download -c playground-series-s6e7 -p .
unzip playground-series-s6e7.zip
```

Or download from the competition's Data tab and extract here. You need `train.csv`
and `test.csv`; `sample_submission.csv` shows the required output format.

## What the analysis needs

- `train.csv`: 690,088 rows, target `health_condition` (three classes) plus 13 features.
- `test.csv`: 295,753 rows, same features without the target.
