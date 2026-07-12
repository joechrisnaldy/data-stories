# Post 07 design: what moves mental health, and what it's worth

**Date:** 2026-07-12
**Series:** data-stories (Post 07)
**Folder:** `Projects/analytics-blog/mental-health-productivity/`
**Dataset:** Kaggle `harpartapsingh13/mental-health-prediction-dataset` (500 rows, 18 cols, CC0, synthetic)

## The idea

Jonathan's hypothesis: good work-life balance and social support produce good mental
health, which improves productivity, for the person, the company, and the economy. It is a
causal chain, and he flagged the honest complication himself: mental health and productivity
are chicken-and-egg.

The dataset lets us *rank the levers* of mental health, bridge them to a proxy for "can you
actually work," and then price the payoff with real-world evidence the toy data cannot supply.

## Thesis (chosen: "real levers, honest data")

Take the hypothesis seriously. Use the data to show the pattern, be upfront that it is
synthetic so it *illustrates* rather than *proves*, and carry the productivity/economic leg
with real external evidence. The one-sentence stance:

> The things that most move your mental health are the unglamorous, non-medical ones: balance
> and support, more than sleep tips or a gym streak. And mental health is an input to
> productivity, not a reward you earn by being productive first.

## What the data can and cannot do (decided in brainstorming)

- **Synthetic and self-confirming.** Perfectly balanced (125 each of Normal / Anxiety /
  Burnout / Depression); the label is ~86% reconstructable from the lifestyle inputs. The
  clean relationships are partly built in. We say this plainly and early. It stops the essay
  from overclaiming and separates it from Post 03.
- **No productivity column.** In-data bridge = `concentration_level` (ability to focus), with
  `mood_score` secondary. The macro payoff comes from real citations, not our numbers.
- **Cross-sectional.** One snapshot, so it cannot resolve the chicken-and-egg. It can show the
  pieces fit; it cannot say which way the arrow runs. This is the honesty section, not a
  buried caveat.
- **Trust comes from outside the data.** The ranking is believable because real literature
  finds the same levers (work-life balance / job strain, social support, exercise). We cite
  that, so the toy data is the illustration and the peer-reviewed work is the evidence.
- **No Indonesia frame this time.** Universal essay.

## Analytical backbone

Reused venv `sberbank-housing/.venv` (pandas, numpy, scikit-learn, matplotlib).

1. **Outcome.** `distress` = mean of z-scored `stress_level`, `anxiety_score`,
   `depression_score` (higher = worse). Productivity proxy = `concentration_level`;
   `mood_score` secondary.
2. **Lever ranking, raw vs adjusted (the core technique).** Seven lifestyle inputs:
   work_life_balance, social_support, sleep_quality, sleep_hours, physical_activity_days,
   academic_work_pressure, social_media_hours. Report, per lever:
   - raw |correlation| with distress, and
   - standardized regression beta (all inputs z-scored, so betas are comparable and adjusted
     for the other levers), cross-checked against permutation importance from a
     HistGradientBoosting model.
   The honest story: work-life balance and social support stay on top; sleep quality and
   exercise deflate sharply once you stop double-counting shared variance. Verified numbers
   (listwise-complete n=319, OLS R^2=0.79):

   | lever | raw corr | std beta (adjusted) |
   |---|---|---|
   | work_life_balance | -0.82 | -0.29 |
   | social_support | -0.72 | -0.18 |
   | academic_work_pressure | +0.66 | +0.13 |
   | sleep_hours | -0.34 | -0.11 |
   | physical_activity_days | -0.66 | -0.10 |
   | sleep_quality | -0.68 | -0.08 |
   | social_media_hours | +0.48 | +0.07 |

3. **The bridge to work.** Same adjusted-importance method with `concentration_level` as the
   target. Verified: work_life_balance beta +0.66, social_support +0.55, pressure -0.35,
   sleep_quality +0.32 (OLS R^2=0.60). The same levers that set mental health set focus.
4. **Missing data.** Every column has ~4-7% missing; listwise deletion across all 7 inputs +
   3 score components drops n to ~319. Report n explicitly; cross-check the ranking with a
   NaN-native model (HistGradientBoosting permutation importance) on the fuller sample so the
   headline does not hinge on the deletion. State the choice in method notes.

## Charts (3, series palette)

1. **`01_levers.png` — rank the levers, raw vs adjusted.** Paired horizontal bars per lever:
   raw |corr| and adjusted importance, sorted by adjusted. The visual point: work-life balance
   and social support hold the top; sleep quality and exercise shrink. Caption names the
   double-counting.
2. **`02_bridge.png` — mental health is upstream of focus.** Scatter of the `distress`
   composite (x) vs `concentration_level` (y), r about -0.7, with a fitted line and points
   shaded by mental_health_condition so the Normal-to-Burnout gradient is visible. A short
   text callout notes the same two levers (balance, support) sit behind both. Point: worse
   mental health tracks worse focus at the person level, so mental health is an input to output.
3. **`03_payoff.png` — what it is worth (real numbers).** A clean annotated figure carrying the
   external macro evidence: depression and anxiety cost the global economy about US$1 trillion
   a year in lost productivity, and about US$4 comes back for every US$1 put into scaled-up
   treatment (WHO / Chisholm et al., 2016). Visually and textually separated from the toy data,
   clearly sourced.

## Section spine (~1,300-1,700 words, no long dashes)

1. **Open, stance-first.** Everyone has a theory about what wrecks their head. Here is a
   dataset that lets us rank the levers, with one honest caveat up front: it is synthetic, so
   read it as a hypothesis made visible, not proof.
2. **Rank the levers (chart 1).** Raw ranking, then the adjusted one; the deflation of sleep
   quality and exercise as the teachable, slightly counterintuitive moment; balance and support
   on top.
3. **The bridge to work (chart 2).** The same levers predict concentration; mental health is
   an input to output. Introduce `concentration_level` honestly as a proxy.
4. **What it is worth (chart 3).** The real external numbers for the productivity and economic
   payoff. This is where the essay earns its "for the economy/company" claim, on real evidence.
5. **The honesty reckoning.** Synthetic and self-confirming; cross-sectional, so it cannot cut
   the chicken-and-egg; why we still trust the ranking (real literature finds the same levers).
6. **Close, universal.** The biggest levers are relational and structural, not medical or
   heroic. Reframe the chicken-and-egg: stop asking which comes first and invest in the input.
   Analysis, not medical or financial advice.

## Citations to verify (pin in the plan)

- Harpartap Singh. (2026). *Mental health prediction dataset* [Data set]. Kaggle.
- WHO on lost productivity (~US$1 trillion/yr) and the 4:1 return: WHO "Mental health at work"
  and Chisholm, D., et al. (2016). Scaling-up treatment of depression and anxiety: A global
  return on investment analysis. *The Lancet Psychiatry*, 3(5), 415-424. VERIFY the exact
  figures and attribution before publishing.
- Two or three peer-reviewed anchors for "the levers are real" (verify exact refs): job strain
  / work-life balance and common mental disorders; social support and mental health; exercise
  and depression.

## Guardrails

- No long dashes; APA 7 references for every external fact.
- Correlational and associational language only; no causal claims from the data; no personalized
  medical or financial advice.
- Foreground the synthetic + cross-sectional nature; do not let the clean numbers imply proof.

## Title (CHOSEN)

**"What Actually Moves Your Mental Health (It Isn't the Sleep Tips)"**

Other candidates considered: "The Best Thing You Can Do for Your Productivity Isn't About
Work"; "Mental Health Is an Input, Not a Reward"; "You Can't Sleep-Hack Your Way Out of This".

## Verification (for the plan)

Data sanity (distress composite, n reporting), adjusted-vs-raw ranking reproduced, citation
checks (WHO/Lancet figures especially), long-dash scan, slug match, Astro build.
