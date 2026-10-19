# Post 27 design: testing the fear chain after MSCI's Standalone proposal for Indonesia

Status: **pre-registration, written before any data was downloaded** (2026-10-16); approved by the
owner on 2026-10-16. Amendments are added in place under section 8 with their date and reason; nothing above
section 8 is edited after the data comes in except to mark it AMENDED with a pointer.

## 1. Origin and stance

On 15 October 2026 MSCI opened a consultation on a proposal to reclassify Indonesia from Emerging
Market to Standalone Market status, with feedback until 30 April 2027 and a decision on or before
30 June 2027. On 16 October the IHSG fell sharply, with a trading halt at the open. (These details
come from press coverage of MSCI's release; they are verified against the release itself, stored
in `sources/`, before any of them reaches the draft.)

The fear people repeat is a chain: the downgrade makes **stocks crash and stay down**, the
**rupiah weakens**, **foreign investors leave**, and the **cost of living rises**.

- **Stance:** test each link against Indonesia's own history and say which links that history
  supports. The post is not a forecast and not financial advice.
- AMENDED: see 8.5 (MSCI's documents are not quoted; press coverage is used).
- AMENDED: see 8.7 (the post is rebuilt around the family; savings, borrowing and unemployment tests are
  added; fuel is described).
- **Hook:** "Standalone" is read as "poor, corrupt, at war", because of the company it keeps. MSCI's
  own criteria are size and liquidity and market accessibility (economic development counts only
  for Developed status). The post quotes MSCI's definition from its classification page.
- **Personal angle:** my family and the prices they pay.
- **Reader:** Indonesians worried by the 16 October headlines. **Takeaway:** which fears history
  supports, which it does not, and what to watch before the June 2027 decision.
- **Close:** practical: what to worry about, what not to, and one or two signals to watch.
- **Title direction:** the family question, for example "What Should My Family Worry About If MSCI
  Drops Indonesia?"; final wording after the results.

## 2. Comparison set and its limit

AMENDED: see 8.7 (the 1997 slide in L5 and L6).

- **Indonesia's own history only** (owner decision). No other country's reclassification is used.
- **Limit, stated in the post:** no past Indonesian shock was an MSCI reclassification. The stock
  link therefore compares this fall with past falls; it does not measure what a downgrade does. The
  January 2026 MSCI freeze is the one MSCI-driven Indonesian event; it is reported separately if its
  dates and the market's reaction are verified from a stored source.
- **1997 to 1998** is shown, as the outer bound, but excluded from every verdict count: it combined a
  banking and currency crisis with the end of the managed rupiah. Each verdict is also reported with
  it included, alongside.

## 3. Shock days, fixed in advance

AMENDED: see 8.1 (monthly series and shock months replace the daily rule).

- **Data:** the IHSG daily close (source chosen at the vet).
- **Shock day:** a trading day on which the IHSG closes 7% or more below the previous close. Shock
  days within 20 trading days of an earlier one belong to that earlier day's episode.
- **Fallback, decided by count alone before any outcome is computed:** if fewer than 4 episodes
  (excluding 1997 to 1998 and October 2026) meet the 7% rule, the threshold becomes 5%.
- **Day 0** is the shock day; **"before"** is the close on the trading day before day 0.
  **Horizons:** 20, 60 and 250 trading days after day 0 (about a month, three months, a year).
- **October 2026:** day 0 is 16 October 2026. Its outcomes are reported only as far as the data
  reaches (the post's as-of date); it is never counted in a verdict.

## 4. The four links: measures and verdict rules

AMENDED: see 8.1 (horizons in months), 8.2 (L3), 8.3 (L4), 8.4 (rupiah source), 8.7 (L4's wording;
L5 to L7) and 8.8 (L7 is dropped).

**Verdict words**, from the share of past episodes (excluding 1997 to 1998 and October 2026) that meet
the link's condition, always with n: two thirds or more, **holds by my test**; one third or fewer,
**does not hold by my test**; otherwise, **mixed**.

- **L1. Stocks crash and stay down.** The crash itself is a fact for October 2026; the test is "stay
  down". Condition: the IHSG at day 250 is still below "before". Also reported: the lowest close
  within 250 days relative to "before", and the trading days until the IHSG closes back at or above
  "before".
- **L2. The rupiah weakens.** Condition: rupiah per US dollar at day 60 is at least 5% weaker than
  "before". Changes at days 20 and 250 are reported too. Episodes before the rupiah's float in
  August 1997 are excluded from L2.
- **L3. Foreign investors leave.** Condition: foreign investors are net sellers of Indonesian equities
  from day 0 to day 60 (daily exchange data), or, where only quarterly data exists, over the quarter
  of day 0 and the next. The size of that selling is reported as a share of the market's value where
  the data allows. An external estimate of index-driven selling under Standalone status is used only
  with a stored, citable source; otherwise it is omitted.
- **L4. The cost of living rises.** Its episodes are **rupiah slides**, not stock shock days: a month
  in which the rupiah is 10% or more weaker against the US dollar than three months earlier (month
  end to month end), after the August 1997 float. Slides within 12 months of an earlier one belong to
  its episode; fallback, decided by count alone: if fewer than 4 episodes (excluding 1997 to 1998)
  meet 10%, the threshold becomes 7%. Condition: consumer-price inflation over the 12 months after
  the slide starts exceeds the 12 months before it by 2 percentage points or more. Food prices are
  reported alongside if BPS publishes a consistent food series for the window. The post also reports
  whether the rupiah has made a slide by this rule since 16 October.

## 5. Charts (exactly four, each at most 2000 px on its long edge)

AMENDED: see 8.7 (the four charts are replaced) and 8.8 (chart 2 becomes the foreign-flows chart).

1. **IHSG lined up on shock days:** 100 = "before"; each past episode a thin line, 1997 to 1998 drawn
   apart, October 2026 bold up to the as-of date; days 0 to 250.
2. **Rupiah lined up on the same shock days:** 100 = "before", with the axis labelled so a higher
   line plainly means a weaker rupiah.
3. **Foreign equity net flows after each shock**, October 2026 so far marked as incomplete.
4. **Inflation before and after each rupiah slide** (12 months each side), food prices alongside if
   available.

## 6. What the post will not claim

AMENDED: see 8.7 (no asset comparisons and no instructions).

- No forecast: history gives ranges, each reported "by my test" with its n.
- No causal claim that a downgrade produces any link; the episodes are falls, not downgrades.
- No investment advice; the post carries a not-financial-advice line.
- MSCI's reasons only in MSCI's own words, quoted from the stored release.
- "Steepest since 1998" or any such ranking only if the data or a cited source shows it.

## 7. Sources and rights (each checked at the vet, before use)

AMENDED: see 8.1 to 8.5 for the sources chosen.

**Owner requirement (2026-10-16): the data must be real.** Every figure comes from a file downloaded
from its primary publisher and frozen by SHA-256, or from a stored source document with a verbatim
quote; nothing is typed from memory or from press summaries. Each series is cross-checked at the
vet against at least one independent published figure (for example, a reported IHSG close or a
BPS inflation release) before it is used.


- **MSCI:** the 15 October 2026 release and the Market Classification page, quoted and stored. MSCI
  index data is proprietary and is not used.
- **IHSG daily close:** IDX or another primary source; licence checked before download.
- **Rupiah per US dollar:** Bank Indonesia's JISDOR for recent years; an earlier daily series from a
  primary source; licence checked.
- **Foreign equity flows:** IDX statistics and Bank Indonesia's balance of payments.
- **Consumer prices:** BPS (Statistics Indonesia).
- Credits go in the post's method notes, each chart's footer and `data/README.md`; the blog is
  non-commercial.

## 8. Amendments

Amendments 8.1 to 8.6 were decided by the owner on 2026-10-17 after the source vet and before any outcome
was computed; 8.7 states its own timing. The detailed rules below were proposed by Claude and shown to the
owner with the choice.

**8.1 Stock data and the shock rule move to months.** (Its series is replaced by 8.6.) Reason: no free, licensed, long daily IHSG
series exists (IDX publishes daily closes only in patchy PDF yearbooks and bars scraping; TICMI is
paid and needs written permission for public charts; Stooq needs permission). Replaces section 3 and
the horizons in section 4:
- **Series:** OECD Financial market indicators, share prices, Indonesia (DSD_STES@DF_FINMARK, monthly,
  2015=100, from July 1997), reused with attribution. Whether each value is a monthly average or a
  month-end is taken from OECD's own metadata and stated in the post.
- **Shock month:** a month whose value is 10% or more below the previous month's. A shock month within
  3 months after an earlier one belongs to that episode. Fallback, decided by count alone: if fewer
  than 4 episodes (excluding 1997 to 1998 and October 2026) meet 10%, the threshold becomes 7%.
- **Month 0** is an episode's first shock month; **"before"** is the previous month's value.
  **Horizons:** 1, 3 and 12 months after month 0.
- **L1:** the value at month 12 is still below "before". **L2:** the rupiah at the end of month 3 is at
  least 5% weaker than at the end of the "before" month.
- **October 2026** has no monthly value yet. It is shown from IDX's daily closes (the owner downloads
  the quarter from IDX's own page with its Download button, cited with source and access date as IDX's
  terms require) and OJK's daily index; it is never counted in a verdict.

**8.2 L3 uses quarterly balance-of-payments flows for every episode.** Series: IMF Balance of Payments,
Indonesia, portfolio investment liabilities, equity and investment fund shares, net (US dollars),
from 1993 Q1 (the zeros for 1981 to 1992 are treated as missing), reused with attribution. Bank
Indonesia's SEKI Table V.7 is a cross-check only. Condition: the quarter containing month 0 and the
next quarter add up to a net outflow. October 2026 cannot be judged until the fourth-quarter data is
published; OJK's weekly foreign net buying on the exchange is shown as context only. Exchange flows
(rupiah) and balance-of-payments flows (dollars) measure different things and are never combined in
one verdict.

**8.3 L4 runs on the IMF consumer price series, with BPS alongside.** Series: IMF CPI, Indonesia,
headline, monthly, linked to BPS's 2022=100 index, reused with attribution. For each episode window,
BPS's officially published year-on-year rates are shown next to it, from BPS tables the owner
downloads by hand (BPS's site requires a human check); where the two differ, the post says so. Food:
BPS regrouped its food category more than once, so no consistent series exists and, as section 4
allows, food is not reported. The rupiah month-end for slide months is the last BIS observation in
the month.

**8.4 Rupiah source.** BIS US dollar exchange rates, daily, Indonesia (WS_XRU, D.ID.IDR.A), reused with
attribution and credited with its national sources; days after BIS's last observation are filled with
the ECB cross rate (rupiah per euro divided by dollars per euro), stated as computed. Bank Indonesia's
JISDOR is used only as a cross-check and in the text. Data quirks in the 1997 to 1998 segment are
noted in the method notes.

**8.5 MSCI's own documents stay out of the pipeline.** MSCI's terms bar use of its content with
language models without a licence, so no MSCI document is read, stored or quoted by Claude or any
fact-check agent. MSCI's announcement, dates and stated reasons are reported from press coverage
(ANTARA; the Jakarta Post's Reuters copy), attributed to those outlets; the same applies to the
definition of Standalone and the list of Standalone markets, and "Zimbabwe" appears only if such a
source confirms it. Copies of MSCI documents saved by a vet agent before this rule were deleted on
2026-10-17. This replaces the MSCI parts of sections 1 and 7.

**8.6 The stock series becomes month-end closes from 2004; the press rule tightens.** Decided by the
owner on 2026-10-17, after the provenance check and before any outcome was computed. Reason: OECD's
metadata names Singapore Yahoo Finance as the source of its Indonesian share series (OECD's terms
leave third-party rights to the user), and its monthly values are averages of daily closes. This
replaces the series in 8.1; 8.1's shock rule, horizons and conditions stand, applied to month-end
closes.
- **Series:** the IHSG month-end close. From December 2005: Bank Indonesia, SEKI Table III.3,
  credited to Bank Indonesia as its data policy (PBI 12/2024, Article 21(4)) requires. January 2004
  to November 2005: Bapepam's weekly Statistik Pasar Modal, Table 8, column Akhir (archived copies of
  Bapepam's own files), which match Bank Indonesia for December 2004 and December 2005.
- **Checks and precedence, fixed before the checks of 2006 to 2022 report:** every month is compared
  with the exchange's own publications (IDX statistics books) and with Bapepam or OJK statistics where
  they exist. Where they disagree with Bank Indonesia, the exchange's figure is used, then Bapepam's
  or OJK's. Each month's source is recorded in the data README.
- **1995 to 2003 are not used.** Bank Indonesia's older sheet disagreed with the exchange's own files in
  9 of 85 checked months and with Bapepam in 7 more, and the owner's rule was to drop it if it did
  not check out. So 1997 to 1998 appear only in the rupiah and price links.
- **Episodes** can start no earlier than February 2004, since a shock month needs the month before it.
- **Incomplete horizons:** an episode counts for a link only if that link's horizon has passed by the
  as-of date; otherwise it is reported as incomplete and not counted.
- **Preliminary values** (Bank Indonesia marks June to August 2026 with an asterisk) are used as
  published and flagged as preliminary.
- **Press:** ANTARA bars AI use in its robots file and on every article, so it is excluded; Kabar
  Bursa, IDNFinancials and France24 block Claude and are not used; MarketScreener's terms forbid even
  partial reproduction, so it is not used. Facts from the remaining outlets (the Jakarta Post's Reuters
  copy, Jakarta Globe, CNBC Indonesia, CNN Indonesia, Euronews, Fortune Indonesia, Databoks) are stated
  in the post's own words with citations and no direct quotes. Standalone markets are named only as
  these outlets name them, with attribution. Copies from the excluded outlets were deleted on
  2026-10-17. This extends 8.5.

**8.7 The post is rebuilt around the author's family; savings, borrowing and unemployment tests are added;
fuel is described.** Decided by the owner on 2026-10-17. The detailed rules were proposed by Claude,
reviewed by four independent reviewers and a completeness critic, and shown to the owner with each choice.

- **What was known when these rules were written.** Unlike 8.1 to 8.6, this amendment comes after outcomes
  were computed. The author knew every result in `results.json` (L1 to L4, including inflation over the
  twelve months after each slide, which is one side of L5), the dates of the fuel price rises found in the
  source vet (which, with L4, decide the fuel description below), and Indonesia's economic history in general
  terms (for example Bank Indonesia's rate rises in 2005 and 2008 and the jump in unemployment in 2020). The
  source vet opened Bank Indonesia's SEKI Tables I.25.A, I.26 and I.28 to check coverage, gaps and whether
  rows were equal, and reported no values; web search summaries showed it some 2005, 2006 and 2022 inflation
  figures, which it did not record. BPS table 543 was seen only through archived copies, for its rounds and
  notes. Bank Indonesia's Data Inflasi file (`data/Data Inflasi.xlsx`, SHA-256
  `5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217`, downloaded by the owner on 2026-10-17
  at 16:46 New York time) has not been read by the author: the page showed the owner, and the author's
  browser, only its ten latest months (November 2025 to August 2026), outside every window compared here,
  and a vetting agent reported only its last row, a "Desember 2002, 0,00 %" placeholder. These rules are
  fixed before their data is read, not written blind; the predictions make that checkable.
- **Predictions, before any new data is read.** `docs/2026-10-17-predictions-8.7.csv`, committed with this
  amendment, gives the author's predicted outcome for every new comparison and each new link's verdict,
  with what each prediction rests on. The build stores each prediction beside its result, and the method
  notes report how many came true.
- **L5. Savings lose buying power.** For each slide counted in L4, a one-month rupiah time deposit, rolled
  over every month with its interest added, earns less after tax over the twelve months after the slide
  month than prices rose over the same months (L4's "after" rate: the IMF index at the slide month against
  twelve months later). Return: the product over k = 0 to 11 of (1 + (1 minus the tax rate) times
  r(s + k) / 1,200), minus 1, where r(m) is SEKI Table I.28's one-month rate for all commercial banks (Bank
  Umum) in month m, in percent a year as published, read as the rate earned over month m + 1. The tax is the
  final tax on deposit interest in force in each window, from its regulation stored in `sources/` with a
  quote; small exempt balances are not modelled. The before-tax return is recorded in `data/README.md`.
  Before any value is read, what SEKI's notes say the rate is (weighted or simple; new or outstanding
  deposits; month average or month end) is recorded in the provenance audit and stated in the post. A window
  with a missing month is incomplete; provisional months are used as published and flagged. The post says
  "a one-month deposit rolled over each month", never "savings", and treats it as a hypothetical deposit,
  not the family's account. Beside the verdict: the share of all twelve-month windows, one starting in each
  month from January 2004 to the last complete one, that meet the same condition. No comparative word ("more
  often than usual") unless the slides' share exceeds that share by at least a third of it; otherwise both
  shares are printed without comparison.
- **L6. Bank borrowing gets dearer.** For each slide counted in L4, SEKI Table I.26's rupiah consumer-loan
  rate (Konsumsi, all commercial banks, as printed) in the twelfth month after the slide month is at least
  1.00 percentage point above its rate in the slide month. One point is a round number fixed before the
  table is read. What SEKI's notes say the rate is gets recorded first; if they show a change in how it is
  compiled inside a window, the episode is counted as published and flagged. The post calls it "the average
  rate banks charged on consumer loans". Beside the verdict, not a verdict: whether the policy rate at the
  end of the slide month, or of any of the three months after it, is at least 0.25 points above its rate at
  the end of the month before the slide month. Policy rate: to June 2005, the one-month SBI rate at the
  month's last auction (called that in the post, never a decision); July to September 2005, the BI Rate from
  Bank Indonesia's decision page, stored with a quote; from October 2005, SEKI Table I.25.A at month end;
  from 19 August 2016, the BI 7-day reverse repo rate, renamed BI-Rate on 21 December 2023. A comparison that
  would cross an instrument change is reported as not comparable.
- **L7. Unemployment rises.** For each IHSG shock episode, the before round is the latest February or August
  Sakernas round held in a calendar month earlier than month 0 (a round in month 0 itself is not "before");
  the after round is the same season one year later. The condition: BPS's national open unemployment rate
  (table 543, as published to two decimals) is at least 0.50 percentage points higher in the after round.
  Pairs: August 2005 shock, February 2005 and February 2006; March 2008, February 2008 and February 2009;
  September 2008, August 2008 and August 2009; March 2020, February 2020 and February 2021; February 2025,
  August 2024 and August 2025; March 2026, February 2026 and February 2027 (incomplete, not counted). No pair
  uses the 2004 round or November 2005. Where table 543 gives more than one value for a round (as published
  and backcast), both rounds of a pair use the same basis, the backcast where both have one; a pair inside a
  break with only one basis is flagged. Half a point is a round number fixed before the table is read. The
  post names each pair's rounds and says "6 to 11 months after the shock month", never "a year after"; it
  calls the link "unemployment rises", not "jobs disappear", and says the two 2008 windows overlap. Beside
  the verdict: the share of all same-season pairs from February 2006 onward that meet the same condition,
  under L5's rule for comparative words. Only Sakernas national figures are used.
- **Fuel, described, never a verdict.** Both of its inputs, L4's per-slide results and the dates of the
  rises, were known when this was written. For each slide counted in L4: every change in the government-set
  retail price of Premium gasoline or Solar diesel (the Java price where prices differed) whose effective
  date falls in the before window (the slide month and the eleven months before it) or the after window (the
  twelve months after it), with its date, product, direction and percentage change. Each change comes from
  its regulation or an official notice stored in `sources/` with a quote, extracted by script into a
  hash-pinned file. A change whose date is verified but whose prices are not is listed as "size not
  verified". The post never says a window had no change unless a stored document shows the list is
  complete; otherwise it says "among the changes I verified". Changes in a window's edge month are flagged.
  Kerosene, LPG, electricity tariffs, transport fares and Pertamax are named as not covered; the 1997 slide
  is not checked; changes outside the windows are not mentioned. The list is printed beside L4's result with
  no causal wording of the author's own; Bank Indonesia's statement that the 2005 and 2008 fuel rises caused
  inflation surges is reported with attribution.
- **L4 is worded "does inflation speed up?".** The rule is unchanged. The post says, bound to the results,
  that prices rose over the twelve months after every counted slide, and uses each slide's after rate as the
  family's figure; "inflation fell" becomes "prices rose more slowly than in the year before". L4's other
  reading in `results.json`, with the pivot at the month before the slide, is printed in Limits, and prices
  join the links where one episode changes the verdict. Food is not tested: no consistent food series exists
  (8.3), and BPS's split of inflation into parts begins in 2009, after every slide whose inflation sped up;
  Limits says so.
- **BPS's published rates (amends 8.3).** From the Data Inflasi file above: BPS's officially published
  year-on-year headline inflation, which Bank Indonesia's inflation page (Fungsi Utama, Moneter, Inflasi)
  says BPS calculates; credited to Bank Indonesia, as its data policy requires, and to BPS. For each counted
  slide, the published rate in the slide month and twelve months later is set beside L4's before and after
  rates; the post reports the largest gap in percentage points and whether L4's count would change. The
  placeholder row is excluded. The IMF series stays the measure of record; the 1997 slide is not compared.
- **Verdicts for L5 to L7** use section 4's words, from complete episodes only, excluding 1997 to 1998 and
  the open 2026 episode; a link with fewer than four complete episodes gets no verdict word. L5 and L6 use
  L4's registered slides; L4's cut-at-1998 reading is not carried over. L5 and L6 are computed for the 1997
  slide where SEKI has every month of its windows, shown apart and reported in a count including it, as
  section 2 requires; the policy-rate note marks 1997 not available. For every link, L1 to L7,
  `results.json` records whether a different outcome in one episode would change the verdict word, and the
  post says so for each link where it would. The opening and the closing name every link's verdict with its
  n, in chain order.
- **What the post prints.** First tier, in the post: each link's verdict with its n, the per-episode values
  in its chart, and one figure beside each new link (L5 and L7, the share of all windows; L6, the policy-rate
  note; L4, the published-rate comparison and the fuel list). Everything else the build emits (the
  before-tax return, other bases, other deposit terms) stays in `results.json` and `data/README.md`, and
  reaches the prose only through a later dated amendment.
- **Independent recomputation before drafting.** An agent that did not write these rules recomputes L5 to L7,
  the fuel list and the published-rate comparison from this text and the frozen files. Where a result
  differs because the text allows two readings, this text decides if it can; otherwise both readings go into
  `results.json` sensitivity and Limits, and the verdict stays on the reading committed here.
- **Sources, checks and fallbacks.** SEKI Tables I.25.A, I.26 and I.28 (direct downloads from bi.go.id,
  credited to Bank Indonesia); BPS table 543 (downloaded by the owner after this amendment is committed:
  Indonesia, every round from 2005 to the latest, all years in one export, every basis offered; the owner
  records what the screen showed); the fuel regulations (official copies). Before any download, each site's
  robots file and terms are stored and checked against the test that excluded ANTARA (bans on AI use or text
  and data mining, blocks on Claude). Each new series is checked, before any window value is read, against a
  second publication of the same figures for three months outside every window (for SEKI, the IMF's copy or
  an archived earlier edition of the table; for table 543, BPS's release for that round), within 0.05
  points; if no second publication can be found, the method notes say the series was not independently
  checked. A series that fails its check, or cannot be obtained, is dropped and its link reported as not
  tested. If L7 is dropped, chart 2 becomes the foreign-flows chart; if L5 and L6 are both dropped, chart 4
  does; if one of them is dropped, chart 4 keeps the other's panel. Only national series are used. Kompas
  bans AI use and text and data mining in its robots file and blocks Claude, so it joins the outlets
  excluded in 8.6.
- **A slide since 16 October** means a month-end from October 2026 to the as-of date at least
  `rules.slide_used` weaker than three month-ends earlier, the L4 rule as applied; until October's month-end
  exists, the latest daily rate against the end of July stands in, against the same line. The as-of date is
  the last day in the frozen rupiah files (16 October 2026). A slide found by then is an open episode, shown
  and never counted. This corrects the build's earlier test against the 10% line.
- **The post's shape.** Rebuilt around the author's family on Java (groceries, fuel, daily basics;
  retirement savings in rupiah), read from New York. Only facts the owner supplied are used; the loans and
  unemployment sections address readers. Order: opening; what Standalone means; how I tested; markets
  (stocks, the rupiah, foreign money); unemployment; prices and fuel; savings and loans; what I would tell
  my family (every link's verdict with its n, and what to watch); limits; method notes. About 2,300 words
  before the references.
- **Charts (replaces section 5).** Exactly four: (1) markets, two stacked panels, the IHSG and the rupiah
  lined up on shock months, October 2026 dotted and not counted; (2) unemployment before and after each
  shock, one column per episode; (3) inflation before and after each slide, with the fuel list in rows under
  it and no colour for fuel; (4) savings and loans, two panels, the after-tax deposit's buying power and the
  change in the consumer-loan rate for each slide. The foreign-flows chart is dropped and its figures stay
  in the text. Blue marks the latest episode, amber a link's condition met, grey everything else.
- **What the post will not do (adds to section 6).** No comparison of rupiah savings with any other asset or
  currency, and no sentence telling a reader to buy, sell, move, hold, borrow or repay. No reading of any
  link without the 2020 episode.
- **The essay's method sentence** becomes: "I wrote the first four tests before downloading any data, then
  changed their data sources and some details after checking the data but before computing any result;
  every change is dated in the pre-registration. I added the savings, borrowing and unemployment tests after
  seeing those four results. Their rules were fixed before I opened the rate and unemployment data, but not
  before I knew the broad outline of Indonesia's economic history." The README says the same.
- **October's close (amends 8.1; recorded after the closes were read, and changes no rule).** IDX's
  quarterly file for the fourth quarter of 2026 is not yet published (on 2026-10-17 its Digital
  Statistic lists 2026 to the third quarter), so the 15 and 16 October closes come from the
  exchange's IDX Daily Statistics, downloaded by the owner. Chart 1 continues the open 2026 episode
  past Bank Indonesia's last month (August 2026) with OJK's 30 September close and the 16 October
  close, drawn dotted and never counted.

**8.8 BPS's own site is excluded, and the unemployment test (L7) is dropped.** Decided by the owner on
2026-10-17, as the fallback the owner chose before the search: if no other source passed, jobs would be dropped.
- **Why.** bps.go.id's robots file names ClaudeBot with "Disallow: /" (Internet Archive copy of 7 May 2026; the
  live file sits behind a human check), the kind of block that excluded Kabar Bursa, IDNFinancials and France24
  in 8.6. BPS table 543 and BPS's releases are therefore not used. The archived copies of five BPS pages stored
  during earlier vets were moved out of `sources/` on 2026-10-17, and provenance entries that rested only on them
  are marked excluded. BPS remains the compiler of the consumer price index and of the published inflation
  rates, which reach the post through the IMF and Bank Indonesia.
- **No other source passed 8.7's tests.** ILOSTAT (CC BY 4.0) carries the ILO-harmonised measure, not BPS's,
  for 2008 to 2023 only: three of the five pairs, below the four a verdict needs. The Asian Development Bank's
  Key Indicators are annual. The Ministry of Manpower's portal starts in 2020, and the ministry's terms bar
  automated tools. Satu Data Indonesia's files sit on a private network address.
- **What changes.** L7 is reported as not tested, with this reason, in one sentence. Chart 2 becomes the
  foreign-flows chart, as 8.7 fixed. The predictions for L7 cannot be checked and are reported as such. The
  essay's method sentence names the savings and borrowing tests only.
- **The family's city.** On 2026-10-18 the owner named it: Jakarta (8.7 said Java). The essay says Jakarta; the
  fuel prices it describes for Java, Madura and Bali are the ones that apply there.
- **Disclosure.** During the search, the Ministry of Manpower's homepage showed a vetting agent one unemployment
  figure, for February 2026 (the open 2026 pair, never counted); it was not recorded.

**8.9 Round 1 corrections to the record (2026-10-17, New York time; revised after rounds 2 and 3).** None changes a
test rule or a result.
- **Length.** The rebuilt essay ran to about 2,800 words before the references, not the 2,300 that 8.7 planned,
  when the owner read it and accepted the length on 2026-10-17.
- **How the fuel list is printed.** 8.7 said each change prints with its date, product, direction and percentage
  change. Instead, chart 3 prints, for each counted slide, the number of rises and cuts in each window. The full
  list, with date, product and direction for each change, is in `docs/fuel-manifest.csv` in the post's folder.
  Edge-month flags are recorded in `results.json` and not printed.
- **Dates.** 8.8's item on the family's city is dated 2026-10-18. In New York time, which this document uses
  elsewhere, the owner named Jakarta on 2026-10-17.
- **Credits.** BPS is credited by name in the essay's credits line, as 8.7 requires for the published rates.
- **The opening** gives the six results in chain order.
- **Fuel not covered.** 8.7 names kerosene, LPG, electricity tariffs, transport fares and Pertamax as not covered;
  chart 3 names kerosene, LPG, electricity and other fuels, and transport fares are not named.
- **The method sentence.** The essay's version departs from 8.7's wording: "opened" became "read"; "every change
  is dated in the pre-registration" became "with later changes dated", in the first sentence; and the
  unemployment test is dropped with L7 (8.8). The README words it differently.
