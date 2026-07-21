# Post 12 design: the benefit that costs less than it delivers (WIC food rebates)

**Date:** 2026-07-19
**Series:** data-stories (Post 12)
**Folder:** `Projects/analytics-blog/wic-foodaid/`
**Title (CHOSEN):** "The Benefit That Costs Less Than It Delivers"
**Slug / filename base:** `the-benefit-that-costs-less-than-it-delivers`
**Dataset:** Kaggle `jpmiller/publicassistance` ("US Public Food Assistance 1 - WIC"), real USDA FNS
WIC administrative tables (state agencies + tribal orgs, FY2013-2016) + Census SAIPE poverty
(`est13_16us/`). CC/public-domain government data. Legit (vetted).

## The idea

WIC (the Special Supplemental Nutrition Program for Women, Infants, and Children) hands families
more food than taxpayers pay for. Because states make infant-formula manufacturers compete to be the
single WIC brand, the program recovers a large share of its food cost as rebates. So the "cost" of the
benefit on the budget line is far below the value of the food that actually reaches families. This is
an objective, largely non-partisan story about the under-appreciated economics of a food benefit.

## Thesis (chosen)

> WIC delivers close to twice the food value of its net public cost. Infant-formula rebates, won
> through competitive sole-source bidding, claw back roughly 44% of the food bill, so a private
> industry quietly subsidizes part of a public benefit. The benefit is bigger than its budget line.

Landing (locked): **the benefit is bigger than the budget** (industry subsidizes part of a public good).
Objective, descriptive, no politics.

## Brainstorm decisions (locked)

- **Angle:** stretching the dollar (the rebate mechanism).
- **Landing:** the benefit is bigger than the budget line.
- **Hook:** a mother at the register (illustrative composite, since the data is aggregate), what she
  carries home vs what the state actually paid, then pull back to the mechanism.
- **Framing:** universal + ONE light Indonesia touch (the transferable design lesson: scale +
  competitive bidding can make suppliers subsidize a food program). Strictly mechanism/cost, NO politics.
- **Scope (4 charts, his picks):** the rebate wedge; rebate share over time; what a family gets;
  the formula engine.

## What the data shows (RECONCILED against USDA; net-vs-gross corrected)

Reconciliation (resolved): drop the **"Mountain Plains" REGIONAL SUBTOTAL row** (double-counts its
member states) and stray blank rows; Texas IS present. Cleaned, the dataset matches USDA national
figures. ALWAYS exclude the 7 FNS region names and blanks.

**KEY CORRECTION (verified by sourcing):** the dataset's `Food_Costs` = USDA's **NET (post-rebate)**
food cost, NOT gross. Dataset FY2016 net $3.949B matches USDA net $3,949.6M; dataset rebates $1.71B
matches USDA $1.72B. Therefore:
- **Gross food delivered = net + rebates ≈ $5.67B** (FY2016).
- **Net taxpayer food cost ≈ $3.95B**.
- **Rebates ≈ $1.72B = ~30% of GROSS** (NOT 43%; 43% was rebate/net with the wrong denominator).
  Matches GAO: rebates were 27% (2023) to 39% (2020) of WIC food costs.
- **Participation FY2016 = 7.70M** (matches USDA). Trend 8.66M (2013) -> 7.70M (2016).
- **Per person (FY2016): ~$61/month gross food value vs $42.77/month net** taxpayer cost (USDA verified).
- **Breastfeeding FY2016 (USDA FNS BF report):** 13.2% fully breastfed, 18.5% partially, so ~68%
  formula-only. WIC buys "over half" of US formula (GAO) -> formula scale powers the rebate.
- Current context (USDA FY2024): net food cost $4.91B, rebates ~$1.6B (~19% of caseload / ~1 in 5),
  6.70M participants, ~$61/month net per person. Mechanism still current (GAO-25-106503, 2025).

## The four charts (real data; wic-N-name.png)

1. `wic-1-rebate-wedge`: FY2016 gross food ($5.66B) split into net taxpayer cost ($3.95B) + rebate
   ($1.71B). The thesis image.
2. `wic-2-rebate-share`: rebates as a share of GROSS food cost, FY2013-2016 (~30% each year); GAO
   band 27% (2023) to 39% (2020). A durable mechanism.
3. `wic-3-per-person`: per-participant food value (~$61/month gross) vs net taxpayer cost
   (~$43/month). Makes the benefit concrete.
4. `wic-4-formula-engine`: WIC infants ~68% formula-only (13.2% fully breastfed, 18.5% partial); WIC
   buys over half of US formula, so formula scale is the engine of the savings. The honest nuance.

## Section spine (~1,300-1,800 words, no long dashes)

1. **Open, a mother at the register.** What she takes home vs what the state paid. [sets up the gap]
2. **The gap, and who fills it (chart 1).** Food delivered exceeds net cost; the rebate is the wedge.
3. **How the rebate works (chart 2).** States bid a sole-source formula contract; makers pay to be the
   only WIC brand; ~44% clawed back, every year.
4. **What a family actually gets (chart 3).** Per-person value vs net public cost per person.
5. **The engine is formula (chart 4).** The savings ride on WIC being a huge formula buyer; honest
   nuance (efficiency is coupled to formula scale, and to formula over breastfeeding).
6. **The design lesson (light Indonesia touch).** Net cost vs sticker cost; scale + competitive bidding
   can make suppliers subsidize a food program. Transferable to any country building one (Indonesia is
   scaling its own food benefits). Mechanism only, no politics.
7. **Close.** A benefit worth more than its line item, because someone engineered it that way.
   Descriptive analysis, not policy advocacy.
8. **Method notes + References.**

## Citations to verify (verified-or-omit; pin at sourcing)

- **USDA FNS WIC national totals** (food cost, rebates, net, participation) for the relevant FY, to
  reconcile/replace the dataset's ex-Texas absolutes. Source: USDA FNS WIC program data / National
  Level Annual Summary. VERIFY exact figures + year.
- **The rebate mechanism**: competitive sole-source infant-formula rebate system. Source: USDA FNS
  "Infant Formula Cost Containment" / GAO reports on WIC formula rebates. VERIFY wording + that rebates
  are ~85% of wholesale and fund additional participants (~1 in 4 / a stated share).
- **WIC's share of the US infant-formula market** (~50-60%). Source: USDA/GAO/IOM. VERIFY figure.
- **Per-participant average monthly food cost.** Source: USDA FNS. VERIFY.
- **WIC breastfeeding rates.** Corroborate the dataset split with USDA/CDC. VERIFY.
- **Indonesia food-benefit program** (Makan Bergizi Gratis / free nutritious meals), existence + scale
  only, for the light design-lesson touch. VERIFY figure; keep apolitical; omit if not cleanly sourced.

## Guardrails

- Objective and descriptive; NO politics, no advocacy for or against the program.
- No em or en dashes; APA 7 references for every external fact; verified or omit.
- The rebate RATIO is the robust core; cross-check absolute dollars/people against USDA published
  figures (the reconciled dataset already matches USDA on participation; drop the Mountain Plains
  regional subtotal row and blank duplicates before summing).
- Data is FY2013-2016 (historical); frame as how the benefit works; add one current USDA figure only
  if verifiable.
- The "mother at the register" is an illustrative composite, not a real individual.

## Verification plan

Source + reconcile all absolutes against USDA (dataset go/no-go already passed: data is legit).
Full rank/summary tables before any claim; 4 charts; long-dash scan; adversarial-fact-check skill;
slug match; local astro build; publish to joechrisnaldy.com.
