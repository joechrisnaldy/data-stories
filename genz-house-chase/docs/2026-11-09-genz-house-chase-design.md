# Post 29 design: the house chase, pre-registration

Written 2026-11-09 (New York time), before the chase or any other result is computed. Section 7 lists every figure
already seen during the dataset vet, so the predictions in section 6 can be judged honestly. Later changes are added as
dated amendments at the end, each with its reason.

## 1. Question and stance (the owner's)

The owner's view, in his words of 2026-11-09, abridged: houses and basic needs got expensive while pay rose little and AI
takes jobs; Boomers and Millennials could save their way to a home because their savings caught up with housing, and Gen Z
cannot; so spending on small things is what Gen Z can afford, to be happy. He asked for the ratio of home prices to salary.

The hook is Bakhtiari's Forbes column (2026), which calls this the "permanent lipstick effect". The post tests the claim
that savings can no longer catch up with housing, and whether skipping treats would change that. The voice states the
owner's view plainly, with no personal circumstances. Not financial advice: no sentence tells a reader to buy, sell, save
or spend in any particular way.

## 2. Owner decisions so far

- 2026-11-09, brainstorm: main test "savings can't catch up"; the US, plus an Indonesia note; the measure is "the chase";
  scope covers spending by age, wages against home prices, and AI and entry-level jobs; mortgage rates are out, named as a
  limit; hook "Skip the treats, still no house"; personal angle "my view, plainly"; closing "rational, not reckless";
  working title "Skip the Matcha, Still No House", final only once the results support it.
- 2026-11-09, dataset checkpoint: go, using the Internet Archive copies of the BLS files; keep the Indonesia note and say
  plainly what it found; say plainly that young households' treat share of spending fell.
- 2026-11-09, design checkpoint: this document approved as written, before any result; headline saving share 10%; both
  treat tests (R9 broad, R10 narrow); the fourth chart is AI and entry-level jobs, so homeownership goes in the prose.

## 3. Data

Vetted 2026-11-09. Files in `data/`, pinned by sha256 in `profile_data.py`. Definitions in `docs/provenance-audit.md`.

- **Home prices.** Census Survey of Construction: median sales price of new houses sold, annual, 1963 to 2025, current
  dollars, lot included. Census constant-quality (Laspeyres) price index of new houses sold. Median floor area of new
  houses sold. FHFA House Price Index, all-transactions, US, 1975 to 2026. Census 2000 median value of owner-occupied
  single-family homes ($119,600) and ACS 2025 median value, as anchors.
- **Income.** Census Table H-10: median household income by age of householder, current dollars, 1967 to 2025.
- **Interest.** Federal Reserve Board H.15: 3-month Treasury bill, secondary market, discount basis, annual, 1954 to 2025.
- **Pay.** BLS: median usual weekly earnings of full-time wage and salary workers aged 25 to 34, annual, 1979 to 2025.
  Deflators: R-CPI-U-RS (headline) and CPI-U (check).
- **Spending.** BLS Consumer Expenditure Survey, LABSTAT database: mean annual spending by age of reference person,
  1984 to 2024. Two printed tables (1984, 2024) check the database.
- **Homeownership.** Census HVS Table 17, rates by age of householder, 1982 to 2025.
- **AI context.** New York Fed, unemployment of recent college graduates and of all workers, monthly, 1990 to September
  2026. Prose only: BLS unemployment by age; Brynjolfsson, Chandar and Chen (2026); the Budget Lab at Yale (2025, 2026).
- **Generations.** Pew Research Center (Dimock, 2019).
- **Indonesia.** Bank Indonesia residential property price index for the primary market (2018 = 100, national composite of 18
  cities); ILOSTAT monthly earnings of employees, Indonesia.
- Not used: FRED (its terms bar use with AI), NAR (terms bar automated access and storage), FHFA's mortgage survey (a
  convenience sample), Bank Indonesia's 2002 = 100 series (superseded), the five BLS API responses (robots disallow).

## 4. Rules fixed before any result

- **R1 Start years and generations.** A saver turns 25 in start year S, from 1971 to 2025. Generations follow Pew's
  birth years, so the start years are: Boomers 1971 to 1989, Gen X 1990 to 2005, Millennials 2006 to 2021, Gen Z 2022 to 2025.
- **R2 The saver's income.** In year t the saver is 25 + (t - S) years old. Income is the H-10 current-dollar median for
  that age bracket: 25 to 34, then 35 to 44, then 45 to 54. For 2013 and 2017, use the rows Census marks for comparison
  with later years (2013 (39), 2017 (40)); the other two rows are a check.
- **R3 Saving share.** Each year the saver puts aside s = 10% of that year's income. The results are also reported at
  5%, 15% and 20%.
- **R4 Interest.** B(t) = B(t-1) x (1 + r(t)) + c(t) x (1 + r(t)/2), where c(t) = s x income(t) and r(t) is the year's
  T-bill rate. Contributions arrive mid-year. Interest is untaxed. Check: the chase with no interest at all.
- **R5 The target.** 20% of the year's median sales price of new houses sold: T(t) = 0.20 x P(t). Check: a 10% down
  payment.
- **R6 When the chase ends.** At the end of the first year t with B(t) >= T(t). Years of saving: Y = t - S + 1. A chase
  that has not ended by 2025 is unfinished. Report its years so far (2026 - S) and the share reached, B(2025) / T(2025).
  Nothing is projected.
- **R7 Like-for-like.** For every S up to 2023: the share of the down payment saved after three years, B(S+2) / T(S+2).
  Each generation is summarized by the median over its start years; Gen Z has two (2022, 2023). The table also gives
  shares after one, two and four years.
- **R8 Checks on the house.** (a) The same house: P(t) = P(S) x Q(t) / Q(S), with Q the Census constant-quality index.
  Each saver chases the typical new house of their own start year at constant quality. (b) Existing homes:
  P(t) = 119,600 x H(t) / H(2000), with H the FHFA all-transactions index (annual mean of the four quarters, not
  seasonally adjusted), for start years from 1975. The implied 2025 level is compared with the ACS 2025 median.
- **R9 Treat test, broad.** For S from 1984 to 2024, each year's saving also includes X(t). X(t) is the mean annual
  spending of consumer units in the saver's age bracket on food away from home, entertainment, and personal care
  products and services (CE codes FOODAWAY + ENTRTAIN + PERSCARE). For 2025, which has no CE data yet, X(2025) = X(2024),
  flagged. Report years of saving with and without, by start year, and the median change by generation. The test is
  generous on purpose: means count big spenders, and the categories hold non-treats (school meals, toiletries, pet food).
- **R10 Treat test, narrow (the matcha line).** CE "snacks and nonalcoholic beverages" bought away from home (SNKNABEV),
  25 to 34 consumer units, 2010 to 2021: the yearly amount, and how many years of it equal that year's down payment.
  Also: how many years of the broad X equal the down payment in 2024.
- **R11 Price in years of pay.** P(t) / the H-10 median for 25 to 34 households, 1971 to 2025. P(t) / (52 x the BLS
  median weekly pay of full-time workers aged 25 to 34), 1979 to 2025. Nominal over nominal: no deflator.
- **R12 Treat share of spending.** (FOODAWAY + ENTRTAIN + PERSCARE) / average annual expenditures (TOTALEXP), 1984 to
  2024, for all consumer units, 25 to 34, and under 25. Under 25 is a centered 3-year average, because the group is small
  and noisy.
- **R13 Pay and prices after inflation (prose).** The change in real median weekly pay for 25 to 34 full-time workers
  and in the real median new-home price, 1979 to 2025, with the R-CPI-U-RS; the CPI-U as a check.
- **R14 AI and entry-level jobs (context).** The NY Fed monthly rates, recent college graduates against all workers,
  as published. In prose: what the Stanford and Yale studies find and do not find, in paraphrase. No sentence says or
  implies that AI caused anything.
- **R15 Indonesia note.** Bank Indonesia's national composite index (annual mean of four quarters) against ILOSTAT
  median monthly earnings of employees, all ages and ages 25 to 34, 2018 to 2024. The urban median is a check. Report
  growth over the window and say plainly which rose faster. There are no price levels, so no ratio and no chase. The
  ILO flags a methodology break in 2021.
- **R16 Homeownership (prose).** HVS Table 17 rates for under 35 and under 25, in 1982 and 2025 (1993r1 and 2002r2 are
  the rows used for those years). Both age groups are always shown together. The rates count householders only, so
  young adults who live with their parents are outside them.

## 5. Charts (four)

1. `gz-1-years-of-pay`: the typical new home in years of pay, 1971 to 2025. One line for 25 to 34 households; one for a
   single full-time salary at 25 to 34, from 1979.
2. `gz-2-chase`: years of saving to reach a 20% down payment at 10% of income, by the year the saver turned 25,
   colored by generation. Unfinished chases are marked as such, with years so far and share reached. For start years
   from 1984, a marker shows the years needed when the treat budget is saved too.
3. `gz-3-treat-share`: share of spending on eating out, entertainment and personal care, by age, 1984 to 2024.
4. `gz-4-recent-grads`: unemployment rate, recent college graduates against all workers, 1990 to 2026 (NY Fed).

## 6. Predictions (written before any result)

- P1. The new home costs more years of 25 to 34 household income in 2025 than in 1971.
- P2. In years of one full-time salary, the price rose more from 1979 to 2025 than it did in years of household income.
- P3. At 10%, the median years of saving across Boomer start years are fewer than across the Millennial start years whose
  chase finished by 2025.
- P4. After three years, the Gen Z savers (2022, 2023) hold a smaller share of the down payment than the median Boomer
  saver after three years.
- P5. Saving the broad treat budget as well shortens the median chase by at least a third, for start years from 1984. If
  it does, "skip the treats, still no house" holds only for small treats, and the closing and title go back to the owner
  before drafting.
- P6. A year of snacks and nonalcoholic beverages away from home costs 25 to 34 households less than 1% of the year's down
  payment in every year from 2010 to 2021.
- P7. The same-house check narrows the gap between Boomer and later start years but does not close it. The existing-home
  check points the same way as the new-home chase.

## 7. Already seen during the vet (not predictions)

- New-home median price: 1963 $18,000; 1971 $25,200; 1990 $122,900; 2022 $434,500; 2025 $417,400.
- H-10 median for 25 to 34 households: 1967 $8,012; 2024 $90,020; 2025 $94,880 (so the 2025 ratio is about 4.4).
- BLS median weekly pay, 25 to 34 full time: 1979 $255; 2025 $1,143. That is $1,058 (BLS's series) or $1,060 (own
  deflation) in 2025 dollars; the build uses one method and states it.
- T-bill rate: 1971 4.33; 1981 14.04; 1990 7.50; 2009 0.15; 2022 2.02; 2025 4.07.
- Treat share of spending, 1984 against 2024: all consumer units 12.12% and 10.86%; under 25 13.71% and 11.65%; 25 to 34
  12.47% and 10.75%. Broad treat spending of 25 to 34 consumer units in 2024: $8,005.
- Homeownership (recomputed from Table 17): under 35, 41.2% (1982) and 37.0% (2025, an 11-month average); under 25, 19.3%
  (1982) and 24.2% (2025).
- NY Fed: the recent-graduate rate has been above the all-worker rate every month since January 2021; 2025 means 5.42
  and 4.08.
- Indonesia, 2018 to 2024: Bank Indonesia's index rose 9.2%, while ILOSTAT employee earnings rose 13.3% (urban mean) to 25.6%
  (ages 25 to 34, median).
- The Forbes column's own housing figure is for the UK.
- Bank of America Institute (August 2026) reports, from its card data, more Gen Z spending on small beauty items. That is
  a possible counterpoint for the hostile reader; it has not been vetted.

## 8. Limits stated in the post

- New houses built for sale only, and they grew: R8's two checks address both.
- Income is pre-tax household money income: the median of an age bracket, not the saver's own cohort. Two-earner
  households are included, which is why the single-salary line is shown. Census says 2019 to 2025 income runs about 2% to
  4% high because of nonresponse.
- The saving share is an assumption, shown at four levels. Interest is untaxed. The chase stops at the down payment: no
  mortgage, closing costs or rent.
- Mortgage rates are not modeled. Early-1980s rates were far higher than 2010s rates; any number cited needs a vetted
  source.
- T-bill rates are on a discount basis. CE figures are means, not medians; 2024 food away from home includes delivery fees;
  2025 spending is not yet available. Pay covers full-time wage and salary workers only; BLS's 2025 figures are 11-month
  averages.
- AI: context only. None of the four sources shows that AI caused the rise in young graduates' unemployment.
- Indonesia: an index of developer-reported selling prices of new houses in 18 cities, not adjusted for quality; employees'
  main-job earnings only.

## 9. Model routing

This design was written on Opus. Once the owner approves it, the build (profile, `build_analysis.py`, charts) is
mechanical and can run on Sonnet, following the rules above literally.

## 10. Amendments

- **A1 (2026-11-09, before any result; a clarification of R13).** R13 deflates with the stored R-CPI-U-RS file
  (`data/bls_rcpiurs_allitems_ia20260819.xlsx`). BLS's own 2025-dollar series for 25 to 34 year olds (LEU0258178800),
  behind section 7's $1,058, sorts past the cut in the stored 2026 copy of the pay file and reached the vet only through
  the BLS API, which is excluded. So the post uses its own deflation throughout ($1,060 for 1979 in 2025 dollars) and
  does not cite $1,058.
- **A2 (2026-11-09, after the first results; owner decisions, no rule changed).** P5 came true (the broad treat budget
  halves the median chase), so the closing and title went back to the owner, as section 6 required. He chose: keep the
  title "Skip the Matcha, Still No House", which the narrow test (R10) supports; close on "rational, not reckless" and
  say plainly that giving up all eating out, entertainment and personal care would halve the chase. The results also
  put Millennials with Gen Z rather than with Boomers (after three years: Millennials 29% of the down payment, Gen Z 34%,
  Gen X 39%, Boomers 47%). He chose to state his view in his words, then show that the chase got longer for Millennials
  first and that Gen Z inherited it. P7's same-house part failed: pricing the same house over time leaves the gap
  between Boomers and Millennials unchanged. The post reports that, and that existing homes shrink the gap to two years.
- **A3 (2026-11-10, after fact-check round 1; corrections, no rule changed).**
  - "For Millennials first" (A2) was wrong. Gen X chases were already longer than Boomer chases: a median of nine years
    against seven, and 39 percent of the down payment after three years against 47. The post now says the chase got
    longer before Gen Z ("not first for Gen Z"), and that wording supersedes A2's.
  - R8(a) holds each saver's own starting house at constant quality during their chase. It does not remove the growth
    in house size between generations. The round 1 lenses priced one constant-quality house for every start year and
    found a gap of one to three years between Boomers and Millennials, depending on the anchor year (their computation,
    recorded in docs/round1-verdicts.json, not in the build). The post now describes R8(a) as it is, and names only the
    existing-home check, R8(b), as the check on bigger houses. This supersedes section 8's "R8's two checks address
    both".
  - Section 5 said chart 2 would show the share reached by unfinished chases. The chart shows the years so far only;
    results.json carries the shares reached (chase.by_start and the generation medians).
  - R10 measures average spending across all households aged 25 to 34, including those that buy none. No daily habit
    was tested, so the closing now speaks of that average spending, not of "a daily matcha".
  - Section 3's "FRED (its terms bar use with AI)" overstated FRED's terms, which restrict using its data to develop or
    train AI systems. FRED stays out.
  - The two ILOSTAT mean-earnings files were vetted but never used, so they are no longer pinned. The printed BLS tables
    for 1984 and 2024 both check the LABSTAT file in profile_data.py.
- **A4 (2026-11-11, after fact-check rounds 2 and 3; corrections, no rule changed).**
  - Round 2 edited A3 in place: it added the last sentence of A3's second bullet and cut the last sentence of its fifth
    bullet to "FRED stays out." The reasons are in docs/round2-verdicts.json (r2:extra:K7 and r2:item:53).
  - In sections 2, 4 and 6 and in A1, "before any result" now reads "before the chase was run", and the header's "or
    any other result" is withdrawn. The reason is in docs/round3-verdicts.json (r3:item:10).
- **A5 (2026-11-11, after fact-check round 4; corrections, no rule changed).**
  - The header's "every figure already seen during the dataset vet" now reads "figures already seen during the dataset
    vet", and its "so the predictions in section 6 can be judged honestly" is withdrawn.
  - A2's three-year share for Millennials was corrected in place before fact-check round 1.
  - A3's date, 2026-11-10, is the UTC date; in New York time, the header's clock, A3 was written on 2026-11-09.
  - The reasons are in docs/round4-verdicts.json (r4:extra:H1, r4:extra:H2 and r4:extra:K3).
