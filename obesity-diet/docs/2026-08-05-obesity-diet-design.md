# Post 20 design: Calories In, Calories Out Is True. It Explains Almost Nothing.

Date: 2026-08-05
Slug: `calories-in-calories-out-explains-almost-nothing`
Folder: `Projects/analytics-blog/obesity-diet/`
Chart prefix: `diet-`

## Thesis

Across countries, daily calorie supply explains about 6% of the variation in adult obesity.
Energy balance is true for every individual and nearly useless as an explanation of why one
country is heavier than another. The identity is the accounting, not the mechanism.

## Approved brainstorm decisions

| Dimension | Decision |
|---|---|
| Core question | Does diet explain obesity? Tested across countries. |
| Hook | Same calories, different bodies. |
| Takeaway | Calories are the accounting, not the explanation. |
| Health guardrail | Establish the harm with IHME data early and cited; scope every finding across countries. |
| Indonesia | None. Global post, the fourth in a row. |
| Scope | Add GDP per capita only. No other rival explanations. |
| Closing lesson | An accounting identity is not an explanation. Travels to GDP components, unit economics, budget arithmetic. |
| Title | Calories In, Calories Out Is True. It Explains Almost Nothing. |

## Sources

| File | Series | Producer | Coverage |
|---|---|---|---|
| `obesity-age-standardized.csv` | Adult obesity, BMI >= 30, **age-standardised**, both sexes, 18+ | WHO Global Health Observatory (2026) via OWID | 206 entities, 1980-2024 |
| `daily-per-capita-caloric-supply.csv` | Daily calorie supply per person | FAO Food Balance Sheets (2025) via OWID, plus historical reconstructions before 1961 | 244 entities, 1274-2023 |
| `daily-caloric-supply-derived-from-carbohydrates-protein-and-fat.csv` | kcal from animal protein, vegetal protein, fat, carbohydrate | FAO (2025) via OWID | 244 entities, 1961-2023 |
| `gdp-per-capita-worldbank.csv` | GDP per capita, PPP, international $ in 2021 prices | Eurostat, OECD, IMF, World Bank (2026) via OWID, jointly | 212 entities, 1990-2025 |

Analysis year **2023**, the latest year all four series overlap. **168 countries** survive the join.

## What the vet established

- Calorie supply explains **R2 = 0.057** of cross-country obesity variance. That is the post.
- log GDP per capita explains **0.072** across all 168, but **0.233** across the 157 non-Pacific
  countries. Eleven Pacific island states move the headline by themselves. Disclosed, not buried.
- Diet composition explains more than either: fat share **0.210**, animal-protein share **0.223**,
  carbohydrate share **0.225** (negative).
- **The hook is a threshold, not a rank.** The ten countries at or above 3,700 kcal per person
  span **14.1% to 40.7%** obesity, a 2.9x spread, across a food supply range of only 5.8%. None is
  a Pacific state and all are rich, so neither poverty nor small-island outliers can be blamed:
  United States 3,947 kcal / 40.7%, Belgium 3,921 / 20.5%, Ireland 3,921 / 27.6%, Turkey 3,892 /
  28.9%, Serbia 3,879 / 21.5%, Austria 3,756 / 16.3%, Israel 3,754 / 22.3%, Italy 3,753 / 14.2%,
  Denmark 3,734 / 14.1%, Poland 3,730 / 21.8%.
  An earlier pass framed this as "the five highest-calorie countries", which is a hand-picked set
  whose headline span moves when the fifth country changes. Use the stated threshold.
- **Adding calories and income to diet composition buys almost nothing.** Animal-protein share
  alone explains 0.223; all three together explain 0.235. The joint model leaves **76.5%**
  unexplained (72.7% excluding the Pacific states). That is the closing number.

## Four charts

**1. `diet-1-same-calories.png`: the hook.**
Scatter, calorie supply against age-standardised obesity, 168 countries, 2023. Fit line with R2
printed on the figure. Shade the band at or above 3,700 kcal and label the countries inside it, so
the reader sees ten rich countries stacked vertically across 26 points of obesity at essentially
one level of food supply. Vietnam and Egypt marked as the dramatic near-identical pair. The reader
should see the cloud, not a line.

**2. `diet-2-the-rival.png`: income, and the countries that decide it.**
Scatter, log GDP per capita against obesity, with the eleven Pacific island states drawn in a
distinct colour and two fits shown: all countries (R2 0.072) and excluding the Pacific cluster
(R2 0.233). Makes the sensitivity visible rather than relegating it to a footnote. Honest about
income doing real work once that cluster is set aside.

**3. `diet-3-the-mix.png`: what the mix does that the total does not.**
Scatter, share of calories from animal protein against obesity, R2 0.223 printed. Footnote states
plainly that this is a decomposition of the same FAO total, not a second measurement.

**4. `diet-4-what-is-left.png`: the accounting does not close.**
Variance explained by each factor alone, and by all three together, against the unexplained
remainder. The closing image for the closing argument. Must state that the single-variable figures
do not sum to the joint figure because the predictors overlap; no additive decomposition is claimed.

Fallback if chart 4 will not carry its weight honestly: replace with residual countries, ranked by
distance from the joint model's prediction, framed strictly as unexplained by this model.

## Method rules for this post

- **Age-standardised obesity, never crude.** The crude series partly measures age structure:
  Greece reads 33.3 crude against 27.2 standardised, Palestine 33.0 against 37.2 (2023 values; an earlier pass quoted 2024). The two correlate
  0.99 but individual countries move up to 6.1 points, with exactly the demographic structure you
  would fear. State the choice in the method notes.
- **FAO measures supply, not intake.** Retail and household waste sits inside the calorie number,
  so the x-axis is a proxy for intake rather than a measure of it. SUPERSEDED BY ROUND 1: this rule
  used to add "and richer countries waste more, which biases the x-axis in the same direction as the
  outcome. This makes the weak correlation more surprising, not less." Both halves were withdrawn.
  The empirical premise is sourced from nothing in this repository, and the direction of the
  resulting bias in the correlation cannot be signed from these files. Do not describe the 5.7% as
  conservative, generous, or biased in any stated direction.
- **BMI >= 30 is a threshold on a continuous measure** and does not measure body fat. One honest
  sentence.
- **Filter OWID aggregates.** The FAO files carry 52 non-country entities (World, continents, FAO
  regions, Belgium-Luxembourg). Keep only rows with a real ISO3 code. SUPERSEDED BY ROUND 1: this
  rule used to say "Kosovo lacks one in the GDP file and drops out; note it." No real country is
  lost to the ISO3 rule. Kosovo has no rows at all in the obesity file or either FAO file. The four
  countries actually lost, at the income join rather than this one, are French Polynesia, Syria,
  Venezuela and Yemen.
- **Ecological, not individual.** Every finding is scoped across countries. Nothing here says
  anything about whether one person's intake affects their weight, and the post says so.
- Exactly 4 charts. No em or en dashes. APA 7 references. Nothing joined beyond the four files.

## Draft outline

1. Open on the ten countries at or above 3,700 kcal and the 14.1-to-40.7 spread.
2. Establish the harm immediately with IHME figures, cited: "around 5 million people died prematurely in 2019 as a result of obesity" and
   "almost 10%" of deaths that year, quoted from Ritchie and Roser citing the Global Burden of
   Disease study. The post is about
   explanation, not existence.
3. Chart 1 and the R2 of 0.057. State the folk model and show it failing at country level.
4. The obvious rival: income. Chart 2, both fits, and the Pacific cluster named as the thing that
   decides which number you quote.
5. The mix: chart 3, and the honest note that it is the same FAO total cut differently.
6. What is left: chart 4. Most of the variation is unexplained by all three together.
7. Close: an accounting identity is not an explanation. Energy balance is true by definition, which
   is exactly why it cannot explain the spread. Generalise to GDP components, unit economics,
   budget arithmetic.
8. Method notes, then references.
