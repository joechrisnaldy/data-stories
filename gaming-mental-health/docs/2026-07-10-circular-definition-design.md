# Design: "The conclusion was in the definition" (gaming-addiction essay)

**Date:** 2026-07-10
**Status:** Approved by Jonathan
**Series:** data-stories, post 03 (third in the "measuring stick" arc)

## Thesis

A dataset that looks like proof gaming is wrecking a generation's mental health. But
its headline `addiction_score` is 96% reconstructable from the other columns (linear
R2 = 0.957) and is dominated by playtime (daily playtime r = 0.86, screen time 0.82,
consecutive hours 0.80). So "addicts play a lot" is a tautology, not a finding.
Meanwhile the mental-health harm the dataset implies is near-zero noise (playtime vs
anxiety 0.14, depression 0.12, loneliness -0.07, GPA 0.008). When the outcome variable
is built from the input variables, you cannot discover anything; you recover your own
definition. Third measuring-stick story: the ruler lied (currency, post 01), the ruler
was a values choice (metric, post 02), and now the ruler is circular (the target is the
input).

## Springboard (the big lesson)

Circular targets are everywhere: apps that define "engagement" then optimize for it,
"addiction" defined as usage, risk scores that encode the outcome. Transferable rule:
before trusting a finding, check whether the target was constructed from the inputs.

## Data

- Kaggle dataset `dreamtensor/gaming-addiction-and-mental-health-analysis`, Apache 2.0.
- One file, `gaming_addiction.csv`: 250 rows, 49 columns. Synthetic exploratory survey.
- Feature groups: demographics; gaming behavior (playtime, sessions, consecutive hours,
  toxicity, spending, lootboxes); six psychological scales (stress, loneliness,
  dopamine dependency, self-control, impulsiveness, anxiety, depression, emotional
  stability); lifestyle (sleep, exercise, caffeine, social hours); real-life outcomes
  (GPA, missed deadlines, absenteeism, screen time); and engineered target columns
  (`addiction_score`, `addiction_binary`, `addiction_severity`, `behavioral_cluster`,
  `mental_health_risk_score`, `burnout_probability`, `churn_probability`).
- Raw data NOT committed (Kaggle terms); repo carries download instructions.

## Key measured facts (from profiling)

- Linear R2 reconstructing `addiction_score` from the other numerics: **0.957**.
- Top |correlations| with `addiction_score`: daily_playtime 0.86, screen_time 0.82,
  consecutive_hours 0.80, dopamine_dependency 0.79, late_night 0.76, weekly_sessions
  0.75, weekend_playtime 0.74; then sleep -0.50, missed_deadlines 0.47.
- Playtime vs wellbeing: sleep -0.40, stress 0.33, anxiety 0.14, depression 0.12,
  loneliness -0.07, social hours 0.07, GPA 0.008.
- Degenerate/constructed tells: `burnout_probability` = 1.0 for 247/250; `gpa_or_
  performance_score` = 4.0 for 177/250; `behavioral_cluster` mostly tracks the score.
- `addiction_binary` positive rate 17%; `addiction_severity` Mild 112 / Moderate 117 /
  Severe 5 / missing 16.

## Charts (target 4)

1. **The score is a formula**: predicted vs actual `addiction_score` scatter on the
   diagonal, R2 = 0.957 annotated. "Not a measurement, arithmetic."
2. **Made of vs named for**: paired/diverging bars of `addiction_score` correlations,
   playtime block (0.74-0.86) vs the mental-health block (anxiety/depression/loneliness
   near zero).
3. **The harm that isn't there**: playtime vs anxiety / depression / loneliness / GPA
   (all ~0), with sleep (-0.40) as the one real, unsurprising thread.
4. **The tells**: the constructed giveaways (burnout_probability 1.0 for 247/250; GPA
   4.0 for 177/250) as a small evidence panel.

## Essay outline (~1,600-1,900 words, opinionated first person)

1. Hook: a dataset that looks like proof gaming is destroying a generation. The trick.
2. The score that is really a formula (R2 0.957; addiction = playtime relabeled).
3. The tautology: define addiction as hours and of course "addicts" play a lot.
4. The harm that isn't there: the mental-health links are noise; only sleep moves, and
   "people who play more sleep less" is not a discovery.
5. The tells: degenerate columns; how you know a target was constructed.
6. Springboard: circular targets everywhere (engagement, addiction-as-usage, risk
   scores). The rule: check whether the outcome was built from the inputs.
7. Close: the trilogy payoff, the most dangerous ruler is the one that already
   contains the answer.

## Stated caveats (must appear)

- Synthetic, n = 250: zero claims about real gamers or real gaming addiction.
- Gaming disorder is a real, studied clinical concept (WHO ICD-11); this dataset simply
  cannot speak to it because its measure is circular. Real research finds small effects
  (cite Przybylski/Weinstein-style work) which keeps the boundary honest.
- The critique is of the analytical trap and the artifact, not the dataset's author (an
  honest exploratory/educational dataset). Do not stigmatize gamers.
- Correlations on n = 250 are themselves noisy.

## Deliverables & pipeline

Notebook + charts + code in `data-stories/gaming-mental-health/` -> Word draft for
Jonathan's review -> MDX post on the blog. No Kaggle submission (dataset, not
competition). Conventions: no long dashes; APA 7 references.

## Division of labor

Jonathan drives POV and interpretive calls; Claude writes and runs code and explains.
Voice: opinionated first-person essay.
