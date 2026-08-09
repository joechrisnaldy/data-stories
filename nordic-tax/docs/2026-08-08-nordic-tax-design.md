# Post 21 design: How Scandinavia Actually Pays for Itself, and What Others Can Learn From It

Date: 2026-08-08. Status: approved 2026-08-08.
Slug: `how-scandinavia-actually-pays-for-itself`
Folder: `Projects/analytics-blog/nordic-tax/`
Chart prefix: `tax-`

## Stance

This post explains a financing system. It does not prosecute one, and it does not celebrate one.
The author's instruction is explicit: be objective, make it insight and learn, do not mislead, and
where the data cannot support a claim, drop the claim.

That rules out the two easy versions of this topic. It is not "high tax is a scam" and it is not
"Nordics solved it". It is: here is how the money is actually raised, here is what it demonstrably
buys, here is what it demonstrably does not, and here is the arithmetic that generalises.

## Thesis

Denmark's top income tax rate begins at 1.24 times the average wage, against 8.73 in the United
States. That is a design choice, not a consequence of collecting a lot: round 2 showed the
correlation between the tax level and where the top bracket starts is minus 0.06 across the 31
richer OECD members.

**Revised after round 1 of the fact-check.** An earlier thesis said the threshold sits low "because
the top of a distribution is not large enough to fund universal provision no matter how steeply it
is taxed". That was refuted: this repository holds no distributional data, and across the rich OECD
there is essentially no relationship between how much a country collects and how low its top bracket
starts (France 45.5 percent of GDP at 12.94 times, Austria 42.4 at 17.44). Denmark chose a broad
base; it was not compelled to.

What the revenue buys is also narrower than first drafted. It is not associated with longer life
once income is known, and its association with poverty removal is close to definitional, because
poverty removed IS the market-minus-disposable gap. The defensible thesis is: how rich a country is
predicts how long its people live; how much it taxes tracks how much levelling its transfer system
does; and the equalising happens on the spending side. Round 2 rejected "how big its transfer
system is": nothing in this repository measures transfer spending, only its effect on the Gini.

## Approved brainstorm decisions

| Dimension | Decision |
|---|---|
| Core question | Who actually pays for Scandinavia. Revenue side first, spending side as the payoff. |
| Hook | The top bracket lands near average pay. Denmark 1.24x the average wage, United States 8.73x. |
| Output | A bundle: health, schooling, poverty. **One chart, not three.** |
| Comparison set | The full rich-country field, roughly six labelled by name. |
| Indonesia | A cited closing passage, deliberately outside the charts. |
| Closing lesson | A universal benefit needs a universal bill. |
| Title | How Scandinavia Actually Pays for Itself, and What Others Can Learn From It. Author's steer, 2026-08-08: the title must carry the learning half, not just the description. The transferable lesson is therefore a named section, not a closing aside. |
| Stance correction (2026-08-08) | Author redirected from a corrective framing to an explanatory one. The earlier working title, "Scandinavia Doesn't Tax the Rich. It Taxes Everyone.", is **withdrawn**. Any surface still carrying a gotcha framing is a defect. |

## Sources

All primary. No Kaggle. Each series was confirmed by reading its own metadata, not its name.

| File | Series | Producer | Coverage |
|---|---|---|---|
| `pit_thresh.csv` | Top statutory PIT rate, the marginal rate at that threshold, the threshold **as a factor of the average annual wage**, and the average wage | OECD Tax Database, Table I.7 (`DSD_TAX_PIT@DF_PIT_TOP_EARN_THRESH`) | 38 countries, 2000 to 2025 |
| `rev_oecd.csv` | Tax revenue by full OECD revenue classification, percent of GDP, general government | OECD Revenue Statistics (`DSD_REV_COMP_OECD@DF_RSOECD`) | 38 countries plus an OECD row, to 2022 |
| `rev_asap.csv` | The same classification for Asia and the Pacific, used only for Indonesia | OECD Revenue Statistics in Asia and the Pacific (`DSD_REV_COMP_ASAP@DF_RSASAP`) | Indonesia 2015 to 2022. An earlier pass recorded 2018, which was an artefact of a startPeriod in `fetch_data.py`, not the source | 
| `idd.csv` | Poverty rate on market and on disposable income; Gini on market, gross and disposable income | OECD Income Distribution Database (`DSD_WISE_IDD@DF_IDD`) | 2015 to 2025, coverage varies by country |
| `gdp.csv` | GDP per capita, PPP, constant 2021 international dollars | Eurostat, OECD, IMF and World Bank jointly, with minor processing by Our World in Data. Required by `build_analysis.py`; round 3 found it missing from `fetch_data.py`, so a clean checkout could not reproduce the analysis | to 2025 |
| `le.csv` | Life expectancy at birth | A Riley (2005), Zijdeman et al. (2015), HMD (2025) and UN WPP (2024) composite, with major processing by Our World in Data. An earlier version of this row credited UN WPP alone, which is wrong | to 2023 |

The measure identifier that carries the hook is `TS_PIT_TH`, unit `FCTR_WG_A_SAL_A`, "Factor of
average annual wage". This is OECD's own published multiple. It is not a ratio this repository
computes by dividing a threshold by a wage, and it must not be replaced by one, because the Danish
top-tax threshold is defined on personal income after the 8 percent labour market contribution
while the average wage is gross. Dividing one by the other gives a different and wrong number.

## What the vet established

Confirmed by running the data. Every figure below is reproduced by `build_analysis.py`.

**Threshold at which the top rate starts, 2025, as a factor of the average wage:**
Belgium 1.03, Sweden 1.15, Ireland 1.16, Netherlands 1.17, **Denmark 1.24**, Iceland 1.33,
Norway 1.76, **Finland 2.97**, Germany 4.42, **United States 8.73**, France 12.94.

Two disciplines fall out of that list and both belong in the post:

- **Scandinavia is not a bloc.** Sweden 1.15, Denmark 1.24, Iceland 1.33, Norway 1.76, Finland
  2.97. Finland is nearer Canada than Sweden. Any sentence beginning "the Nordics" must survive
  Finland or be rewritten.
- **A low threshold is not a Nordic invention.** Belgium, Ireland and the Netherlands sit at or
  below Denmark. The honest description is a Northern European pattern, not a Scandinavian one.

**SUPERSEDED BY ROUND 1: the table below is the 2022 revenue year and the analysis now uses 2021.**
Do not quote these figures; run `build_analysis.py` and read `results.json` instead. The 2021
figures differ (Denmark's personal income tax is 25.05, not 23.5). Kept only to show what changed.

Personal income tax is `T_1100`, not the narrower `T_1110`. The difference between the two codes is
capital gains, not the individual-versus-corporate split, and `T_1110` is missing for five countries
in 2021 and seven in 2022.

| | Total | Personal income | Social contributions | VAT | Corporate | Property |
|---|---|---|---|---|---|---|
| Denmark | 41.9 | **23.5** | **0.0** | 9.2 | 3.1 | 1.7 |
| Sweden | 41.3 | 11.5 | 8.7 | 9.2 | 3.2 | 0.9 |
| Norway | 44.3 | 8.0 | 7.7 | 6.7 | **18.8** | 1.1 |
| Finland | 43.0 | 12.9 | 11.9 | 9.3 | 3.0 | 1.4 |
| Iceland | 34.9 | 13.9 | 3.0 | 8.3 | 2.6 | 2.0 |
| Germany | 39.3 | 10.7 | 14.6 | 7.4 | 2.4 | 1.1 |
| France | 46.1 | 9.9 | 15.0 | 7.6 | 2.9 | 3.7 |
| Netherlands | 38.0 | 8.2 | 12.6 | 7.3 | 4.3 | 1.5 |
| United Kingdom | 35.3 | 10.2 | 7.1 | 7.3 | 3.1 | 4.0 |
| United States | 27.7 | 12.5 | 6.0 | 0.0 | 1.8 | 2.9 |
| OECD unweighted mean | 34.2 | 8.2 | 8.9 | 7.1 | 3.8 | 1.8 |

**The correction this table forces, as revised after round 1.** Denmark's personal income tax is the
highest in the OECD and its social security contributions are essentially zero, while Germany and
France collect around 15 percent of GDP in contributions. Against those two countries specifically,
Denmark's income tax is the same money routed through one channel instead of two.

But the unqualified claim "Denmark's income tax is not uniquely heavy" was **REFUTED**. Denmark's
personal income tax is three times the OECD mean and 72 percent above second-placed Iceland; the
contributions it does not levy are worth 9.0 points of GDP against the mean, against an excess of
16.7, so routing accounts for about 54 percent of it. Round 2 refuted the "at most half" bound as
arithmetically false, and in the direction that flattered the conclusion. Counting all labour taxes Denmark ranks 4 of 38; counting all
taxes, 1 of 38. Denmark is a heavy-taxing country. Say so, then make the routing point about the
comparison it actually supports.

**Life expectancy at birth, 2023:** Japan 84.71, South Korea 84.33, Switzerland 83.95, Italy 83.72,
Spain 83.67, France 83.33, Norway 83.31, Sweden 83.26, Iceland 82.69, Netherlands 82.16,
**Denmark 81.93**, Finland 81.91, Germany 81.38, United Kingdom 81.30, **United States 79.30**.

Denmark levies the developed world's heaviest personal income tax and lives about 1.7 years less
than Spain, which taxes considerably less. That is one pair of countries, and the fits below are
what the post actually rests on.

**WITHDRAWN BY ROUND 2, AND THE ROUND-1 FIGURES BELOW ARE WRONG.** Round 1 claimed Indonesia's series
begins in 2018 and moved the comparison to a 2018-2021 window. That was false: the 2018 start was an
artefact of `startPeriod=2018` in this repository's own `fetch_data.py`. The dataflow carries
Indonesia from 2015. The window is 2017 to 2021, the same as every other tax level in the post.

**LIVE FIGURES:** Indonesia total tax 11.22, personal income tax 1.09; Denmark personal income tax
24.66; ratios 2.2 times Indonesia's entire tax take and 22.7 times its own personal income tax.

**Superseded round-1 figures, do not quote:** 11.12, 1.08, 24.79, 2.23x, 22.9x.

**Superseded text:** Indonesia, 2022, percent of GDP: total tax revenue 12.07, personal income tax 1.62, corporate
income tax 3.47, social contributions 0.52, VAT 3.41. Denmark's personal income tax alone, at
23.49, is **1.95 times Indonesia's entire tax take** and **14.5 times Indonesia's own personal
income tax**. An earlier pass in this conversation ran those two ratios together into a single
"factor of fifteen" claim, which was wrong. Use both numbers or neither.

## What the analysis established. This is the load-bearing section.

**The naive fit says tax buys longevity. It does not.** Across all 36 OECD members with data,
total tax revenue correlates positively with life expectancy at R-squared 0.294. That number is an
income effect wearing a tax label, and the robustness table proves it:

| Sample | Life expectancy | Poverty rate | Poverty reduction |
|---|---|---|---|
| All OECD (36) | 0.294 | 0.247 | **0.513** |
| Excluding the United States (35) | 0.286 | 0.225 | 0.500 |
| Excluding poorer members (31) | 0.111 | 0.125 | 0.377 |
| Excluding poorer members and the US (30) | **0.090** | **0.076** | **0.342** |

**Superseded numbers, kept visible.** The table above was computed on a single revenue year and a
hand-picked exclusion list. Both were replaced. The tax level is now the mean of 2017 to 2021,
because Denmark's single-year total swings from 47.4 to 41.9 percent of GDP on its pension yield
tax; and the excluded countries are now chosen by rule, as the five OECD members with the lowest
GDP per capita, which turn out to be Colombia, Mexico, Costa Rica, Chile and Türkiye, with Greece
sixth and staying in. The current figures are:

| Sample | Life expectancy | Poverty rate | Poverty reduction |
|---|---|---|---|
| All OECD (38 for life expectancy, 37 for the two poverty columns; Colombia has no poverty observation) | 0.166 | 0.362 | **0.548** |
| Excluding the five lowest income (33) | **0.023** | 0.253 | 0.409 |

**And the version that needs no cutoff at all.** Ordinary least squares on the full field, adding
the tax level to a model that already knows log GDP per capita:

| Outcome | Income alone | Income plus tax | What tax adds |
|---|---|---|---|
| Life expectancy | 0.291 | 0.325 | **+0.034** |
| Poverty rate | 0.268 | 0.463 | +0.195 |
| Poverty removed by the state | 0.073 | 0.548 | **+0.475** |

**REVISED AFTER ROUND 1: the symmetry was refuted.** The sentence originally drafted here, "how
rich a country is predicts how long its people live, and how much it taxes predicts how much poverty
it removes", presents the two halves as twin discoveries. They are not. Life expectancy and GDP per
capita are measured independently of each other; poverty removed is not measured independently of
the tax system, because it IS market poverty minus disposable poverty. Diagnostics: income adds
0.00002 once the tax level is known, market poverty alone predicts the outcome better (0.583) than
the tax level does (0.548), and tax correlates 0.45 with market poverty, so high-tax countries have
more to remove.

The approved wording is: **how rich a country is predicts how long its people live; how much it
taxes tracks how much levelling its transfer system does.** Round 2 rejected the earlier candidate
"how big its transfer system is", because nothing in this repository measures transfer spending,
only its effect on the Gini. Do not reinstate it. The post must define "poverty removed" at
first use, concede the near-definitional part, and carry the France counterexample (45.5 percent of
GDP removing 27.4 points against Denmark's 46.2 removing 15.9), which is what stops it being purely
circular.

**SUPERSEDED. Do not use the wording that stood here.** It re-issued the refuted symmetry as
a binding instruction. The approved wording is the one above: how rich a country is predicts how
long its people live; how much it taxes tracks how much levelling its transfer system does. The
superseded text asserted that what the tax level predicts "is how much poverty the state takes
out", which round 1 refuted as near-definitional and round 2 confirmed.

It also carries the methodological lesson the title now promises. Anyone running the obvious
regression on the full OECD field would have concluded that taxation buys longer life. It does not.
It buys the difference between rich countries and poorer ones, which is a different sentence.

**Transfers do the equalising, not taxes.** Across the 35 OECD members with all three Gini series,
the median country does **77 percent** of its total inequality reduction through cash transfers and
the remainder through direct taxes. **34 of 35** are above 50 percent. This is the payoff of the
revenue-side argument: if the tax side is broad and comparatively flat, the progressivity has to be
downstream, and it is.

## The education panel: DROPPED, and the reason is a section of the post

Resolved 2026-08-08. Two investigators split, USE against DROP, and an adjudicator ruled DROP after
verifying the decisive fact independently. Chart 3 runs on life expectancy, poverty rate and
poverty reduction. There is no schooling panel, and the post explains why in a paragraph, because
the explanation is more interesting than the panel would have been.

**The decisive argument.** Sixteen education systems breached PISA's 5 percent exclusion cap in
2022, and the breach list is led by exactly this post's protagonists: **Denmark 11.6 percent**, up
from 5.7 in 2018, then the Netherlands 8.4, Latvia 7.9, Sweden 7.4, Norway 7.3, the United States
6.1. The OECD's own Adjudication Group states that high exclusions may bias performance upwards.
Denmark's excess is driven by dyslexic students who normally use electronic assistive devices to
read on screen, which the PISA assessment does not accommodate, so schools excluded them. The word
"diagnosed" was this session's addition and does not appear in the OECD source; do not reinstate it.
The exclusion rates are in PISA 2022 Results Volume I; the dyslexia attribution is in the separate
Denmark country note, so the two need different citations.

**DIRECTION CORRECTED TWICE. READ THE FINAL VERSION AT THE END OF THIS BLOCK.** Round 1's wording
was wrong, and round 2's replacement was ALSO wrong: it said an upward bias "cannot hide" a true
effect, which is false, because a positive contribution from a high-x country can drag a true
negative slope to zero. The shipping argument, verified in round 3 from the OLS derivative
d(slope)/d(y_j) = (x_j - x_bar) / sum((x_i - x_bar)^2), is: Denmark sits 12.65 points of GDP above
the mean on the x axis, so inflating its score RAISES the fitted slope and pushes the panel toward
"tax buys learning". Do not reinstate either earlier version.

The original round-1 wording here said a flat line could not be
separated from "the measurement washed the learning out". That inference is backwards. Excluding
weak readers biases Denmark's score **upward**, and an upward bias can manufacture a result that is
not there but cannot hide one that is. So a flat panel would be consistent with a true relationship
that is **negative**, and there would be no way to tell the two apart.

Also do not generalise the mechanism. The 2022 breach list includes Latvia and the United States,
which are not high-tax generous states, so "exclusion tracks generosity" is not supported. Scope the
argument to Denmark: at 11.6 percent against a 5 percent standard, Denmark is simply not comparable
with countries inside the cap, and a panel that cannot distinguish its own finding from its own bias
has no place in a figure whose entire point is a lesson about naive fits.

**Two further reasons, each sufficient alone.**
- **Timing.** PISA 2025 initial results are dated 8 September 2026, thirty-one days after this
  design was written, with the full report in December. A PISA 2022 panel would need rebuilding
  within a month.
- **Flat by construction.** OECD's own finding is that cumulative spending per student relates to
  performance only up to roughly USD 75,000 PPP between ages 6 and 15, and every country in the
  rich subsample is above that. The only slope on offer comes from the poorer members this post
  explicitly removes.

**Alternatives considered and rejected.** UNESCO expected years of schooling is a throughput
measure that ranks Greece and Türkiye above Finland. World Bank Harmonized Learning Outcomes
correlates with PISA maths at r = 0.948 across the 37 shared OECD countries, so it is the same test
with more steps, and it has not been refreshed since 2020. OECD attainment is a stock of
credentials produced by schooling from 1995 to 2020, so plotting it against recent tax revenue
asserts a causal direction the data cannot carry.

**One correction to carry forward.** The investigator arguing DROP wrote proposed copy claiming
Finland was on the breach list. **Finland is not on it**; 7.4 is Sweden and 7.3 is Norway. The
argument sharpens once fixed, since Denmark excluded 11.6 percent and still outscored a Finland
that stayed inside the cap, but any PISA score quoted in the post must be sourced to OECD country
notes rather than a secondary compilation.

## Everything required by the chart spine is now computed.

Nothing in the "not yet computed" list remains. The poverty rates, the Gini decomposition, the
correlations and the income control are all in `results.json`, and the education question is closed.

## Four charts

**1. `tax-1-where-the-top-begins.png`: who the word "top" refers to.**
The threshold as a factor of the average wage, 2025, for the OECD field, sorted. Denmark, Sweden,
Finland, Germany and the United States labelled, plus Belgium, Ireland and the Netherlands, because
their presence at the bottom is what stops the chart being read as a story about Scandinavia. The
axis spans 0 to 51.5, so the scale treatment must be decided at build time rather than assumed; a
linear axis will crush the entire interesting region. Flat-tax countries reading 0.00 are excluded
with a stated reason, not silently dropped.

**2. `tax-2-how-the-money-is-raised.png`: the mix, and the labelling difference.**
Composition by tax type as percent of GDP, for a named set including Denmark, Sweden, Norway,
Finland, Germany, France, the Netherlands, the United Kingdom and the United States. The
load-bearing visual is Denmark's tall personal income tax bar against its absent social
contributions bar, mirrored by Germany and France. Every band label must name everything inside it;
"goods and services" is not an acceptable label for a band containing VAT plus excises plus vehicle
taxes, so either the band is split or the label enumerates. Norway is annotated on the figure for
petroleum, not left to a footnote.

**3. `tax-3-what-it-buys.png`: the bundle, as small multiples, showing a collapse.**
One figure, three panels, common x axis of total tax revenue as percent of GDP. Panels: life
expectancy, poverty rate, and poverty reduction in percentage points. **No schooling panel**, for
the reasons in the education section above, which the post states rather than passes over.

The design changed after the robustness run. Each panel must show **two fits, not one**: the full
OECD field and the same relationship with the five poorer members removed. The reader has to see
two of the three associations collapse when the comparison is restricted to comparable countries,
because that collapse is the finding. A single fit line per panel would show the opposite of what
is true and would be the misleading version of this chart.

Poorer members are drawn in a distinct, clearly labelled colour so it is obvious which points leave.
The R-squared for both samples is printed in each panel.

**4. `tax-4-where-the-equalising-happens.png`: taxes or transfers.**
Market Gini to gross Gini to disposable Gini, with the total reduction split into the part done by
transfers and the part done by taxes. Closes the argument: if the revenue side is broad and flat,
the equalising has to be happening somewhere else, and this locates it.

Fallback if chart 4 cannot be computed honestly, for example if the gross-income Gini is missing
for too many countries: replace with the same countries' poverty rate before and after the state
acts, which uses `PR_INC_MRKT` and `PR_INC_DISP` and requires no three-stage decomposition. If the
fallback is used, the post says the decomposition was not available rather than implying it was
never wanted.

## Method rules for this post

- **FIVE time bases, never blended.** Thresholds 2025, revenue **2021** (not 2022; the 2022 file
  drops Japan, Australia and Greece), life expectancy 2023, a 2017 to 2021 mean tax level, and
  income-distribution data at the latest year per country, 2019 to 2025. An earlier version of this
  rule said "three vintages" and named 2022 as the revenue year. Both were wrong and were corrected
  after round 1 of the fact-check.
- **Denmark's 2026 reform: RESOLVED 2026-08-08, and it becomes a section of the post.**
  Verified against primary Danish sources by three independent investigators, all agreeing.

  **The law.** LOV nr 482 af 22/05/2024, implementing the political agreement of 14 December 2023.
  The act commenced 1 June 2024 but its § 1 "har virkning fra og med indkomståret 2026". Denmark's
  single topskat is replaced by three national taxes, all stated on personlig indkomst, which is
  already net of the 8 percent AM-bidrag:

  | Tier | Rate | Threshold (after AM-bidrag) | Cumulative surtax |
  |---|---|---|---|
  | Mellemskat, PSL § 7 | 7.5% | DKK 641,200 | 7.5% |
  | Topskat, PSL § 7 a | 7.5% | DKK 777,900 | 15% |
  | Toptopskat, PSL § 8 | 5% | DKK 2,592,700 | 20% |

  For 2025 there was one tier: topskat at 15% from DKK 611,800. skat.dk says plainly that
  "Mellemskat er det, der til og med 2025 hed topskat": the entry point did not move, the rate on
  it was halved, and two new tiers were added above.

  **A figure this session got wrong.** An earlier pass put the toptopskat threshold at "around
  DKK 2.3 million". That is the 2023-level number printed in the bill's own table. Statutory
  indexation under PSL § 20 carries it to **DKK 2,592,700** for 2026, about 11 percent higher. Do
  not quote bill-table figures as current law.

  **A sentence this session drafted and an adjudicator ruled FALSE.** The rejected wording was:
  "the reform moves the OECD-published top-rate threshold from about 1.24x to roughly 4-5x, even
  though the marginal rate faced by an average earner barely changed." Four grounds, all verified:

  1. **There is no OECD-published 2026 figure.** A re-query of Table I.7 for 2024 to 2026 returns
     228 observations in 2024, 228 in 2025 and **zero in 2026**, for every country. The sentence
     asserts a published transition that does not exist.
  2. **The range is wrong even on our own method.** At 2 to 6 percent average-wage growth off the
     2025 wage of DKK 537,071.115052, the toptopskat factor runs **4.95 to 5.14**. It is "about
     five", not "4 to 5", and the stated uncertainty is really about the wage, not the bracket.
  3. **The top rate rose.** From 52.07 to 57.07 percent of personal income, which is 55.90 to 60.50
     on OECD's gross-earnings basis. A clause saying the marginal rate "barely changed" invites the
     reader to conclude the reform was rate-neutral. It was not.
  4. **OECD has not chosen which tier it will report.** Denmark's statutory ceiling covers only
     municipal tax, bundskat and mellemskat, and Skatteministeriet sets no concrete ceiling over
     topskat and toptopskat. A compiler following the ceiling mechanically would report mellemskat,
     landing at 1.22 to 1.27, visually unchanged. Unlikely, but live.

  **The approved wording**, which is true and better:

  > For 2025 the OECD put Denmark's top statutory income tax rate at 55.90 percent of gross wage
  > earnings, starting at 1.24 times the average wage. From 1 January 2026 the single 15 percent
  > topskat was split into three tiers, and Denmark's highest rate now starts far higher up: DKK
  > 2,592,700 of personal income, about five times the average wage. It is also a higher rate,
  > about 60.5 percent on the same basis. The average earner sat below the old threshold and sits
  > below the new bottom tier, so almost nothing changed for them. OECD has not yet published a
  > 2026 figure; the five-times number is this post's calculation from the statutory threshold and
  > a projected average wage.

  **Five conditions on opening with the 1.24.** Name the year in the same sentence. Say what the
  number is made of (DKK 611,800 of personal income after AM-bidrag, DKK 665,000 gross, against an
  average wage of DKK 537,071) and publish the rate alongside the threshold. Disclose the reform in
  the same paragraph, not a footnote. Never present a 2026 factor as OECD-published. And **never
  draw a continuous line across 2025 to 2026**: the naive continuation gives a spurious "no change"
  if it tracks mellemskat and a spurious fivefold jump if it tracks toptopskat, and neither is a
  like-for-like change in burden. Show a break.

  **Further constraints, none optional.**
  - The reform is a **cut** for everyone between DKK 611,800 and 777,900, roughly neutral above
    that, and a rise only above DKK 2,592,700. Mellemskat and topskat stack back to a 15 percent
    combined surtax above 777,900, so the old 15 percent did not disappear.
  - **The three tiers do not share a base.** Mellemskat includes positive net capital income above
    DKK 55,000; topskat and toptopskat are on personal income alone. Modelling all three on one
    base is an error. **SUPERSEDED IN ROUND 5.** The instruction below was "print the 55,000
    unmarried figure only; the married-couple doubling is single-sourced". That is obsolete and
    was itself the defect: the DKK 110,000 married figure sits on the same Skatteministeriet
    satser table the draft already cites, so the bare 55,000 was simply wrong for couples. Print
    both, with the filing status named.
  - **20 percent is a cumulative increment, not a rate.** A secondary Danish site claims a
    "top-topskat på 20 pct."; the statute says 5. Do not repeat the 20.
  - **Bundskat at 12.01 percent is a higher standalone rate than any of the three tiers.** Say
    "highest rate on labour income" rather than "highest statutory rate", and note that share
    income is taxed at 42.
  - **Do not pin a paragraph-level citation.** Two investigators quoted different commencement
    paragraphs for the same act and one of them is wrong. Cite "LOV nr 482 af 22/05/2024, effective
    for income year 2026" and stop.
  - **Gross-work-income equivalents are derived, not statutory.** DKK 696,957 / 845,543 / 2,818,152
    come from dividing by 0.92 and assume all income is AM-liable work income. Never print them as
    figures Denmark legislated.

  **A trap for the later fact-check round.** The threshold ratio is basis-invariant: 611,800 / 0.92
  / 537,071.12 and 611,800 / (537,071.12 x 0.92) are the same number. So reproducing 1.238198
  proves **nothing** about whether OECD works gross or net. The gross basis is established by the
  unit code on the rate (`PT_WG_EARN_G`), by 55.9044 = 8 + 92 x 0.5207, and by OECD's statement
  that Danish employees pay no social security contributions. A verifier who "confirms" the basis
  from the ratio has confirmed nothing.
- **Norway is not a model.** Corporate tax is 10.0 percent of GDP in 2021, the post's revenue year,
  against an OECD mean of 3.3, and 18.8 percent in 2022. Petroleum revenue. Wherever
  Norway appears, this is stated on the figure or in the sentence, not deferred.
- **Finland is the test of every generalisation.** Before any sentence beginning "the Nordics" or
  "Scandinavia", check it against Finland at 2.97. If it fails, rewrite it.
- **Use `T_1100`, not `T_1110`, unless verified.** Personal income tax at the `T_1110` level is
  missing for Chile, Spain, Mexico, Poland and Portugal in 2021; Australia and Greece join them in
  2022. Decide the treatment once, apply
  it in one shared function, and state it. Two scripts must never filter the same data differently.
- **RESOLVED IN ROUND 3, and the rule below was itself wrong.** Latvia is NOT a flat tax. It
  reports a threshold of 3.9 to 4.9 times the average wage in every year from 2018 to 2024 at a top
  rate of 31 to 35 percent, and both fields drop to exactly zero only in 2025, which is a
  missing-value placeholder. Hungary IS a flat tax: threshold zero every year alongside a real 15
  percent rate. `build_analysis.py` now separates `flat_tax_excluded` from `unusable_excluded` on
  exactly that test. The superseded rule follows.

  Superseded: Latvia and Hungary report a 0.00
  percent top statutory rate, which is not plausible on its face. Resolve before either appears.
- **The OECD average row has no component breakdown.** Any "OECD average" drawn in a chart is
  computed here, and the chart says whether it is a weighted or unweighted mean.
- **Poverty definitions are choices.** The IDD carries two poverty lines, 50 and 60 percent of
  median disposable income, two methodology vintages, and many age scopes. Pick one of each, state
  all three on the chart, and use the same choice everywhere in the post.
- **Association, not causation, and say which.** This is cross-country observational data. That
  Denmark taxes heavily and does not lead on life expectancy is not evidence that health spending
  fails; it is evidence that the level of tax revenue does not predict longevity across rich
  countries, which is a narrower and defensible claim. No sentence may sign a causal direction the
  data cannot sign.
- Exactly 4 charts. No em or en dashes. APA 7 references. Nothing joined beyond the SIX files in
  `data/` (round 3 found `gdp.csv` was a sixth file the fetch script did not download).

## Draft outline

> **SUPERSEDED BY THE SHIPPED DRAFT (rounds 1 and 2).** This outline still carries refuted framings:
> "comprehensive rather than merely heavy", "the arithmetic forces the threshold down into the
> middle", and the 2022 Indonesia figures. Read `draft/how-scandinavia-actually-pays-for-itself.md`
> for what the post says. Kept only as a record of what changed.


1. Open on the threshold: in Denmark the top rate starts at 1.24 times the average wage, in the
   United States at 8.73. The word "top" is doing very different work in each country.
2. Chart 1, and immediately the two disciplines: Finland breaks the bloc, and Belgium, Ireland and
   the Netherlands show the pattern is Northern European rather than Scandinavian.
3. How the money is actually raised. Chart 2, and the correction: Denmark's income tax is
   comprehensive rather than merely heavy, because it absorbed the contributions other countries
   bill separately. Totals are closer than the headline lines suggest.
4. What it buys. Chart 3, and the collapse. The naive fit across the whole OECD says tax buys
   longer life; restricted to comparable rich countries it does not, and neither does the poverty
   level. Only poverty reduction survives. State the numbers, state what leaves the sample, and do
   not dress a surviving association as proof of cause.
5. Where the equalising happens. Chart 4, and the 77 percent median. If the revenue side is broad,
   the progressivity is downstream of it, and this locates it in the transfer system.
6. **What travels.** The section the title now promises, so it is a named section and not an aside.
   A universal benefit needs a universal bill: the arithmetic forces the threshold down into the
   middle of the distribution, and that is a constraint rather than a preference. What copies is
   the structure (a broad base, and equalising done through transfers rather than through the rate
   schedule); what does not copy is the collection capacity and the consent underneath it.
7. Then Indonesia, cited and outside the charts: 12.07 percent of GDP in total, 1.62 from personal
   income tax, against a Danish personal income tax alone worth 23.49 percent of Danish GDP, which
   is 1.95 times Indonesia's entire tax take and 14.5 times its personal income tax. A tax on the
   rich is not the missing piece, and the post says what the missing piece actually is.
8. Method notes, then references.
