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

1. **sh-1, the window I wrote about:** Bitcoin, gold and the S&P 500 indexed to 100 on 5 March 2020,
   daily, to 5 May 2020, with the 2020 draft's endpoints marked and each asset's drawdown inside
   the window.
2. **sh-2, the worst days:** mean return of Bitcoin and gold on the S&P 500's worst 5% days, with
   confidence intervals; zero marked.
3. **sh-3, every episode:** drawdown of each asset in each stress episode found by the rule.
4. **sh-4, digital gold or a tech stock:** rolling 90-trading-day correlation of Bitcoin and of gold
   with the S&P 500, 2020 to the sample end.

## 6. Data sources to vet (dataset checkpoint comes next; primary sources first)

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

(none yet)

Revision before any data was downloaded: on 2026-10-09 the owner's review replaced LQ45 with the
S&P 500 and made the scope global (no rupiah conversion, no Indonesian series, world Covid-19
cases). Sections 1 to 7 were edited in place, which the rule above allows because no data had
been downloaded.
