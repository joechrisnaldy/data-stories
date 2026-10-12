# Post 26 design: re-testing my 2020 Bitcoin claim against gold and the S&P 500

Status: **pre-registration, written before any data was downloaded** (2026-10-09); approved by the
owner on 2026-10-09. Amendments are
added in place under section 8 with their date and reason; nothing above section 8 is edited after
the data comes in except to mark it AMENDED with a pointer.

## 1. Origin and stance

In 2020 I drafted a research proposal, "Pengaruh COVID-19 dan Indeks LQ45 terhadap harga Bitcoin"
(the influence of Covid-19 and the LQ45 index on the price of Bitcoin). It was never finished:
chapter 1 exists, chapters 2 and 3 are headings. Its window was 5 March to 5 May 2020 and it asked:

- **Q2020a.** Do Covid-19 (daily new cases) and the LQ45 index influence the price of Bitcoin?
- **Q2020b.** Is Bitcoin a better investment than LQ45 stocks during the pandemic?

Its background section already answered Q2020b: Bitcoin was "much more stable and tended to rise",
with "a price fall on 11 March, then a significant rise again", so during a pandemic Bitcoin was
"more promising and safer" than LQ45 stocks. The planned method was a neural network.

**Scope: global.** The re-test drops the Indonesian market. The 2020 claim is tested against the
S&P 500, the benchmark most readers know, and Covid-19 cases are world totals. The post says once,
plainly, that the 2020 draft compared Bitcoin with LQ45, so its verdict is on the general claim
("Bitcoin was steadier and safer than stocks"), not on LQ45 itself.

**Stance:** this post audits that claim publicly, whatever the data says. The hook is the dip the
2020 draft mentioned and set aside: whether "more stable" survives depends on whether you compare
two dates or look at the path between them.

**Reader:** someone who has heard that Bitcoin is "digital gold". **Takeaway:** a safe-haven test
anyone can run, and how Bitcoin and gold score on it.

## 2. Definitions fixed in advance

AMENDED: see 8.1 (sources and timing) and 8.2 (gold is monthly; two layers).

- **Assets (all priced in US dollars):** Bitcoin; gold; the S&P 500. Price indexes, not
  total-return indexes (stated in the post; dividends would favour the S&P 500 slightly).
- **Daily return:** log change in the dollar close between consecutive S&P 500 trading days.
  Bitcoin and gold are sampled at those same dates. The three prices are not taken at the same
  moment of the day (gold's benchmark price is set in London; Bitcoin never closes), so every
  worst-days result is also computed on two-day returns as a robustness check, and the post says so.
- **Safe haven, hedge** (definitions to be quoted from the source in the provenance audit, not from
  memory): the post uses the standard split in the finance literature, under which an asset is a
  *hedge* if it is uncorrelated or negatively correlated with stocks on average, and a *safe haven*
  if it is uncorrelated or negatively correlated with stocks in times of extreme market decline.
  Candidate source: Baur and Lucey (2010), to be fetched, stored and quoted before it is cited.
- **Stress episode (the rule):** on S&P 500 daily closes from 2 January 2020 to the latest available
  date, an episode runs from a running all-time-high close to the lowest close before that high is
  regained. Episodes with a peak-to-trough fall of **at least 15%** are the primary set; **at least
  10%** is the robustness set. The 5 March to 5 May 2020 window is analysed separately as the
  original paper's window, whatever the rule finds.
- **Worst days:** the S&P 500's worst 5% of daily returns over the whole sample (primary) and worst
  1% (robustness).

## 3. Measures (every number in the post comes from these)

AMENDED: see 8.2 (measures 6 and 7 added; gold leaves measures 1 to 4) and 8.3 (measure 5 weekly).

1. **Worst-days return:** for Bitcoin and gold, the mean daily return on the S&P 500's worst days,
   with its t statistic and the share of those days the asset rose. This is the safe-haven test.
2. **Average co-movement:** the correlation of daily returns with the S&P 500 over the whole sample
   (the hedge test), and a rolling correlation over 90 S&P 500 trading days for the chart.
3. **Drawdown per episode:** each asset's largest peak-to-trough fall inside each episode window, and
   the trading days it took to regain its pre-episode level (or "not regained" by the sample end).
4. **The 2020 window:** each asset's return from 5 March to 5 May 2020, its largest drawdown inside
   the window, and its daily volatility. Endpoints against path is the hook.
5. **The Covid aside (Q2020a):** correlation of Bitcoin's daily returns with the growth of world
   daily new Covid-19 cases and with the S&P 500's returns, in the 2020 window. A short section,
   with the honest reason a neural network on two months of daily data could not have answered it.

## 4. Falsification conditions (scored in the repository)

AMENDED: see 8.2 (FC2 split into FC2a daily and FC2b monthly).

- **FC1, the 2020 claim.** "Bitcoin was more stable than stocks from 5 March to 5 May 2020", tested
  against the S&P 500, survives only if Bitcoin's largest drawdown in that window is smaller than
  the S&P 500's AND its daily volatility is lower. If either fails, the post says the 2020 claim was
  wrong, in those words.
- **FC2, digital gold.** Bitcoin counts as a weak safe haven against the S&P 500 only if its mean
  return on the S&P's worst 5% days is not significantly below zero (two-sided t at 5%), and as a
  strong safe haven only if it is significantly above zero. The same test is applied to gold as the
  benchmark, and the post reports both whichever way they fall.
- **FC3, the pattern is not one crash.** Whatever FC2 finds must also hold when the 2020 crash is
  excluded; if it does not, the post says the result rests on one episode.

## 5. Charts (exactly four, prefix `sh`)

AMENDED: see 8.2.

1. **sh-1, the window I wrote about:** Bitcoin, gold and the S&P 500 indexed to 100 on 5 March 2020,
   daily, to 5 May 2020, with the 2020 draft's endpoints marked and each asset's drawdown inside
   the window.
2. **sh-2, the worst days:** mean return of Bitcoin and gold on the S&P 500's worst 5% days, with
   confidence intervals; zero marked.
3. **sh-3, every episode:** drawdown of each asset in each stress episode found by the rule.
4. **sh-4, digital gold or a tech stock:** rolling 90-trading-day correlation of Bitcoin and of gold
   with the S&P 500, 2020 to the sample end.

## 6. Data sources to vet (dataset checkpoint comes next; primary sources first)

AMENDED: see 8.1 for the sources actually used.

| Series | First choice | Fallback |
|---|---|---|
| S&P 500 daily close | FRED `SP500` | Stooq |
| Bitcoin daily close | FRED `CBBTCUSD` (Coinbase) | CoinMetrics community data |
| Gold daily price | LBMA PM price (check redistribution terms) | FRED or World Bank series if daily; else a futures or ETF series, labelled as such |
| Covid-19 daily cases, world | WHO COVID-19 dashboard data | Our World in Data |

Each is checked in the ten-minute vet before anything is built: coverage to the latest date, gaps,
holidays, units, and whether the series is the one the label says.

## 7. Out of scope, and guardrails

- Other cryptocurrencies, bonds, other stock markets (LQ45 included), currency conversion, and any
  claim about why an asset moved.
- Investment advice: the post carries a not-financial-advice line, and no sentence recommends a
  holding.
- No neural network: the post explains why the original method could not answer its own question.
- The title waits for the results so it cannot presuppose them.

## 8. Amendments

### 8.1 Data sources after the vet (2026-10-09, after the data was downloaded; APPROVED by the owner 2026-10-09)

Reason: the dataset vet (two rounds, each verdict attacked by an independent verifier working from
a fresh download) found three problems with section 6:

- FRED `CBBTCUSD` carries the next day's price under every date from 2024-09-08 to 2025-11-03,
  confirmed against Bitstamp, Coinbase and Coin Metrics. Rejected.
- No free daily gold price allows publishing derived charts: the LBMA price needs a paid licence,
  FRED's LBMA series is discontinued, and the GLD ETF archive's terms bar derivative works without
  written consent.
- WHO's daily world cases in the 2020 window are distorted by weekly reporting (a group of European
  countries report only on Sundays), and France is absent from WHO's counts for the whole window.

Owner decisions on 2026-10-09: Bitcoin from Coin Metrics; gold from the World Bank's monthly Pink
Sheet; Covid-19 cases weekly from WHO; the blog is non-commercial.

| Series | Source | What it is |
|---|---|---|
| S&P 500 | FRED `SP500` (unchanged) | Daily close, price index |
| Bitcoin | Coin Metrics Community data, `PriceUSD` | Multi-exchange reference rate fixed at 00:00 UTC at the end of the stamped day, 3 to 4 hours after the S&P 500 close; mapped to the same date with no shift |
| Gold | World Bank Commodity Price Data (the Pink Sheet), monthly | Calendar-month average of daily rates: the London afternoon fixing to May 2025, a spot rate from June 2025 |
| Covid-19 | WHO daily file, summed to WHO's reporting weeks | Weekly world new cases |

Every raw file is frozen by its SHA-256 in `data/README.md` and is not re-downloaded without a new
vet.

**Bitcoin route: (b), chosen by the owner at approval.** (a) The Community API, to the latest date, under the
CC BY-NC 4.0 statement in Coin Metrics' current API documentation. Coin Metrics' former terms of
use, no longer online, limited API data to internal use and barred use in relation to AI systems
unless a separate licence applied. Or (b) the Coin Metrics GitHub CSV, which those terms named as
permitted and which is CC BY-NC 4.0, but which ends on 23 May 2026. The two agree on every
overlapping day to within rounding (vet round 2).

### 8.2 Two layers instead of one (amends sections 2 to 5; APPROVED 2026-10-09)

Gold exists only as monthly averages, so the analysis runs at two frequencies, and gold is only
ever compared with the other assets like for like.

**Daily layer: Bitcoin against the S&P 500.** Sections 2 to 4 apply as written with gold removed:
measures 1 to 4, FC1, FC2 for Bitcoin, FC3. Because Bitcoin is sampled 3 to 4 hours after the
S&P 500 close, two-day returns are the robustness check for the hedge correlation as well as for
the worst days.

**Monthly layer: Bitcoin and gold against the S&P 500.** The monthly value of Bitcoin and of the
S&P 500 is the mean of their values on that month's S&P 500 trading days, so all three series are
monthly averages. The post says that monthly averages dampen how deep a crash month looks.

6. **Worst-months return:** the mean monthly change of Bitcoin and of gold in the S&P 500's worst
   10% of months (the lowest monthly changes, their number being 10% of the months rounded up),
   with its t statistic, 95% interval and the share of those months the asset rose; worst 20% as
   the robustness check.
7. **Monthly co-movement:** the correlation of monthly changes with the S&P 500, for Bitcoin and
   for gold, over the whole sample, and a rolling 24-month correlation for the chart.

**FC2 amended.** FC2a (daily) is FC2 as written, for Bitcoin. FC2b (monthly) applies the same rule
to Bitcoin and to gold in the S&P 500's worst 10% of months. The monthly test has few months, so
whenever an asset's 95% interval includes both zero and the S&P 500's own mean change in those
months, the post says the monthly test cannot tell, instead of reporting a pass. FC3 for the
monthly layer excludes calendar 2020.

**Gold robustness.** The World Bank's May 2025 value sits further from the London fixing average
implied by GLD's net asset value than any other month since 2020 (vet round 2), and the series
definition changed in June 2025. Every monthly gold result is also computed without the May and
June 2025 changes, and the post notes the definition change in a footnote.

**Charts (still four).**

1. **sh-1:** Bitcoin and the S&P 500 only; gold has no daily series.
2. **sh-2:** two panels: daily, Bitcoin on the S&P 500's worst 5% days; monthly, Bitcoin and gold
   in the S&P 500's worst 10% of months. Each panel prints its n.
3. **sh-3:** Bitcoin and the S&P 500 in each episode; the footnote says gold has no daily series.
4. **sh-4:** rolling 24-month correlation of monthly changes with the S&P 500, Bitcoin and gold.

### 8.3 The Covid aside, weekly (amends measure 5; APPROVED 2026-10-09)

Weekly world new cases are the sum of WHO's daily rows over WHO's reporting weeks (Monday to
Sunday); these sums reproduce WHO's own weekly world aggregate (vet round 1). Measure 5 becomes the
correlation of week-on-week log growth in world cases with weekly Bitcoin and S&P 500 log returns
(last S&P 500 trading day of one week to the last of the next), over the WHO weeks that contain
any day from 5 March to 5 May 2020. The post states the number of weeks, that France is absent
from WHO's counts in that window, and that countries' reports reach WHO up to two days late.

### 8.4 Sample end and attribution (APPROVED 2026-10-09)

- The daily layer ends on the last S&P 500 trading day with a Bitcoin value; the monthly layer ends
  with the last complete month that all three series cover.
- On the page and in the chart footers: the S&P Dow Jones Indices copyright line and the FRED
  citation, and no raw daily levels (charts show values rebased to 100, returns or drawdowns);
  Coin Metrics credited with a link to CC BY-NC 4.0 and "transformed by the author"; the World
  Bank Pink Sheet credited under CC BY 4.0 with the changes stated; WHO's own metadata citation,
  with WHO's name used nowhere else and no emblem. No wording implies endorsement by any of them.

### 8.5 Implementation notes (2026-10-09, after the first results were seen)

An independent code review checked the build against sections 2 to 8.4. One defect changed a
reported number and was fixed to match the design as written: each episode's window had run from
the high to the day it was regained, where section 2 ends it at the trough (Bitcoin's 2022 fall
moved from 67% to 61% of its high; nothing else moved). The rest are choices the design left open,
fixed here after the first results were seen, so they carry less weight than the rules above:

- The number of worst periods is the share times the number of returns, rounded up, in both layers
  (the monthly layer ranks its monthly changes, not its months).
- Two-day returns do not overlap. Days can be paired from the first or the second trading day, and
  the two pairings give different magnitudes, so every two-day check is reported for both, and the
  worst 1% of days is also checked on two-day returns (both pairings give a different verdict from
  the daily one; the post says so).
- FC3 for the daily layer drops every return that overlaps the 2020 crash episode, peak to trough,
  as section 4 says; the monthly layer drops calendar 2020, as 8.2 says. FC3 is scored in
  `results.json`.
- Monthly changes are log changes, like daily returns, and every chart and sentence says "log".
- The gold check without May and June 2025 covers every monthly gold result, the rolling
  correlation included.
- Chart sh-2 has three panels (Bitcoin daily, Bitcoin monthly, gold monthly) instead of two, so
  each panel's n matches its dots; sh-1 marks each asset's largest fall inside the window, the FC1
  measure.

### 8.6 Owner decisions at the draft review (2026-10-10)

- Title: "The Dip I Waved Away".
- S&P notice: FRED asks users to keep S&P's notice with the data. The page prints its copyright
  line verbatim and links the full notice on the FRED series page; every chart carries the
  copyright line. The owner may paste the full notice into the method notes by hand.
- World Bank gold: the workbook carries an internal "Official Use Only" sensitivity tag; the World
  Bank's commodity page links the data to CC BY 4.0, so the tag is treated as a template label.
  The credit follows the World Bank's required form, sources included.
- "Digital gold" is used as framing, attributed to no one.
- The owner asked for every chart and page surface to be checked against each publisher's terms
  before publishing; that check is a lens of fact-check round 1.

### 8.7 Corrections from fact-check round 1 (2026-10-10)

- 8.3 promised a statement that countries' reports reach WHO up to two days late. No stored source
  supports it (provenance audit), so the post does not make it.
- 8.5 said every chart and sentence says "log". In fact the method notes, the README and charts sh-2
  and sh-4 say so; the body sentences rely on the method notes.
- 8.4's rule on WHO's name is applied literally: the post names WHO only in its citation and
  reference entries, and the data README names the source only in WHO's citation form.
- The 2020 draft judged Bitcoin from its daily chart (its Figure 2), not from two dates. The post
  now says the draft's window ran from 5 March to 5 May 2020 and that the draft saw the dip and
  waved it away; it no longer says the draft compared two dates.
- The monthly layer's tests (8.2) were written after the data was downloaded; the post now says only
  the daily tests were fixed before any data.

### 8.8 Corrections from fact-check round 2 (2026-10-11)

- Round 1's fix to the recovery sentence described the regain count as the first close back at the
  high-day level; the count is to the first such close after the asset's lowest point in the
  episode, as the sh-3 footnote says. The post now says so.
- 8.7's note on "log" is narrowed: one body sentence (the volatility definition) also says "log".
- The data README now carries the World Bank credit with its sources, WHO's citation with its URL,
  licence links and the FRED series link, matching the page.

Revision before any data was downloaded: on 2026-10-09 the owner's review replaced LQ45 with the
S&P 500 and made the scope global (no rupiah conversion, no Indonesian series, world Covid-19
cases). Sections 1 to 7 were edited in place, which the rule above allows because no data had
been downloaded.
