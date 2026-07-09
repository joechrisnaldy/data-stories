# Competition model: predicting `price_doc`

The [essay](../README.md) was descriptive. This folder is the other half: a
prediction model for the original Kaggle task, which is to estimate the sale
price of 7,662 held-out Moscow apartments (July 2015 to May 2016), scored on
**RMSLE** (root mean squared log error).

## Approach

- **Target:** `log1p(price_doc)`. RMSLE on prices equals RMSE on `log1p`, so a
  squared-error learner in log space optimizes the metric directly.
- **Model:** scikit-learn `HistGradientBoostingRegressor`. It is strong on tabular
  data and handles this dataset's heavy missingness natively, so there is no
  imputation step to get wrong.
- **Validation:** time-based. The newest ~15% of sales are held out, because the
  real test set is the future and a random split would flatter the score.

It began as a plain baseline (RMSLE 0.2709) and folds in four improvements, each
validated on its own before being combined. Each was built and scored as a
separate experiment in [`variants/`](variants/), against a byte-identical baseline
reproduction, so the numbers below are directly comparable.

| Improvement | Alone | What it does |
|---|---|---|
| Robust cleaning + de-noising | 0.2665 | Fix swapped `life_sq`/`full_sq`, blank more impossible attributes, and drop the cheapest ~1% price-per-m² rows from **training only** (residual mislabeled sales). One-sided on purpose: dropping the expensive-per-m² tail removes real luxury flats and hurts. |
| Leak-free `sub_area` encodings | 0.2678 | Frequency (count) encoding plus a smoothed mean-log-price encoding fit on the training slice only, then mapped onto the holdout and test. |
| Property features | 0.2688 | 11 deterministic ratios from existing size/floor/room/year columns (age, area ratios, floor position). |
| Hyperparameter tuning | 0.2695 | `max_features=0.8` (per-split column subsampling) and `max_iter=1000`. |
| **Combined (this model)** | **0.2651** | All four together. |

**Leakage control when combined:** the time split is taken before any row is
dropped, so the holdout is byte-identical to the baseline and the CV stays
comparable; both the de-noising and the target encoding are fit on the training
slice only and mapped outward.

## Result

Time-based holdout **RMSLE ≈ 0.265** (from 0.271 baseline). What was tried and
honestly rejected (see the variant notes): symmetric price-per-m² trimming,
month-level macro deltas and rent series, and deeper trees all made the holdout
worse.

Submitted as a late submission to the (closed) competition: **private-leaderboard
RMSLE 0.331** (public 0.331). That is higher than the holdout, exactly as
expected: the holdout sits just before the test window, while the leaderboard
test period runs further into 2016 and its macro drift is not in the training
data. For reference, the winning private score was 0.30087 and the top ten
clustered around 0.309 to 0.312, so a single tuned model at 0.331 is a
respectable baseline against 3,264 teams that ensembled heavily.

## Run it

```bash
pip install -r ../../requirements.txt      # needs scikit-learn
python train_predict.py                    # writes submission.csv
```

The [`variants/`](variants/) scripts are the individual experiments (each runs
standalone and prints its own CV); they are kept as a record of what helped.

## Submit it

The submission file is `submission.csv` (`id,price_doc`, 7,662 rows). The
competition is closed but accepts **late submissions** for a private-leaderboard
practice score.

- **Kaggle MCP** (this project's setup): once the `kaggle` MCP server is
  connected and authenticated, submit `submission.csv` to the
  `sberbank-russian-housing-market` competition from the assistant.
- **Kaggle CLI** (alternative): `kaggle competitions submit -c
  sberbank-russian-housing-market -f submission.csv -m "HGBR tuned"`.
