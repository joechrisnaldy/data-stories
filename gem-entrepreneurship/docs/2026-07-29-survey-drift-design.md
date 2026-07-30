# Post 16 design: The Survey Found Indonesia's Business Owners. It Just Couldn't Count Them.

> **SUPERSEDED SECTIONS BELOW.** This doc was first written for an earlier thesis, "Indonesia didn't
> stop starting businesses, the survey stopped finding them", with a cause the analysis could not
> identify. Two rounds of adversarial fact-checking changed both the thesis and the title. GEM's
> screening question *did* find Indonesia's business owners; the failure is in the derived
> established-ownership indicator, and it is localised to the 42-month classification step. Anything
> below that contradicts the shipped post is retained as a record of what was retracted and why.

Date: 2026-07-29. Status: approved, building.

## Where this came from

Jonathan supplied two links: the Data Is Plural edition of 2024-05-08, and the GEM Consortium's
Adult Population Survey. GEM is the entry in that edition.

The angle he first picked was **Indonesia's belief-to-action gap**: in the 2022 round Indonesia
ranks 2nd of 49 economies on seeing good business opportunities, 8th on self-rated capability and
among the five least afraid of failure, yet 36th on actually starting anything. The plan was to name
that gap, test the usual explanations, and crown no cause.

The pre-check killed it, which is why the pre-check existed. Pulling Indonesia's eight GEM rounds
showed the gap is not a standing feature; it opened because two lines crossed, with belief rising
and measured activity falling by roughly two thirds. A fall that large had to be validated before
anything was built on it. It did not validate. The post that survives is about the measurement.

## Thesis

The world's flagship entrepreneurship survey and the world's labour statistics stopped telling the
same story about Indonesia, and about each other more generally. Indonesia's own labour force survey
records 10.6 million MORE business owners in 2022 than in 2013. Over the same decade GEM records
Indonesia losing roughly three quarters of its established business owners. In 2013 the two sources
sat 4.0 points apart, which is about what their differing definitions predict. By 2022 they sit 22.6
points apart, which nothing predicts.

I can demonstrate that the series broke. I cannot say why. The essay says so plainly.

## Stance, tone, structure

- **Stance** (his pick): name the divergence, test the usual suspects, refuse to crown a cause.
- **Tone toward GEM** (his call, confirmed): constructive, not a takedown. GEM is a large
  international research consortium, not the individual uploader of the cancelled Post 08. It gets
  explicit credit, because it is GEM's own openly published microdata that made this check possible
  at all. Most survey programmes do not let an outsider do this.
- **Hook** (his pick): the popular story first, then the contradiction. Everyone says Indonesia is a
  nation of entrepreneurs; the world's standard measure says it stopped being one; the twist is that
  the measure is what moved.
- **Close** (his pick): return to the person introduced in the opening.
- **Title** (his pick): "Indonesia Didn't Stop Starting Businesses. The Survey Stopped Finding Them."
  Chosen because "stopped finding" describes what the data shows without asserting a cause, which
  matters in a piece that explicitly declines to name one. Rejected: anything using "missing" or
  "lost", which imply GEM mislaid real people rather than an instrument drifting.

## The evidence chain

**1. The divergence, on one denominator.** Business owners as a share of the 18 to 64 population.

| Year | Sakernas employers + own-account | GEM established ownership | Distance |
|------|------|------|------|
| 2013 | 25.2% (43.0M) | 21.2% | 4.0 pts |
| 2017 | 25.8% (46.3M) | 10.4% | 15.4 pts |
| 2020 | 27.6% (51.3M) | 11.4% | 16.2 pts |
| 2022 | 28.3% (53.6M) | 5.7%  | 22.6 pts |

Indonesia's own survey shows employers plus own-account workers rising 24.6%, from 43.0 to 53.6
million people. The 4-point gap in 2013 is expected: GEM requires owner-manager status and excludes
contributing family workers. The widening is not.

Critically this is **Sakernas via ILOSTAT, not a model**. The World Bank's headline self-employment
series is a modelled ILO estimate and a flat modelled series would prove nothing. The direct
national survey data settles it.

**2. Three suspects, all ruled out.**

| Suspect | Test | Result |
|---|---|---|
| Sample halved, 4,500 to 2,600 | Partial correlation of sample size with TEA, controlling for year | r = +0.16, p = 0.71. Raw r = +0.67 is spurious; both series simply decline over time. |
| Sample got richer and less working-class | Reweight 2022 to 2013's income x work x education composition | TEA moves 8.14% to 8.90%, against 24.75% in 2013. Explains 5% of the fall. |
| Survey weighting | GEM's own weights | 8.12% unweighted against 8.07% weighted. No effect. |

**3. Indonesia is the sharp end of something global.** Of 55 economies with five or more rounds,
Indonesia has the largest negative divergence between GEM ownership and ILO self-employment. But its
z-score is only -1.54, because the distribution is enormously wide (Saudi Arabia +218, Estonia +128,
Qatar -65, Mexico -64). The measures barely agree anywhere.

**4. The two measures never agreed well. CORRECTED FINDING, see below.**

Median within-country correlation over time is +0.13 for established ownership and -0.001 for TEA,
across 45 economies with six or more rounds. Cross-country, on a near-constant panel of economies
with eight or more rounds, the correlation sits between +0.19 and +0.48 in every year from 2013 to
2022 with no trend, and is not statistically significant in seven of those ten years.

### A wrong claim I caught before drafting

My first pass reported that the agreement was DECAYING: full-sample r of +0.65 in 2013 falling to
+0.28 in 2022, which is a real arithmetic fact and significant on a Fisher test (z = 2.51, p = 0.012).
It is also an artefact. The set of participating economies changes every round, from 68 down to 47.

Two checks kill the decay story:

- On a near-constant panel (8+ rounds) the correlation is flat across all ten years: 0.477, 0.187,
  0.215, 0.342, 0.413, 0.224, 0.334, 0.277, 0.219, 0.244. No trend.
- On the identical 33 economies present in both 2013 and 2022, r goes 0.473 to 0.215, and a Fisher
  test says those are **not distinguishable**: z = 1.14, p = 0.253.

So the honest claim is the simpler and stronger one: these two measures of the same idea have never
tracked each other well anywhere, and Indonesia is the most extreme case of a disagreement that is
everywhere. The essay must not say the measures "drifted apart" or "stopped agreeing" globally. The
Indonesia finding is unaffected, because it rests on Sakernas against GEM directly, not on this.

## Four charts

1. `gem-1-divergence.png` The two sources on one denominator, 2013 to 2022. The whole thesis.
2. `gem-2-suspects.png` The three candidate explanations and how much of the fall each accounts for.
3. `gem-3-not-alone.png` Indonesia against all 52 economies' divergences.
4. `gem-4-drifting-apart.png` Cross-country agreement by year, 0.65 falling to 0.28.

## Honesty requirements

- Say plainly that the cause is undiagnosed. Do not imply GEM did something wrong; imply only that
  the series stopped matching the country.
- GEM and ILO measure different things by design. The story is the CHANGE in the distance between
  them, never the level gap.
- Indonesia is missing from GEM in 2019 and 2021, so the series has holes. State them.
- Indonesia's z-score is -1.49, so it is the most extreme case but not a statistical freak. Do not
  call it an outlier without that qualifier.
- GEM's attitude questions are not implicated by any of this; only the business-ownership questions
  are tested here. Do not generalise to the whole instrument.
- Credit GEM for the open microdata. Without the individual-level files the reweighting test would
  have been impossible and this post could not exist.

## Data sources

- GEM APS national-level files 2013 to 2022, `gemconsortium.org/file/open?fileId=N`, public, no
  login. Individual-level 2013 and 2022 for the composition tests. Three-year public release lag.
- ILOSTAT `EMP_TEMP_SEX_STE_NB_A` for Indonesia, source BA:510 (Sakernas), non-modelled.
- World Bank `SL.EMP.SELF.ZS` for the 52-economy comparison and `SP.POP.1564.TO` for the denominator.

## What the two fact-check rounds changed (authoritative over anything above)

**Round 1 (12 agents, 49 findings).** Killed "more than half of Indonesian workers work for
themselves" (39.6% on the essay's own cut, employers plus own-account as a share of employment).
Found `ESTBBUS1` used in place of `ESTBBUSO`. Found country aliases applied to the merge key but not
the groupby, double-counting four economies. Corrected the weighting suspect, which runs the opposite
way to the suspicion: weighting makes the fall look steeper.

**Round 2 (3 agents, 5 HIGH findings).** The decisive one: `omyr5job` is a five-year headcount
projection, not the payment-year question, so the entire mechanism had been computed on the wrong
item. The real gate is `omwageyr` (Q2E2). Also: the 56/44 decomposition was an artefact of ordering
(symmetric split is 37/63, and the reverse ordering gives 22/78); raw `ownmge` is not what the
published screen equals (`OWNMGEyy` is); and the "same denominator" claim was false, since GEM is
18-64 while the Sakernas share used here is 15-64 with an all-ages numerator.

**Retracted claims, for the record.** "The survey stopped finding them" (it found them). "The
classification step held flat at 45.6% for six years, then broke" (an artefact of having microdata for
only 2013, 2016 and 2018; the published series swings 29% to 63%). "Six tenths of a point apart" (too
precise for mismatched bases). "The residual is zero" as evidence of robustness (it is zero by
construction in every ordering).

**Final shipped findings.** Sakernas up 43.0M to 53.6M, +24.6%. GEM published established ownership
21.2% to 5.7%. GEM screen 46.5% to 28.9%, moving from far above the national count to close to it.
Payment-year nonresponse 24.1% to 83.0%, the highest of 49 economies against a median of 55.3%. Pass
rate among those who answered, 57.6% to 64.1%, so the rule did not tighten. Symmetric decomposition
37% screen and 63% classification. 54 economies, Indonesia last, z = -1.50.
