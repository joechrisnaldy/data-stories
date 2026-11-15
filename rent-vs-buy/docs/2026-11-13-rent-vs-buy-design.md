# Post 30 design: buy, or rent and invest the difference (pre-registration)

Written 2026-11-13 (New York time), after the dataset vet and before the simulation is run, and revised the same day
after a builder check, refute-checks of this document and the owner's answers to two open questions, before it
went to the owner for approval. Section 7 lists a selection of the figures already seen during the vet.
Section 10 lists the design calls that are Claude's, not the owner's. Later changes
are added as dated amendments at the end, each with its reason.

## 1. Question and stance

The owner's request of 2026-11-13, abridged: buying a home is getting harder and more expensive, and some people may
decide a home is not necessary. Robert Kiyosaki said a home is a liability, not an asset. A home gives comfort and
security, but paying a big mortgage and fees "will feel like a jail" (the owner's words). The owner asked for buying
against renting with the fees counted, and for a simulation of someone who only rents and invests the difference in
stocks or an ETF. The owner's example: A pays $700 a month in mortgage and fees; B pays $200 in rent and invests the
other $500. What does net worth look like in the long run?

Stance (the owner's choice): lead with the owner's lean. On money alone, renting and investing the gap can beat buying,
so a house buys comfort rather than wealth. Every start year tests it, and where buying comes out ahead the post says so
plainly.

- A correction the vet asked for (listed in section 10): Kiyosaki's test is cash flow. In the column used here
  (Kiyosaki, 2016), an asset puts money in your pocket and a liability takes money out, and by that test a house is a
  liability; the same column dismisses balance-sheet net worth. The post asks a different question, which path ends with
  more wealth, and does not claim to prove or disprove the definition.
- The owner's choice (2026-11-13, "None, my view only"): the voice states the owner's view plainly, with no personal
  circumstances. House rule: not financial advice; no sentence tells a reader to buy, rent or invest.

## 2. Owner decisions so far

- 2026-11-13, brainstorm answers: country "US"; stance "Your lean, tested"; "Several stays + break-even" (who is
  ahead after 5, 10 and 30 years, and how many years a buyer had to stay before buying pulled ahead); "Every dollar +
  share to tie" (the renter invests every dollar of the gap, and the post finds the share of the gap the renter must
  invest to tie); "All costs, taxes left out" (buyer: closing costs, mortgage interest, property tax, insurance, upkeep
  and selling costs; renter: rent and fund fees; income taxes out of both sides, and the post says so).
- 2026-11-13, the playback the owner approved ("It's all good, you can proceed"), in its words: "Each start year, a
  buyer and a renter live in the same typical US home"; the same starting cash, a 20% down payment (which "avoids
  mortgage insurance") plus closing costs, which the renter invests on day one; "A 30-year fixed mortgage at that year's
  average rate, plus property tax, insurance and upkeep"; the rest of the buyer's monthly outlay goes "into the whole US
  stock market, with dividends reinvested and a small fund fee taken off"; "When rent passes the buyer's costs, the buyer
  invests the difference instead"; net worth for the buyer is "the home's value, minus the loan still owed, minus selling
  costs, plus anything invested", and for the renter the portfolio; the rent of the same home from "a published series
  of rent relative to price for owner-occupied homes". The $700 against $200 example opens the post.
- 2026-11-13, after the dataset vet, the owner answered the two questions put with the go recommendation: the rent input
  "Both, verdict where they agree" (R3, R10) and the data terms "Use with credit, I download" (the owner downloads
  Freddie Mac's survey file and the AEI-hosted workbook by hand; the post publishes figures and charts derived from them,
  never the files). Logged in `decisions/20261113-210048-...` and `decisions/20261113-210049-...`.
- 2026-11-13, two questions put with this document: the main run refinances ("Refinance in main run", R9; the approved
  playback had one fixed loan, and R15.2 runs that), and the post has no personal angle ("None, my view only"). Logged
  in `decisions/20261113-220444-...`.
- Open once results are in: the title, the closing line, the reader takeaway and the final framing.

## 3. Data

Vetted 2026-11-13 by seven finder agents, seven refuting agents and a completeness critic. In step 3 each file goes to
`data/`, pinned by sha256 in `profile_data.py`, with its definition recorded from its defining document in
`docs/provenance-audit.md`.

- **Mortgage.** Freddie Mac Primary Mortgage Market Survey (PMMS), weekly file: the US 30-year fixed rate (from
  1971-04-02) and 30-year fees and points (1971-05-28 to 2022-11-10; one point is 1% of the loan; values rounded to 0.1
  point). Through 2022-11-10 the rate is a lender's commitment rate quoted without points and fees; from 2022-11-17 it is
  an average over loan applications whose points are unknown (Freddie Mac's November 2022 research note). The owner's
  hand download. FHFA's Monthly Interest Rate Survey was the vet's cross-check only (annual means of its lender fees and
  of PMMS points correlate at 0.914 over 1972 to 2011) and is not in the build.
- **Rent of the same home, level A, "rental equivalence".** Davis, Lehnert and Martin rent-price ratio for the
  aggregate stock of owner-occupied housing, quarterly 1960Q1 to 2018Q2 (RENT-PRICE-RATIO.2018q2.xlsx, hosted by the
  AEI Housing Center; sheet 'rent-price data', column F, which follows the FHFA purchase-only index after 2000). The
  owner's hand download. After 2000Q2 the workbook chains rent and price by index ratios with no quality drift (its
  formulas in rows 165 to 236 of the data sheet); after
  2018Q2 the same method continues it with BLS owners' equivalent rent of primary residence (CUSR0000SEHC01, seasonally
  adjusted) and the FHFA purchase-only index (US, seasonally adjusted). Both are vetted in step 3 (definitions, current
  vintages against the workbook's 2018 values, the 2018Q2 splice). BLS has reweighted owners' equivalent rent every
  January since 2023.
- **Rent of the same home, level B, "national accounts".** BEA imputed rental of owner-occupied stationary homes
  (DOSTRC, NIPA Table 2.4.5U line 162; BEA's flat file through an Internet Archive capture) over the Federal Reserve Z.1
  value of households' owner-occupied real estate excluding vacant land and mobile homes (FL155035013), annual. From 2005
  BEA estimates this rent by rental equivalence paired with an owner premium, which raised aggregate owner imputed rent
  by 35% to 40% in 2005 to 2019; 2002 to 2004 are interpolated between methods; before 2002 the level rests on BEA's
  older rent-to-value benchmark (NIPA Handbook, chapter 5, for the owner premium; Survey of Current Business, May 2021,
  for the rest). The 2023 update
  changed how utilities are removed from 2013, and Z.1 values come from Zillow estimates times ACS housing counts from
  2001.
- **Home value.** FHFA House Price Index, all-transactions, US, quarterly, not seasonally adjusted, 1975Q1 to 2026Q2.
  For 1972 to 1974, the Census constant-quality (Laspeyres) price index of new single-family houses sold, annual,
  interpolated to quarters (R2). For R15.3, the FHFA purchase-only index, US, not seasonally adjusted, from 1991.
- **Stocks.** Kenneth R. French Data Library, Fama/French 3 Factors, monthly: market return = Mkt-RF + RF,
  value-weighted, dividends reinvested. The archived cut of the September 2026 update (data through August 2026), so a
  reader can download the same file. Through December 1972 the market covers NYSE and AMEX stocks only; NASDAQ stocks
  enter in January 1973 (CRSP's NASDAQ data begin on 1972-12-14).
- **Fund fee.** Investment Company Institute (ICI, http://www.ici.org), Trends in the Expenses and Fees of Funds, 2025: asset-weighted average expense ratio of index
  equity mutual funds, 1996 to 2025. Vanguard: First Index Investment Trust, now the Vanguard 500 Index Fund, launched on
  1976-08-31 (Vanguard's press release on the fund's 50th anniversary), with a first expense ratio of 0.43% (Vanguard's
  "50 years. 50 facts.", fact 38).
- **Property tax.** Census owner surveys: the Annual Housing Survey, 1973 to 1983 (mean real estate taxes per $1,000
  value); the American Housing Survey, 1985 to 2003, odd years (median per $1,000 value); the ACS 1-year, 2005 to 2025
  (aggregate real estate taxes over aggregate value of owner-occupied units), and ACS medians by mortgage status (B25103)
  for R15. Read during the vet: AHS 1975, 1980 and 2005, ACS 2021 to 2025; the rest are read in step 3.
- **Insurance.** The NAIC homeowners reports for data years 2021 to 2023 (countrywide average HO-3 premium; all three
  read during the vet) over the ACS median value (B25077); the AHS 2005 national median monthly property insurance
  payment over the ACS 2005 median value; for R15.5, NAIC 2023 owner-occupied premiums over the ACS 2023 aggregate value.
- **Upkeep and depreciation.** BEA owner-occupied housing accounts over Z.1 households' owner-occupied real estate
  including vacant land and mobile homes (LM155035015): intermediate inputs (routine upkeep), residential improvements
  (A946RC, all tenures), and consumption of fixed capital (B2607C, bridge years only), with an owner-occupied share of
  the residential net stock from BEA's fixed-asset tables by tenure (vetted in step 3). For R15.5, AHS 2023 routine
  maintenance over the AHS mean value.
- **Buying and selling costs.** CFPB, 2023 Mortgage Market Activity and Trends (HMDA), Tables 3A and 3D: median loan
  amount and median total loan costs of conventional conforming home-purchase loans, 2018 to 2023. Selling: Hsieh and
  Moretti (2003), median total selling expenses of 6.1% from the Consumer Expenditure Survey, 1980 to 1998; Banerjee and
  Paciorek (2025), a Federal Reserve FEDS Note on buyer-agent commissions. REAL Trends commission rates (through FTC and
  DOJ, 2007) were seen during the vet and are not used in the post.
- **CPI series for R15.1.** CPI-U rent of primary residence (CUUR0000SEHA) and owners' equivalent rent of primary
  residence (CUUR0000SEHC01), not seasonally adjusted, from BLS's LABSTAT file through an Internet Archive capture.
- **Dollars for chart 2.** The Census 2000 median value of specified owner-occupied homes, read by `profile_data.py` from
  Post 29's stored `census_coh_values_unadj.txt` (line 5), and the R-CPI-U-RS file stored for Post 29.
- **Text sources.** Kiyosaki (2016), the Entrepreneur column; Rappaport (2010) and Cox and Followill (2018), read in full;
  Beracha and Johnson (2012) and Beracha, Skiba and Johnson (2017), abstracts only; Davis, Lehnert and Martin (2008);
  Freddie Mac's November 2022 PMMS research note; BEA's NIPA Handbook, chapters 5 and 12; the Survey of Current Business
  articles of May 2021 (BEA's housing services method) and November 2023 (the utilities change from 2013); the Federal
  Reserve's Financial Accounts Guide entry for FL155035013 (Z.1 values from 2001); BLS's R-CPI-U-RS homepage (a
  research series with no rent component) and its table of method changes (through Internet Archive capture
  20260819055434: the 1985, 1988 and 1995 changes, the 1999 error and the 1987 to 1994 drift); BLS's Beyond the
  Numbers article of 2014 (the CPI before 1978), the CPI chapter of its Handbook of Methods, the Monthly Labor Review
  article of June 1999, a 2005 paper for the Federal Economic Statistics Advisory Committee (FESAC), and BLS's notice on
  the yearly OER weights from 2023 (the limits in
  R15.1 and section 8); CRSP's US Stock Databases page (exchange coverage); Vanguard's press release on the fund's 50th
  anniversary and its "50 years. 50 facts." The post ends with an APA 7 reference list covering every data and text
  source it uses.
- Not used: FRED; FHFA's Monthly Interest Rate Survey (above); the Jordà-Schularick-Taylor rental yield (a net yield on
  an investor benchmark); Shiller's stock file (a cross-check during the vet); Freddie Mac's Conventional Mortgage Home
  Price Index, a lead for the 1970s price bridge that was not vetted (a thin 1970 to 1974 sample, history revised in every
  release, Freddie Mac's data terms; only a 2003 archived release was found, and its successor was not checked). The
  new-house bridge with depreciation (R2) was chosen instead, as was a 1972 start rather than the critic's 1978.

## 4. Rules fixed before the simulation is run

- **R1 Timeline and start years.**
  - The model runs monthly. Month 1 is January of the start year S. Payments, rent and new investments happen at the
    end of each month; the day-one investment is made at the start of month 1.
  - Start years S = 1972 to 2025. A result is measured at the end of a December after h whole years (h = 1 to 30),
    and never after December 2025.
  - The reported stays are 5, 10 and 30 years (start years 1972 to 2021, 1972 to 2016 and 1972 to 1996). Chart 3
    shows every h.
  - A quarterly series gives each month its quarter's value; an annual series gives each month its year's value; a
    weekly PMMS value is averaged over the weeks dated in the year or month a rule names.
  - Units: PMMS rates, PMMS points and ICI fees are published in percent, and so are the French returns. In the rules,
    a rate enters as i = the PMMS rate / 100, a fee as f = the ICI value / 100, points as p / 100 of the loan, and a
    market return as (Mkt-RF + RF) / 100. AHS taxes per $1,000 of value are divided by 1,000, and CFPB loan amounts,
    published in thousands of dollars, are multiplied by 1,000 before any division. Every other ratio (k, c_np, tau,
    iota, u, d) is a decimal share.
  - Start years 1972 to 1976 are labeled wherever they appear, for their substitute inputs: the 1972 to 1974 home value
    comes from the new-house bridge (R2); through December 1972 the market return covers NYSE and AMEX stocks only;
    1972's property tax takes the 1973 value (R7a); and no S&P 500 index fund was open to individual investors before
    31 August 1976 (Vanguard), so those start years invest in a portfolio no individual could buy. For some years after
    that, the only broad index fund an individual could buy tracked the S&P 500, not the whole market (the first
    whole-market fund for individuals is not dated here).
  - Headline counts are reported for all start years and again for start years from 1977.
- **R2 The home and its value.**
  - The home costs P0 = 1 at purchase. Every result is a ratio or a share, so the price level does not matter; dollars
    appear only in R14.
  - Its value in month t is V(t) = [J(q(t)) / J(q0)] x D(t), where q(t) is the quarter of month t, q0 is the first
    quarter of S, and D(t) is the product of (1 - d(y)/12) over the bridge months before month t (months up to December
    1974, y the month's year). D(1) = 1, and D stays fixed from January 1975.
  - J is the FHFA all-transactions index from 1975Q1. Before 1975, J(q) = FHFA(1975Q1) x C(q) / C(1975Q1), with C the
    Census constant-quality index of new houses: its annual values placed at mid-year and interpolated log-linearly to
    each quarter's midpoint, so a bridge year's growth is spread over its quarters rather than arriving in one step.
  - d(y) = BEA owner-occupied consumption of fixed capital (B2607C) / the mean of the four quarter-end values of Z.1
    LM155035015 in year y. (Section 7's 1.49% used the mean of two year-end values.)
  - Why: C prices new houses, which do not age. From 1975 the repeat-sales index reflects aging, so no depreciation is
    charged after 1974.
- **R3 The rent of the same home.**
  - Rent in month t is r(t) = k(t) x V(t) / 12, where k is the annual rent-to-price ratio. This assumes the aggregate
    ratio applies to this home: the rent level and its path come from one ratio and one value index.
  - Level A: k_A(q) = DLM column F for quarters up to 2018Q2. After that, k_A(q) = k_A(2018Q2) x [OER(q) /
    OER(2018Q2)] / [PO(q) / PO(2018Q2)], where OER(q) is the mean of the monthly CUSR0000SEHC01 values in q (a month
    BLS did not publish, such as October 2025, is skipped) and PO is the FHFA purchase-only index, US, seasonally
    adjusted, both in the vintages frozen in step 3.
  - Level B: k_B(y) = DOSTRC(y) / the mean of the four quarter-end values of FL155035013 in year y. DOWNRC over
    LM155035015 is recorded as a scope check only.
  - Both levels are value-weighted ratios for the owner-occupied stock (section 8). Level B's scope is close, not
    exact: its rent is nonfarm (DOSTRC), while its value (FL155035013) also counts farm houses, second homes that are
    not rented and vacant homes for sale (Z.1 table S14.b, note 2).
  - Every simulation runs once under each level.
  - Check: the build tests whether k_A < k_B in every month from 1972 to 2025. If so, it asserts that the renter's
    net worth minus the buyer's is higher under A than under B in every cell, since a lower rent can only help the
    renter.
- **R4 The mortgage.**
  - Loan L0 = 0.80 (80% of the price), 30 years, fixed rate i0 = the mean PMMS 30-year rate over all weeks dated in year
    S, divided by 100: "that year's average rate", as approved. It includes weeks after the January purchase.
  - Monthly payment m = B x (i/12) / (1 - (1 + i/12)^(-n)), with B the balance and n the months left; each month the
    balance grows by i/12 and falls by the payment. After month 360 the payment is zero.
  - Points at purchase, p0 = the mean PMMS 30-year fees and points over the weeks dated in year S that carry a value.
    For years with none (from 2023), p_fix = the mean of all weekly values dated 2018 to 2022, the window R5 uses.
- **R5 Buying costs.** Paid by the buyer at purchase; the renter invests the same amount on day one.
  - K_buy = (p0 / 100 + c_np) x L0.
  - c_np, the loan's other costs as a share of the loan: the mean over 2018 to 2022 of the CFPB median total loan
    costs over the median loan amount (conventional conforming home-purchase loans), minus the mean PMMS 30-year fees
    and points over the weeks dated 2018 to 2022, as a share of the loan. One constant for every year. The two CFPB
    medians may come from slightly different sets of loans, since some lenders need not report loan costs.
  - Transfer taxes and the owner's title policy are assigned to the seller's 6% (R6). The buyer's recording fees, which
    have no national source, are left out of the main run; the high-cost run (R15.6) adds 1% of the price for them.
- **R6 Selling costs.** 6% of V at the sale and at every year-end valuation: total selling expenses, after Hsieh and
  Moretti's 6.1% median (1980 to 1998). Since August 2024 part of the commission may move to buyers (Banerjee and
  Paciorek, 2025); the low-cost run's 5% (R15.5) stands in for that.
- **R7 Carrying costs.** Each month the buyer pays (tau(y) + iota(y) + u(y)) x V(t) / 12.
  - R7a Property tax tau(y), the share of value owners report paying:
    - 1973 to 1983: Annual Housing Survey, H150 Part C, Table A-1, United States, specified owner-occupied units,
      "real estate taxes last year, mean (per $1,000 value)", total column, over 1,000, assigned to the survey year
      (for 1973 the same row, column and universe sit in Table A-2 of the volume, printed p. 22).
    - 1985 to 2003, odd years: American Housing Survey national tables, median real estate taxes per $1,000 value, over
      1,000, assigned to the survey year.
    - 2010 to 2025: ACS 1-year, aggregate real estate taxes paid (B25090) over aggregate value (B25082),
      owner-occupied units, United States. B25090 is not in the 1-year summary files before 2010, so 2005 to 2009 use
      the ACS ratio of medians, median real estate taxes paid (B25103_001) over median value (B25077_001), read from the
      same files; the build prints both measures for 2010 to 2019 as a check (A2).
    - Years with no survey value (1982, when no national survey was run; 1984; the even years 1986 to 2004; 2020; and
      any table that cannot be read in step 3)
      are filled by a straight line between the nearest years with values; 1972 takes the 1973 value. The vet proposed
      shaping the gaps with BEA's owner property-tax series; a straight line is used because each gap is a single year
      and BEA splits property taxes between owners and tenants partly by "judgmental trends" (NIPA Handbook, chapter
      12).
  - R7b Insurance iota(y):
    - iota_2005 = 12 x the AHS 2005 national median monthly property insurance payment / the ACS 2005 median value
      (B25077).
    - iota_late = the mean over data years 2021 to 2023 of the NAIC countrywide average HO-3 premium over that year's
      ACS median value.
    - iota(y) = iota_2005 up to 2005, a straight line from iota_2005 in 2005 to iota_late in 2022, and iota_late after.
  - R7c Upkeep u(y) = routine(y) + improvements(y), each over the mean of the four quarter-end values of Z.1
    LM155035015 in year y:
    - routine(y) = (DOWNRC - B1300C) + W307RC - W316RC: BEA's intermediate inputs of nonfarm owner-occupied housing
      (DOWNRC - B1300C), net of borrower services (W307RC, recorded as a negative) and premium supplements (W316RC);
      the vet's construction, confirmed against BEA's definitions in step 3.
    - improvements(y) = NIPA residential improvements (A946RC, private, all tenures) x the owner-occupied share of the
      private current-cost net stock of residential fixed assets: BEA Fixed Assets Table 5.1, line 11 (owner-occupied)
      over line 2 (private), year-end of year y. The pinned table is BEA's 2024 vintage and ends in 2023, so 2024 and
      2025 hold the 2023 share (A2).
    - Improvements are charged from January 1975 only: the repeat-sales index includes what owners' improvements add to
      a home's value, and the bridge's new-house index does not.
- **R8 The renter, the buyer's own investing, and the fund.**
  - Day one: the renter invests 0.20 + K_buy, the cash the buyer paid at closing.
  - Each month: the buyer's outlay O(t) = the mortgage payment + carrying costs (R7) + any refinancing cost that month
    (R9). The renter pays r(t). If O(t) > r(t), the renter invests the difference; if r(t) > O(t), the buyer invests
    the difference in the same fund. Each month both households spend the same on housing plus investing.
  - Fund: each month a balance earns R(t) = (Mkt-RF + RF) / 100 - f(y) / 12, then the month's investment is added.
    f(y) is the ICI index equity mutual fund average for y (1996 to 2025) divided by 100, so 0.27 becomes 0.0027; 1972
    to 1995 take the 1996 value.
  - No income taxes on either side, no costs to sell fund shares, no cash buffer, and no renter's insurance or security
    deposit (the owner's cost list for the renter: "rent and fund fees").
- **R9 Refinancing** (proposed by Claude; the owner chose it for the main run on 2026-11-13; R15.2 runs without it).
  - At the end of month t the buyer refinances when all three hold: at least 12 months have passed since the purchase
    or the last refinancing; at least 60 months of the loan remain; and the month's mean PMMS 30-year rate is at least
    1.00 percentage point below the loan's current rate.
  - The new rate is that month's mean, the payoff date stays the same, and the new payment follows R4's formula.
  - Cost: (p / 100 + c_np) x the balance, with p the mean PMMS fees and points over the month's weeks that carry a
    value, and p_fix for any month with none (from December 2022), paid that month as part of O(t). The cost is the
    same in every run.
  - Why: the 30-year rate fell from double digits in the early 1980s, and a buyer who kept a loan at that rate for 30
    years would be an unfair stand-in for buyers. The one-point threshold is a rule of thumb.
- **R10 Net worth and verdicts.**
  - After h years (the end of December of S + h - 1): the buyer's net worth = V x (1 - 0.06) - the loan balance + the
    buyer's fund; the renter's net worth = the renter's fund.
  - Under each level, buying is ahead if the buyer's net worth is higher, and renting is ahead if the renter's is.
  - The verdict for (S, h) is "buy" if buying is ahead under both levels, "rent" if renting is ahead under both, and
    "depends on the rent" otherwise.
  - Headline: for 5, 10 and 30 years, the number of start years with each verdict, for all start years and for start
    years from 1977. The build also emits, for every cell and level, the renter's net worth as a multiple of the
    buyer's.
- **R11 Break-even.**
  - For each S and level: the first h within the data at which buying is ahead, and whether it stays ahead at every
    later year-end within the data; "not within the data" if never.
  - The agreed break-even is the first h with the verdict "buy".
- **R12 Share of the gap to tie.**
  - For each S with a 10-year or 30-year history, each level, and h = 10 and 30: the share s of each monthly gap the
    renter invests at which the two net worths are equal. The day-one sum is always invested in full, and the buyer's
    side does not change with s.
  - The renter's fund is linear in s, so s = (NW_B - W_R(0)) / (W_R(1) - W_R(0)), with W_R(x) the renter's fund when
    a share x of each gap is invested.
  - If s > 1: "cannot tie". If s <= 0: 0%, the day-one sum alone ties or wins. If the renter never has a positive gap:
    "no gap".
- **R13 The monthly split** (chart 1, and the opening example). For each S and level, the month-1 rent as a percent of
  the buyer's month-1 outlay (mortgage payment plus carrying costs), with V(1) = 1. The owner's example is 200 / 700 =
  2/7, about 28.6%.
- **R14 One household in dollars** (chart 2).
  - Start year 1996, the latest with a full 30-year history to December 2025.
  - Price: the Census 2000 median value of specified owner-occupied homes (section 3) x FHFA(1996Q1) / the mean of
    FHFA's four 2000 quarters.
  - Net worth of the buyer and the renter at each December from 1996 to 2025, under both levels, in 2025 dollars with
    the R-CPI-U-RS annual averages as published in the stored file (for 2025, its printed annual average). The chart
    applies the aggregate rent ratios to a median-priced home (section 8).
- **R15 Sensitivities.** Each reruns everything and reports the verdict counts at 5, 10 and 30 years and the number of
  cells whose verdict changes.
  1. Rent path from the CPI: the month-1 rent from R3, then grown with CPI-U rent of primary residence (CUUR0000SEHA)
     through December 1982 and owners' equivalent rent of primary residence (CUUR0000SEHC01) from January 1983, chained.
     October 2025 is skipped (November chains to September). Before 1978 BLS's rent index is its wage-earner (CPI-W)
     index rescaled, so start years 1972 to 1977 cross a population and sample break in January 1978; they are kept,
     with the break stated. BLS's index left out aging before 1988 (0.1 to 0.2 percent a year in the BLS Handbook, about
     0.3 percent in other BLS papers); no adjustment is made. BLS also changed the rent method in 1985 (vacancy
     imputation) and 1995 (a new estimator; BLS says the old one underestimated price changes), and both indexes carry a
     1999 error in their calculation; owners' equivalent rent drifted upward over 1987 to 1994 by BLS's account, and its
     estimator changed in 1987, 1995, 1999 and 2023. BLS carries the 1985, 1988 and 1995 changes back to 1978, and
     corrects the 1999 error and the 1987 to 1994 drift, only inside its research series (R-CPI-U-RS: all items, and all
     items less food and energy), which has no rent component.
     From 1988 the CPI path is adjusted for aging while the FHFA value is not.
  2. No refinancing: every buyer keeps the start year's rate for the whole stay.
  3. FHFA purchase-only (US, not seasonally adjusted) in place of all-transactions from 1991Q1, chained, for the value
     and so for the rent.
  4. Fund fee 0.43% for 1972 to 1995 (the Vanguard 500 Index Fund's first expense ratio); and, separately, no fee.
  5. Owner costs low: property tax times the ACS 2025 ratio of the median tax of owners without a mortgage to that of
     all owners (B25103); insurance 0.32%, NAIC 2023 owner-occupied premiums (the sum of the HO-1, HO-2, HO-3, HO-5 and
     HO-8 total written premiums in NAIC's Table 4, dwelling fire left out) over the ACS 2023 aggregate value; routine
     upkeep 0.29%, AHS 2023 routine maintenance over the AHS mean value, and no improvements; buying costs 1% of the
     price; selling 5%.
  6. Owner costs high: property tax times the ACS 2025 ratio for owners with a mortgage; insurance at R7b's 2023 ratio,
     the NAIC countrywide average HO-3 premium over the ACS 2023 median value (the highest of iota_late's three data
     years), throughout; upkeep with the improvements share set to 1; buying costs plus 1% of the price; selling 7%.
  - The vet proposed a property-tax band spanned each year by the survey series and BEA's owner tax series (BEA's series
    is the lower one from 2005 and slightly higher in 1975), with the top raised 10% (about the ACS with-mortgage ratio).
    Both runs instead scale the survey series alone, by the ACS without-mortgage and with-mortgage ratios, because BEA's
    owner tax rate on the Z.1 value base runs 36% to 41% below the rate owners report in 2021 to 2025 and rests on the
    modeled split named in R7a. So from 2005 the low run stays a quarter to a half above BEA's rate, the vet's floor, and
    in 1975 the high run sits below the vet's top.
- **R16 Text.**
  - Kiyosaki: a fragment of the fourth sentence of the column's definitions paragraph ("your house is not an asset, but
    rather a liability"), matched against the stored copy; never the fifth sentence, which holds an em dash. With the
    scope note of section 1.
  - Prior research, with how each design differs from this post's: Rappaport (2010), read in full: national data, an
    identical house, ten-year stays starting 1970 to 1999, income taxes, and a renter who invests all in stocks or all in
    bonds. Cox and Followill (2018), read in full: six metro areas, one start in 1984 for each, nominal dollars, federal
    tax rates of 15% and 28% (the counts quoted are at 15%), owners who deduct mortgage interest and property tax, a
    renter holding half stocks and half bonds (all stocks as a check), and the rent of a four-bedroom apartment against a
    three-bedroom house.
    Beracha and Johnson (2012) and Beracha, Skiba and Johnson (2017): abstract-level findings only, with no design
    details.
  - Income taxes: left out of both sides, and the post says that Cox and Followill (2018) found higher tax brackets
    favored buying.

## 5. Charts (four)

1. `rb-1-monthly-split`: the month-1 rent as a percent of the buyer's month-1 outlay, by start year 1972 to 2025, one
   line per rent level, with a reference line at 2/7 labeled with the owner's example; start years 1972 to 1976 marked,
   and level A for start years 2019 to 2025 marked as resting on the extension (R3).
2. `rb-2-one-household`: net worth of the 1996 buyer and renter, December 1996 to December 2025, in 2025 dollars, under
   both rent levels.
3. `rb-3-who-is-ahead`: start year across, years held up; each cell "buy", "rent" or "depends on the rent"; the rows
   for 5, 10 and 30 years marked, and start years 1972 to 1976 marked.
4. `rb-4-share-to-tie`: the share of the monthly gap the renter must invest to tie after 30 years, by start year 1972
   to 1996, one line per rent level; start years 1972 to 1976 marked; "0%" drawn at zero; "cannot tie" and "no gap"
   marked as such.

## 6. Predictions (written before the simulation is run)

No buy-versus-rent result for this model was computed before these were written. They rest on the inputs seen during
the vet (section 7) and on Rappaport (2010), and they are scored on the main run, per rent level where a level is named.

- P1. Under level B, the month-1 rent is more than 2/7 of the buyer's month-1 outlay in every start year from 1972 to
  2025; under level A, in at least 45 of the 54. Under each level, the lowest share falls in a start year from 1979 to
  1985.
- P2. At 5 years, the verdict is "rent" in more than half of the start years 1972 to 2021.
- P3. At 10 years, the verdict is "buy" in most start years from 1972 to 1976 and "rent" in most from 1980 to 1989.
- P4. At 30 years, the verdict is "rent" in more than half of the start years 1972 to 1996.
- P5. Across the start years with at least 10 years of data (1972 to 2016), the median agreed break-even is longer
  than 5 years, counting "not within the data" as longer.
- P6. Under level A, in at least half of the start years whose 30-year verdict is "rent", the renter ties by investing
  less than half of the monthly gap.
- P7. "Depends on the rent" is the verdict in at least a fifth of the start years at 10 years.

## 7. Already seen during the vet (a selection; not predictions)

- PMMS 30-year rate: 7.33% in the first week (1971-04-02) and 7.11% on 2026-11-12; weekly values from 12.175% to
  16.025% among the 1980 weeks shown in the vet. Freddie Mac's discontinued annual averages: 7.38% (1972), 8.04% (1973),
  9.19% (1974), 9.05% (1975), 8.87% (1976), 8.85% (1977), 3.94% (2019), 3.11% (2020), 2.96% (2021); fees and points 0.9
  (1972) and 0.53, 0.74 and 0.69 (2019 to 2021).
- Rent-to-price, level A (annual means of the quarters): 5.60% (1960), 5.78% (1970), 4.88% (1980), 4.84% (1990),
  4.63% (2000), 3.60% (2005), 3.52% (2006), 4.52% (2010), 4.06% (2017). Level B: 7.10% (1960), 7.45% (1970), 6.64%
  (1980), 6.08% (1990), 6.51% (2000), 4.63% (2005), 4.58% (2006), 6.65% (2010), 5.89% (2017), 5.73% (2018), 5.26%
  (2025). Checks that are not inputs: Consumer Expenditure Survey owner reports, 7.27% (1990), 8.18% (2000), 6.57%
  (2010), 6.56% (2017), 6.15% (2023) and 6.01% (2024); the ACS single-family bracket, 4.32% to 5.05% (2017); the
  Jordà-Schularick-Taylor net yield, 4.57% (2017).
- DLM's Table 2 (`sources/dlm_roiw_2008-13.txt`): census net rents against the BLS rent index, and census average
  prices against Freddie Mac's repeat-sales index, decade by decade.
- Property tax: 1.5% (AHS 1975), 1.1% (AHS 1980), a 0.9% median (AHS 2005); 0.89% to 0.98% (ACS 2021 to 2025);
  0.54% to 0.57% on the BEA and Z.1 basis (2022 to 2025), which R7a does not use.
- Insurance: 0.501%, 0.489% and 0.511% (NAIC HO-3 premium over the ACS median value, 2021 to 2023); 0.470% for the
  median-coverage band (2023); about 0.37% (AHS 2005 over the ACS 2005 median value); 0.320% (NAIC 2023 owner-occupied
  premiums over the ACS 2023 aggregate value).
- Upkeep: the BEA routine line averaged 0.62% of value in 1970 to 2025 (0.40% to 0.93%; 0.43% in 2025); residential
  improvements of all tenures averaged 0.946% of owner-occupied value (0.739% to 1.300%; 0.894% in 2025); AHS 2023
  routine maintenance, 0.29% of mean value. Depreciation: BEA consumption of fixed capital over Z.1, mean 1.49%
  (1.28% to 1.74%).
- Stocks, 1971 to 2025 annualized: 11.26% (French) and 11.17% (Shiller).
- Fund fees: index equity mutual funds 0.27% (1996) and 0.05% (2025); index equity ETFs 0.28% (2005) and 0.14% (2025);
  the Vanguard 500 Index Fund's first expense ratio 0.43%.
- Buying costs: HMDA conventional conforming total loan costs 1.58%, 1.56%, 1.50%, 1.41%, 1.59% and 1.75% of the loan
  (2018 to 2023, ratios of medians); FHFA MIRS lender fees 1.4% to 2.6% of the loan (1979 to 1987) and 0.3% to 0.5%
  (2001 to 2008).
- Selling costs: a 6.1% median of total selling expenses (CEX, 1980 to 1998); buyer-agent offers of about 3% (late
  1990s) to about 2.7% (2023). REAL Trends average commissions were also seen; the post does not use them.
- Prior results. Rappaport (2010), ten-year stays starting 1970 to 1999, with income taxes: owning built more wealth
  than renting and investing in either stocks or bonds for slightly more than half of the stays, mostly those starting in
  the early and mid-1970s and most of the 1990s; renting and investing in stocks built more for a quarter, all starting
  in the 1980s; the remaining quarter was unclear, because rent and price are hard to measure for identical houses. Cox
  and Followill (2018), six metro areas from 1984 at a 15% federal tax rate: renting won five of six markets over 8 to 12
  years and three of six over 30. Beracha and Johnson (2012), abstract: renting and investing beat buying over most of
  their window at a typical holding period. Beracha, Skiba and Johnson (2017), abstract: households that do not
  reinvest the cash-flow difference accumulate less wealth.

## 8. Limits stated in the post

- One national home on the national price index. Cox and Followill (2018) used six metro areas and found the answer
  depended on place; Rappaport (2010) used national data, as this post does.
- The rent of the same home is uncertain. Level B runs about a quarter to a half above level A in the years checked,
  and the "depends on the rent" verdict says so. Both levels are value-weighted ratios for the whole owner-occupied
  stock, and they probably understate the ratio for a median-priced home, which leans the result toward renting (chart
  2 applies them to a median-priced home). The academic ratio prices owners' homes partly from apartments; the national
  accounts add BEA's owner premium from 2005, rest on an older rent-to-value benchmark before 2002, and carry method
  breaks in 2002 to 2005 and 2013 and Z.1's switch to Zillow-based values in 2001. Level A after 2018Q2 is an index
  extension, with owners' equivalent rent reweighted every January from 2023.
- The rent is an aggregate ratio times the home's value. After 2000, level A's rent grows like a home that does not age
  (owners' equivalent rent is adjusted for aging) while the value follows homes that do (the FHFA index is not), which
  leans slightly toward buying.
- Income taxes are left out of both sides (R16). The model treats future rent as known, so it puts no value on owning
  as a hedge against rising rents, which leans toward renting.
- The renter invests every dollar of the gap in the main run; the share to tie shows how much discipline a result
  needs.
- PMMS describes a prime borrower with 20% down. From 2022-11-17 it averages loan applications whose points are unknown,
  so adding p_fix may count some points twice, or miss some, for purchases from 2023 and refinancings from December
  2022. The year's
  average rate includes weeks after the January purchase. The refinancing rule is a rule of thumb; R15.2 runs without
  it, where a start year with a high rate keeps that rate, which leans toward renting.
- Property tax is the average rate owners report, applied to current value. The series splices AHS means (1973 to 1983),
  AHS medians (1985 to 2003), ACS medians (2005 to 2009) and ACS aggregates (2010 to 2025), all on owner-estimated
  values, and the universes change: the AHS means cover specified one-family or one-unit homes (no condominiums,
  cooperatives or mobile homes), and the AHS medians cover all owner-occupied units, mobile homes included.
- Insurance before 2006 rests on the AHS 2005 median among owners who pay property insurance, not all owners; the NAIC
  owner-occupied forms leave out condominium-unit policies. CPI rents for October 2025 were carried forward by BLS, so
  the November and December 2025 index levels sit about a month of growth low.
- Insurance from 2022 is the mean of the 2021 to 2023 ratios of the average premium to the median value; 2006 to 2021
  follow a straight line from the AHS 2005 reading, which is held back to 1972. The BEA routine upkeep line also holds some insurance,
  closing costs, brokers' commissions on land and loan fees that R5, R6 and R7b charge too. The cost rates rest on
  different value measures (owner reports for tax and insurance, Z.1 market value for upkeep). The low and high runs
  (R15) bracket the vet's ranges for insurance and upkeep; for property tax both runs scale the survey series by the ACS
  mortgage-status ratios instead of using BEA's series, so from 2005 the low run stays a quarter to a half above BEA's
  rate (the vet's floor), and in 1975 the high run sits below the vet's top (R15).
- The loan's other costs are a 2018 to 2022 share carried back to 1972; fixed-dollar fees were a larger share of
  smaller loans. The buyer's recording fees are left out of the main run.
- Start years 1972 to 1976 rest on the substitute inputs named in R1, and headline counts are also given without them.
  For some years after August 1976 the only broad index fund an individual could buy tracked the S&P 500, not the whole
  market, so later start years also invest in a portfolio no individual could exactly buy.
- The fund fee is an industry average; ICI says its averages are not meant for benchmarking any one investor's fees.
- The all-transactions index includes refinance appraisals; the purchase-only run (R15.3) checks it.
- Everything is in current dollars except chart 2.
- Not financial advice.

## 9. Credits and notices (method notes, chart footers, data/README.md)

- FHFA's required notice, "This product uses FHFA data but is neither endorsed nor certified by FHFA.", and its credit
  form naming each index used: "Source: FHFA HPI®", all-transactions, not seasonally adjusted, nominal (the value);
  purchase-only, seasonally adjusted, nominal (level A after 2018Q2); purchase-only, not seasonally adjusted, nominal
  (R15.3).
- Freddie Mac, Primary Mortgage Market Survey, credited as the file's footer asks; the post publishes figures and
  charts derived from it, never the file.
- Davis, Lehnert and Martin (2008), with the AEI Housing Center named as the data source and no relationship with AEI
  implied; the workbook is not re-hosted.
- Kenneth R. French Data Library, with the file's copyright line.
- ICI: values cited with attribution and its URL; no ICI table or chart is reproduced. NAIC: individual figures cited;
  no table reproduced. Vanguard: the launch date and first expense ratio cited as facts, with attribution. The
  Entrepreneur column: one short quotation, attributed. REAL Trends: not used in the post.
- BLS, Census, BEA, the Federal Reserve and CFPB: public domain, cited. The Internet Archive is named for every file
  retrieved through it.
- As in every post of the series, the post states that it is non-commercial and that no publisher of these data
  endorses it.

## 10. Claude's design calls (the owner can override any of them when approving)

- The Kiyosaki scope note (section 1), a correction the vet asked for.
- A monthly model: the purchase and the renter's day-one investment at the start of January of the start year, and
  every later flow at the end of a month (R1).
- Start years from 1972 with 1972 to 1976 labeled, rather than a 1978 start (R1).
- The new-house bridge for 1972 to 1974, with depreciation and no improvements charge (R2, R7c).
- Rent as the rent-to-price ratio times the home's value, with the CPI rent path as a sensitivity (R3, R15.1).
- Points fixed at the 2018 to 2022 mean where PMMS publishes none (purchases from 2023, refinancings from December
  2022; R4, R9): the vet's second preference. Its first, requesting the legacy-method points that the February 2023
  version of Freddie Mac's November 2022 note promised through 2023, was set aside: the January 2024 version drops that
  promise, so the file may not exist; the request form asks for personal data; and 2024 and 2025 would need p_fix
  either way. Its third, HMDA loan-level files, is unvetted and large.
- The buyer's other loan costs from CFPB data, transfer taxes and the owner's title policy in the seller's 6%, recording
  fees left out of the main run (R5, R6).
- The property tax, insurance and upkeep constructions and their low and high runs (R7, R15.5, R15.6).
- The fund fee: ICI's index-fund average, with its 1996 value carried back to 1972 (R8).
- The refinancing rule itself (R9); the owner chose to use it in the main run.
- The measures and the 1996 household (R11 to R14), and the sensitivity set (R15).

## 11. Model routing

This design was written on Opus. Once the owner approves it, the build (`profile_data.py`, `build_analysis.py`, charts)
is mechanical and can run on Sonnet, following the rules above literally; review rounds go back to Opus.

## 12. Amendments

- **A1 (2026-11-13, New York time, after the owner's approval; wording corrections, no rule changed).** The fifth
  check of this document, still running when the owner approved it (the owner was told it could change only wording),
  found four statements to correct, and they were corrected in place:
  - R15's closing property-tax bullet said that in years when BEA's rate is above the survey's, "as in 1975, the high
    run sits below the vet's top". That is false for 1980, when BEA's rate is just above the survey's and the high run
    sits just above the vet's top. The bullet and section 8 now name 1975 alone, and both add the larger departure:
    from 2005 the low run stays a quarter to a half above BEA's rate, the vet's floor.
  - R15.1 said BLS makes its corrections only inside its "all-items" research series; it publishes two research
    indexes (all items, and all items less food and energy), and the text now says so.
  - Section 10 described Freddie Mac's legacy-method points file as if it existed; the text now says it was promised
    in the February 2023 version of the note, that the January 2024 version drops the promise, and that the vet ranked
    the request first.
  - Spelling and grammar in the same bullet ("modeled"; "BEA's series is the lower one").
- **A2 (2026-11-14, New York time, after step 3 gathered the data and before any result; Claude's calls, made in place
  and listed here).** Step 3 found facts the rules did not foresee:
  - R7a: ACS table B25090 is not in the 1-year summary files before 2010, so 2005 to 2009 use the ACS ratio of medians
    (B25103 over B25077) from the same files, which ran within 2% of the aggregate ratio in 2021 to 2025, rather than a
    six-year straight line that would hide the swings in home values over those years. No national housing survey was
    run in 1982, so 1982 joins the straight-line years. For 1973 the tax row sits in Table A-2 of the same volume, with
    the same row, column and universe.
  - R7c: the owner-occupied share is owner-occupied over private residential fixed assets (BEA Fixed Assets Table 5.1,
    line 11 over line 2), because the improvements series is private only; year y uses the year-end y stock. No
    archived BEA vintage has the tenure table for 2024 or 2025, so those years hold the 2023 share, which moved by
    less than 0.001 in its last year.
  - R15.5 names the NAIC forms behind the owner-occupied premium total; R14 names the 2025 price base.
  - Wording made exact: R3's level B scope, R7c's routine line, two citations in section 3, and three limits in section
    8 (the survey universes behind property tax, the AHS insurance median, the October 2025 CPI gap).
- **A3 (2026-11-14, New York time, fact-check round 1; a wording correction, no rule changed).** Section 3 said each
  file's definition is quoted in `docs/provenance-audit.md`. The audit paraphrases the definitions in copyrighted
  documents (its Copyright reading rule), so "quoted" became "recorded".
- **A4 (2026-11-14, New York time, fact-check round 2; no rule changed).** The header no longer points to the full
  list of figures seen during the vet, and that list is not committed: it copies values from ICI and NAIC tables and
  from the AEI workbook, which section 9 says the post does not reproduce or re-host.
- **A5 (2026-11-15, New York time, fact-check round 3; no rule changed).** The header no longer gives a count of the
  refute-checks, which was stale, and section 7 points to DLM's Table 2 instead of reproducing its figures from the
  copyrighted article.
- **A6 (2026-11-15, New York time, fact-check round 4; no rule changed).** Section 3's fund-fee input names the
  Investment Company Institute in full, with http://www.ici.org, as ICI's Copyright and Linking Policies ask of anyone
  who cites its information.
