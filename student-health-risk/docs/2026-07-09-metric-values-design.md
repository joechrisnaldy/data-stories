# Design: "The metric encodes your values" (Playground S6E7 student-health essay)

**Date:** 2026-07-09
**Status:** Approved by Jonathan (with "add a domain thread" modification)
**Series:** data-stories, post 02

## Thesis

On this data, 85.9% of students are labeled `at-risk`. A model that blindly predicts
`at-risk` for everyone is 85.9% accurate and worthless (balanced accuracy 0.333, the
floor). The competition scores on **balanced accuracy** (mean per-class recall), which
forces the model to care about the 6% `fit` and 8% `unhealthy` students as much as the
majority. Choosing that metric is a values statement about who counts, not a technical
detail. This is a sequel to the money-illusion post: the measuring stick is the story
again, but this time you choose it.

**Integrated domain thread:** the metric is also what makes the health story *visible*.
A plain-accuracy model is blind to who the fit and unhealthy students are (it lumps
everyone into `at-risk`). Only when balanced accuracy forces the model to care about
the tails does it have to learn the real behavioral signal (sleep, movement, BMI). The
health findings are the payoff of the values choice.

## Data

- Kaggle Playground Series S6E7, "Predicting Student Health Risk". Active, deadline
  2026-07-31. Metric: balanced accuracy. Max 10 submissions/day. Reward: swag.
- `train.csv` 690,088 rows, `test.csv` 295,753 rows, `sample_submission.csv`.
- Target `health_condition`: `at-risk` 85.87% / `unhealthy` 8.36% / `fit` 5.77%.
- 13 features: 7 numeric (sleep_duration, heart_rate, bmi, calorie_expenditure,
  step_count, exercise_duration, water_intake), 6 categorical (diet_type, stress_level,
  sleep_quality, physical_activity_level, smoking_alcohol, gender), all 3-level.
- Missingness is real: sleep 11%, stress 12%, sleep_quality 8%, calorie 8%, water 6%,
  and 1-5% on the categoricals.
- **Synthetic**: Kaggle generated it from a real College Student Health Behavior
  Dataset with altered distributions. No real-world epidemiology claims.
- Raw data is NOT committed (competition data); repo carries download instructions.

## The demonstration (proving ground)

Two models, same `HistGradientBoostingClassifier` family, same features, same data. The
only difference is what each is told to care about:

- **Model A (accuracy-tuned):** default class weights. Leans on the majority, scores
  ~86% accuracy but low balanced accuracy (~0.33-0.45); largely ignores the rare classes.
- **Model B (balanced-accuracy-tuned):** balanced class weights (per-sample weights).
  Sacrifices raw accuracy, catches the tails, scores far higher balanced accuracy.

Both are submitted to the live leaderboard. The board rewards B and punishes A even
though A is "more accurate": that contrast on the real board is the argument. Validation
is a single stratified holdout reporting balanced accuracy, accuracy, and the confusion
matrix for each model. Model B is a clean, solid entry, not a leaderboard grind.

Signal that B learns (mean by class, from profiling): `fit` = ~11,600 steps, ~50 min
exercise, ~8h sleep, BMI 21.8; `unhealthy` = 5.4h sleep, BMI 24.1; `at-risk` = the
ambiguous middle. Sleep and activity separate the classes; heart rate does not (~75 for
all three).

## Charts (target 5)

1. **The imbalance** (86 / 8 / 6) with the "all at-risk" baseline: 85.9% accurate,
   0.333 balanced accuracy. The setup.
2. **Two confusion matrices side by side** (row-normalized = recall): A ignores
   `fit`/`unhealthy`; B lights up the diagonal. The money chart for the metric point.
3. **Accuracy vs balanced accuracy** for both models, with the two live leaderboard
   balanced-accuracy scores annotated: "more accurate" and "better" point opposite ways.
4. **Health separators** (domain): sleep duration and daily steps by class, showing
   `fit` and `unhealthy` diverging from the `at-risk` middle.
5. **Per-class behavior profile** (domain): compact small-multiples of sleep, steps,
   exercise, BMI by class, the "who these students are" payoff.

## Essay outline (~1,700-2,000 words, opinionated first person)

1. Hook: a model that is right 86% of the time and useless.
2. The imbalance and the floor: why 85.9% accuracy is the baseline, not an achievement.
3. Balanced accuracy: what it is, and that choosing it is a values choice (measuring-
   stick callback to post 01).
4. The proof: two models, same everything, opposite behavior; the leaderboard rewards
   the "less accurate" one. Confusion matrices.
5. The payoff (domain thread): what caring about the tails reveals about student health,
   sleep, movement, BMI; the fit and unhealthy students you could only see once the
   metric forced you to look.
6. Honest counterpoints: balanced accuracy is not universally right (deployment
   tradeoff, false alarms); the data is synthetic.
7. Close: the metric is a moral choice; what you optimize is what you value.

## Stated caveats (must appear in post)

- Data is synthetic; conclusions are about modeled patterns, not real epidemiology.
- The demonstration is illustrative, not a leaderboard-optimal solution.
- Balanced accuracy is not always the right metric; it trades false alarms for coverage.

## Deliverables & pipeline

Notebook + model code + charts in `data-stories/student-health-risk/` -> Word draft for
Jonathan's review -> MDX post on the portfolio blog -> two Kaggle submissions (Model A
and Model B) via the Kaggle MCP. Conventions: no long dashes; APA 7 references for
external facts.

## Division of labor

Jonathan drives the POV and interpretive calls; Claude writes and runs the code and
explains the techniques. Voice: opinionated first-person essay.
