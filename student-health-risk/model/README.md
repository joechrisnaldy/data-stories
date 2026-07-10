# The two models

The essay's whole argument is a controlled experiment. Two models, one difference.

Both are scikit-learn `HistGradientBoostingClassifier` with identical features,
hyperparameters, and validation. The only change is the fit-time class weights:

- **Model A (accuracy):** no weights. It leans on the 86% majority.
- **Model B (balanced):** `sample_weight="balanced"`. Every class counts the same,
  which is exactly what the competition metric (balanced accuracy) rewards.

## Results (stratified 80/20 holdout)

| | Accuracy | Balanced accuracy | Leaderboard (balanced acc) |
|---|---|---|---|
| All "at-risk" baseline | 0.859 | 0.333 | — |
| Model A (accuracy) | **0.967** | 0.873 | 0.87241 |
| Model B (balanced) | 0.937 | **0.950** | 0.94991 |

Per-class recall: Model A catches fit 0.83 / at-risk 0.99 / unhealthy 0.80; Model B
catches fit 0.95 / at-risk 0.93 / unhealthy 0.97.

The tradeoff, and the honest cost: Model B wins the leaderboard by catching more rare
students, but its rare-class flags are far noisier. About a third of its "unhealthy"
calls and a quarter of its "fit" calls are false alarms (precision 0.68 and 0.73),
versus roughly one in twenty for Model A. Balanced accuracy rewards the catch and never
charges for the false alarm. The validation matched the live leaderboard almost exactly.

## The leaderboard push (after the essay)

The essay models were deliberately simple. A follow-up push explored four axes on a
mandatory shared protocol ([`eval_common.py`](eval_common.py): stratified 5-fold OOF,
because single-holdout noise swamps differences this small). Verdicts, all vs the
0.94958 OOF baseline: feature engineering added nothing (HGBC already exploits the
missingness); LightGBM tied but added ensemble diversity; seed averaging alone was
within noise; the hyperparameter screen's winner did not replicate on the full
protocol. What worked was the blend: two bigger HGBCs plus a LightGBM, probabilities
averaged, class priors tuned on OOF ([`final_push.py`](final_push.py)), OOF 0.94982,
**public leaderboard 0.95012** (up from 0.94991). A wider 7-member blend
([`final_push2.py`](final_push2.py)) looked marginally better locally (0.94990) but
scored worse on the public board (0.94989 / 0.94973): at that point local deltas of
±0.0002 no longer transfer, which is the signal to stop rather than start fitting
leaderboard noise. One environment note: LightGBM on macOS needs the OpenMP runtime;
without Homebrew, adding the venv's sklearn-vendored `libomp` directory to the
LightGBM dylib's rpath works (`install_name_tool -add_rpath` + ad-hoc `codesign`).

## Run and submit

```bash
pip install -r ../../requirements.txt        # needs scikit-learn
python train_models.py                       # writes submission_A.csv, submission_B.csv, results.json
```

The two submission files (`id,health_condition`, 295,753 rows each) are gitignored
because they are large and regenerate from the script. Submit either to the (live)
competition:

- **Kaggle MCP:** submit `submission_B.csv` to `playground-series-s6e7`.
- **Kaggle CLI:** `kaggle competitions submit -c playground-series-s6e7 -f submission_B.csv -m "HGBC balanced weights"`.
