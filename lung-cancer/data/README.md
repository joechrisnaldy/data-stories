# Data

The data is not committed here (gitignored). Download it from Kaggle.

## Source

[Lung Cancer](https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer) (mysar ahmad bhat), a
small CC0 survey, `survey lung cancer.csv`, 309 rows, 16 columns. Per the dataset page, the data was
"collected from the website online lung cancer prediction system."

## IMPORTANT: this file is used as a FOIL, not as evidence

This post uses the file to illustrate a selection-bias trap, NOT to draw any conclusion about what
causes lung cancer. Two properties make it unusable for causal questions and are the whole point of
the story:

1. **No control group.** 270 of 309 respondents (87 percent) already have lung cancer. The sample is
   people who visited an online cancer-prediction tool because they were worried, so it is almost all
   patients. With almost no healthy comparison group, no risk factor can stand out.
2. **The smoking signal collapses.** In this file smoking is not a significant predictor of cancer
   (Fisher exact odds ratio 1.42, p = 0.39) and ranks last of 15 features (correlation 0.06). This is
   an artifact of (1), not a fact about smoking. The real, well-established science is the opposite:
   smoking causes the large majority of lung cancer, and there is no safe level (see the post's
   References).

Other quality notes: 33 exact duplicate rows; binary symptom columns are coded 1 = NO, 2 = YES.

## Download

```bash
kaggle datasets download -d mysarahmadbhat/lung-cancer -p .
unzip lung-cancer.zip
```

## Note

Descriptive survey data, used only as a teaching specimen for selection bias. All real-world
epidemiology in the post is sourced separately from primary authorities (NCI, CDC, WHO, Doll & Hill,
and peer-reviewed cohorts).
