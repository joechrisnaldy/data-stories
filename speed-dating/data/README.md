# Data

Not committed to this repository (download it from Kaggle).

## Source

[Speed Dating Experiment](https://www.kaggle.com/datasets/annavictoria/speed-dating-experiment)
(annavictoria), which redistributes the Columbia speed dating experiment (Fisman, Iyengar,
Kamenica & Simonson, 2006). One CSV, `Speed Dating Data.csv` (8,378 date-level rows, 195
columns), plus a Word data key (`Speed Dating Data Key.doc`).

## Download

With the [Kaggle CLI](https://github.com/Kaggle/kaggle-api):

```bash
kaggle datasets download -d annavictoria/speed-dating-experiment -p .
unzip speed-dating-experiment.zip
```

## Notes

- The CSV is **latin-1** encoded, not UTF-8; read it with `encoding="latin-1"`.
- The stated "what I look for" scale changed across waves: waves 1-5 and 10-21 used a
  100-point allocation across the six traits; waves 6-9 used a 1-to-10 importance scale. The
  analysis restricts the stated-preference figures to the 100-point-allocation waves.
- Gender is recorded as a binary (0 = female, 1 = male) and matching is opposite-sex only.
