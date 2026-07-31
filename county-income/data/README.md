# Data

One source: the US Bureau of Economic Analysis. Nothing is joined from anywhere else, so there is no
external series to reconcile. Files are not redistributed here; everything below reproduces from
scratch in about a minute.

## The tables

| Table | What it is | Years |
|---|---|---|
| **CAINC1** | Personal income, population, and per capita personal income, by county | 1969 to 2024 |
| **CAINC35** | Personal current transfer receipts, broken out benefit by benefit | 1969 to 2022 |

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
for f in CAINC1 CAINC35; do
  curl -sL -A "$UA" -o "$f.zip" "https://apps.bea.gov/regional/zip/$f.zip"
  mkdir -p "$f" && unzip -oq "$f.zip" -d "$f"
done
```

Expected layout: `data/CAINC1/CAINC1__ALL_AREAS_1969_2024.csv` and
`data/CAINC35/CAINC35__ALL_AREAS_1969_2022.csv`. Read with `encoding="latin-1"`. `GeoFIPS` arrives
quoted and space-padded, so strip both.

CAINC35 breaks transfers into 23 line codes, including Social Security (2110), Medicare (2210),
Medicaid and other medical vendor payments (2220), SSI (2310), EITC (2320), SNAP (2330) and
unemployment insurance (2400). The medical total (2200) is used throughout this post as the
"paid on the person's behalf" category.

## TRAP 1: the zip contains both the parts and the whole

`CAINC1.zip` ships **52 per-area CSVs, one per state plus DC plus a national one, and an
`_ALL_AREAS_` file**. A glob like `CAINC1_*.csv`
matches both and silently doubles every row. Mine did. It surfaced only because Connecticut printed
twice in a diagnostic.

**Handling: read only the `_ALL_AREAS_` file.** `build_analysis.py` asserts zero duplicate
(`GeoFIPS`, `LineCode`) pairs, which fails loudly if the per-state files creep back in.

## TRAP 2: the geography changes inside the panel

Connecticut abolished county government for statistical purposes and BEA followed.

| Rows | 2023 | 2024 |
|---|---|---|
| Connecticut's 8 counties (09001 to 09015) | data | missing |
| Connecticut's 9 planning regions (09110 to 09190) | missing | data |

Alaska carries 55 county-level units of which 25 stop before 2024, the residue of repeated boundary
changes. No county row in the file is missing for every year. The per-year
county count is a reassuring 3,114, 3,114, 3,115 across 2022 to 2024, and it is stable **precisely
because 8 units leave as 9 arrive**. Of the 3,149 county codes in the file, **3,089 have an unbroken
record from 1969 to 2023**.

A fourth wrinkle, found late: each CSV ends with four trailer rows (the table title, a "Last updated"
line, a footnote pointer and "U.S. Bureau of Economic Analysis") whose `GeoFIPS` cell holds prose. A
filter of `~endswith("000")` lets them through and inflates the county count to 3,153. Require
`GeoFIPS.str.fullmatch(r"\d{5}")`. The trailer is also where the file's vintage is printed: CAINC1 is
dated 5 February 2026 and CAINC35 16 November 2023.

## TRAP 3: the two tables end in different years

CAINC1 runs to 2024, CAINC35 only to 2022. Any analysis using both must stop at **2022**, and this
one does.

## Other things worth knowing

- **Per capita personal income is a derived ratio**, exactly personal income divided by population,
  matching to the rounded dollar in every year tested (maximum absolute difference 0.5 in 1969, 2000
  and 2024). It is not measured. It is also the figure most often quoted from this dataset.
- **Everything here is a share of personal income, so no deflator is needed.** Nominal dollars cancel
  in a ratio. This is why the post can run 1969 to 2022 without a price index.
- **"Transfers" means line 1000, the full total.** That is government transfers plus small amounts
  from businesses and to nonprofit institutions. Government alone (line 2000) is 7.29% of personal
  income in 1969 and 17.37% in 2022, against 7.88% and 18.07% for the total, so government is 92.6%
  and 96.1% of it respectively. Do not call the headline figure "government transfers".
- **The national figure is income-weighted; the median county is not.** In 2022 the US aggregate is
  18.07% while the median county is 26.24%, because transfer share falls steeply as counties get
  richer. State which correlation you mean: -0.671 against income per head, -0.774 against its
  logarithm, -0.807 on ranks.
- **Keep the weighting ladder on one statistic.** 26.44%, 19.85% and 18.07% are the unweighted,
  population-weighted and income-weighted **mean** county share, and the population step is 78.7% of
  that gap. Do not descend from the unweighted **median** 26.24% to those two, which is what an
  earlier draft did: the genuine weighted medians are 19.16% and 17.01%, and on the all-median ladder
  the population step is 76.8%. The means are the ones to quote, because the income-weighted mean is
  identical to the published national figure.
- **Line 4000 is not line 3000.** Line 3000 is transfer receipts **of** nonprofit institutions, which
  never reach an individual. Line 4000 is transfer receipts of individuals **from** businesses,
  defined by BEA as mostly personal injury liability payments to individuals, which do. An earlier
  version of the non-medical-residual figure counted both and reported 16.4% instead of 13.4%.
- **Medians of parts are not parts of a median.** The median transfer share is 26.24%, the median
  medical share 11.44% and the median cash share 14.50%. Those are three different rankings of the
  same 3,114 counties and they do not sum: 11.44 plus 14.50 is 25.94. There is also no single median
  county, since n is even; the middle pair is Clark, IL (26.241%) and Lenawee, MI (26.245%).
- **The medical split is exact.** Line 2200 equals 2210 plus 2220 plus 2230 with maximum absolute
  error 0.0, so "cash versus paid on the person's behalf" is a genuine partition rather than an
  overlap.
- **Median of ratios is not the ratio of medians.** The essay quotes the median of each county's own
  medical-to-transfers ratio (43.54%). The ratio of the two medians is 43.58% and the national
  aggregate is 44.26%. They agree here; they need not, and the script computes all three.
- FIPS codes ending `000` are state and national aggregates, not counties.

## The definition that the post turns on

From BEA's own *County Personal Income: Concepts and Methods*:

> Personal income is the income received by, **or on behalf of**, all persons from all sources.

And from note 2 to table H of the same document, on the public assistance medical care line:

> Consists of Medicaid, beginning in 1966, and other medical vendor payments.

That wording also appears in `CAINC35__definition.xml` under LineCode 2220. It is **not** in
`CAINC35__Footnotes.html`, which is where an earlier version of this note wrongly placed it. On Medicare the
methodology says the benefits are "payments made directly or through intermediaries to vendors for
the care provided to individuals" (paragraph 5.13); Medicaid is described the same way in paragraph
5.15, and military medical insurance is called vendor payments outright in paragraph 5.19.

**The two documents disagree on one word.** `CAINC35__definition.xml` describes LineCode 2210 as
"federal government payments made through intermediaries to **beneficiaries** for the care provided
to individuals", where the methodology says "to vendors". Only Medicare is affected; 2220 and 2230
say vendors in both. The post quotes the methodology and flags the conflict rather than smoothing it
over.

Medical benefits are paid to providers. They are counted as the income of the person treated. Both
statements are BEA's, published, and free to read.

Note also that the international standard draws the line elsewhere. Under the System of National
Accounts 2008 these are "social transfers in kind", defined at paragraph 8.141 as goods and services
provided to households by government and non-profit institutions free or at prices that are not
economically significant. They are excluded from household disposable income and appear only in
adjusted disposable income, which paragraph 8.32 defines as disposable income plus social transfers
in kind receivable. Cite the SNA itself for this, not a national agency's implementation page.

## What the vet found

Nothing wrong with the data. This is official statistical-agency output with documented methods, and
the post says so. The three traps above are packaging and coverage boundaries, not errors. What the
post argues is that the phrase "personal income" carries an assumption the definition explicitly
disclaims, and that nearly nobody quoting the number passes the disclaimer along.
