# Post 08 design: numbers wearing a lab coat (nutrition scores)

**Date:** 2026-07-14
**Series:** data-stories (Post 08)
**Folder:** `Projects/analytics-blog/nutrition/`
**Dataset:** Kaggle `utsavdey1410/food-nutrition-dataset` (2,395 foods, 35 nutrient columns per 100g, CC0)

## The idea

A popular nutrition dataset ships a "Nutrition Density" column that 25,000+ downloaders may
treat as a healthiness signal. Reverse-engineering shows it is a meaningless unit-mixing sum.
Its calorie column, by contrast, is a disclosed, validated formula. The essay uses the two
columns to teach a transferable skill: before trusting any score you did not build, find out
what goes in, how it is weighted, and whether anyone checked it.

## Thesis (chosen: "numbers wearing a lab coat")

Some numbers that look measured are just formulas. Calories are a formula done right;
"Nutrition Density" is a formula done wrong. The one-line stance:

> A single score that bundles many things is a stack of somebody's choices. Calories are an
> honest, disclosed, validated formula. This dataset's "Nutrition Density" is a hidden,
> arbitrary one that adds milligrams to grams. Learn to tell them apart before you trust the
> number.

## Brainstorm decisions (locked)

- **Angle:** numbers wearing a lab coat (calories = arithmetic done right; Nutrition Density =
  arithmetic done wrong; teach interrogating derived columns).
- **Hook:** villain first (the score that adds mg to grams), then rewind to the honest calorie column.
- **Reach:** broad. The lesson is about ANY score you did not build (health-app ratings, sleep
  scores, wellness indices, credit scores).
- **Tone:** neutral, critique the practice not the person. Credit the dataset as a useful,
  popular resource; name it factually; pull no punches on the metric itself.
- **Indonesia:** none (universal).
- **Constructive foil:** contrast with Nutri-Score (published, purposeful, validated weights).
  One verified citation.

## What the data shows (verified in profiling)

- **`Nutrition Density` is an exact sum of 8 columns.** A linear fit returns R^2 = 1.000 with
  coefficients of 1.0 on exactly: Fat, Carbohydrates, Protein, Dietary Fiber, Vitamin A,
  Vitamin C, Calcium, Iron (max abs diff between the column and the raw sum = 0.21). It ignores
  the other 25 nutrients entirely.
- **The sum is dominated by units, not nutrition.** Contribution shares of the mean score
  (106.9): Calcium 48.7% (mg), Carbohydrates 17.4% (g), Protein 12.5% (g), Fat 9.5% (g),
  Vitamin C 7.3% (mg), Dietary Fiber 2.1% (g), Iron 1.7% (mg), Vitamin A 0.7% (ug). Nearly half
  the "nutrition" score is calcium; the vitamins it is named for barely register because of
  their units. The score correlates 0.54 with calories, so it partly just rewards caloric,
  heavy foods, the opposite of a nutrient-density metric.
- **Calories are Atwater arithmetic.** Caloric Value vs (4*carb + 4*protein + 9*fat):
  correlation 0.98, median absolute error 3.2 kcal, 88% within 20 kcal. The calorie column was
  computed from three macros with the century-old 4/4/9 factors, not measured per food.
- **Honest misses of 4/4/9:** alcohol (wine, spirits) carries ~7 kcal/g that the macro columns
  do not capture; a handful of rows are simply broken (impossible 2,000-3,000+ kcal/100g).
- **Data-quality caveat (state it):** the dataset is not reliably per-100g. 821 foods list
  water > 100 g/100g and ~48% of rows have fat+carb+protein+water > 105 g/100g (physically
  impossible), though the median row (93.3 g) is fine. The two findings above are robust
  because they are about formulas and relationships, not individual absolute values. We do NOT
  do any "rank the foods" analysis (those would be corrupted by the bad rows).

## Analytical backbone

Reused venv `sberbank-housing/.venv` (pandas, numpy, scikit-learn, matplotlib).

1. Combine the 5 group CSVs (drop the two unnamed index columns). 2,395 foods.
2. **Recover the score:** linear regression of `Nutrition Density` on the 33 nutrient columns;
   report R^2 and the recovered weights; confirm it equals the raw sum of the 8.
3. **Decompose the score:** mean contribution and % share of each of the 8 terms; tag each
   with its unit (g / mg / ug) to make the unit-mixing explicit.
4. **Calories = Atwater:** predicted 4/4/9 vs actual; correlation, median abs error, % within
   20 kcal; identify the alcohol-driven and broken-row residuals.
5. Write `results.json`.

## Charts (3, series palette)

1. **`01_recipe.png` — the recovered formula.** Horizontal bar of the recovered weight for all
   33 nutrients, the 8 real ingredients at ~1.0 highlighted, the other 25 at ~0 greyed.
   Caption: fed the score to a regression, got back the recipe.
2. **`02_madeof.png` — what the score is really made of.** Bar of each of the 8 terms' % share
   of the score, labeled with units. Calcium 49% on top, vitamins near zero. Caption: half the
   "nutrition" score is calcium, only because calcium is counted in milligrams.
3. **`03_calories.png` — arithmetic done right.** Scatter of Atwater-predicted vs actual
   calories, tight y=x line (r 0.98), a few labeled misses (alcohol; a broken row). Caption:
   calories are also a formula, but a disclosed, validated, physically grounded one.

Nutri-Score is handled in prose (the constructive close), no chart.

## Section spine (~1,300-1,700 words, no long dashes)

1. **Open, villain first.** A nutrition score in a dataset 25,000 people downloaded that adds
   grams of fat to milligrams of calcium to micrograms of vitamin A. Set up: a single number
   sold as "nutrient richness."
2. **The reveal (chart 1).** Feed the score to a regression; it hands back the recipe, a sum of
   8 nutrients, weight 1 each, the other 25 ignored. Explain reverse-engineering plainly.
3. **Why it is nonsense (chart 2).** The 8 are in different units, so the sum is dominated by
   big-number columns: half is calcium, most of the rest is macros in grams, the vitamins
   barely count, and it tracks calories. Not a health score.
4. **The honest counterexample (chart 3).** Calories look like the same kind of derived number,
   but they are arithmetic done right: 4/4/9, disclosed, century-old, physically grounded,
   accurate to ~3 kcal. A formula is not the problem; a hidden, arbitrary one is. Note the
   honest misses (alcohol) and that a few rows are just wrong (the dataset is imperfect).
5. **What good looks like (Nutri-Score, prose).** Also one number from many nutrients, but the
   weights are published, chosen for a purpose (diet quality), and validated against health
   outcomes. The difference between a good bundled score and a bad one is not bundling; it is
   disclosure, purpose, and validation.
6. **The general lesson (broad).** Any score you did not build, health-app ratings, sleep
   scores, wellness indices, credit scores, is a bundle of someone's choices. Before trusting
   it, ask three things: what goes in, how it is weighted, whether anyone checked it against
   reality. You can often reverse-engineer it in an afternoon. Analysis, not medical or
   financial advice.
7. **Method notes + References.**

## Citations to verify (pin in the plan)

- Dey, U. (2024). *Food nutrition dataset* [Data set]. Kaggle. (the dataset)
- Atwater 4/4/9 factors: a primary reference, e.g. FAO (2003), *Food energy: methods of
  analysis and conversion factors*, or a standard nutrition source. VERIFY exact citation.
- Nutri-Score: the underlying nutrient-profiling model and a validation study, e.g. the
  UK FSA/Ofcom model (Rayner et al.) and/or a Nutri-Score validation against health outcomes
  (Sante publique France). VERIFY exact citations and that the "published + validated" claim is
  accurately stated.

## Guardrails

- No long dashes; APA 7 references for every external fact.
- Associational / descriptive only; no causal or medical or financial advice.
- Neutral tone: credit the dataset, critique the metric and the practice, not the person.
- State the dataset's per-100g data-quality problem honestly; do not build any food ranking on
  the absolute values.

## Title (CHOSEN)

**"The Score You Didn't Build (and Shouldn't Trust)"**

Other candidates considered: "The Nutrition Score That Adds Milligrams to Grams"; "Half of
This 'Nutrition' Score Is Just Calcium"; "How to Tell if a Number Was Measured or Made Up".

## Verification (for the plan)

Data sanity (recovered formula R^2 = 1.0; contribution shares; Atwater fit), citation checks
(Atwater factors, Nutri-Score published + validated), long-dash scan, slug match, Astro build.
