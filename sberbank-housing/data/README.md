# Data

The raw data is **not committed** to this repository. It comes from a Kaggle competition and stays under Kaggle's rules; please download it yourself.

## Source

[Sberbank Russian Housing Market](https://www.kaggle.com/c/sberbank-russian-housing-market) (Kaggle competition).

## Download

With the [Kaggle CLI](https://github.com/Kaggle/kaggle-api) (`pip install kaggle`, then add your API token):

```bash
kaggle competitions download -c sberbank-russian-housing-market -p .
unzip sberbank-russian-housing-market.zip
unzip 'train.csv.zip' && unzip 'macro.csv.zip'
```

Or download the zip manually from the competition's Data tab and extract it here.

## What the analysis needs

Place these two files in this folder:

- `train.csv`: the transactions (one row per sale; the target is `price_doc`).
- `macro.csv`: daily macroeconomic indicators (exchange rates, CPI, wages, deposit rates).

`data_dictionary.txt` (shipped with the download) documents all 292 transaction columns. `test.csv` and `sample_submission.csv` belong to the original prediction contest and are not used here.
