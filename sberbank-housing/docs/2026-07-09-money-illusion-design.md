# Design: "Property isn't the hedge you think" (Sberbank Moscow housing essay)

**Date:** 2026-07-09
**Status:** Approved by Jonathan
**Series:** analytics-blog, post 01

## Thesis

Property is treated as the ultimate safe asset (in Indonesia: *tanah, rumah, emas*).
Moscow 2014 is the natural experiment that breaks this belief: apartment prices held
almost perfectly flat **in rubles** while the ruble halved, meaning owners lost roughly
half their wealth in hard-currency terms while feeling safe. Property hedged the
measuring stick, not reality.

## Data

- `data/train.csv`, 30,471 Moscow transactions, Aug 2011 → Jun 2015, 292 features.
  Target: `price_doc` (declared sale price, RUB).
- `data/macro.csv`, 100 daily macro indicators, 2010 → Oct 2016
  (usdrub, cpi, salary, deposits_rate, oil_urals, ...).
- Source: Kaggle "Sberbank Russian Housing Market" competition.
  **Raw data is NOT committed to git** (competition license); repo carries download
  instructions instead.

## Cleaning rules (documented in post)

1. Drop declared-price fakes: `price_doc` exactly 1,000,000 or 2,000,000 RUB
   (747 + 757 rows, tax-avoidance declarations, concentrated in Investment deals).
2. Drop absurd areas: `full_sq` ≤ 10 or ≥ 1,000 m².
3. Compute `psqm = price_doc / full_sq`; trim psqm outside the 1st-99th percentile.
4. Everything else stays. Cleaning decisions are part of the story.

## Analysis steps

1. Monthly median price/m² (nominal RUB) + monthly transaction counts.
2. Join macro (resampled to monthly means): usdrub, cpi, salary, deposits_rate, oil_urals.
3. Re-denominate the housing series: USD terms, CPI-deflated (real) terms,
   and salary terms (m² affordable per average monthly wage).
4. Counterfactual from Jan 2014: 1M RUB into (a) housing (median psqm index),
   (b) USD cash, (c) ruble deposit compounding at deposits_rate, value through Jun 2015.

## Charts (target 4-5)

1. **The illusion**: median price/m² in RUB (flat) with USD/RUB overlaid, crisis shaded.
2. **Re-denominated**: housing indexed (base ≈ Jan 2014 = 100) in nominal RUB vs USD vs real.
3. **Affordability**: m² per average monthly Moscow salary (the local-earner view).
4. **Counterfactual**: housing vs USD cash vs ruble deposit, Jan 2014 → Jun 2015.
5. *(Optional)* **Volume**: monthly transaction count; stable prices on collapsing volume.

## Essay outline (~1,800 words, opinionated first person)

1. Hook: the Indonesian property instinct.
2. Moscow 2014: oil, sanctions, ruble 33 → 60+.
3. The illusion chart, "stable" prices.
4. Re-denominate, three lines, three stories.
5. Honest counterarguments: the local-earner view (affordability + frozen volume),
   and "what was the alternative?" (counterfactual, report honestly even if housing
   beats deposits).
6. Close: property hedges local inflation, not currency collapse; what that means for
   a rupiah earner. 1998 parallel.

## Stated caveats (must appear in post)

- Median transaction price ≠ repeat-sales index; mix shift possible.
- Declared prices understate true prices even after cleaning.
- Data ends June 2015, the crisis wasn't over.

## Deliverables & pipeline

Notebook + charts → Word draft for Jonathan's review → MDX post on portfolio blog →
GitHub repo `analytics-blog` (one folder per post; data gitignored).

## Division of labor

Jonathan drives the POV and every interpretive call; Claude writes/runs code and
explains techniques. Voice is Jonathan's: opinionated first-person essay.
