# Post 18 design: A Quarter of the Median County's Income Is a Transfer. Nearly Half of That Is Paid to a Provider.

Date: 2026-07-30. Status: awaiting approval.
Slug: `a-quarter-of-county-income-is-a-transfer`. Chart prefix: `income-`.

## Where this came from

Jonathan supplied the Data Is Plural edition of 2021-12-01 and the BEA's personal-income-by-county
page. The DIP entry is the BEA county series. Pulled directly from BEA's bulk endpoint
(`apps.bea.gov/regional/zip/CAINC1.zip`, `CAINC35.zip`), not from a re-upload.

## Brainstorm outcome, his picks

| Dimension | Choice |
|---|---|
| Angle | A quarter of American income is now a transfer, the structural arc |
| Hook | A quarter of "income" is money nobody receives: BEA's "by, or on behalf of" |
| Stance | The accounting is right, the word is wrong |
| Frame | **US only. No external joins, nothing to source beyond BEA.** |
| Close | Ask what is inside the number before you use it |
| Title | A Quarter of the Median County's Income Is a Transfer. Nearly Half of That Is Paid to a Provider. |

He rejected the 2020 pandemic angle, the emptying-counties denominator angle, and the
convergence-then-divergence angle (which I flagged as structurally identical to Post 17). He also
rejected an Indonesia comparison and a first-person outsider frame.

## Thesis

American personal income is not what the phrase implies, and the BEA says so in the first line of its
own definition. Transfers have gone from 7.9% of US personal income in 1969 to 18.1% in 2022, and in
the median county from 9.9% to 26.2%. Nearly half of that is now medical benefits, which are payments
made to hospitals and insurers on a person's behalf and counted as that person's income. Nothing here
is hidden or wrong. The number is honest and the word is not, and the gap is wide enough that two
counties can report the same income and mean different things.

## The evidence chain

**1. The long arc.** Transfers as a share of personal income.

| | 1969 | 1990 | 2010 | 2019 | 2022 |
|---|---|---|---|---|---|
| United States | 7.9% | 12.2% | 18.5% | 17.1% | 18.1% |
| Median county | 9.9% | 16.3% | 24.8% | 25.2% | 26.2% |
| 90th percentile county | 15.6% | 23.6% | 35.1% | 35.8% | 37.8% |

**2. What actually grew.** Change in share of US personal income, 1969 to 2022:

| Component | 1969 | 2022 | Change |
|---|---|---|---|
| Medicare | 0.85% | 4.18% | +3.33 |
| Medicaid and other medical vendor payments | 0.59% | 3.74% | +3.15 |
| Social Security | 3.33% | 5.47% | +2.14 |
| Income maintenance (SSI, EITC, SNAP, TANF) | 0.92% | 2.03% | +1.11 |
| Unemployment insurance | 0.29% | 0.10% | -0.19 |

Total transfers rose 10.2 points. **Medical is 6.5 of those points, 64% of the entire rise.** The
politically loudest category, income maintenance, is 1.1 points.

**3. Cash versus on behalf of.** Line 2200 (medical benefits) equals 2210 + 2220 + 2230 exactly, max
absolute difference 0.0, so the split has no residual.

| | 1969 | 2000 | 2022 |
|---|---|---|---|
| Medical, share of personal income | 1.5% | 5.0% | 8.0% |
| Cash transfers, share of personal income | 6.4% | 7.7% | 10.1% |
| Medical as a share of all transfers | 18.6% | 39.3% | **44.3%** |

At county level in 2022: median county 26.2% transfers, splitting 11.4 points medical and 14.5 points
cash. **169 counties where medical alone exceeds 20% of all personal income. 434 counties where the
money paid on residents' behalf exceeds the money paid to them.**

**4. The same number meaning different things.** Queens, New York and Saluda, South Carolina both draw
about 26.4% of personal income from transfers. In Queens 60.6% of that is medical; in Saluda 34.2%.
This is the close, made concrete.

## Four charts

1. `income-1-the-long-arc.png` Transfers as a share of personal income, 1969 to 2022: the US line and
   the median county, with the interquartile band across counties. Sets up the scale.
2. `income-2-cash-or-on-behalf.png` The same total, split into cash paid to people and medical paid to
   providers, as shares of personal income. The medical band overtakes on the way to 44.3% of all
   transfers. This is the hook made visual.
3. `income-3-everywhere.png` The distribution across all counties, 1969 against 2022. The point is
   that the whole distribution moved, not just a tail: zero counties above 40% in 1969, 203 in 2022.
4. `income-4-same-number.png` Every county in 2022 plotted as cash share against medical share, with
   the diagonal marking where medical overtakes cash (434 counties above it), Owsley labelled at the
   extreme and the Queens/Saluda pair marked to carry the close.

## Statistical care

**The title's second clause is computed as the median of per-county ratios, not the ratio of two
medians.** Those are different statistics and conflating them is the kind of thing this series
catches in other people's work. Here they happen to agree, which is worth stating rather than
relying on:

| Method | Value |
|---|---|
| Median of each county's medical/transfers ratio | **43.5%** (the one quoted) |
| Ratio of the median medical share to the median transfer share | 43.6% |
| US aggregate | 44.3% |
| Mean of per-county ratios | 43.8% |

## Coding traps found in the vet

**Trap 1: the zip contains both the parts and the whole.** `CAINC1.zip` holds 53 per-state files AND
`CAINC1__ALL_AREAS_1969_2024.csv`. A glob like `CAINC1_*.csv` matches both and silently doubles every
row. Mine did, and I only caught it because Connecticut printed twice. **Handling: read only the
`_ALL_AREAS_` file.** Verified: 9,631 rows, zero duplicate (GeoFIPS, LineCode) pairs.

**Trap 2: the geography changes inside the panel.** Connecticut's 8 counties carry data through 2023
and NaN in 2024; its 9 planning regions carry NaN until 2023 and data only in 2024. Roughly 50 defunct
Alaska census areas are retained as all-NaN rows. The county count looks reassuringly stable at about
3,110 per year precisely because 8 units leave as 9 arrive. **Handling: the transfer analysis ends at
2022 anyway (see below), and any county-level series states its balanced panel, 3,089 counties with an
unbroken 1969 to 2023 record.**

**Trap 3: per capita income is a derived ratio.** Line 3 is exactly line 1 divided by line 2, matching
to the rounded dollar in every year tested. It is not measured. This post barely uses it, but it is
worth one line in the notes because it is the number everyone quotes.

## Honesty requirements

- **Do not say "a quarter of American income is not paid to Americans."** 26.2% is the transfer share;
  the on-behalf-of part is 11.4 points of it. The title's two clauses are separate claims and the body
  must keep them separate.
- **Medical vendor payments buy real care.** They are not fake income and the post must not imply it.
  The stance is that the label misleads, not that the money is imaginary.
- **CAINC35 ends in 2022** while CAINC1 runs to 2024, so every transfer figure stops at 2022. Say so.
- **Everything is a share, so nominal dollars are fine.** No deflator is needed and none is used. State
  this, because a reader will reasonably wonder.
- **Counties are not households.** A county's transfer share is an aggregate over its whole personal
  income, not the budget of a typical family in it.
- **Do not claim the age link.** The obvious explanation for high Medicare counties is an older
  population, but there is no age variable in these files and I am not joining Census data. If the
  essay raises it, it raises it as an untested explanation.
- **The 2020 and 2021 spike is visible and must not be mistaken for the trend.** The structural arc is
  the subject; the pandemic years are an excursion that partly reverses by 2022.
- **This is not a takedown of BEA.** The definition is public, the methodology PDF is free, the
  footnotes name medical vendor payments explicitly. The failure is entirely downstream.

## Sources, all BEA, all verified

- BEA. *County Personal Income: Concepts and Methods*. Verbatim: "Personal income is the income
  received by, or on behalf of, all persons from all sources". Also, for Medicaid: "Consists of
  Medicaid, beginning in 1966, and other medical vendor payments."
- BEA CAINC1, county personal income summary, 1969 to 2024.
- BEA CAINC35, personal current transfer receipts, 1969 to 2022.
- Data Is Plural, 2021-12-01 edition, as the entry point.

No non-BEA data is joined, so there is nothing else to verify.
