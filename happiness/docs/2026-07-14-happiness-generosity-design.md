# Post 09 design: Indonesia's generosity paradox (two kinds of happiness)

**Date:** 2026-07-14
**Series:** data-stories (Post 09)
**Folder:** `Projects/analytics-blog/happiness/`
**Dataset:** Kaggle `jainaru/world-happiness-report-2024-yearly-updated` (World Happiness Report; 2024 cross-section of 143 countries + 2005-2024 panel, CC0)

## The idea

Indonesia gives more than any country on earth and feels more daily joy than almost anywhere,
yet ranks about 80th of 143 on the world happiness ladder. The essay uses that paradox to open
up a real distinction: how you RATE your life (the ladder) and how you FEEL living it (daily
affect) are two different questions, and they only loosely agree.

## Thesis (chosen: hold both truths)

> How you rate your life and how you feel living it are two different questions. Indonesia gives
> the most, feels a lot of daily joy, and still rates its life a middling six, and all of that
> is true at once. The happiness ranking measures the judging, not the feeling.

Honest and reflective: the ladder is not "wrong", it measures life-evaluation; daily emotion
and generosity are real things it does not capture. Resist both flag-waving and
ranking-bashing.

## Brainstorm decisions (locked)

- **Angle:** Indonesia's generosity paradox as the way into evaluated-vs-experienced happiness.
- **Hook:** "two people, same country", open human and concrete on the felt-vs-judged gap (an
  Indonesian can laugh with friends all afternoon and still rate their life a six), then data.
- **Stance:** honest, hold both truths; the ladder measures judged life, not felt life.
- **Cultural context:** LIGHT and verified, the World Giving Index as independent corroboration
  of the generosity finding, plus a careful, sourced nod to communal/religious giving (zakat,
  gotong royong) WITHOUT claiming it causes the ladder gap.
- **Close:** turn it on the reader, the two-happinesses question applies to everyone; no single
  score holds both. Which happiness are you optimizing?

## What the data shows (verified in profiling)

Two files. The 2024 cross-section's factor columns are "explained-by" CONTRIBUTIONS (the six
factors + Dystopia+residual sum to the ladder, mean abs diff 0.0006), so it is used only for
the official 2024 ladder ranking. All analysis uses the 2005-2024 PANEL's latest year per
country (~150 countries, mostly 2023), which holds raw values plus positive/negative affect.

- **Indonesia is 1st of 150 in generosity** (0.590, ahead of Myanmar 0.548). In the WHR,
  "generosity" is the residual of charity-donation responses regressed on GDP, so this means
  Indonesians give far more than their income predicts.
- **Indonesia is 5th of 150 in daily positive affect** (0.814). The daily-joy leaders are Latin
  America and SE Asia (Guatemala, Paraguay, Panama, Costa Rica, Mexico, El Salvador; Indonesia,
  Thailand, Philippines) plus Senegal.
- **Indonesia ranks about 80th of 143 on the 2024 ladder** (score 5.57 in the cross-section;
  5.70 in the 2023 panel).
- **Generosity's correlation with the ladder is 0.055, essentially zero.** The most generous
  countries (Indonesia, Myanmar, Gambia, Haiti, Ukraine) sit all across the ladder. Giving
  does not move the score.
- **Felt and judged only loosely agree:** ladder vs positive affect r = 0.46; ladder vs
  negative affect r = -0.57. By contrast the ladder tracks social support strongly (r = 0.79)
  and log GDP (R^2 = 0.61 alone). So the ladder rewards money and social support, not daily joy
  or giving.
- **Two off-diagonal groups:** feel-more-than-they-rate (Latin America, much of Africa: Senegal,
  Kenya, Rwanda); rate-more-than-they-feel (Eastern Europe: Israel, Lithuania, Poland, Serbia,
  Slovenia, Montenegro, Turkiye, Romania).

## Analytical backbone

Reused venv `sberbank-housing/.venv` (pandas, numpy, scikit-learn, matplotlib). Read both CSVs
with `encoding="latin-1"` (accented country names). Panel: latest year per country.

1. Indonesia's ranks: generosity (1/150), positive affect (5/150), ladder (~80/143).
2. Correlations: generosity~ladder (0.055), positive-affect~ladder (0.46), social-support~ladder
   (0.79).
3. The two-happinesses scatter (ladder vs positive affect) and the two off-diagonal clusters.
4. Generosity ranking (top countries) with their scattered ladder scores.
5. Feeling-rank vs ladder-rank for a curated set (Indonesia, Finland, Costa Rica, Poland).
6. Write `results.json`.

## Charts (3, series palette)

1. **`01_two_happinesses.png`** — scatter, ladder score (x, "how they rate life") vs positive
   affect (y, "how they feel day to day"), ~150 countries, loose fit annotated (r 0.46).
   Indonesia highlighted; label the feel-more corner (Latin America / SE Asia) and the
   rate-more corner (Eastern Europe). The core visual.
2. **`02_generosity_crown.png`** — ranked horizontal bar, the ~10 most generous countries,
   Indonesia #1 and clearly ahead. Caption: generosity's correlation with the ladder is 0.06,
   so these givers sit all over the ranking; giving buys nothing on the score.
3. **`03_feeling_vs_judging.png`** — dumbbell/slope for a curated set (Indonesia, Finland, Costa
   Rica, Poland): each country's world rank on daily positive emotion vs its rank on the ladder.
   Indonesia high on feeling, middling on judging; Finland the reverse-ish; Costa Rica high on
   both; Poland high judging, low feeling. Crystallizes the thesis and sets up the reader turn.

## Section spine (~1,300-1,700 words, no long dashes)

1. **Open, two people / one country.** An Indonesian laughs with friends all afternoon, then,
   asked to rate their life 0 to 10, says six. Both are honest. Two different questions.
2. **The two happinesses (chart 1).** The ladder (evaluation) and daily affect (feeling) only
   loosely agree (r 0.46). Latin America and SE Asia feel the most; Eastern Europe rates high
   but feels low. Indonesia sits high on feeling, middling on rating.
3. **The generosity crown (chart 2).** Indonesia gives more than any country on earth (WHR
   generosity residual; corroborated by the World Giving Index). And giving does not move the
   ladder at all (r 0.06). The most generous countries are scattered across the ranking.
4. **Light cultural corroboration.** The World Giving Index has ranked Indonesia the most
   generous for years; communal and religious giving (zakat, gotong royong) are part of the
   texture, stated carefully as context, not as a proven cause of the ladder gap.
5. **Where Indonesia stands (chart 3).** High on feeling, middling on judging. What the ladder
   rewards (money, social support) versus what Indonesia has a lot of (daily joy, giving).
   Neither picture is the whole truth.
6. **Turn it on the reader.** Rating your life and feeling your life are two questions for you
   too. No single number, national or personal, holds both. Which one are you optimizing?
   Analysis, not life advice.
7. **Method notes + References.**

## Citations to verify (pin in the plan; verified-or-omit)

- The World Happiness Report 2024 itself (Helliwell, Layard, Sachs, De Neve, Aknin, Wang, eds.),
  for the ladder, the Cantril question, and the generosity definition, not just the Kaggle
  mirror. VERIFY editors, year, publisher, URL.
- The Kaggle dataset (jaina, 2024) as the data source used.
- World Giving Index (Charities Aid Foundation) ranking Indonesia most generous, VERIFY the
  exact years/editions and wording before stating "topped it for years".
- Kahneman, D., & Deaton, A. (2010). High income improves evaluation of life but not emotional
  well-being. PNAS, for the evaluated-vs-experienced distinction. VERIFY exact citation and that
  it supports the two-happinesses framing (do not overclaim the income-threshold specifics).

## Guardrails

- No long dashes; APA 7 references for every external fact; verified or omit.
- Descriptive/associational only; the generosity-ladder and affect-ladder relationships are
  correlations, no causal or policy claims; culture is context, not a proven cause.
- Neutral, honest tone: credit the ranking as measuring one real thing; do not bash it or
  flag-wave for Indonesia.
- Be precise about the two files (cross-section = contributions/official rank; panel = raw
  values + affect); state which number comes from where.

## Title (CHOSEN)

**"The Most Generous Country on Earth Isn't the Happiest"**

Other candidates considered: "Two Kinds of Happiness (and Indonesia Has One of Them)";
"Indonesia Gives the Most. The Ranking Doesn't Notice."; "How You Feel and How You Rate Your
Life Are Different Questions".

## Verification (for the plan)

Data sanity (Indonesia ranks, the 0.055 generosity-ladder correlation, the affect correlations),
citation checks (WHR 2024, World Giving Index, Kahneman & Deaton 2010), long-dash scan, slug
match, Astro build.
