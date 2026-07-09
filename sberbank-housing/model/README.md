# Competition model: predicting `price_doc`

The [essay](../README.md) was descriptive. This folder is the other half: a
prediction model for the original Kaggle task, which is to estimate the sale
price of 7,662 held-out Moscow apartments (July 2015 to May 2016), scored on
**RMSLE** (root mean squared log error).

It is a deliberately clean baseline, not a leaderboard-grind. The point is a
correct, readable end-to-end pipeline.

## Approach

- **Target:** `log1p(price_doc)`. RMSLE on prices equals RMSE on `log1p`, so a
  squared-error learner in log space optimizes the metric directly.
- **Model:** scikit-learn `HistGradientBoostingRegressor`. It is strong on tabular
  data and handles this dataset's heavy missingness natively, so there is no
  imputation step to get wrong.
- **Cleaning:** light and defensible only. Fix `full_sq` errors (0/1 values fall
  back to `life_sq`), blank impossible `life_sq`/`kitch_sq`/`build_year`/`state`,
  and drop the 1,504 declared-price fakes (exactly 1M or 2M ₽) from training.
- **Features:** all numeric columns plus ordinal-encoded categoricals, with six
  macro indicators (USD/RUB, CPI, oil, mortgage rate, salary, deposit rate)
  joined by month.
- **Validation:** time-based. The newest ~15% of sales are held out, because the
  real test set is the future and a random split would flatter the score.

## Result

Time-based holdout **RMSLE ≈ 0.27**. Treat that as optimistic: the holdout sits
just before the test window, while the actual leaderboard test period runs
further into 2016, so the live score will be somewhat higher. This is a
respectable baseline; the obvious next steps (engineered size/age features,
target de-noising, light tuning) are left as a follow-up.

## Run it

```bash
pip install -r ../../requirements.txt      # needs scikit-learn
python train_predict.py                    # writes submission.csv
```

## Submit it

The submission file is `submission.csv` (`id,price_doc`, 7,662 rows). The
competition is closed but accepts **late submissions** for a private-leaderboard
practice score.

- **Kaggle MCP** (this project's setup): once the `kaggle` MCP server is
  connected and authenticated, submit `submission.csv` to the
  `sberbank-russian-housing-market` competition from the assistant.
- **Kaggle CLI** (alternative): `kaggle competitions submit -c
  sberbank-russian-housing-market -f submission.csv -m "HGBR clean baseline"`.
