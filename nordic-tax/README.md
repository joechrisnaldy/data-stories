# How Scandinavia Actually Pays for Itself, and What Others Can Learn From It

Post 21 in the data-stories series. [Read the essay](https://joechrisnaldy.com/blog/how-scandinavia-actually-pays-for-itself).

## The question

Everyone has a picture of how the Nordic model is financed, and it usually involves taxing the
rich. This post goes and looks at the revenue tables instead, then asks what the money demonstrably
buys and what it does not.

It is an explanatory post, not a corrective one. The Nordic systems work. The interesting thing is
the design, not a gotcha about it.

## What the data says

**Where the top bracket begins.** In 2025 Denmark's top statutory rate started at 1.24 times the
average wage. In the United States, 8.73. That is the hook, and two things immediately discipline
it. The Nordic countries are not a bloc: Sweden 1.15, Denmark 1.24, Iceland 1.33, Norway 1.76,
Finland 2.97. And a low threshold is not a Nordic invention: Belgium at 1.03, Ireland 1.16 and the
Netherlands 1.17 all sit at or below Denmark. Hungary applies its top rate from the first unit of
income, which is why a multiple of the average wage is undefined for it, and Estonia's single 22
percent rate starts at 0.31.

**How the money is raised, and the correction that matters.** Denmark raises 25.0 percent of GDP
from personal income tax, the highest in the OECD, and 0.06 percent from social security
contributions. Germany and France are the mirror image: modest income taxes and around 15 percent
of GDP in contributions. Read one line and the countries look wildly different. Read every tax on
labour together and Denmark, Sweden, Finland, Germany and France land between 24.9 and 26.5 percent
of GDP, a spread of 1.6 points, against personal income tax lines that differ by a factor of 2.6.
Against Germany and France in particular, Denmark's income tax is the same money routed through one
channel instead of two. Two qualifications: that convergence belongs to those five countries, and
swapping France for Norway widens the spread to 6.06 points; and Denmark still ranks fourth of 38 on
all labour taxes and first of 38 on total tax, so it is a heavy-taxing country either way.

**What the revenue buys.** Across the whole OECD field, tax revenue correlates with life expectancy
at R-squared 0.166, which looks like evidence that taxing more buys longer life. It is not. Remove
the five members with the lowest GDP per capita and it falls to 0.023. Control for log GDP per
capita instead, so no cutoff has to be defended, and the tax level adds 0.034 to a model that
already knows how rich a country is.

What survives is redistribution, but it is weaker than it first appears. "Poverty removed" is
defined as market poverty minus disposable poverty, so it is the arithmetic output of the tax and
transfer system, and the regressor is the size of that same system. Market poverty alone, measured
before the state acts, predicts it slightly better (R-squared 0.583) than the tax level does
(0.548). So:

> How rich a country is predicts how long its people live. How much it taxes tracks how much
> levelling its transfer system does.

**Where the equalising happens.** Mostly in the transfer system. Across 35 OECD countries the median
does 77 percent of its total inequality reduction through cash transfers rather than through direct
taxes and employee social contributions, and 34 of 35 do more than half that way. The tax level
predicts the transfer step at R-squared 0.497 and the tax step at 0.066, and
86.0 percent of the
covariance between the tax level and total inequality reduction runs through transfers.

## The lesson

A universal benefit needs a universal bill. That is a prior, not a finding: nothing here measures
what share of the bill each income group carries, only how much is collected and what it does. The
testable version does not survive. Across the 31 richer OECD members the correlation between how
much a country collects and where its top bracket starts is minus 0.06, the sign the claim predicts
and a magnitude of nothing: it accounts for 0.3 percent of the variation. Across all 36 members it
is minus 0.47, carried by the same five low-income countries excluded above. France and Austria are
top-ten collectors whose top brackets start at 12.94 and 17.44 times the average wage. Denmark chose
a broad base; it was a choice, not an arithmetic necessity. What does look transferable is the
second half, equalising through what the state pays out rather than through how steeply it taxes.
What does not transfer is the capacity to collect, and the consent underneath it.

For scale: Indonesia's entire tax take averaged 11.22 percent of GDP over 2017 to 2021, of which
personal income tax was 1.09. Denmark's personal income tax alone, over the same five years, was
24.66 percent of Danish GDP, which is 2.2 times Indonesia's whole tax take and 22.7 times its own
personal income tax.

## Charts

| | |
|---|---|
| `charts/tax-1-where-the-top-begins.png` | The threshold as a multiple of the average wage, 36 of the 38 OECD members, log scale. Hungary is excluded because a flat tax has no such multiple; Latvia because its 2025 threshold and rate are both reported as zero, a missing value |
| `charts/tax-2-how-the-money-is-raised.png` | Revenue by type of tax, percent of GDP |
| `charts/tax-3-what-it-buys.png` | Life expectancy, poverty, and poverty removed, each against the tax level, with and without the five lowest-income members |
| `charts/tax-4-where-the-equalising-happens.png` | Gini reduction split into the transfer-driven and tax-driven parts |

## Running it

```bash
python3 fetch_data.py       # six files, about 290 MB, from the OECD SDMX API and Our World in Data
python3 build_analysis.py   # writes results.json
python3 make_charts.py      # writes charts/
```

Every number in the essay is produced by `build_analysis.py` and read from `results.json`.
Chart labels are formatted from the three-decimal `tax_mix_raw3` fields rather than the rounded
ones, because rounding twice drifted four labels in the first version of chart 2.

## Notes on doing this honestly

The traps in these files are documented in [`data/README.md`](data/README.md), and several of them
would have produced a confidently wrong post:

- The 2022 revenue year silently drops Japan, Australia and Greece, including the OECD's
  longest-lived country from a chart about longevity. The analysis uses 2021, where all 38 members
  report every code.
- Denmark's headline tax take swings 5.5 points of GDP between two adjacent years. Its pension yield
  tax explains about 38 percent of that and nominal GDP growth most of the rest, so the tax level is
  a five-year mean rather than any single year.
- OECD's threshold factor cannot be recomputed by dividing a threshold by a wage. Danish law states
  the threshold net of the 8 percent labour market contribution, so it must be grossed up first.
  The naive division returns 1.139 instead of 1.238.
- Switzerland's transfer share exceeds 100 percent because its disposable-income Gini is published
  above its gross-income Gini. Drawn as the exception rather than smoothed away.
- Denmark replaced its single top bracket with three tiers from January 2026. OECD has published no
  2026 figure at all, so the essay uses the 2025 value, names the year, and explains the break
  rather than drawing a line across it. The reform also raised Denmark's top rate, from 55.9 to
  about 60.5 percent on OECD's basis, so it is not simply a threshold moving up the scale.
- **There is no schooling panel, on purpose.** The obvious candidate, PISA, allows up to 5 percent
  of the target population to be excluded, and sixteen systems breached that cap in 2022 led by
  Denmark at 11.6 percent. That is an upward bias on a country sitting near the top of the chart's x
  axis, so it tilts the fitted line toward showing that tax buys learning, which is the direction a
  reader of this post could least easily discount. The essay explains the absence rather than
  shipping a panel it would have to caveat into uselessness.

Written by Jonathan Chrisnaldy. Sources are OECD Tax Database, OECD Revenue Statistics, OECD
Revenue Statistics in Asia and the Pacific, the OECD Income Distribution Database, and Our World in
Data. Datasets are not committed; `fetch_data.py` reproduces them.
