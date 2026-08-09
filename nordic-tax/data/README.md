# Data

Six extracts, four of them straight from the OECD's SDMX API and two from Our World in Data.
All primary. Nothing from Kaggle, nothing hand-typed, nothing joined from anywhere else. The files
are not redistributed here. Run `python3 fetch_data.py` from the post folder and they reproduce.

## The files

| File | What it is | Producer | Coverage |
|---|---|---|---|
| `pit_thresh.csv` | Top statutory personal income tax rate, the marginal rate at that threshold, the threshold **as a factor of the average annual wage**, and the average wage itself | OECD Tax Database, Table I.7 | 38 countries, 2000 to 2025 |
| `rev_oecd.csv` | Tax revenue by the full OECD revenue classification, as percent of GDP, in national currency and in US dollars | OECD Revenue Statistics | 38 countries plus an OECD row, to 2022 |
| `rev_asap.csv` | The same classification for Asia and the Pacific. Used for Indonesia only | OECD Revenue Statistics in Asia and the Pacific | Indonesia 2015 to 2022 |
| `idd.csv` | Poverty rate on market and on disposable income, and Gini on market, gross and disposable income | OECD Income Distribution Database | 2015 to 2025, coverage varies sharply by country |
| `gdp.csv` | GDP per capita, PPP, constant 2021 international dollars | Eurostat, OECD, IMF and World Bank jointly, with minor processing by Our World in Data | to 2025 |
| `le.csv` | Life expectancy at birth | A Riley (2005), Zijdeman et al. (2015), HMD (2025) and UN WPP (2024) composite, with major processing by Our World in Data | to 2023 |

## Traps in these files

Recorded during the ten-minute vet, before anything was built. Each one is a way to publish a wrong
number while running correct code.

**TRAP 1. The threshold is a published series. The naive division gets it wrong by 9 percent.**
The hook of this post is `TS_PIT_TH`, unit `FCTR_WG_A_SAL_A`, "Factor of average annual wage". It
is tempting to recompute it by dividing a country's top-bracket threshold by its average wage.
That is wrong for Denmark, because Danish law states the threshold on *personlig indkomst*, which
is already net of the 8 percent AM-bidrag, while the average wage is gross.

What OECD actually does, established by reconstructing it exactly for two consecutive years: take
the statutory threshold, gross it up by dividing by 0.92, then divide by the gross average wage.

| Year | Statutory threshold | Grossed up | Average wage | Computed | OECD published |
|---|---|---|---|---|---|
| 2025 | 611,800 | 665,000.00 | 537,071.115 | 1.238197 | 1.238198 |
| 2024 | 588,900 | 640,108.70 | 521,300 | 1.227908 | 1.227910 |

The naive division, 611,800 / 537,071, returns 1.139 instead of 1.238. Use OECD's own factor. If
you ever must compute one, gross up first and say so.

The same logic explains Denmark's published top rate of 55.9044 percent, which is 8 + 0.92 x 52.07:
OECD classifies AM-bidrag as income tax rather than a social contribution, and the OECD Taxing
Wages country note states plainly that Danish employees pay no social security contributions.

**TRAP 2. Personal income tax is missing at the level you will reach for first.**
`T_1110`, "Taxes on income and profits of individuals", is absent for five countries in 2021
(Chile, Spain, Mexico, Poland, Portugal) and seven in 2022. The difference between `T_1100` and
`T_1110` is **capital gains**, not the individual-versus-corporate split; that split is `T_1300`,
"unallocable between taxes on income of individuals and corporations". An earlier version of this
note gave the wrong reason. All 38 report the wider `T_1100` in 2021. Choose once, apply through one
shared function, and state the choice. Silently dropping five countries would quietly change which
countries the post is about.

**TRAP 3. Denmark's near-zero is real and it breaks naive comparisons.**
Denmark's social security contributions are 0.06 percent of GDP in 2021. That is not missing data,
and it is not rounding noise standing in for a real number. Denmark
raises through personal income tax what most countries bill separately as contributions, which
makes its income tax line the highest in the OECD by a wide margin. Comparing income tax lines
across countries therefore compares plumbing, not burden. Compare totals, or compare income tax
plus contributions, and say which you did.

**TRAP 4. Norway's corporate tax is oil.**
Norway reports corporate income tax at 10.0 percent of GDP in 2021 against an OECD mean of 3.3, and
18.8 percent in 2022, because petroleum is taxed there under a separate regime at a 78 percent
marginal rate rather than the ordinary 22. Note that the figure itself swings by more
than eight points of GDP between two adjacent years, which is a second reason to distrust any
single-year reading of Norway. Any chart including Norway needs this on its face. Norway
is not evidence about what a tax system can raise from ordinary companies.

Say "mostly petroleum", not "petroleum". The band is the whole 1200 code and nothing in this
repository computes a petroleum share, so an unqualified label asserts a number no script here
produces. Round 4 caught the bare label on chart 2.

**TRAP 5. A zero threshold means two different things, and conflating them puts a false statement
about a country's tax law into print.**
Hungary reports a threshold of 0.00 in every year alongside a real 15 percent top rate: a genuine
flat tax, which should be labelled rather than dropped as missing. Latvia reports 0.00 for BOTH the
threshold and the rate, and only in 2025, after thresholds of 3.9 to 4.9 times the average wage at
31 to 35 percent in every year from 2018 to 2024. That is a missing-value placeholder. Three
fact-check rounds shipped "Hungary and Latvia tax from the first unit of income" before round 3
caught it. Test on rate AND threshold together, never the threshold alone.

**TRAP 6. Five time bases, and the newest revenue year is not the best one.**
Thresholds run to 2025, life expectancy to 2023, and the analysis uses 2021 for revenue rather than
the available 2022. In 2022 the file has no total for Japan or Australia and no personal income tax
split for Greece, so a 2022 analysis silently drops three countries including the OECD's
longest-lived one. Every code this analysis uses is complete for all 38 members in 2021.

There are FIVE time bases in this post, not three: thresholds 2025, revenue 2021, life expectancy
2023, a 2017 to 2021 mean tax level, and income-distribution data at the latest year per country,
which runs 2019 to 2025. They must never be presented as though they were one year.

**TRAP 7. The poverty series is three choices, not one number.**
`PR_INC_DISP` and `PR_INC_MRKT` are published against two poverty lines (50 and 60 percent of
median disposable income), two methodology vintages (`METH2011`, `METH2012`), and many age scopes.
Pick one of each, state all three wherever the number appears, and use the same combination
everywhere in the post.

**TRAP 8. The OECD row is a total, not a breakdown.**
`OECD_REP` carries a total tax revenue figure but no component detail. Any "OECD average" component
shown in a chart is computed in this repository, and the chart must say whether it is a weighted or
an unweighted mean.

**TRAP 9. One country's tax step runs backwards, and it is not an arithmetic error.**
Switzerland's disposable-income Gini (0.3146) is published slightly *above* its gross-income Gini
(0.3037), so the market-to-gross-to-disposable decomposition gives it a negative tax effect and a
transfer share of 113 percent. This is what the OECD publishes. A stacked chart will draw that
segment leftwards on top of the preceding bar unless it is handled explicitly, which silently makes
Switzerland look like an ordinary short bar rather than the exception it is. Israel, at 49 percent,
is the only country where transfers do less than half the work.

**TRAP 10. Denmark's headline tax take swings on investment returns.**
Denmark's total tax revenue is 47.4 percent of GDP in 2021 and 41.9 in 2022. The pension yield tax
sits in the unallocable income tax category and follows markets, and it collapsed when markets fell,
but it accounts for only about 38 percent of the fall (2.1 of 5.5 points). The rest is the
denominator: nominal GDP rose about 11 percent while revenue in kroner fell about 2 percent. An
earlier version of this note blamed the whole fall on the pension tax.
Whichever single year you pick decides whether Denmark looks like the OECD's heaviest taxer or its
seventh. Use a multi-year average for any cross-sectional "how much does this country tax" measure,
and say that you did.

## Reproducing

```bash
python3 fetch_data.py
```

Roughly 290 MB, most of it the two revenue files. The OECD SDMX endpoint has no server-side filter
for the revenue classification, so the whole table comes down and is filtered locally.

**TRAP 11. A startPeriod in the fetch script is not a property of the source.**
An earlier version of `fetch_data.py` requested the Asia and Pacific revenue file with
`startPeriod=2018`. Indonesia's series then appeared to begin in 2018, a fact-check round accepted
that as a property of the data, and a correct five-year comparison was "corrected" into a wrong
four-year one. The dataflow actually carries Indonesia from 2015. Before explaining a gap in a
downloaded file, re-query the endpoint without your own filters.
