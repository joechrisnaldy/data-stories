# Post 30 provenance audit

Written 2026-11-14 (New York time). Updated later the
same day to record the ACS B25103 files that A2's 2005 to 2009 rule needs (section 9.2,
open item 1); no rule changed. For every input
the rules R1 to R16 use, each file or file group in `data/` and each variable a rule reads, this record gives the
publisher, the URL, the transport (direct, owner's hand download, or Internet Archive capture), the retrieval time, the
sha256, what the file covers, the definition from its defining document, the universe, and
the traps the dataset vet and step 3 recorded. The design (`docs/2026-11-13-rent-vs-buy-design.md`)
says how each input is used; this record says what each input is.

How to read it:

- **Hashes.** Appendix A lists every file in `data/` (143 files) with its bytes, sha256, URL, transport and retrieval
  time, hashed on 2026-11-14. Each hash equals the value step 3 or the vet recorded, except `data/acs/acs_positions.csv`,
  whose current hash was recorded when its 29 added positions were written (folder `p30impl/fix2`), and `profile_data.py`, the build's
  pin file (version of 2026-11-14T15:21:32Z), pins the same 143 values. Appendix B lists every stored document in
  `sources/` (128 documents; the readable `.txt` extracts beside them are derived and not listed). Both folders are
  git-ignored.
- **Quote checks.** Each quote line names the stored document and the place, then a check: FOUND (the quote occurs in
  the stored copy after whitespace and Unicode normalization, line-break hyphens tried joined and kept), LOOSE (equal once
  only letters and digits are compared, where text extraction dropped a hyphen), MANUAL (a scanned page with no text
  layer, read by eye on a 200 dpi render and cross-checked against a local OCR of the page), or PARAPHRASE (a copyrighted
  document, paraphrased; a script confirmed the key terms at the locator). Fragments of one passage are joined by
  " ... ".
- **Copyright.** US government documents are quoted verbatim and short. Copyrighted documents (Freddie Mac, the DLM paper
  and AEI notes, French, CRSP, ICI, Vanguard, NAIC, Hsieh and Moretti, Kiyosaki) are paraphrased with exact locators;
  the one verbatim copyrighted fragment is ten words of Freddie Mac's commitment-rate definition (section 1).
- **Dashes.** No em or en dashes appear here. Where a source sentence carries one, the quote stops before it or another
  sentence is used.
- **Records used.** Times are UTC. "Vet" refers to the dataset vet of 2026-11-13 and "step 3" to the data build of
  2026-11-13 and 14. Their reports and download logs sit in the session scratchpad
  (`/private/tmp/claude-501/-Users-jonathanchrisnaldy-Claude-Workspace/7a1b9d4a-a613-4eb1-a1d2-f4d11a2b1ecc/scratchpad/`,
  folders `p30data/<topic>` for the vet, `p30build/<topic>` for step 3 and `p30impl/` for the build checks), which is
  not kept; what a rule needs from them is restated here.

## 1. Mortgage rate and points (R4, R5, R9, R13)

- File: `data/freddiemac_pmms_historicalweeklydata.xlsx` (218,952 bytes; sha256 3066c422d5b7ec93038a60078871d4b43c51c9df268afa9a0ac363b18c7e292a).
- Publisher: Freddie Mac, Primary Mortgage Market Survey (PMMS).
- URL: https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx
- Transport and time: the owner's hand download in a browser. The copy in the owner's Downloads folder has file time
  2026-11-13T23:14:32Z and a quarantine record of 23:14:36Z (agent "Claude"), with no where-from record; it was copied
  unchanged to the scratchpad at 23:15:38Z and into `data/` by the staging script. Same bytes as the vet's direct copy of
  2026-11-13T10:33:54Z (`p30data/mortgage` dl-04); the vet found its weekly values equal, week for week, to Internet
  Archive copies of 2022-10-18, 2022-11-18, 2024-01-11 and 2026-10-20.
- Coverage: one sheet, 'Full History'. Column A 'Week'; column B 'U.S. 30 yr FRM', 2,903 weekly values from 1971-04-02
  to 2026-11-12; column C 'U.S. 30 yr fees & points', 1971-05-28 to 2022-11-10 (52, 52, 53, 52 and 45 weekly values in
  2018 to 2022, none in 2023). Percent. The 15-year and 5/1 columns are not used.
- Definitions:
  - **Rate through 2022-11-10** (`sources/fm_pmms_definitions_ia20260412130140.html`, entry 'Commitment Rate', extract line 167; FOUND): "exclusive of the fees and points required by the lender"
  - **Loans the commitment rate describes** (`sources/fm_pmms_definitions_ia20260412130140.html`, entry 'Commitment Rate', extract line 167; PARAPHRASE): conventional financing on conforming mortgages with a loan-to-value ratio of 80 percent or less.
  - **Fees and points** (`sources/fm_pmms_definitions_ia20260412130140.html`, entry 'Origination Fees and Discount Points', extract line 173; PARAPHRASE): the total the lender charges at settlement; one point is one percent of the loan amount.
  - **What the points add up** (`sources/fm_pmms_note_2019_explained_ia20251012225852.html`, Freddie Mac insight of 2019-06-14, extract line 183; PARAPHRASE): PMMS points are discount points plus origination points.
  - **Rate from 2022-11-17** (`sources/fm_202210-Note-PMMS-12_ia20250819015623.pdf`, November 2022 research note, current version, 'Limitations of the loan application data' and Methodology, printed and PDF pp. 3 to 4; PARAPHRASE): the average interest rate on home-purchase applications submitted to Freddie Mac's Loan Product Advisor that meet the PMMS criteria (conventional, conforming, fully amortizing, 20 percent down, loan-to-value 75 to 80, FICO 740 or above), taken at application rather than origination.
  - **Points stop** (`sources/fm_202210-Note-PMMS-12_ia20250819015623.pdf`, printed and PDF p. 3; PARAPHRASE): because Loan Product Advisor does not capture discount points or origination fees, average points and fees for the 30-year loan are no longer reported.
  - **Legacy-method results** (`sources/fm_202210-Note-PMMS-07_ia20230513054834.pdf`, February 2023 version of the same note, Conclusion, printed and PDF p. 8; PARAPHRASE): results under the historical method, with fee and point estimates, were to continue through 2023 for users who ask; the current version of the note drops this.
- Universe: through 2022-11-10, lenders' commitment rates for prime borrowers on conventional conforming loans at 80
  percent loan-to-value or less, quoted without points; from 2022-11-17, purchase applications in Loan Product Advisor
  meeting the criteria above, with points unknown.
- Traps (vet `p30data/mortgage`, `mortgage-verify`, `critic`; step 3):
  - The method changed on 2022-11-17. The commitment-rate definition describes only the earlier survey; Freddie Mac's
    definitions page was not updated.
  - Points end on 2022-11-10. R4 and R9 use p_fix from then on (design section 10 records why the legacy-method file was
    not requested).
  - Weekly points are rounded to 0.1 point. Freddie Mac's discontinued monthly point averages equal plain means of the
    weekly values in only 262 of 604 months.
  - 1971: the points are eight monthly-spaced values, Freddie Mac published no 1971 annual average, and 31 of the 32 blank
    1971 point cells hold a single space character rather than nothing.
  - Ten years carry 53 weekly values (1976, 1981, 1987, 1992, 1998, 2003, 2008, 2014, 2020, 2025); the extra 2025 value
    is dated Wednesday 2025-12-31.
  - The plain calendar-year mean of the weekly values reproduces Freddie Mac's discontinued annual averages for 1972 to
    2021 within 0.0115 percentage point (vet, against Internet Archive capture 20220531200035 of `30yr_pmmsmnth.xls`).
  - Freddie Mac's current PMMS FAQ gives a different reason for dropping fees and points (lenders need not supply them)
    than the November 2022 note (Loan Product Advisor does not capture them); the note is the one cited.
  - Terms: Freddie Mac's site terms keep Data to internal or personal use and bar automated access; the file and the
    PMMS page allow use with attribution and without alteration. The owner chose "Use with credit, I download" (design
    section 2): the post publishes derived figures and charts, never the file.

## 2. Rent of the same home, level A (R3, R13, chart 1)

### 2.1 Davis, Lehnert and Martin rent-price ratio, 1960Q1 to 2018Q2

- File: `data/aei_dlm_rent_price_ratio_2018q2.xlsx` (84,617 bytes; sha256 eba71363889d5207a140c1600c3395fc847b2f04bbc148bb45978190207efb9e).
- Publisher: Davis, Lehnert and Martin (2008), data maintained by Morris A. Davis, hosted by the AEI Housing Center.
- URL: https://www.aei.org/wp-content/uploads/2018/10/RENT-PRICE-RATIO.2018q2.xlsx
- Transport and time: the owner's hand download in a browser. The Downloads copy has file time 2026-11-13T23:14:38Z and a
  quarantine record of 23:14:40Z, with no where-from record. Same bytes as Internet Archive capture 20200229184452
  (`p30data/rentprice-verify` dl-05, retrieved 2026-11-13T11:24:07Z) and as the vet's direct copy (`p30data/rentprice`
  dl-06, 10:35:56Z).
- Coverage: sheet 'rent-price data', rows 3 to 236: column A 'Date' (1960.1 to 2018.2, 234 quarters), column B 'Average
  annual rent (imputed)', and under the header 'FHFA purchase only after 2000' column E 'Average house price' and column
  F 'rent-price ratio' (columns C and D carry the Case-Shiller variant). Sheet 'BLS CSW OFHEO index data' rows 3 to 75
  (2000Q2 to 2018Q2) hold the indexes the chain uses; sheet 'BLS wksheet' holds monthly CUSR0000SEHC01 for 2000-01 to
  2018-07. File properties: last modified 2018-09-11 by 'Davis, Morris A'.
- Definitions:
  - **Rent-price ratio** (`sources/dlm_roiw_2008-13.pdf`, Introduction, printed p. 279, PDF p. 1; PARAPHRASE): a quarterly series from 1960 of homeowners' imputed rents divided by the value of owner-occupied housing, for the aggregate owner-occupied stock of the United States.
  - **Census benchmarks** (`sources/dlm_roiw_2008-13.pdf`, section on the benchmark estimates, printed p. 281, PDF p. 3; PARAPHRASE): in each decennial census from 1960 to 2000, renters' gross rents are regressed on building age, bedrooms, metropolitan area and state; the fitted rent is predicted for each owner-occupied unit and owners' utilities are subtracted; mobile homes are excluded.
  - **Gross of taxes and depreciation** (`sources/aei_LandPriceNotes_October18_ia20200229184449.pdf`, 'Notes on the Rent-Price Ratio Data Set', PDF p. 2; PARAPHRASE): the rents are gross, with no allowance for income taxes or depreciation; the data are benchmarked every ten years from 1960 to 2000, and after 2000 rents follow a BLS rent index and prices the FHFA index.
  - After 2000Q2 (vet `p30data/rentprice-verify`; step 3 `p30build/dlmext`): rows 165 to 236 of 'rent-price data' chain
    rent and price by pure index ratios from the 2000Q2 benchmark (formula B165 = B164 times the ratio of consecutive rows
    of 'BLS CSW OFHEO index data' column B), with no quality drift. That sheet's column B is the three-month mean of
    monthly CUSR0000SEHC01; column D holds FHFA purchase-only, seasonally adjusted, US values typed in. The 2008 paper
    (printed p. 283) extrapolated with an assumed quality drift instead, so the design's no-drift statement rests on the
    workbook's formulas, not on the paper.
- Universe: the aggregate stock of owner-occupied housing in the United States, as a ratio of averages (value-weighted);
  mobile homes excluded from the census benchmarks.
- Traps:
  - The workbook's average prices at the census quarters differ from the paper's Table 1 averages (1970Q2: 21,184.19
    against $20,867) while its rents agree; the file, not Table 1, is the series used (vet).
  - The average price falls 3.5 percent in nominal terms from 1969Q4 to 1970Q3 while rent rises; before Freddie Mac's
    CMHPI starts in 1970 the price path follows median new-home prices (paper footnote 9) (vet). R3 reads no quarter
    before 1972.
  - DLM's hedonic rent model has building age, bedrooms, metropolitan area and state, and no structure type or room
    count (paper p. 281) (vet).
  - The FHFA and OER values inside the workbook are 2018 vintages. Its 73 FHFA values equal the seasonally adjusted US
    column of FHFA's `HPI_PO_summary.xls` as archived on 2018-09-17, and its OER months 2000-01 to 2018-05 equal
    CUSR0000SEHC01 in BLS's `cu.data.0.Current` as archived on 2018-06-23 (221 of 221); both captures are now stored
    (section 18). In the current vintages the purchase-only index grew 2.9 percent less from 2000Q2 to 2018Q2 and OER
    0.01 percent less (step 3). R3 keeps the workbook's values through 2018Q2.
  - AEI's housing terms give no licence to re-host the workbook; it stays in the git-ignored `data/`, and the post
    names the AEI Housing Center as the data source with no relationship implied.

### 2.2 Extension after 2018Q2: OER and FHFA purchase-only, seasonally adjusted

- Files:
  - `data/bls_cu_data_12_ushousing_ia20261029154324.txt` (2,708,166 bytes; sha256 b2ecc4021ea612ee9acf3629f2cbcfc7e1b063338ee5ede5ae10d74512019704).
    Publisher: U.S. Bureau of Labor Statistics, CPI LABSTAT database. URL:
    https://download.bls.gov/pub/time.series/cu/cu.data.12.USHousing. Transport: Internet Archive capture
    20261029154324, served gzip (389,500 bytes; sha256 220ce77eea98b761a7ebd8cfa80f31d46cdcf737ebdb6f8d2868cc37bb8e5372),
    stored decompressed; the archived bytes match the capture's CDX digest. Retrieved 2026-11-13T10:40:18Z
    (`p30data/indexes` dl-41).
  - `data/fhfa_hpi_po_us_and_census.txt` (38,749 bytes; sha256 4776cd3261d1a5ba71701d2fd7c934184d86494b7b2332ba6b20afa63fae1fea).
    Publisher: Federal Housing Finance Agency. URL: https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_us_and_census.txt.
    Transport: direct. Retrieved 2026-11-13T10:36:08Z (`p30data/indexes` dl-13; the verifier fetched the same bytes at
    11:01:24Z).
- Coverage: CUSR0000SEHC01, monthly 1983-01 to 2026-09, 524 of 525 months published (2025-10 is '-' with footnote X),
  December 1982 = 100, one decimal through 2006 and three from 2007. The FHFA file is tab-separated, with header fields
  division, year, qtr, index_po_not_seasonally_adjusted and index_po_seasonally_adjusted; USA 1991Q1 to 2026Q2 (142
  quarters, no gaps) plus nine census divisions; 1991Q1 = 100. It is the vintage whose last quarter is 2026Q2.
- Definitions:
  - **CUSR0000SEHC01** (`sources/bls_ia20261021074323_cu.series`, LABSTAT cu.series, row CUSR0000SEHC01; FOUND): "Owners' equivalent rent of primary residence in U.S. city average, all urban consumers, seasonally adjusted"
  - **What OER measures** (`sources/bls_ia20261107234217_calculation.htm`, BLS Handbook of Methods, CPI, Calculation, 'Estimation of price change for shelter'; FOUND): "In essence, OER measures the change in the amount a homeowner would pay in rent or earn from renting his or her home in a competitive market."
  - **OER uses rents without utilities** (`sources/bls_ia20261107234217_calculation.htm`, same section, 'Six-month chained estimator'; FOUND): "The OER estimator uses the change in the pure rent which excludes the cost of any utilities included in the rent contract."
  - **Seasonal factors revised** (`sources/bls_ia20261107234217_calculation.htm`, 'Calculation of seasonally adjusted indexes', 'Revision'; FOUND): "Each year in February, BLS recalculates and publishes revised seasonally adjusted indexes for the previous 5 years."
  - **Aging adjustment** (`sources/bls_ia20261107234217_calculation.htm`, 'Aging adjustment'; FOUND): "The aging adjustment accounts for the small loss in quality as housing units age (or depreciate) between interviews."
  - **October 2025** (`sources/bls_shutdown-cpi-faq_ia20261110081902.htm`, question 2, extract line 240; FOUND): "Rents for October 2025 were carried forward from April 2025, yielding unchanged index values for rent and owners’ equivalent rent for October."
  - **Footnote X** (`sources/bls_ia20261001052102_cu.footnote`, LABSTAT cu.footnote, code X; FOUND): "Data unavailable due to the 2025 lapse in appropriations"
  - **OER weights each January** (`sources/bls_ia20260819121638_rent-oer-information.htm`, BLS notice on rent and OER weights, extract line 215; FOUND): "These data are updated annually effective with the January index."
  - **Purchase-only sample** (`sources/fhfa_faqs_hpi.html`, FHFA HPI FAQ, question 8, extract line 192; FOUND): "We base the Purchase-Only FHFA HPI on transactions for single-family properties involving conforming, conventional mortgages purchased or securitized by Fannie Mae or Freddie Mac."
  - **Exclusions** (`sources/fhfa_faqs_hpi.html`, question 8; FOUND): "The sample also excludes data on condominiums, cooperatives, multi-unit properties, and planned unit developments."
  - **Seasonal adjustment** (`sources/fhfa_faqs_hpi.html`, question 16; FOUND): "FHFA uses the Census Bureau’s X-13 autoregressive integrated moving average (ARIMA) procedure, as implemented in the SAS software package."
  - **Revisions** (`sources/fhfa_faqs_hpi.html`, question 13; FOUND): "FHFA revises historical FHFA HPI estimates as additional transaction data become available."
  - **Nominal** (`sources/fhfa_faqs_hpi.html`, question 14; FOUND): "The FHFA HPI is not adjusted for inflation and therefore measures house price changes in nominal terms."
- Universe: OER, all urban consumers, U.S. city average, priced from the rents of sampled rental units reweighted to
  owner-occupied housing; FHFA purchase-only, single-family homes with conforming conventional mortgages purchased or
  securitized by Fannie Mae or Freddie Mac.
- Traps:
  - October 2025 was not collected. Rents were carried forward, so the November and December 2025 OER levels sit about
    one month of growth low, and the catch-up falls in April 2026, after the model's last month (BLS FAQ questions 2, 5
    and 8; step 3). R3 skips the month.
  - Seasonally adjusted OER values for 2022 to 2025 in the frozen file are not final; BLS revises five years each
    February.
  - OER weights have been refreshed every January since 2023.
  - OER is adjusted for unit aging; the FHFA index is not (design section 8).
  - FHFA revises the whole history in each release; the frozen file is the vintage ending 2026Q2 (FHFA's next release
    was due 2026-11-24).
  - The vet's first report printed this FHFA file's sha256 with a typo; the value above is the file's.

## 3. Rent of the same home, level B (R3, R13)

- File (numerator): `data/bea_nipadataa_ia20261020095433.txt` (11,967,684 bytes; sha256 9f8e96bb72181d14d7b555f3e1b09c71e900fb8de4c305dc9217424de4757f27).
  Publisher: U.S. Bureau of Economic Analysis, NIPA annual flat file, 2026 annual-update vintage. URL:
  https://apps.bea.gov/national/Release/TXT/NipaDataA.txt. Transport: Internet Archive capture 20261020095433
  (apps.bea.gov/national/ is closed to crawlers by its robots file). Retrieved 2026-11-13T10:36:15Z (`p30data/carrying`
  dl-01; the same bytes at `p30data/rentprice` dl-39, 10:43:47Z).
- Coverage of the series the rules read: DOSTRC 1959 to 2025; DOWNRC, B1300C, B2607C and A946RC 1929 to 2025; W307RC and
  W316RC 1946 to 2025; annual, millions of current dollars.
- Denominator: Z.1 FL155035013 (section 4).
- Definitions:
  - **DOSTRC** (`sources/bea_SeriesRegister_2026-09.txt`, NIPA series register, row DOSTRC (Table 2.4.5U line 162); FOUND): "DOSTRC,"Owner-occupied stationary homes","Current Dollars","Level",-6,U20405:162,DOWNRC"
  - **DOWNRC, the parent line** (`sources/bea_SeriesRegister_2026-09.txt`, row DOWNRC; FOUND): "DOWNRC,"Imputed rental of owner-occupied nonfarm housing (21)""
  - **Method** (`sources/bea_nipa_handbook_chapter-05.pdf`, NIPA Handbook ch. 5, printed p. 5-46, PDF p. 46; FOUND): "For owner-occupied dwellings, the rental value is estimated using the rental equivalence approach paired with an owner premium."
  - **Size of the owner premium** (`sources/bea_scb_2021-05_housing_services.htm`, Survey of Current Business, May 2021, extract line 116; FOUND): "the owner premium increases the aggregate imputed rental value of owner-occupied units by 35 to 40 percent of the rental equivalence value in a given year"
  - **Benchmark before 2002** (`sources/bea_scb_2021-05_housing_services.htm`, extract line 97; FOUND): "To estimate the 2001 benchmark AARV, BEA used a rent-to-value approach, which assumed that owner-occupied units with similar values as tenant-occupied units also had similar rent-to-value-ratios."
  - **2002 to 2004** (`sources/bea_scb_2021-05_housing_services.htm`, extract line 107; FOUND): "national estimates for those years are wedged between 2001 and 2005 using the Denton method"
  - **Utilities from 2013** (`sources/bea_scb_2023-11_nea_comprehensive_update.htm`, Survey of Current Business, November 2023, extract line 183; FOUND): "Beginning with 2013, by-unit ACS data on utility costs are used to derive estimates of rent excluding utilities for rental housing that includes utilities and for owner-occupied housing units"
- Universe: imputed rent of nonfarm owner-occupied permanent-site homes (DOSTRC sits under DOWNRC, nonfarm; mobile homes
  are the separate line DOMHRC). The denominator also counts farm houses, second homes that are not rented and vacant
  homes for sale (section 4); R3 calls the scope close, not exact.
- Traps:
  - Method breaks: rental equivalence with an owner premium from 2005; 2002 to 2004 interpolated between methods; a
    rent-to-value benchmark before 2002, with no revisions to national levels before 2002 (SCB May 2021); utilities
    removed by a new method from 2013 (SCB November 2023).
  - The stored NIPA Handbook chapter 5 (December 2024) never mentions the pre-2002 rent-to-value benchmark; only the SCB
    article of May 2021 does (step 3). The design's section 3 cites each for its own part.
  - The flat file is an Internet Archive copy, digest-verified, not a file served directly by BEA (vet).
  - DOWNRC over LM155035015 is a scope check only (R3).

## 4. Federal Reserve Z.1 owner-occupied real estate (R2, R3, R7c)

- Files:
  - `data/frb_z1_csv_2026-09-11.zip` (64,219,006 bytes; sha256 83b8eded0bc7f9b74c0269ef503a863cee88312460fd7eef076284b98fc28c06).
    Publisher: Board of Governors of the Federal Reserve System, Financial Accounts of the United States (Z.1), release
    of 2026-09-11. URL: https://www.federalreserve.gov/releases/z1/data/FRB_Z1_csv.zip. Transport: direct. Retrieved
    2026-11-13T10:40:56Z (`p30data/rentprice` dl-31; the same bytes at `p30data/carrying` dl-12, 10:40:31Z).
  - `data/z1_owner_occupied_extract.csv` (71,150 bytes; sha256 6148186b68d2d404e32ac425689eca0c130fa3282c989616f9bec225ae1efab2):
    written by `extract_z1.py` from the zip, not downloaded; the step-3 critic rebuilt it byte-identical.
- Coverage: the zip holds one member, `Z1.csv`. The extract keeps LM155035015.Q and FL155035013.Q, 305 rows each,
  1945-12-31 to 2026-06-30, millions of dollars, with all four quarter-ends in every year from 1970 to 2025.
- Definitions:
  - **FL155035013** (`sources/frb_fof_series_FL155035013.html`, Financial Accounts Guide, series title; FOUND): "Households; owner-occupied real estate at market value"
  - **FL155035013 from 2001** (`sources/frb_fof_series_FL155035013.html`, Data Source, extract line 295; FOUND): "After 2001Q1, quarterly stocks outstanding estimated by FOF section based on automated valuation model (AVM) data from Zillow and housing count estimates from the American Community Survey of the U.S. Census."
  - **FL155035013 before 2001** (`sources/frb_fof_series_FL155035013.html`, Data Source, extract line 295; FOUND): "Before 2001Q1, biennial stocks outstanding estimated by FOF section based on data from the U.S. Census Bureau's American Housing Survey on the total value of owner-occupied and vacant homes, excluding mobile homes."
  - **FL155035015, of which FL155035013 is a part** (`sources/frb_fof_series_FL155035015.html`, Computed, extract line 295; FOUND): "= + FL155035013 + FL155010103 + FL155012013"
  - **LM155035015** (`sources/frb_fof_series_LM155035015_v2.html`, series title, extract line 291; FOUND): "Households; owner-occupied real estate including vacant land and mobile homes at market value"
  - **Scope, table S14.b line 3, note 2** (`sources/frb_z1_current_S14_b.htm`, extract line 786; FOUND): "All types of owner-occupied housing including farm houses and mobile homes, as well as second homes that are not rented, vacant homes for sale, and vacant land, at market value."
- Universe: households' owner-occupied real estate at market value. FL155035013 leaves out vacant land (FL155010103) and
  mobile homes (FL155012013); both series include farm houses, second homes that are not rented and vacant homes for
  sale.
- Traps:
  - From 2001 the values are Zillow estimates times ACS housing counts; before 2001 they rest on biennial American
    Housing Survey benchmarks.
  - The 2026-09-11 release revised LM155035015 year-end levels in 34 years from 1983 to 2025 against the 2026-06-11
    release (largest 0.34 percent); the package is frozen by its sha256 and vintages are not mixed (vet).
  - Z.1 carries the pre-update NIPA consumption of fixed capital from 2021 (vet); R2 takes depreciation from BEA's
    B2607C, not from Z.1.

## 5. Home value (R2, R14, R15.3)

### 5.1 FHFA House Price Index, all-transactions

- File: `data/fhfa_hpi_at_us_and_census.csv` (43,679 bytes; sha256 580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba).
- Publisher: Federal Housing Finance Agency.
- URL: https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_us_and_census.csv
- Transport and time: direct, downloaded on 2026-11-10 (UTC) for Post 29 (release of 2026-10-27) and copied from
  `genz-house-chase/data/` by the staging script; the vet fetched the same bytes again on 2026-11-13T11:01:23Z
  (`p30data/indexes-verify` dl-04).
- Coverage: comma-separated, no header; fields place, year, quarter, index. USA 1975Q1 to 2026Q2 (206 quarters), not
  seasonally adjusted, nominal; census divisions also present.
- Definitions:
  - **All-transactions** (`sources/fhfa_faqs_hpi.html`, FHFA HPI FAQ, Overview, extract line 176; FOUND): "All-Transactions HPI. Adds appraisal values from refinance mortgages to the Purchase-Only data sample."
  - **Method** (`sources/fhfa_faqs_hpi.html`, question 6, extract line 184; FOUND): "FHFA employs a modified version of the Case-Shiller® index methodology, using a geometric weighted repeat-sales procedure to construct the indexes."
  - **Base period** (`sources/fhfa_faqs_hpi.html`, question 29; FOUND): "Notable exceptions are All-Transactions indexes, for which we maintain original base periods for historical consistency"
  - **Aging between sales** (`sources/fhfa_hpi-technical-description.pdf`, Calhoun (1996), footnote 10, PDF p. 6; FOUND): "differential rates of depreciation for otherwise similar properties are more likely over longer periods of time"
- Universe: single-family properties with conforming conventional mortgages purchased or securitized by Fannie Mae or
  Freddie Mac, priced from repeat sales and refinance appraisals; condominiums, cooperatives, multi-unit properties and
  planned unit developments are excluded (FAQ question 8, section 2.2). Revisions and nominal terms as in section 2.2.
- Traps: refinance appraisals are included (R15.3 swaps in purchase-only from 1991); the index is not adjusted for the
  aging of homes; it includes what owners' improvements add to value (vet), which is why R7c charges improvements from
  1975; FHFA revises it in each release, and the frozen file predates the 2026-11-24 release.

### 5.2 Census constant-quality price index of new single-family houses sold (bridge, 1972 to 1974)

- File: `data/census_nrs_price_sold_cust.xlsx` (52,239 bytes; sha256 9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3).
- Publisher: U.S. Census Bureau and U.S. Department of Housing and Urban Development, Survey of Construction.
- URL: https://www.census.gov/construction/nrs/xls/price_sold_cust.xlsx
- Transport and time: direct, downloaded on 2026-11-10 (UTC) for Post 29 and copied by the staging script; the vet
  fetched the same bytes again on 2026-11-13T11:03:55Z (`p30data/indexes-verify` dl-12).
- Coverage: sheet 'Price Index', titled 'Price Indexes of New Single-Family Houses Sold Including Lot Value', with the
  note '(2005 = 100.0.  Index based on kinds of houses sold in 2005.)'; column B 'Annual index', United States, 1963 to
  2026; quarterly columns are also present (R2 interpolates the annual values).
- Definitions:
  - **Index type** (`sources/census_descpi_sold.pdf`, 'Price index design', PDF p. 1; FOUND): "The Constant Quality Price Indexes of New Single-Family Houses Sold Including Value of Lot are Laspeyres type indexes."
  - **Constant quality** (`sources/census_generalinformationaboutpriceindexes.pdf`, 'Laspeyres Price Index (Constant Quality)', PDF p. 1; FOUND): "How much is the sales price today for the same quality house as in the base year?"
  - **Houses left out** (`sources/census_descpi_sold.pdf`, Introduction, PDF p. 1; FOUND): "owner-built houses, and houses built for rent are not included"
  - **Back to 1963** (`sources/census_cpi_2005.pdf`, 'Construction Price Indexes 2005 Series FAQs', question 5, PDF p. 2; FOUND): "We used a series of rebased indexes to enable us to go back to 1963."
- Universe: new single-family houses built for sale and sold, lot included; contractor-built, owner-built and
  built-for-rent houses are excluded.
- Traps: new houses do not age, so R2 charges depreciation d(y) on the bridge months and R7c charges no improvements
  before 1975; the 1972 to 1974 values rest on rebased earlier series.

### 5.3 FHFA purchase-only, not seasonally adjusted (R15.3)

Column `index_po_not_seasonally_adjusted` of `data/fhfa_hpi_po_us_and_census.txt`, USA from 1991Q1; file, transport and
definitions in section 2.2.

## 6. Depreciation on the bridge years (R2)

- Series: B2607C in `data/bea_nipadataa_ia20261020095433.txt` (section 3), over the four quarter-ends of Z.1
  LM155035015 (section 4).
- Definitions:
  - **B2607C** (`sources/bea_SeriesRegister_2026-09.txt`, row B2607C (Table 7.5 line 19); FOUND): "B2607C,"Owner-occupied housing""
  - **Consumption of fixed capital** (`sources/bea_nipa_handbook_chapter-02.pdf`, NIPA Handbook ch. 2, printed p. 2-10, PDF p. 10; FOUND): "the decline in the value of the stock of assets due to physical deterioration, normal obsolescence, and accidental damage except that caused by a catastrophic event"
  - **Glossary** (`sources/bea_glossary_cfc.html`, BEA glossary, extract line 96; FOUND): "It is the decline in the value of the stock of fixed assets due to wear and tear, obsolescence, accidental damage, and aging."
- Universe: consumption of fixed capital of all owner-occupied housing, farm included (Table 7.5 line 19, under
  'Households and institutions'; step 3).
- Traps: B2607C equals BEA Fixed Assets Table 5.4 line 11, owner-occupied depreciation, exactly in 1970 to 2019 (step
  3); the design's section 7 figure used two year-end values, while R2 uses four quarter-ends.

## 7. Stock market return (R8)

- File: `data/french_ff_factors_csv_2026-09-update.zip` (13,065 bytes; sha256 593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66).
- Publisher: Kenneth R. French Data Library (Fama/French 3 Factors), Tuck School of Business at Dartmouth.
- URL: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/09%202026%20Update/ftp/F-F_Research_Data_Factors_CSV.zip
- Transport and time: direct, the archived cut of the September 2026 update. Retrieved 2026-11-13T11:05:19Z
  (`p30data/stocks-verify` dl-11).
- Coverage: one member, `F-F_Research_Data_Factors.csv`, whose header says it was built from CRSP's 202608 database;
  monthly rows 192607 to 202608 (1,202 months) with columns Mkt-RF, SMB, HML and RF in percent, then annual rows; the
  last line is the copyright line of Eugene F. Fama and Kenneth R. French.
- Definitions:
  - **Mkt-RF** (`sources/french_f-f_factors.html`, 'Description of Fama/French Factors', construction of Rm-Rf, extract line 112; PARAPHRASE): the value-weight return of all CRSP firms incorporated in the US and listed on NYSE, AMEX or NASDAQ with share code 10 or 11 and good data, minus the one-month Treasury bill rate.
  - **RF** (`sources/french_f-f_factors.html`, same entry; PARAPHRASE): the one-month Treasury bill rate, from Ibbotson Associates through May 2024 and from the ICE BofA US 1-Month Treasury Bill Index from June 2024.
  - **Dividends** (`sources/french_data_library.html`, Data Library page, opening notes, extract line 40; PARAPHRASE): since the move to CRSP's CIZ format, monthly returns compound daily returns with dividends reinvested on their ex-dates; legacy files reinvested at month end.
  - **The archived cut** (`sources/french_f-f_factors_archive.html`, 'Historical Data', extract line 36; PARAPHRASE): earlier cuts are kept once a year; the list starts with the August 2026 data, the cut pinned here.
  - **NASDAQ in CRSP** (`sources/crsp_us_stock_databases.html`, item 'Exchange Coverage' in the page's embedded data, not in the text extract; PARAPHRASE): NASDAQ data series begin on December 14, 1972.
- Universe: US-incorporated common stocks on NYSE, AMEX and NASDAQ in CRSP; R8's market return is Mkt-RF plus RF.
- Traps: NASDAQ enters only from 1972-12-14, so the months through December 1972 cover NYSE and AMEX alone (vet); firms
  listed only on NYSE Arca or Cboe BZX are outside the universe; French archives one cut a year, and the archived August
  2026 cut equals the current file in all 668 months from 1971-01 to 2026-08 (vet); the January 2025 move from CRSP's
  FIZ to CIZ files changed 429 of 648 months from 1971 to 2024 by up to 0.15 point, so earlier downloads do not
  reproduce (vet); the T-bill source changed in June 2024; the raw file is not redistributed.

## 8. Fund fee (R8, R15.4)

- File: `data/ici_per32_01_data.xlsx` (142,333 bytes; sha256 d6fd8052b5621288194a79665d8e2d74cb977922a6628f03b849c64a3f5c2d70).
- Publisher: Investment Company Institute (ICI), data workbook of 'Trends in the Expenses and Fees of Funds, 2025'
  (ICI Research Perspective 32(1), March 2026).
- URL: https://www.ici.org/files/2026/per32-01-data.xlsx
- Transport and time: Internet Archive capture 20260325214944, retrieved 2026-11-13T10:45:09Z (`p30data/stocks`
  dl-38); the same bytes are the gunzipped body of capture 20260328185035 (`p30data/stocks` dl-37).
- Coverage: sheet 'S3', Figure S3 'Asset-Weighted and Simple Average Expense Ratios for Actively Managed and Index Mutual
  Funds', percent; column E 'Index equity', 'Asset-weighted average', 1996 to 2025 (30 years, no blanks).
- Definitions:
  - **Index equity mutual fund expense ratio** (`sources/ici_per32-01_ia20261103124156.pdf`, section on index mutual funds, printed p. 8, PDF p. 10; PARAPHRASE): ICI reports asset-weighted average expense ratios of index equity mutual funds; the yearly values sit in Figure S3 of the data workbook.
  - **Averages, not benchmarks** (`sources/ici_per32-01_ia20261103124156.pdf`, note 2, printed p. 14, PDF p. 16; PARAPHRASE): the figures give general information on average fees and are not meant as a benchmark for one investor's or one fund's fees.
  - **Vanguard 500 first expense ratio (R15.4)** (`sources/vanguard_50_facts.html`, '50 years. 50 facts.', fact 38, extract line 95; PARAPHRASE): the fund's initial annual operating expenses were 0.43% of average net assets.
- Universe: index equity mutual funds, asset-weighted (the S3 sheet carries no exchange-traded funds).
- Traps: ICI's averages are not a benchmark for one investor, so using one as the renter's fee is a modelling choice
  (design section 8); 1972 to 1995 carry the 1996 value (R8); no index fund was open to individuals before 1976-08-31
  (section 16); the vet first cited ICI's index-fund section as p. 6, but it starts on printed p. 7 (PDF p. 9); Vanguard 500
  Investor Shares are closed to new investors, and its Admiral and ETF shares cost less (vet).

## 9. Property tax (R7a, R15.5, R15.6)

### 9.1 Annual and American Housing Surveys, 1973 to 2003

- Files: 21 report PDFs in `data/ahs/` (`h150-73C.pdf`, `h150-74C.pdf`, `h150-75c.pdf` to `h150-81c.pdf`,
  `h150-83c.pdf`, `h150-85.pdf`, `h150-87.pdf`, `h150-89.pdf`, `h150-91.pdf`, `h150_93.pdf`, `h150_95rv.pdf`,
  `h150-97.pdf`, `h150-99-rv.pdf`, `h150-01.pdf`, `h150-03.pdf`, `h150-05.pdf`), the 2005 Table 3-13 workbook
  `ahs2005_tab3-13.xls` (a cross-check only) and `ahs_values.csv`. Bytes and sha256 of each: Appendix A.
- Publisher: U.S. Census Bureau, Current Housing Reports Series H-150 (Annual Housing Survey, 1973 to 1983; American
  Housing Survey for the United States, 1985 to 2005), sponsored by HUD.
- URLs: https://www2.census.gov/prod2/ahsscan/ followed by the file name for 1973 to 1991;
  https://www.census.gov/content/dam/Census/library/publications/YEAR/demo/ followed by the file name for 1993 to 2005
  (YEAR is the publication year, 1995 to 2006); the 2005 workbook at
  https://www2.census.gov/programs-surveys/ahs/2005/tables/tab3-13.xls. Each file's URL is in Appendix A.
- Transport and time: direct. Step 3 downloaded 19 volumes on 2026-11-14 between 01:58:46Z and 02:10:47Z
  (`p30build/ahs` dl-01 to dl-38); the 1975 and 1980 volumes and the 2005 workbook are the vet's (2026-11-13T11:35:52Z,
  11:37:11Z and 11:38:41Z).
- Coverage: the 1973 to 1991 volumes are scans with no text layer; 1993 to 2005 carry a text layer. Values read
  (`ahs_values.csv`, 10,214 bytes, sha256 bd053dbc9ed39abee158f94fb97871515af66f2b6e92f0ecd3808ffa53d987c3, written by
  step 3): mean real estate taxes per $1,000 value, Part C Table A-1, United States, TOTAL column, 1974 to 1983, and for
  1973 the same row, column and universe in Table A-2 (printed p. 22, PDF p. 50; A2); the median per $1,000 value,
  Table 3-13, 1985 to 2005, odd years; the 2005 median property insurance per month (section 10). Each value was read
  from a 200 dpi render by two independent readers and an adjudicator, and all three agree (step 3, `p30build/ahs`,
  `ahs-2`, `ahs-3`).
- Definitions: section 17 records the real-estate-tax entry of each volume's Appendix A. Two more:
  - **How the mean was computed** (`data/ahs/h150-83c.pdf`, Introduction, 'Derived figures', printed p. X, PDF p. 10; MANUAL): "The mean real estate taxes last year is rounded to the nearest dollar and is computed on the basis of the distribution as tabulated."
  - **Survey years** (`sources/census_ahs-introduction-history.html`, 'Introduction and History of the AHS Survey', Historical Background and Outlook; FOUND): "The survey was conducted on an annual basis from 1973 to 1981. ... Since 1983, the AHS data collection period lasted for about 5 months and was conducted every two years."
- Universe: see section 17. In short: 1973 to 1983, the mean over specified owner-occupied homes (one-family homes, then
  one-unit structures, on less than 10 acres with no business on the property; cooperatives, condominiums and mobile
  homes excluded from 1976), with units paying no tax left out of the mean; 1985 to 2005, the median over all
  owner-occupied units, mobile homes included, with units paying no tax in the lowest bin (the six bins sum to the
  owner-occupied total within one thousand in every year; step 3).
- Traps:
  - 1973: Table A-1 has no real-estate-tax row; the value comes from Table A-2 (A2).
  - 1982: no national survey was conducted (Census history page; no H-150-82 volume); 1982 is a straight-line year (A2).
  - The PDF metadata of `h150-83c.pdf` says Part B, but its cover reads Part C, Financial Characteristics.
  - 1995 and 1999 are revised editions (H150/95RV; H150/99-RV with its errata notice of April 2003, whose list does not
    name taxes per $1,000 value or property insurance).
  - The 1999-RV pages carry a faint diagonal 'CENSUS CONFIDENTIAL DISCLOSURE PROHIBITED' stamp, and its text layer
    lacks lines 50 and 51 of Table 3-13 on PDF p. 156; the 1999 value was read from the image.
  - Table 3-13 weighting notes: none for 1985 to 1989; 'Consistent with the 1990 Census' for 1991 to 2001; Census 2000
    weighting for 2003 and 2005. The 1991 report also has tables consistent with 1985 to 1989 (not read).
  - Table 3-13's first column is headed 'Total occupied units' but holds the owner-occupied total.
  - Values are whole dollars per $1,000 of value, so each carries up to 0.5 per $1,000 of rounding.
  - Every volume's definition and universe as printed: section 17.

### 9.2 American Community Survey 1-year, 2005 to 2025

- Files: 98 in `data/acs/` (Appendix A): for 2005 to 2019, the year's summary-file sequence zips as downloaded (two a
  year, three in 2013), each with its estimate member extracted unchanged (the build reads the members), and the year's
  geography file; for 2021 to 2025, the table-based `.dat` files (B25090 and B25082 each year; B25077 for 2021, 2022,
  2023 and 2025; B25103 for 2025) and the year's Geos file; and `acs_positions.csv` (30,369 bytes; sha256 03d07a97de59164c51c1aa76f1b737c9fc4c2841d365f019d74b0e434bf8242a;
  written by step 3 with 43 positions, read back 43 of 43; the 29 positions of open item 1 added on 2026-11-14, 72 in
  all, read back 72 of 72 by `profile_data.read_acs`). There is no 2020 file (no standard 1-year release).
- Publisher: U.S. Census Bureau, American Community Survey.
- URLs: under https://www2.census.gov/programs-surveys/acs/summary_file/ (each file's URL in Appendix A).
- Transport and time: direct. 31 files are the vet's downloads of 2026-11-13 between 10:48:17Z and 11:31:32Z, reused
  after their sha256 matched the vet's logs (seven of them are estimate members extracted from the vet's zips); the other
  66 were downloaded by step 3 on 2026-11-14, 40 between 02:04:01Z and 02:04:37Z and 26 between 14:51:49Z and
  14:52:55Z (13 zips, `p30build/acs2` dl-01 to dl-13, and their estimate members).
- Cells recorded in `acs_positions.csv`: B25090_001 for 2010 to 2025; B25082_001 for 2005 to 2025; B25077_001 for
  2005 to 2019, 2021, 2022, 2023 and 2025; B25103_001 for 2005 to 2019, and B25103_001 to _003 for 2025. United States
  row: LOGRECNO 0000001 in the sequence files, GEO_ID 0100000US in the table-based files.
- Definitions:
  - **B25090** (`sources/census_acs2010_Sequence_Number_and_Table_Number_Lookup.txt`, ACS 2010 lookup, line 31711 (sequence 150, start 171); FOUND): "MORTGAGE STATUS BY AGGREGATE REAL ESTATE TAXES PAID (DOLLARS)"
  - **B25082** (`sources/census_acs2005_Chapter_5_tables_summary_list.xls`, ACS 2005 table list, sheet Tables_Summary_List; FOUND): "AGGREGATE VALUE (DOLLARS) BY MORTGAGE STATUS"
  - **B25077** (`sources/census_acs2005_Chapter_5_tables_summary_list.xls`, row 2018 (sequence 0131, start 83); FOUND): "MEDIAN VALUE (DOLLARS)"
  - **B25103** (`sources/census_acs2005_Chapter_5_tables_summary_list.xls`, row 2072 (sequence 0132, listed start 163; true field 161, because the list gives B25097, B25099 and B25103 four cells each where the file holds three, so B25103 sits two fields earlier than listed; the checks are in the 2005 B25103_001 row of `acs_positions.csv`); FOUND): "MORTGAGE STATUS BY MEDIAN REAL ESTATE TAXES PAID (DOLLARS)"
  - **Universe of all four tables** (`sources/census_ACS20251YR_Table_Shells.txt`, 2025 table shells, rows B25077, B25082, B25090 and B25103; FOUND): "Owner-occupied housing units"
  - **Real estate taxes** (`sources/census_2025_ACSSubjectDefinitions.pdf`, 2025 Subject Definitions, 'Real Estate Taxes', p. 36; FOUND): "The statistics from this question refer to the total amount of all real estate taxes on the entire property (land and buildings) payable to all taxing jurisdictions, including special assessments, school taxes, county taxes, and so forth."
  - **Unpaid and delinquent taxes** (`sources/census_2010_ACSSubjectDefinitions.pdf`, 2010 Subject Definitions, 'Real Estate Taxes', p. 28; FOUND): "Real estate taxes include state, local, and all other real estate taxes even if delinquent, unpaid, or paid by someone who is not a member of the household. However, taxes due from prior years are not included."
  - **Question unchanged since 1996** (`sources/census_2008_ACSSubjectDefinitions.pdf`, 2008 Subject Definitions, 'Real Estate Taxes', p. 20; FOUND): "Since 1996, the American Community Survey questions have been the same."
  - **Value** (`sources/census_2025_ACSSubjectDefinitions.pdf`, 'Value', p. 53; FOUND): "Value is the respondent's estimate of how much the property (house and lot, mobile home and lot (if lot owned), or condominium unit) would sell for if it were for sale."
  - **Aggregate value from 2008** (`sources/census_2008_ACSSubjectDefinitions.pdf`, 'Value', p. 29; FOUND): "Aggregate value is calculated by adding all of the value estimates for owner occupied housing units in an area."
  - **Aggregate value through 2007** (`sources/census_2007_ACSSubjectDefinitions.pdf`, 2007 Subject Definitions, 'Value', p. 27; FOUND): "To calculate aggregate value, the amount assigned for the category “Less than $10,000” is $9,000."
  - **The 2008 question change** (`sources/census_2008_ACSSubjectDefinitions.pdf`, 'Value', p. 29; FOUND): "Changes introduced in 2008 were removing the pre-coded response categories and adding a write-in box for the respondent to enter the property value amount in dollars"
  - **Comparability 2007 to 2008** (`sources/census_2008_ACSSubjectDefinitions.pdf`, 'Value', p. 29; FOUND): "the changes may introduce an inconsistency in the data produced for this question as observed from the years 2007 to 2008"
- Universe: all owner-occupied housing units, mobile homes and condominium units included.
- Traps:
  - B25090 is not in the 1-year summary files before 2010: each year's lookup (all stored, section 18) lists B25103 but
    no B25090 for 2005 to 2009. A2 uses the ratio of medians (B25103 over B25077) for 2005 to 2009; see open item 1.
  - 2005 aggregates are printed in E-notation with eight significant digits.
  - The 2005 table list overstates the cell counts of B25088 and B25092, so fields listed after start 165 sit one to
    two fields earlier than listed; the two cells read (fields 83 and 106) come before that point and were confirmed by
    content (step 3).
  - Value was collected in 19 categories through 2007, with $1,250,000 assigned to the top category for aggregates, and
    as a write-in amount from 2008; aggregates are rounded to the nearest hundred dollars.
  - The standard distribution for median real estate taxes has no zero cell, while 5.3 percent of owners reported no
    real estate taxes in 2025; whether the medians exclude them is not stated (vet).

## 10. Insurance (R7b, R15.5, R15.6)

- Files: the three NAIC reports in `data/costs/` (Appendix A; byte-identical copies sit in `sources/`), the AHS 2005
  volume `data/ahs/h150-05.pdf` with its Table 3-13 workbook, and ACS B25077 (2005, 2021 to 2023) and B25082 (2023)
  (section 9.2).
- NAIC publisher: National Association of Insurance Commissioners, 'Dwelling Fire, Homeowners Owner-Occupied, and
  Homeowners Tenant and Condominium/Cooperative Unit Owner's Insurance Report', data years 2021 (December 2023 edition),
  2022 (May 2025) and 2023 (July 2026).
- URL: https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf (one address, three
  editions over time).
- Transport and time: Internet Archive captures 20240217020958, 20250706013631 and 20261011104807; each file's base32
  SHA-1 equals its capture's CDX digest. Retrieved 2026-11-13T11:31:11Z, 11:31:09Z and 11:23:25Z (`p30data/carrying-verify`
  dl-45, dl-44 and dl-27).
- Coverage: Tables 1 to 5, all states, the District of Columbia and countrywide. Used: Table 4, countrywide, the HO-3
  column of the Total row, Average line (data year 2021 printed p. 28, PDF p. 32; 2022 printed p. 31, PDF p. 34; 2023
  printed p. 31, PDF p. 34), and the 2023 written premium by form (printed pp. 31 and 32, PDF pp. 34 and 35); the values
  are in `data/costs/cost_values.csv` (section 12).
- Definitions:
  - **Average premium** (`sources/naic2023_naic_hmr_zu_homeowners_report_ia20261011104807.pdf`, Data section and footnote 1, printed p. 1, PDF p. 4; PARAPHRASE): written premium divided by written exposure, counted in house-years, one house-year being one home insured for twelve months.
  - **Owner-occupied forms** (`sources/naic2023_naic_hmr_zu_homeowners_report_ia20261011104807.pdf`, printed pp. 1, 3 and 4, PDF pp. 4, 6 and 7; PARAPHRASE): the homeowners owner-occupied forms are HO-1, HO-2, HO-3, HO-5 and HO-8; dwelling fire (DW) is a separate policy type in Table 4; tenant (HO-4) and condominium unit owner (HO-6) forms are in Table 5.
  - **What the data cover** (`sources/naic2023_naic_hmr_zu_homeowners_report_ia20261011104807.pdf`, printed pp. 1 to 3 and 6, PDF pp. 4 to 6 and 9; PARAPHRASE): the data come from statistical agents and may miss smaller ones; since data year 2011, residual-market supplemental policies add premium but no exposure and are coded HO-3 when the underlying form is unknown; negative and zero cells are included in the Table 4 totals.
  - **AHS property insurance** (`data/ahs/h150-05.pdf`, Appendix A, 'Property insurance', printed p. A-22, PDF p. 533; FOUND): "This item refers to insurance on the structure and/or its contents (such as furniture, appliances, or clothing) and usually contains some liability insurance."
  - **AHS cost basis** (`data/ahs/h150-05.pdf`, Appendix A, 'Property insurance', printed p. A-22, PDF p. 533; FOUND): "The total cost is the most recent yearly cost for which the occupants have actually been billed. Yearly cost was divided by 12 before calculating a monthly median cost."
- Universe: NAIC, countrywide written premiums and exposures reported through statistical agents (Texas and California
  through their insurance departments). AHS 2005: the median monthly property insurance is over the 70,192 thousand
  owners who pay property insurance, out of 74,931 thousand owner-occupied units (Table 3-13, printed p. 150, PDF p. 166;
  the same in the 2005 workbook).
- Traps:
  - The 2023 premium of the five owner-occupied forms is not printed as one figure. It is the sum of the five printed form
    totals, 123,914,695,878, which equals the printed Total column (126,074,901,951) less dwelling fire (2,160,206,073);
    R15.5 names the five forms (A2).
  - HO-6 (condominium unit owners) is outside Table 4, while the ACS aggregate value includes condominium units.
  - The averages include residual-market supplemental premium without exposure, coded HO-3.
  - Each HO-3 average also appears on other pages of its report, so a bare text search is ambiguous; the values were
    pinned by table layout (step 3).
  - iota_late divides a mean premium by a median value (vet); iota_2005 combines two surveys.
  - NAIC copyright: individual figures are cited, no table is reproduced.

## 11. Upkeep (R7c, R15.5, R15.6)

- Files: the NIPA flat file (section 3); the three BEA Fixed Assets files in `data/bea/`; Z.1 LM155035015 (section 4);
  and, for R15.5, `data/costs/census_ahs2023_table_specs_puf_estimates.xlsx`.
- BEA Fixed Assets files: publisher U.S. Bureau of Economic Analysis, Fixed Assets accounts, 2024 annual-update vintage
  (data 1925 to 2023). URLs: https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt,
  https://apps.bea.gov/national/FixedAssets/Release/TXT/SeriesRegister.txt and
  https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx. Transport: Internet Archive captures
  20250202204946, 20250207173438 and 20250202204948; each file's base32 SHA-1 equals its CDX digest. Retrieved
  2026-11-14T02:04:27Z, 02:04:29Z and 02:04:31Z (`p30build/bea`).
- Coverage: FA Table 5.1 lines 1 to 12, among them line 1 k1x53101es00, line 2 k1r53101es00, line 11 k1r53101esoo and
  line 12 k1x53101estx; 1925 to 2023; millions of current dollars, year-end. The workbook's 1,188 cells of lines 1 to 12
  equal the flat file, and its sheet reads 'File created Sep 19 2024'.
- AHS 2023 workbook: publisher U.S. Census Bureau, 'AHS 2023 Table Specifications and PUF Estimates for User
  Verification'. URL: https://www2.census.gov/programs-surveys/ahs/2023/AHS%202023%20Table%20Specifications%20and%20PUF%20Estimates%20for%20User%20Verification.xlsx.
  Transport: direct. Retrieved 2026-11-13T11:28:06Z (`p30data/carrying-verify` dl-39). Used: sheet 'Home Improvement'
  (Table C-15-OO) cell E22 and sheet 'Value, Price' (Table C-13-OO) cell F21, the Table Creator estimates.
- Definitions:
  - **B1300C** (`sources/bea_SeriesRegister_2026-09.txt`, row B1300C (Table 7.4.5 line 9); FOUND): "B1300C,"Owner-occupied","Current Dollars","Level",-6,T70405:9,B499RC"
  - **Why intermediate inputs are deducted** (`sources/bea_nipa_handbook_chapter-12.pdf`, NIPA Handbook ch. 12, printed p. 12-7, PDF p. 7; FOUND): "Housing-related expenses are deducted because they are considered intermediate inputs to the production of rental services"
  - **What the inputs hold** (`sources/bea_RIPfactsheet.pdf`, Mayerhauser and Reinsdorf (BEA, 2007), Table A note 2, PDF p. 4; FOUND): "Includes expenses such as maintance and repairs, property insurance, brokers' commissions on land, closing costs, and property management fees."
  - **W307RC** (`sources/bea_SeriesRegister_2026-09.txt`, row W307RC (Table 7.11 line 88); FOUND): "W307RC,"Owner-occupied housing""
  - **Borrower services enter as negatives** (`sources/bea_ia20251206172244_Section7All_xls.xlsx`, sheet T71100-A, Table 7.11 note, row 132; FOUND): "these services are included as negative amounts paid by the borrowers and received by the financial intermediaries"
  - **W316RC** (`sources/bea_SeriesRegister_2026-09.txt`, row W316RC (Table 7.11 line 65); FOUND): "W316RC,"Owner-occupied housing""
  - **Premium supplements** (`sources/bea_ia20251206172244_Section7All_xls.xlsx`, sheet T71100-A, Table 7.11 note, row 132; FOUND): "premium supplements paid to property and casualty insurance carriers by households and institutions"
  - **Premium supplements, Handbook** (`sources/bea_nipa_handbook_chapter-05.pdf`, printed p. 5-63, PDF p. 63; FOUND): "Premium supplements equal the expected investment income on technical reserves, including capital gains."
  - **BEA's former line 157** (`sources/bea_ia20220703151550_FlatFiles.ZIP`, member SeriesRegister.txt, row Y681RC (Table 7.12 line 157); FOUND): "Intermediate inputs excluding imputations (155-156)"
  - **Owner-occupied borrower services** (`sources/bea_ia20220703151550_FlatFiles.ZIP`, member SeriesRegister.txt, row W546RC (Table 7.12 line 180); FOUND): "W546RC,"Of which: Owner-occupied housing""
  - **A946RC** (`sources/bea_SeriesRegister_2026-09.txt`, row A946RC (Table 5.4.5 line 46); FOUND): "A946RC,"Improvements""
  - **Residential improvements** (`sources/bea_nipa_handbook_chapter-06.pdf`, NIPA Handbook ch. 6, note 14, printed p. 6-6, PDF p. 6; FOUND): "consist of additions, alterations, and major replacements to structures subsequent to their completion ... routine maintenance and repair work is not included"
  - **FA Table 5.1** (`data/bea/bea_fa_section5all_ia20250202204948.xlsx`, sheet FAAt501-A, rows 1 and 2; FOUND): "Table 5.1. Current-Cost Net Stock of Residential Fixed Assets by Type of Owner, Legal Form of Organization, and Tenure Group ... [Millions of dollars; yearend estimates]"
  - **Tenure lines' footnote** (`data/bea/bea_fa_section5all_ia20250202204948.xlsx`, sheet FAAt501-A, row 24; FOUND): "Excludes other residential fixed assets, which consist primarily of dormitories and of fraternity and sorority houses."
  - **Line 11** (`data/bea/bea_fa_seriesregister_ia20250207173438.txt`, row k1r53101esoo; FOUND): "k1r53101esoo,"Owner-occupied","Current Dollars","Level",-6,FAAt501:11,k1x53101es00"
  - **Line 2** (`data/bea/bea_fa_seriesregister_ia20250207173438.txt`, row k1r53101es00; FOUND): "k1r53101es00,"Residential","Current Dollars","Level",-6,FAAt101:8|FAAt501:2,k1ptotl1es00|k1x53101es00"
  - **Owner-occupied residential assets** (`sources/bea_Fixed_Assets_1925_97_ia20251125021830.pdf`, BEA, Fixed Assets and Consumer Durable Goods in the United States, 1925 to 97 (2003), printed p. M-38, PDF p. 41; FOUND): "Owner-occupied residential assets consists of housing occupied by private owners."
  - **Tenant-occupied residential assets** (`sources/bea_Fixed_Assets_1925_97_ia20251125021830.pdf`, printed p. M-38, PDF p. 41; FOUND): "Tenant-occupied residential assets consists of rental housing, including all government-owned residential assets."
  - **AHS 2023 routine maintenance** (`sources/census_ahs2023_definitions.pdf`, 2023 AHS Appendix A, printed p. A-42, PDF p. 42; FOUND): "Routine maintenance consists of regular maintenance activities necessary for the preventive care of the structure, property, and fixed equipment items."
  - **AHS 2023 value** (`sources/census_ahs2023_definitions.pdf`, 'Value', PDF p. 51; FOUND): "Value is the respondent’s estimate of how much the property (house and lot) would sell for if it were for sale."
  - **AHS 2023 rows used** (`data/costs/census_ahs2023_table_specs_puf_estimates.xlsx`, sheet 'Home Improvement' cells A22 to C22 and sheet 'Value, Price' cells A21 to C21; FOUND): "Routine Maintenance Costs in Typical Year ... MAINTAMT ge 0 ... MARKETVAL ge 0"
  - **Rounded estimates** (`data/costs/census_ahs2023_table_specs_puf_estimates.xlsx`, sheet 'Home Improvement' cell G22; FOUND): "Noise added to PUF; Medians and means rounded to 4 significant digits in Table Creator"
- Universe: DOWNRC and B1300C are nonfarm owner-occupied housing; W307RC and W316RC are attributed to all owner-occupied
  housing; A946RC is private residential improvements of all tenures; the share is Table 5.1 line 11 over line 2
  (private), year-end of year y (A2); LM155035015 covers all owner-occupied real estate including vacant land and
  mobile homes. AHS 2023: owner-occupied units (INTSTATUS 1, TENURE 1); the maintenance mean covers units that reported an
  amount (MAINTAMT ge 0) and the value mean units with a value (MARKETVAL ge 0).
- Traps:
  - W307RC is published negative and is added as published; its absolute value would add the borrower services instead
    of removing them (step 3).
  - NIPA Handbook ch. 12 (p. 12-9) lists imputed bank service charges among expenses deducted only from tenant-occupied
    housing, while the 2022 Table 7.12 puts owner-occupied borrower services inside owner-occupied intermediate inputs;
    taking the imputed services out, as R7c does, leaves the routine line clear of the conflict (step 3).
  - The routine line still holds property insurance, closing costs, loan fees and brokers' commissions on land, which
    R5, R6 and R7b also charge (design section 8).
  - The Fixed Assets file is the 2024 vintage, two annual updates behind the NIPA file; no archived vintage has the
    tenure table for 2024 or 2025, so those years hold the 2023 share (A2). Against the 2026 Fixed Assets vintage, the
    private residential net stock is revised by +0.03, -0.73, -1.17 and -0.28 percent in 2020 to 2023 (step 3).
  - In Table 5.1, lines 9 plus 10 exceed line 8 by up to $778 million (2023); lines 1, 2, 11 and 12 are unaffected.
  - AHS 2023: both cells are Table Creator estimates rounded to four significant digits (yellow cells); the PUF column
    of 'Value, Price' shows a median and mean that look transposed and a dropped digit in row 15, so only the Table
    Creator column is used; the maintenance mean leaves out the 9,235 thousand owner units that did not report.

## 12. Buying costs (R5)

- Files: `data/costs/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf` (2,263,304 bytes; sha256
  7aaeadcd06a98abfff9c6c5f957493d2783f19a85752f618efea562867271c58; a byte-identical copy sits in `sources/`) and
  `data/costs/cost_values.csv` (6,578 bytes; sha256 9b5767862bad96824aa0d608867a8f2e42bc9a04a43831c0ba728c97d267974e;
  written by step 3, 24 rows read back from their sources).
- Publisher: Consumer Financial Protection Bureau, Office of Research, '2023 Mortgage Market Activity and Trends'
  (December 2024).
- URL: https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf
- Transport and time: direct, retrieved 2026-11-13T10:40:47Z (`p30data/transaction` dl-31; the verifier fetched the same
  bytes at 11:09:17Z).
- Coverage: Table 3A (p. 28), median loan amount in thousands of dollars, and Table 3D (p. 31), median total loan costs
  in dollars, row 'Enhanced Loan Type(5): Conventional conforming', 2018 to 2023; printed page equals PDF page.
- Definitions:
  - **Total loan costs** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, section 3.2, p. 24; FOUND): "Total loan costs, a data point collected and reported under HMDA since 2018, represent the sum of origination fees that the lender charges, charges for the services that borrowers cannot shop for (e.g., appraisal fees or credit report fees), and charges for services borrowers can shop for such as settlement agent or title insurance fees."
  - **Points included** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, p. 24; FOUND): "Discount points if paid, another data point collected and reported under HMDA beginning in 2018, is also included as a part of the total loan costs."
  - **Buyer-paid only** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, p. 24, footnote 21; FOUND): "It is limited to “buyer-paid” portions of the total loan costs"
  - **Conventional conforming** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, Table 3A note 5, p. 28; FOUND): "whose loan type is reported as conventional and whose loan amount is below the conforming loan limit"
  - **Loans in Tables 3A and 3D** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, NOTE under Tables 3A and 3D, pp. 28 and 31; FOUND): "Closed-end (excluding reverse mortgages) home purchase first-lien mortgages secured by site-built"
  - **Nominal** (`sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf`, p. 22, footnote 19; FOUND): "All dollar amounts are reported in nominal terms."
  - **Loan costs optional for some lenders** (`sources/cfpb_reg_c_1003_3.html`, 12 CFR 1003.3(d)(1)(iii), total loan costs being item (a)(17); FOUND): "(iii) Optional data means the data identified in § 1003.4(a)(1)(i), (a)(9)(i), and (a)(12), (15) through (30), and (32) through (38)."
  - **Loans with no cost field** (`sources/cfpb_reg_c_1003_4.html`, 12 CFR 1003.4(a)(17)(i), official interpretation 1; FOUND): "does not require financial institutions to report the total loan costs for applications, or for transactions not subject to Regulation Z"
- Universe: closed-end, first-lien home-purchase mortgages on site-built one-to-four-family principal residences,
  conventional conforming, from the static HMDA files for 2018 to 2023.
- Traps: Table 3A's medians cover every loan while total loan costs are optional for partially exempt lenders and absent
  for loans outside the Regulation Z requirements, so the two medians may rest on different loan sets (R5 says so);
  lump-sum seller credits and general lender credits are not netted out, and the lender's title policy sits inside loan
  costs at its full premium (vet); total loan costs as a share of the loan fall as loans grow, so a 2018 to 2022 share carried
  back to 1972 is an assumption (design section 8); points sit in both the PMMS series and HMDA total loan costs, which
  is why c_np subtracts the PMMS mean (R5); loan amounts are in thousands of dollars (R1).

## 13. Selling costs (R6, R15.5, R15.6)

No data file: R6 sets 6 percent after Hsieh and Moretti (2003); R15.5 uses 5 percent and R15.6 7 percent.

- **Median selling expenses** (`sources/hm2003_moretti_real-estate19.pdf`, Journal of Political Economy 111(5), printed p. 1082, PDF p. 7; PARAPHRASE): among Consumer Expenditure Survey families who paid a realtor commission, 1980 to 1998, the median commission rate is 6.1 percent, measured with noise.
- **What the survey item is** (`sources/hm2003_moretti_real-estate19.pdf`, footnote 13, printed p. 1085, PDF p. 10; PARAPHRASE): commissions are measured as the survey's total selling expenses, which include expenses other than commissions.
- **The 2024 rule change** (`sources/frb_feds_note_commissions_20250512.html`, Banerjee and Paciorek (2025), FEDS Notes, Introduction, extract line 301; FOUND): "First, sellers' agents can no longer advertise or extend an offer of compensation to buyers' agents through a property listing on an MLS."
- **Since August 2024** (`sources/frb_feds_note_commissions_20250512.html`, Conclusion, extract line 513; FOUND): "since the settlement changes went into place in August 2024, outside estimates suggest that buyer agent commissions may have declined some but have remained at relatively high levels"
- Universe: Consumer Expenditure Survey families who sold a home and paid a realtor commission, 1980 to 1998.
- Traps: the 6.1 percent is total selling expenses, not the commission alone, and covers 1980 to 1998 only; transfer
  taxes and the owner's title policy are assigned to the seller's 6 percent and recording fees enter only R15.6 (R5);
  buyer-paid commissions after August 2024 are 'Other' costs on the closing disclosure, outside HMDA total loan costs
  (vet); REAL Trends commission rates were seen during the vet and are not used.

## 14. CPI rent path for R15.1

- File: `data/bls_cu_data_12_ushousing_ia20261029154324.txt` (section 2.2): CUUR0000SEHA, monthly, every month of 1970
  to 1984 present and the last month 2026-09, October 2025 '-'; CUUR0000SEHC01 from 1982-12 (December 1982 = 100).
- Stored in this step: `sources/bls_ia20250802020823_cw.data.12.USHousing`, the CPI-W counterpart (section 18).
- Definitions:
  - **CUUR0000SEHA** (`sources/bls_ia20261021074323_cu.series`, row CUUR0000SEHA; FOUND): "Rent of primary residence in U.S. city average, all urban consumers, not seasonally adjusted"
  - **CUUR0000SEHC01** (`sources/bls_ia20261021074323_cu.series`, row CUUR0000SEHC01; FOUND): "Owners' equivalent rent of primary residence in U.S. city average, all urban consumers, not seasonally adjusted"
  - **CPI-U from 1978** (`sources/bls_ia20260819181438_why-cpi-w-and-cpi-u.htm`, Beyond the Numbers, February 2014, extract line 199; FOUND): "As part of the 1978 revision, BLS planned to introduce a broader target population, covering all urban consumers (the CPI-U)."
  - **Rental equivalence dates** (`sources/bls_hom_cpi_history_ia20261024112424.htm`, Handbook of Methods, CPI history, extract line 256; FOUND): "Introduced rental equivalence concept in January 1983 for the CPI-U and in January 1985 for the CPI-W"
  - **Aging from 1988** (`sources/bls_hom_cpi_history_ia20261024112424.htm`, entry for 1988; FOUND): "Improved housing estimator to account for aging of the sample housing units"
  - **Size of the aging omission, Handbook** (`sources/bls_ia20261107234217_calculation.htm`, extract line 637; FOUND): "BLS research indicates that annual changes to the residential rent and owners’ equivalent rent indexes would have been 0.1 to 0.2 percent larger if some type of aging adjustment had been included."
  - **Size of the aging omission, MLR 1999** (`sources/bls_mlr1999_06_art4full_ia20260819075117.pdf`, Monthly Labor Review, June 1999, printed p. 32, PDF p. 4; FOUND): "adjusting the residential rent and owners’ equivalent rent indexes upward by about 0.3 percent per year from 1978 to 1987"
  - **1995 estimator** (`sources/bls_mlr1999_06_art4full_ia20260819075117.pdf`, printed p. 32, PDF p. 4; FOUND): "the composite estimator underestimated price changes; therefore, it was replaced by a 6-month chain estimator"
  - **OER, 1987 to 1994** (`sources/bls_treatment-owner-occupied-housing_ia20260819123230.htm`, FESAC paper of December 2005, extract line 378; FOUND): "This average of ratios formula was biased, so it was changed to the ratios of the average pure rents of the matched renters."
  - **Corrections only in the research series** (`sources/bls_r-cpi-u-rs-changes_ia20260819055434.htm`, Table 1 rows for 1985, 1988, 1995 and 2000; FOUND): "Employed new method for imputing price change for rental vacancies ... Rental values in CPI sample were adjusted for aging ... Replaced composite estimator with a 6-month chain estimator. ... Modified imputation of homeowners’ implicit rent to eliminate upward drift property of previous estimator ... To adjust for an error in the calculation of the rent and owners’ equivalent rent indexes for 1999."
- Universe: all urban consumers, U.S. city average; before 1978 BLS priced only for urban wage earners and clerical
  workers (Beyond the Numbers 2014).
- Traps:
  - R15.1's statement that the rent index before 1978 is the wage-earner (CPI-W) index rescaled rests on the vet's
    data check, not on a BLS sentence: monthly CUUR0000SEHA over CWUR0000SEHA stays within 0.99534 to 0.99846 from 1967
    to 1977, computed from the stored CW capture and the CU file (`p30data/indexes-verify`). See open item 3.
  - Before BLS's 1998 item structure, the series now titled 'Rent of primary residence' was 'Residential rent'.
  - BLS revises CPI indexes for collection or processing errors but not for method changes (MLR 1999 footnote 1; vet).
  - October 2025 is '-' (section 2.2); R15.1 chains November to September.

## 15. Dollars for chart 2 (R14)

- `data/census_coh_values_unadj.txt` (4,479 bytes; sha256 5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6).
  Publisher: U.S. Census Bureau, Historical Census of Housing Tables, Home Values. URL:
  https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-values/values-unadj.txt. Transport: direct,
  downloaded on 2026-11-10 (UTC) for Post 29 and copied by the staging script. Coverage: median values in unadjusted
  dollars by census year, 2000 back to 1940 (header on line 3); line 5 is the United States row.
- `data/bls_rcpiurs_allitems_ia20260819.xlsx` (13,916 bytes; sha256 355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8).
  Publisher: U.S. Bureau of Labor Statistics, Consumer Price Index Retroactive Series (R-CPI-U-RS), all items. URL:
  https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx. Transport: Internet Archive capture 20260819055403,
  downloaded on 2026-11-10 (UTC) for Post 29 and copied by the staging script. Coverage: sheet 'All items', U.S. city
  average, not seasonally adjusted, December 1977 = 100, monthly values and an AVG column for 1978 to 2025; in row 55
  (2025) October is '-'.
- FHFA all-transactions for 1996Q1 and the four quarters of 2000: section 5.1.
- Definitions:
  - **Universe of the 2000 median** (`sources/census_coh_values.html`, 'Historical Census of Housing Tables: Home Values', extract line 251; FOUND): "These values refer to owner-occupied single-family housing units on less than 10 acres without a business or medical office on the property."
  - **R-CPI-U-RS** (`sources/bls_r-cpi-u-rs-home_ia20261014233717.htm`, R-CPI-U-RS homepage, extract line 217; FOUND): "presents an estimate of the CPI for all Urban Consumers (CPI-U) from 1978 to the present that incorporates, when possible, most of the improvements made over that time span into the entire series"
  - **October 2025 in the workbook** (`data/bls_rcpiurs_allitems_ia20260819.xlsx`, sheet 'All items', row 57; FOUND): "Note: The Oct 2025 data values are not available due to the 2025 lapse in appropriations."
  - **2025 annual averages, BLS** (`sources/bls_shutdown-cpi-faq_ia20261110081902.htm`, question 10, extract line 271; FOUND): "The 2025 annual average for series which were not published in October 2025 will be computed as the average of the 11 index values published."
- Universe: specified owner-occupied single-family homes in the 2000 census; R-CPI-U-RS, all urban consumers.
- Traps: the 2025 AVG cell is a stored number that differs from the mean of the 11 published months, and no stored BLS
  text explains it (step-3 critic); A2 fixes R14 on the printed annual average. The research series has no rent
  component (design section 3). The 2000 median's universe (specified single-family homes) is narrower than all
  owner-occupied units.

## 16. Dates and text sources the rules name (R1, R16)

- **Vanguard 500 launch** (`sources/vanguard_press_500_50th.html`, press release of August 31, 2026, extract line 8; PARAPHRASE): First Index Investment Trust, later Vanguard 500 Index Fund, launched on August 31, 1976, tracking the S&P 500.
- **First index fund for individuals** (`sources/vanguard_50_facts.html`, fact 1, extract line 16; PARAPHRASE): Vanguard describes the fund as the first index fund for individual investors.
- **Kiyosaki (2016)** (`sources/kiyosaki_page.html`, Entrepreneur column of May 27, 2016, fourth sentence of the definitions paragraph, extract line 301; PARAPHRASE): the column calls a house a liability rather than an asset; the fragment R16 quotes comes from this sentence and is not reproduced here. The 2016 capture (`sources/kiyosaki_ia20160528151441_page.html`, extract line 34) carries the same paragraph.
- Prior research named in R16 is stored, and none of it is a data input: Rappaport (2010)
  (`sources/rappaport_ia20251115193619_PDF-10q4Rappaport.pdf`), Cox and Followill (2018) (`sources/cox_followill_page.html`),
  Beracha and Johnson (2012) (`sources/crossref_beracha-johnson-2012_work.json`, `sources/wiley_ia20200221224323_page.html`)
  and Beracha, Skiba and Johnson (2017) (`sources/tandf_ia20240228204601_page.html`,
  `sources/crossref_beracha-skiba-johnson-2017_work.json`); step 3's sources report holds their locators.
- NASDAQ's entry date: section 7.
- Traps: 'first index fund for individual investors' is Vanguard's own claim (a 1970 retail fund tracking the Dow is
  described elsewhere as earlier, and some sources date the trust to its 1975-12-31 organization) (vet); the CRSP date
  sits only in the page's embedded data, so a gate binding to it needs its own stored text (step 3).

## 17. AHS real-estate-tax definitions, volume by volume

Every volume R7a uses (1973 to 1981, 1983, and 1985 to 2003 in odd years), and the 2005 volume behind R7b, was opened at
its Appendix A entry for real estate taxes. 1973 to 1991 are scans: each entry was found with a local OCR of the
appendix pages (Apple Vision, no network), rendered at 200 dpi and read by eye; the OCR was then compared with the
reading. 1993 to 2005 have a text layer, and each entry was also matched against an OCR of the rendered page.
Hyphens at line breaks are joined in the quotes.

| Volume | File | Entry, printed page (PDF page) | Taxes counted | Special assessments | Rebates | Universe stated in the entry | Units paying no tax | Check |
|---|---|---|---|---|---|---|---|---|
| 1973 | `h150-73C.pdf` | 'Real estate taxes last year', App-7 (206) | total payable on the entire property during the last billing year; State and local | excluded, with sewer tax, road improvement tax and tax collection charge named | not mentioned | owner-occupied one-family homes on less than 10 acres, no commercial establishment or medical or dental office | excluded from the mean | MANUAL |
| 1974 | `h150-74C.pdf` | same entry, App-7 (228) | as 1973 | as 1973 | not mentioned | as 1973 | excluded from the mean | MANUAL |
| 1975 | `h150-75c.pdf` | 'Real estate taxes last year. (Parts A, C, E)', App-16 (238) | total payable during the last billing period | excluded ('special assessments, facilities, or services') | not mentioned | as 1973 | excluded from the mean | MANUAL |
| 1976 | `h150-76c.pdf` | same heading, App-16 (238; folio not printed in the scan, between App-15 at 237 and App-18 at 240) | as 1975 | as 1975 | not mentioned | as 1973, and cooperatives, condominiums, mobile homes and trailers excluded | excluded from the mean | MANUAL |
| 1977 | `h150-77c.pdf` | 'Real estate taxes last year', App-16 to App-17 (238 to 239) | as 1975 | as 1975 | not mentioned | as 1976 | excluded from the mean | MANUAL |
| 1978 | `h150-78c.pdf` | 'Real estate taxes last year', App-11 (289) | the yearly total payable during the last billing period | as 1975 | not mentioned | owner-occupied 1-unit structures on less than 10 acres, no commercial establishment or medical or dental office; cooperatives, condominiums, mobile homes and trailers excluded | excluded from the mean | MANUAL |
| 1979 | `h150-79c.pdf` | same entry, App-11 (289) | as 1978 | as 1975 | not mentioned | as 1978 | excluded from the mean | MANUAL |
| 1980 | `h150-80c.pdf` | same entry, App-11 (289) | as 1978 | as 1975 | not mentioned | as 1978 | excluded from the mean | MANUAL |
| 1981 | `h150-81c.pdf` | same entry, App-11 to App-12 (289 to 290) | as 1978 | as 1975 | not mentioned | as 1978, worded 'one-unit structures' | excluded from the mean | MANUAL |
| 1983 | `h150-83c.pdf` | same entry, App-11 (289) | as 1978 | as 1975 | not mentioned | as 1981 ('cooperatives, condominiums, and mobile homes and trailers') | excluded from the mean | MANUAL |
| 1985 | `h150-85.pdf` | 'Real estate taxes' and 'Annual taxes paid per $1,000', App-20 (510) | special assessments, school, county and any other real estate taxes | included | subtracted | none in the entry; value of the property (house and lot) | not stated in the entry | MANUAL |
| 1987 | `h150-87.pdf` | 'Real estate taxes', App-20 to App-21 (526 to 527); 'Annual taxes paid per $1,000 value', App-21 (527) | as 1985 | included | subtracted | as 1985 | not stated | MANUAL |
| 1989 | `h150-89.pdf` | both entries, App-21 (539) | as 1985 | included | subtracted | as 1985 | not stated | MANUAL |
| 1991 | `h150-91.pdf` | both entries, A-20 (534) | as 1985 | included | subtracted | as 1985 | not stated | MANUAL |
| 1993 | `h150_93.pdf` | both entries, A-20 (535) | as 1985 | included | subtracted | as 1985 | not stated | FOUND |
| 1995 | `h150_95rv.pdf` | both entries, A-20 (555) | as 1985 | included | subtracted | as 1985 | not stated | FOUND |
| 1997 | `h150-97.pdf` | 'Annual taxes paid per $1,000 value', A-1 (457); 'Real estate taxes', A-21 (477) | as 1985 | included | subtracted | value of the house and lot, except the land of mobile homes | not stated | FOUND |
| 1999 | `h150-99-rv.pdf` | A-1 (476); A-21 (496) | as 1985 | included | subtracted | as 1997 | not stated | FOUND |
| 2001 | `h150-01.pdf` | A-1 (490); A-23 (512) | as 1985 | included | subtracted | as 1997, worded 'manufactured/mobile homes' | not stated | FOUND |
| 2003 | `h150-03.pdf` | A-1 (490); A-23 (512) | as 1985 | included | subtracted | as 2001 | not stated | FOUND |
| 2005 | `h150-05.pdf` | A-1 (512); A-23 (534) | as 1985 | included | subtracted | as 2001 | not stated | FOUND |

What changed, as printed: the 1973 and 1974 entries count taxes "during the last billing year"; from 1975 the wording is
"the last billing period", and from 1978 "the yearly total amount". Special assessments are excluded in every volume
from 1973 to 1983 and included in every volume from 1985. No volume from 1973 to 1983 mentions rebates; every volume
from 1985 subtracts them. The 1973 to 1983 entries carry their own universe, which narrows in 1976 (cooperatives,
condominiums, mobile homes and trailers excluded) and changes wording in 1978 (one-family homes become 1-unit
structures); the 1985 to 2005 entries state none, and their Table 3-13 covers all owner-occupied units. From 1997 the
value behind the ratio leaves out the land of mobile homes. The 1974 volume also states, in its comparison with the 1970
census (App-2, PDF p. 223), that its taxes exclude special assessments while the 1970 Residential Finance volume
includes them; the OCR of the 1975 and 1976 volumes (PDF p. 225) and the 1978 and 1983 volumes (PDF p. 281) shows the
same note.

Verbatim, by wording group:

- **1973 universe** (`data/ahs/h150-73C.pdf`, Appendix A, 'Real estate taxes last year', printed App-7, PDF p. 206; MANUAL): "The data are restricted to owner-occupied, one-family homes on less than 10 acres without a commercial establishment or medical or dental office on the property."
- **1973 taxes counted** (`data/ahs/h150-73C.pdf`, printed App-7, PDF p. 206; MANUAL): "refers to the total amount of all real estate taxes payable on the entire property during the last billing year. It includes State and local real estate taxes."
- **1973 exclusions** (`data/ahs/h150-73C.pdf`, printed App-7, PDF p. 206; MANUAL): "Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services such as a sewer tax, road improvement tax, or tax collection charge which are sometimes included with the real estate tax bill. Housing units for which no taxes are paid are excluded from the computation of the mean."
- **1974 exclusions** (`data/ahs/h150-74C.pdf`, printed App-7, PDF p. 228; MANUAL): "Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services such as a sewer tax, road improvement tax, or tax collection charge which are sometimes included with the real estate tax bill."
- **1974 comparison with the 1970 census** (`data/ahs/h150-74C.pdf`, printed App-2, PDF p. 223; MANUAL): "In this report, real estate taxes reflect the total amount of real estate taxes excluding special assessments such as sewer taxes, road improvement taxes, and tax collection charges; in Volume V, real estate taxes include special assessments."
- **1975 taxes counted** (`data/ahs/h150-75c.pdf`, printed App-16, PDF p. 238; MANUAL): "refers to the total amount of all real estate taxes payable on the entire property during the last billing period. It includes State and local real estate taxes. Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1975 mean** (`data/ahs/h150-75c.pdf`, printed App-16, PDF p. 238; MANUAL): "In part C, the mean real estate taxes for last year per $1,000 value of the property (house and lot) are presented. Housing units for which no taxes are paid are excluded from the computation of the mean."
- **1976 universe** (`data/ahs/h150-76c.pdf`, PDF p. 238; MANUAL): "The data are restricted to owner-occupied, one-family homes on less than 10 acres without a commercial establishment or medical or dental office on the property. The data exclude owner-occupied cooperatives, condominiums, mobile homes, and trailers."
- **1977 universe** (`data/ahs/h150-77c.pdf`, printed App-16, PDF p. 238; MANUAL): "The data exclude owner-occupied cooperatives, condominiums, mobile homes, and trailers."
- **1977 exclusions** (`data/ahs/h150-77c.pdf`, printed App-17, PDF p. 239; MANUAL): "Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1978 universe** (`data/ahs/h150-78c.pdf`, printed App-11, PDF p. 289; MANUAL): "The data are restricted to owner-occupied, 1-unit structures on less than 10 acres having no commercial establishment or medical or dental office on the property. The data exclude owner-occupied cooperatives, condominiums, mobile homes, and trailers."
- **1978 taxes counted** (`data/ahs/h150-78c.pdf`, printed App-11, PDF p. 289; MANUAL): "refers to the yearly total amount of all real estate taxes payable on the entire property during the last billing period. It includes State and local real estate taxes. Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1979 taxes counted** (`data/ahs/h150-79c.pdf`, printed App-11, PDF p. 289; MANUAL): "refers to the yearly total amount of all real estate taxes payable on the entire property during the last billing period. It includes State and local real estate taxes. Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1980 taxes counted** (`data/ahs/h150-80c.pdf`, printed App-11, PDF p. 289; MANUAL): "refers to the yearly total amount of all real estate taxes payable on the entire property during the last billing period. It includes State and local real estate taxes. Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1981 universe** (`data/ahs/h150-81c.pdf`, printed App-11 to App-12, PDF pp. 289 to 290; MANUAL): "The data are restricted to owner-occupied, one-unit structures on less than 10 acres having no commercial establishment or medical or dental office on the property."
- **1981 exclusions** (`data/ahs/h150-81c.pdf`, printed App-12, PDF p. 290; MANUAL): "for special assessments, facilities, or services. When the real estate taxes are included with the mortgage, a separate amount for the taxes is obtained."
- **1983 universe** (`data/ahs/h150-83c.pdf`, printed App-11, PDF p. 289; MANUAL): "The data exclude owner-occupied cooperatives, condominiums, and mobile homes and trailers."
- **1983 exclusions** (`data/ahs/h150-83c.pdf`, printed App-11, PDF p. 289; MANUAL): "Not included are payments on delinquent taxes due from prior years or payments for special assessments, facilities, or services."
- **1985 taxes counted** (`data/ahs/h150-85.pdf`, 'Real estate taxes', printed App-20, PDF p. 510; MANUAL): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **1985 per $1,000** (`data/ahs/h150-85.pdf`, 'Annual taxes paid per $1,000', printed App-20, PDF p. 510; MANUAL): "The annual real estate taxes paid per $1,000 value of the property (house and lot) are presented. Medians for taxes per $1,000 value are rounded to the nearest dollar."
- **1987 taxes counted** (`data/ahs/h150-87.pdf`, printed App-20 to App-21, PDF pp. 526 to 527; MANUAL): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **1989 taxes counted** (`data/ahs/h150-89.pdf`, printed App-21, PDF p. 539; MANUAL): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **1991 taxes counted** (`data/ahs/h150-91.pdf`, printed A-20, PDF p. 534; MANUAL): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **1991 per $1,000** (`data/ahs/h150-91.pdf`, 'Annual taxes paid per $1,000 value', printed A-20, PDF p. 534; MANUAL): "The annual real estate taxes paid per $1,000 value of the property (house and lot) are presented."
- **1993 taxes counted** (`data/ahs/h150_93.pdf`, printed A-20, PDF p. 535; FOUND): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **1995 per $1,000** (`data/ahs/h150_95rv.pdf`, printed A-20, PDF p. 555; FOUND): "The annual real estate taxes paid per $1,000 value of the property (house and lot) are presented."
- **1997 per $1,000** (`data/ahs/h150-97.pdf`, 'Annual taxes paid per $1,000 value', printed A-1, PDF p. 457; FOUND): "Real estate taxes paid per $1,000 value of the house (and lot, except on mobile homes) are presented."
- **1999 taxes counted** (`data/ahs/h150-99-rv.pdf`, 'Real estate taxes', printed A-21, PDF p. 496; FOUND): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **2001 per $1,000** (`data/ahs/h150-01.pdf`, printed A-1, PDF p. 490; FOUND): "Real estate taxes paid per $1,000 value of the house (and lot, except on manufactured/mobile homes) are presented."
- **2003 per $1,000** (`data/ahs/h150-03.pdf`, printed A-1, PDF p. 490; FOUND): "Real estate taxes paid per $1,000 value of the house (and lot, except for manufactured/mobile homes) are presented."
- **2003 taxes counted** (`data/ahs/h150-03.pdf`, printed A-23, PDF p. 512; FOUND): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."
- **2005 taxes counted** (`data/ahs/h150-05.pdf`, printed A-23, PDF p. 534; FOUND): "This item includes special assessments, school taxes, county taxes, and any other real estate taxes. Excluded are payments on delinquent taxes due from prior years. Rebates are subtracted from the total."

Printing details: the 1981 entry prints "deliquent" for delinquent; the 1983 entry says the taxes are "included in the
mortgage" where the others say "with the mortgage"; the 1985 heading reads 'Annual taxes paid per $1,000' without
'value'. The 1973 to 1983 headings run on into the text with a dash, which these quotes leave out. The 200 dpi crops of
every scanned entry are in the session scratchpad (`p30prov/img/def/`).

## 18. Documents stored in this step

Step 3 had kept these defining documents only in the scratchpad. Each was copied byte for byte into `sources/` from its
download folder after its sha256 matched the line of its download log; for the six Internet Archive captures, the file's
base32 SHA-1 also equals the CDX digest listed for that capture. No file was fetched in this step. Each name was new in
`sources/`, and no stored file already held the same bytes.

| File in `sources/` | What it defines (rule) | URL | Transport | Retrieved (UTC) | Bytes | sha256 | Download log | Archive digest |
|---|---|---|---|---|---|---|---|---|
| `census_acs2005_Chapter_5_tables_summary_list.xls` | ACS 2005 table-to-sequence list (titles, universes, positions; R7a, R7b) | https://www2.census.gov/programs-surveys/acs/summary_file/2005/documentation/Chapter_5_tables_summary_list.xls | direct | 2026-11-13T10:50:12Z | 330,240 | f387cff6a03f4ecbad22a88e1e6d6443e3d3941cf8bd24bb466d3e8c8678d73e | `p30data/carrying` dl-36, sha256 equal | not an archive capture |
| `census_acs2006_merge_5_6_final.txt` | ACS 2006 table-to-sequence lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2006/documentation/merge_5_6_final.txt | direct | 2026-11-14T02:01:50Z | 1,674,574 | b39ee2cf63c381d835e810e68e1e78aef5e929c6939f82a6657fb8f2ad83441e | `p30build/acs` dl-53, sha256 equal | not an archive capture |
| `census_acs2007_merge_5_6_final.xls` | ACS 2007 table-to-sequence lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2007/documentation/1_year/merge_5_6_final.xls | direct | 2026-11-14T02:01:50Z | 4,410,368 | 8246bc4c0d501a5615dbf0a5f6f06f173b9d384182ec0afaea5ff60b8293915d | `p30build/acs` dl-54, sha256 equal | not an archive capture |
| `census_acs2008_merge_5_6.xls` | ACS 2008 table-to-sequence lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2008/documentation/1_year/user_tools/merge_5_6.xls | direct | 2026-11-14T02:01:51Z | 4,064,768 | 4074b43acc6a37e1e1147797976afa76b562b3781e3a3f779592beeaffcb2b7c | `p30build/acs` dl-55, sha256 equal | not an archive capture |
| `census_acs2009_merge_5_6.txt` | ACS 2009 table-to-sequence lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2009/documentation/1_year/user_tools/merge_5_6.txt | direct | 2026-11-14T02:01:51Z | 2,116,794 | edcebf584f18b0af151db5750669c5a0afc04b83ad6f8c36a1f5f408ba454856 | `p30build/acs` dl-56, sha256 equal | not an archive capture |
| `census_acs2010_Sequence_Number_and_Table_Number_Lookup.txt` | ACS 2010 lookup, first year with B25090 (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2010/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-13T10:49:55Z | 2,075,282 | 6061be158b19563dfdd88c4d8eb0aab6ae7358935dc93ea8e9ae7bb7c55d8832 | `p30data/carrying` dl-33, sha256 equal | not an archive capture |
| `census_acs2011_Sequence_Number_and_Table_Number_Lookup.txt` | ACS 2011 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2011/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:51Z | 2,795,890 | 6dce93f44467c9ce5aeb2b0ef4e6edd28f5628b1a6b038e3dfed0fe3d3e08bf9 | `p30build/acs` dl-57, sha256 equal | not an archive capture |
| `census_acs2012_Sequence_Number_and_Table_Number_Lookup.txt` | ACS 2012 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2012/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:51Z | 2,132,644 | ca59b70dd6cdea7497d4b37dbbb65ec896159fe44abd8acd8858359a5f2e0197 | `p30build/acs` dl-58, sha256 equal | not an archive capture |
| `census_acs2013_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2013 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2013/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z | 2,068,726 | f8fbeb1dfbb4ac521938f9022bce6ce5f873e0196108151e3e448223e11bbdc1 | `p30build/acs` dl-59, sha256 equal | not an archive capture |
| `census_acs2014_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2014 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z | 1,907,089 | b66f2b10bb932de964fad4f95466f6bc85190d181ff17578ebcf95eb910085ee | `p30build/acs` dl-60, sha256 equal | not an archive capture |
| `census_acs2015_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2015 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:49:36Z | 1,901,019 | ec33e9fadf4febd36864e8e9439cf31339e8bece91b32bdae8cdb7da60282e34 | `p30data/carrying` dl-30, sha256 equal | not an archive capture |
| `census_acs2016_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2016 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z | 1,907,695 | 36868b37a395e306a856140e34d4b945bb4a0cb5d6a99d8c8070a6f2b0936874 | `p30build/acs` dl-61, sha256 equal | not an archive capture |
| `census_acs2017_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2017 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:57:39Z | 2,005,809 | d35a4facf6b39902b4df0008072b8719ef97a195279ad93619ed0b4bc98b7d5b | `p30data/rentprice` dl-91, sha256 equal | not an archive capture |
| `census_acs2018_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2018 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2018/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z | 2,120,082 | 36dd6ae97ce97e739a35fe4620a4a6df761b06c4a37d252c316653597e6e64f7 | `p30build/acs` dl-62, sha256 equal | not an archive capture |
| `census_acs2019_ACS_1yr_Seq_Table_Number_Lookup.txt` | ACS 2019 lookup (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:48:29Z | 2,121,821 | b08fe2b87c8720c52bac58146702a732e4d9d281ed0fbec6acf2eabd460d59a0 | `p30data/carrying` dl-26, sha256 equal | not an archive capture |
| `census_ACS20211YR_Table_Shells.txt` | ACS 2021 table shells (R7a, R7b) | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/ACS20211YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z | 7,132,817 | 96271eba7aef8c2ba641b20d691d34e5bc1f02ba8d5014280e761a8fc7ff0345 | `p30build/acs` dl-107, sha256 equal | not an archive capture |
| `census_ACS20221YR_Table_Shells.txt` | ACS 2022 table shells (R7a, R7b) | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/documentation/ACS20221YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z | 7,165,226 | ebffe6952c7eca126c7583e045a30fec349f6bd977107cedd171c912f7c15b06 | `p30build/acs` dl-108, sha256 equal | not an archive capture |
| `census_ACS20231YR_Table_Shells.txt` | ACS 2023 table shells (R7a, R7b, R15.5) | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/documentation/ACS20231YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z | 7,201,348 | e25ee815917f1b660d0b2c2a86d814ee3c18add086e0d6ac94f35c7ecbfb4711 | `p30build/acs` dl-109, sha256 equal | not an archive capture |
| `census_ACS20241YR_Table_Shells.txt` | ACS 2024 table shells (R7a) | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/documentation/ACS20241YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z | 7,230,781 | 2e4d8a460131be19ca06e87bb478e12ccb4dd44892369245049ee0e463454ad4 | `p30build/acs` dl-110, sha256 equal | not an archive capture |
| `census_ACS20251YR_Table_Shells.txt` | ACS 2025 table shells (R7a, R15.5, R15.6) | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/documentation/ACS20251YR_Table_Shells.txt | direct | 2026-11-13T11:20:56Z | 7,242,343 | ff33ade0dad19e66d86027604bcef5f41bbfe1a77ac494735a9f36d693491799 | `p30data/carrying-verify` dl-14, sha256 equal | not an archive capture |
| `census_2007_ACSSubjectDefinitions.pdf` | ACS 2007 Subject Definitions (value in categories; R7a, R7b) | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2007_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:58Z | 413,028 | 4674fae6a2906132c5cad94327cbd455adcec5e201ee40080547ee643c688b06 | `p30build/acs` dl-121, sha256 equal | not an archive capture |
| `census_2008_ACSSubjectDefinitions.pdf` | ACS 2008 Subject Definitions (value question change; real estate taxes) | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2008_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:32Z | 473,226 | a4130bc455e833589db4a5a904ed5625986ad8b6e01a6d5b818a178b0ba7661b | `p30build/acs` dl-119, sha256 equal | not an archive capture |
| `census_2010_ACSSubjectDefinitions.pdf` | ACS 2010 Subject Definitions (first B25090 year) | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2010_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:33Z | 688,859 | dd016f630ab0435e2e3edfe21ec5aed5ca5a24391e1efb7a5f022d0332336012 | `p30build/acs` dl-120, sha256 equal | not an archive capture |
| `bea_nipa_handbook_chapter-02.pdf` | NIPA Handbook ch. 2, consumption of fixed capital (R2) | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-02.pdf | direct | 2026-11-14T02:08:53Z | 757,854 | 82e9efeb46ec54b2d87d2453090457863d9c0527d41ca88c01e5b5dd7a9c30b5 | `p30build/bea` dl-16, sha256 equal | not an archive capture |
| `bea_nipa_handbook_chapter-06.pdf` | NIPA Handbook ch. 6, residential improvements (R7c) | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-06.pdf | direct | 2026-11-14T02:08:53Z | 584,667 | 16ca59e91eb50f3cb88201903cd05bd3988c99ef91543c72bd51d8a82233e109 | `p30build/bea` dl-15, sha256 equal | not an archive capture |
| `bea_Fixed_Assets_1925_97_ia20251125021830.pdf` | BEA Fixed Assets 1925-97 methodology, tenure groups (R7c) | https://apps.bea.gov/national/pdf/Fixed_Assets_1925_97.pdf | Internet Archive capture 20251125021830 | 2026-11-14T02:12:15Z | 905,284 | cf86d271951ebe4464e1e1beccaccf5a5c7507c4abffa727e4ef525a5ea4bf3c | `p30build/bea` dl-20, sha256 equal | CDX digest KCMUVU2IECRVDTPKHLNAJ6MSWZSG7C65, equal |
| `bea_ia20251206172244_Section7All_xls.xlsx` | NIPA Section 7 tables, 2025 vintage (Tables 7.4.5, 7.5, 7.11 labels and notes; R2, R7c) | https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx | Internet Archive capture 20251206172244 | 2026-11-13T10:36:18Z | 989,237 | b1b2b2d2375dfa214d9d7baa72e24eb174187945c2a152ec4a10a70724ef013e | `p30data/carrying` dl-03, sha256 equal | CDX digest 5BJ62KN3B5ERCQVFOHAPHVFSFASJBJMR, equal |
| `bea_ia20220703151550_FlatFiles.ZIP` | NIPA flat files of June 2022 with the discontinued Table 7.12 (R7c construction) | https://apps.bea.gov/national/Release/TXT/FlatFiles.ZIP | Internet Archive capture 20220703151550 | 2026-11-13T11:18:34Z | 18,680,745 | c59d347304100cb1d2fb8ad33e2ee291d0843ad8db3a2d9dfae2f4608c52a527 | `p30data/carrying-verify` dl-12, sha256 equal | CDX digest VMPM5VFV3RXCLDWY62TWVCOOBP7DXQNK, equal |
| `census_ahs-introduction-history.html` | Census AHS history page (1973 to 1981 annual, biennial from 1983; R7a gap years) | https://www.census.gov/programs-surveys/ahs/about/ahs-introduction-history.html | direct | 2026-11-14T02:23:26Z | 346,788 | c739740f94fa8629d1c1afe82dbc7beedb723fc97db3f3cfff32e3c89ff6565c | `p30build/ahs` dl-39, sha256 equal | not an archive capture |
| `fhfa_ia20180917224523_HPI_PO_summary.xls` | FHFA purchase-only summary as served in 2018 (R3 vintage check) | https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_PO_summary.xls | Internet Archive capture 20180917224523 | 2026-11-14T02:06:00Z | 64,512 | 16cec8f2864b08263a708f50c8050a0fd1669c5a5fc8da438f309a5c274bcc4b | `p30build/dlmext` dl-05, sha256 equal | CDX digest Y5J2PA3OOXPTLB7BJ7TENLRR63NAS5PP, equal |
| `bls_ia20180623111013_cu.data.0.Current` | BLS CPI LABSTAT all-current file as of June 2018 (R3 vintage check) | https://download.bls.gov/pub/time.series/cu/cu.data.0.Current | Internet Archive capture 20180623111013 | 2026-11-14T02:06:51Z | 37,386,394 | 8eb6e6b91e501bcf178d69a9e8f5d723345ed3e8b721c2734576de61bf2fa209 | `p30build/dlmext` dl-06, sha256 equal | CDX digest 7DYAKLST4U4VSTFEA3GMR67GRKHL2MGS, equal |
| `bls_ia20250802020823_cw.data.12.USHousing` | BLS CPI-W housing series (R15.1 pre-1978 check) | https://download.bls.gov/pub/time.series/cw/cw.data.12.USHousing | Internet Archive capture 20250802020823 | 2026-11-13T11:14:04Z | 2,575,709 | ddec5d78c0ce19db4233c57b9bddf6bd9b271231e8ca3bd5bd6f0c07bea4465f | `p30data/indexes-verify` dl-60, sha256 equal | CDX digest W36JT3DS7DAAEUKMSPBEFGSAWJRRZGTI, equal |

## 19. Open items

1. **ACS B25103 for 2005 to 2009 (resolved 2026-11-14).** A2 fills R7a for 2005 to 2009 with B25103_001 over B25077_001
   "read from the same files". The B25077 cells are in the staged sequence files (field 83 of sequences 0131 in 2005,
   0130 in 2006, 0135 in 2007, 0139 in 2008 and 0150 in 2009), but B25103 sits in sequences that were never staged:
   0132 in 2005 (listed start 163; the vet read it at fields 161 to 163), 0131 in 2006 (start 161), 0136 in 2007 (start
   132), 0140 in 2008 (start 132) and 0151 in 2009 (start 63), per the stored lookups. Only the 2005 one was ever
   downloaded (`p30data/carrying` dl-37, sha256 54bd413d0376865cd1fe1b106c560918276af58df5857300f6b27c5e1dde9b57, in the
   scratchpad). `acs_positions.csv` records no position for B25077_001 in 2006 to 2009 or for B25103_001 in 2005 to
   2009. Until the four missing sequence files are downloaded, the 2005 one staged, all five pinned and the positions
   recorded, the 2005 to 2009 property-tax values cannot be built from `data/`. **Resolved 2026-11-14:** the 15
   sequence files that hold B25103 for 2005 to 2019 are pinned in `data/acs/`, each with its estimate member extracted
   unchanged (Appendix A): `us0000132.2005-1yr.zip`, `20061us0131000.zip`, `20071us0136000.zip`, `20081us0140000.zip`,
   `20091us0151000.zip`, `20101us0151000.zip`, `20111us0158000.zip`, `20121us0158000.zip`, `20131us0149000.zip`,
   `20141us0144000.zip`, `20151us0144000.zip`, `20161us0145000.zip`, `20171us0145000.zip`, `20181us0154000.zip` and
   `20191us0153000.zip`. Two independent readings agreed on the raw value, file and field of all 29 cells now recorded
   in `acs_positions.csv` (B25103_001 for 2005 to 2019 and B25077_001 for 2006 to 2019; the 2005 B25103 cell at field
   161, section 9.2), and the build now computes the 2005 to 2009 property-tax values from them.
2. **The R-CPI-U-RS 2025 annual average.** A2 fixes R14 on the printed AVG, but no stored BLS document explains why that
   cell differs from the mean of the 11 published months, which is how BLS's FAQ (question 10) says 2025 annual averages
   are computed.
3. **The pre-1978 CPI-W statement in R15.1** rests on a data check, now reproducible from stored files, and on no BLS
   sentence; the post should word it as a finding from the data, not as a BLS statement.
4. **Duplicate bytes in `sources/`** (housekeeping, no rule affected; step-3 critic): the CFPB report and the three NAIC
   reports are stored in both `data/costs/` and `sources/`; `bls_cu_series_ia20261021074323.txt` equals
   `bls_ia20261021074323_cu.series.gunzipped.txt`, `fhfa_faqs_hpi.html` equals `fhfa_hpi_faqs_2026-11-13.html`, and
   `fhfa_hpi-technical-description.pdf` equals `fhfa_hpi_technical_description_1996.pdf`; three BLS captures are stored
   both as served (gzip) and decompressed. Nothing was renamed or removed here.
5. **The CRSP NASDAQ date** sits only in the page's embedded data; a gate check that binds to it needs a stored text
   copy of that item.

## Appendix A. Every file in `data/`

Hashed 2026-11-14. Generated files show where they came from and when they were written; their inputs are listed in the
same table.

| File | Bytes | sha256 | URL | Transport | Retrieved (UTC) |
|---|---|---|---|---|---|
| `data/acs/20061us0130000.zip` | 1,610,882 | b2abf6e8c4034530b0c85f8fa136023030c2b50ee0388c6865c501810708e112 | https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0130000.zip | direct | 2026-11-14T02:04:01Z |
| `data/acs/20061us0131000.zip` | 1,686,883 | be2e87784dd23dc9335393d4b6e7afa7303b7c004436d8eca656f8da2c4c62de | https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0131000.zip | direct | 2026-11-14T14:51:49Z |
| `data/acs/20071us0135000.zip` | 1,650,588 | 315ffe752f8f2d1769924a3d50556bccddfcc982360665200d8143a2f5ce5b96 | https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0135000.zip | direct | 2026-11-14T02:04:02Z |
| `data/acs/20071us0136000.zip` | 2,077,222 | 79a1c945f67390d9c77d62f255cd49d9306111270b910aa6f304f73b30c13105 | https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0136000.zip | direct | 2026-11-14T14:51:55Z |
| `data/acs/20081us0139000.zip` | 1,691,114 | 81e6eabd821ab564daffc1d5967e2485178a3f51219bb9daabe8f7a0ae197d61 | https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0139000.zip | direct | 2026-11-14T02:04:02Z |
| `data/acs/20081us0140000.zip` | 2,117,374 | 620d1ada604d712e02a564694738e6268232dd6a89577daab0bf1bcb8becb5cc | https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0140000.zip | direct | 2026-11-14T14:52:00Z |
| `data/acs/20091us0150000.zip` | 1,151,104 | b1a434da8bfcaad9141cf4fe030f14c7bba35c32aed5c51ea0bf5f221922b95b | https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0150000.zip | direct | 2026-11-14T02:04:03Z |
| `data/acs/20091us0151000.zip` | 1,534,609 | af4d1ed4e0c89758aabd473e5de9f24ea42e09098e9305c62f177f2419920106 | https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0151000.zip | direct | 2026-11-14T14:52:06Z |
| `data/acs/20101us0150000.zip` | 1,153,397 | 83f7c3296fab5298e6b2d01547e2f0b9af38a93097e8fcc74b379b0da13563c2 | https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0150000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:02Z |
| `data/acs/20101us0151000.zip` | 1,535,963 | cacefb40b20545dec4a1e643ebdf05f36d5208a703242c07806835be9e2f076c | https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0151000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:02Z |
| `data/acs/20111us0156000.zip` | 1,135,507 | 09ffcd907b358561e9e49339045c143b6d2ca4ea583ad2268825a9b179a8ed85 | https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0156000.zip | direct | 2026-11-14T02:04:12Z |
| `data/acs/20111us0158000.zip` | 1,545,170 | 725aad4877332153011a101df4721404c0a07a893a33c1c243e686345da63552 | https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0158000.zip | direct | 2026-11-14T14:52:11Z |
| `data/acs/20121us0156000.zip` | 1,194,352 | ad004a2a781e091bc52f6e1aba48708ad42727c037c7908f8e908e376967736c | https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0156000.zip | direct | 2026-11-14T02:04:12Z |
| `data/acs/20121us0158000.zip` | 1,551,051 | 219b9f798a5b51704c552d8dad4ab6bd1bfabd6c23bd8fbcbe2da644125e80cc | https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0158000.zip | direct | 2026-11-14T14:52:17Z |
| `data/acs/20131us0147000.zip` | 935,824 | 6cfb4cddb45f7d66274a1c4f428233043c2f216d2fb50d0bbebc60fce89f161d | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0147000.zip | direct | 2026-11-14T02:04:13Z |
| `data/acs/20131us0148000.zip` | 1,176,287 | cb496701d7a356726cd03ffaacb104532f0bd26efd5570ae597c96803ad5979f | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0148000.zip | direct | 2026-11-14T02:04:13Z |
| `data/acs/20131us0149000.zip` | 1,419,820 | 0de206de2028ae1faaa19812d82dead69aaaa17bb9dbcf19113a3c1dfbc71b1e | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0149000.zip | direct | 2026-11-14T14:52:22Z |
| `data/acs/20141us0142000.zip` | 1,028,834 | d07a2433845a3d77cdcfc3ac0a4f4e25f05fc5546eace082528b7dfb928d40bb | https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0142000.zip | direct | 2026-11-14T02:04:14Z |
| `data/acs/20141us0144000.zip` | 1,537,490 | cb516aa038db9e411067f715ca8f0eb85d450f5c3c20bed41f97a7d8b64a0b21 | https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0144000.zip | direct | 2026-11-14T14:52:28Z |
| `data/acs/20151us0142000.zip` | 1,076,346 | 6a1a37f7cd281f2605d7546eae62d0b0ce51cae723f19b727c6c094dd330e497 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0142000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:49:45Z |
| `data/acs/20151us0144000.zip` | 1,481,163 | d24a0abb3bfb2b0023212fe6f056283e2418ebef535fa4ec5493e15e847e49b7 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0144000.zip | direct | 2026-11-14T14:52:33Z |
| `data/acs/20161us0143000.zip` | 1,071,372 | eac638abfa4d6cdd604108b52d015f714329124fc0dcc250f2b5b00d01db6b22 | https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0143000.zip | direct | 2026-11-14T02:04:14Z |
| `data/acs/20161us0145000.zip` | 1,513,115 | ccf69d66d113b99f83a61b750fbbe3ab084cbb1919d71af0bfdaf5de185629ba | https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0145000.zip | direct | 2026-11-14T14:52:38Z |
| `data/acs/20171us0143000.zip` | 1,063,195 | 48acf6545a2dcdf280abcc84bb3a7285a8f4c505fdc1e7445277c611a310462b | https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0143000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:57:54Z |
| `data/acs/20171us0145000.zip` | 1,521,894 | d731127fb98bb05c1b7e49efa96d908b3f53d52a481265d1a6957fa5b3262586 | https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0145000.zip | direct | 2026-11-14T14:52:44Z |
| `data/acs/20181us0152000.zip` | 1,068,269 | 34572a5d5979222c9bba567f57bf913ad5abcaf663b243b7c11c0653311e2b6b | https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0152000.zip | direct | 2026-11-14T02:04:15Z |
| `data/acs/20181us0154000.zip` | 1,543,431 | 89965287fa62b2e62d01061b2bf92ff0d909dd7fc5cc988c1662e0b3a5fd0f6c | https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0154000.zip | direct | 2026-11-14T14:52:49Z |
| `data/acs/20191us0151000.zip` | 1,058,747 | 9b5836dc0b1dbd725ca6c46e8568ac3dff1e14842459ed7b2f62729308c27b18 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0151000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:49:11Z |
| `data/acs/20191us0153000.zip` | 1,546,038 | b000aa74d49ceac807e1faace6f4d8154c1d8e115485d1a34fd0716869faa466 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0153000.zip | direct | 2026-11-14T14:52:55Z |
| `data/acs/Geos20211YR.txt` | 1,044,165 | f24e9ac0d255cf38d20c0c23ebed6b6874b181f462f417b522304047a03286ea | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/Geos20211YR.txt | direct | 2026-11-14T02:04:37Z |
| `data/acs/Geos20221YR.txt` | 1,059,747 | f29667153e72ac95a5a76b87725cf1e509b53bd5611802432a04f06806e8b63f | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/documentation/Geos20221YR.txt | direct | 2026-11-14T02:04:37Z |
| `data/acs/Geos20231YR.txt` | 1,075,332 | d0e8ca5b28243016f89cb20588675ff6ace83cac503cf0273ec3f2ee7f9fcb62 | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/documentation/Geos20231YR.txt | direct | 2026-11-14T02:04:37Z |
| `data/acs/Geos20241YR.txt` | 1,065,169 | 2155acb3c81672eee9b0bd971cca60cd77d8b66222b34973928f57c087ea4afe | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/documentation/Geos20241YR.txt | direct | 2026-11-14T02:04:37Z |
| `data/acs/Geos20251YR.txt` | 1,070,561 | c8e9250ae8d2632bff4c9e800e5880722ea2cbd899a81c3ef071165fea13e387 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/documentation/Geos20251YR.txt | direct | 2026-11-14T02:04:37Z |
| `data/acs/acs_positions.csv` | 30,369 | 03d07a97de59164c51c1aa76f1b737c9fc4c2841d365f019d74b0e434bf8242a | none (generated) | generated by step 3 (scripts/make_positions.py) from the ACS files above with 43 positions, read back 43 of 43 by scripts/verify_positions.py; on 2026-11-14 the 29 positions of open item 1 were added and the 43 rows kept unchanged (scratchpad `p30impl/fix2/work/scripts/make_new_positions.py`), 72 in all, read back 72 of 72 by profile_data.read_acs | written 2026-11-14T15:20:35Z |
| `data/acs/acsdt1y2021-b25077.dat` | 228,851 | 0bc6d61db91997024c5cdfa07b43c692ffbe8f417dcdf9853db83f1ad21d5e40 | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25077.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:48:17Z |
| `data/acs/acsdt1y2021-b25082.dat` | 654,770 | 997448ed26bcc1741c5cfcc86a66433df6482865087ce46330679800c76deb93 | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25082.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:16Z |
| `data/acs/acsdt1y2021-b25090.dat` | 556,761 | f56d8908d9743a75de1d657e4b044824a01c6ff303c6edfdc7dbcb82b16d7737 | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25090.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:16Z |
| `data/acs/acsdt1y2022-b25077.dat` | 234,051 | 2ce7a81314c8290186972e1675f3fbea3bfd19dab53cd8f206c2964130a40eb5 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25077.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:48:17Z |
| `data/acs/acsdt1y2022-b25082.dat` | 669,756 | 28a4407f22248834a64d624d0786775eaa6d18bd62502f862f6894a9334f8bc6 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25082.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:31:31Z |
| `data/acs/acsdt1y2022-b25090.dat` | 568,470 | 8327d702e247c98d705174d07eb9d39ebe289c13121c3f15bb9394e72bc518e7 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25090.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:31:31Z |
| `data/acs/acsdt1y2023-b25077.dat` | 234,323 | c39987ce683bc4ac8d5831ac9fb67cbcdfaa9bbb81193bc3af4582ad97353723 | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25077.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:48:18Z |
| `data/acs/acsdt1y2023-b25082.dat` | 671,254 | 302624aa5a8374f126a686ba948bca4b508b13e17efeeb882f175275d123303c | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25082.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:15Z |
| `data/acs/acsdt1y2023-b25090.dat` | 570,549 | 4cf509db1f0379673ed44c666b842211523504bf9a2bc76d6ff6b77ca7c2c433 | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25090.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:15Z |
| `data/acs/acsdt1y2024-b25082.dat` | 677,100 | 7b35e18067f951a57338d88bb31a16f59f4a1d607f632a9a11e39b1462950b2f | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/1YRData/acsdt1y2024-b25082.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:31:32Z |
| `data/acs/acsdt1y2024-b25090.dat` | 575,351 | 60f95c0745c34d9bd9d4dfca86d09947f463ef61c76d0e525b0b4b80a018810b | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/1YRData/acsdt1y2024-b25090.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:31:31Z |
| `data/acs/acsdt1y2025-b25077.dat` | 237,779 | 7ab895b182348af2e79cb31e45717be5fdcc38ab1e1ad959cb4e0e7e9393b772 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25077.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:48:18Z |
| `data/acs/acsdt1y2025-b25082.dat` | 682,864 | 4db69c6f29eee4d7fe117c5c9dc054be8c1bf7f64cfb6ab29c8a6065b0b9a3c7 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25082.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:14Z |
| `data/acs/acsdt1y2025-b25090.dat` | 580,509 | de416cf2b861cfe14e30ce1278a87d813fa30693450d7f6415e8e1b555a5ecd0 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25090.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T11:21:14Z |
| `data/acs/acsdt1y2025-b25103.dat` | 357,506 | 4f3ee59fbf3149db9a06cb1f5a4e3170dc19668d6c69f33f5123127e63c068b3 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25103.dat | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:48:18Z |
| `data/acs/e20061us0130000.txt` | 1,516,919 | e6d7c16c7a80ff4657383e9926d03498baa696dc473cc41aabcd5ede115fa519 | https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0130000.zip | direct | 2026-11-14T02:04:01Z |
| `data/acs/e20061us0131000.txt` | 1,538,927 | 88114192d147aa8553e696717fb2ed9fa452cb44547ae4174cc97286b265b907 | https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0131000.zip | direct | 2026-11-14T14:51:49Z |
| `data/acs/e20071us0135000.txt` | 1,551,326 | 6c635a50710b0c36ce623cac9bd01c7265ea2d81dd2ad11e5f9ec59cdbd598a6 | https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0135000.zip | direct | 2026-11-14T02:04:02Z |
| `data/acs/e20071us0136000.txt` | 1,849,816 | 00549c1f8a72736ad463018cd41529526886a1df9470b9a7b47a07c596bbd281 | https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0136000.zip | direct | 2026-11-14T14:51:55Z |
| `data/acs/e20081us0139000.txt` | 1,553,377 | 639a6a60b8067e99424d6b54356f80cfbad99a9b016b4331ef78b09386d7b352 | https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0139000.zip | direct | 2026-11-14T02:04:02Z |
| `data/acs/e20081us0140000.txt` | 1,851,434 | 13eaeacd3e1fd77c76ede695a6493817c7b2ec3c16d2b1a61a9a87dfc6059d00 | https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0140000.zip | direct | 2026-11-14T14:52:00Z |
| `data/acs/e20091us0150000.txt` | 1,560,259 | 4662d04733325728e21704570c21c46387c8e7a7a0e338df45c89682816dd573 | https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0150000.zip | direct | 2026-11-14T02:04:03Z |
| `data/acs/e20091us0151000.txt` | 1,942,259 | f58b1aacdc398b42f899f36f32f058a3d31c7b65c01dff590fd09aaa3422977a | https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0151000.zip | direct | 2026-11-14T14:52:06Z |
| `data/acs/e20101us0150000.txt` | 1,497,704 | 7d8f4ab67c41f527488a3795f7e1b1e966ae6eaac021357ad5a436bdf9514b25 | https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0150000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:02Z |
| `data/acs/e20101us0151000.txt` | 1,939,516 | f53205c5efb1ec10c4a803e0678ef1525b8dff89d1571376ab846808d3f9c05a | https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0151000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:02Z |
| `data/acs/e20111us0156000.txt` | 1,464,246 | 50bf52bd064307d940d2b4f7ec44971371de92c1cbd9eac87c4460fe2988c49d | https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0156000.zip | direct | 2026-11-14T02:04:12Z |
| `data/acs/e20111us0158000.txt` | 1,950,184 | 73879742f9bc6137f7db076f08fa4e369c051ab965ae6e2d432cd6be424500af | https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0158000.zip | direct | 2026-11-14T14:52:11Z |
| `data/acs/e20121us0156000.txt` | 1,549,318 | fb52e05f835faa69639bc3b77a81de43f57d16c6db253de2d100c60137c90790 | https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0156000.zip | direct | 2026-11-14T02:04:12Z |
| `data/acs/e20121us0158000.txt` | 1,961,095 | 912df931e195c60aa65e6a50e2e65e35ecdd2198b99aead8d5875b10035d04bb | https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0158000.zip | direct | 2026-11-14T14:52:17Z |
| `data/acs/e20131us0147000.txt` | 1,228,525 | 28cfe09295507016b5293eef51cd8441b5e8c3ccc3c881ae12213468f922bd31 | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0147000.zip | direct | 2026-11-14T02:04:13Z |
| `data/acs/e20131us0148000.txt` | 1,511,031 | 2738c276973199440e7e044b54e8dbcf37aafe74d2cb8825c46888eed63e875b | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0148000.zip | direct | 2026-11-14T02:04:13Z |
| `data/acs/e20131us0149000.txt` | 1,774,165 | 6c6a170125c9364c6503c1222f9c095bcdd5552c306c1767e66ab67cf7103156 | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0149000.zip | direct | 2026-11-14T14:52:22Z |
| `data/acs/e20141us0142000.txt` | 1,333,331 | a5bb4d346f17b471258edf521d3c4aa6f36e60c42c1e223c7c05711573450b53 | https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0142000.zip | direct | 2026-11-14T02:04:14Z |
| `data/acs/e20141us0144000.txt` | 1,901,086 | 73e5d351a39588f0a6a1c0fecfc15abb4254fbd96ae3310ce186bee19c0ac3ce | https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0144000.zip | direct | 2026-11-14T14:52:28Z |
| `data/acs/e20151us0142000.txt` | 1,391,603 | 31b17e35a546887c98acbc8dbac1f24a11e798a097cebf5a20ae018dcea9e1b6 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0142000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:49:45Z |
| `data/acs/e20151us0144000.txt` | 1,839,750 | 1aba27110677e45b19454ca3679d876aa9dace8e05f93e75b07add18923a9492 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0144000.zip | direct | 2026-11-14T14:52:33Z |
| `data/acs/e20161us0143000.txt` | 1,387,785 | 74b5d1e575b4fd0c370ac4052f1f7bc0b77ef35b661c0fa1e90f78bc943daed1 | https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0143000.zip | direct | 2026-11-14T02:04:14Z |
| `data/acs/e20161us0145000.txt` | 1,875,780 | f3257a271f9a266cefa028e78e3352e13edbe94e36e78ca43afd63b1d6d41664 | https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0145000.zip | direct | 2026-11-14T14:52:38Z |
| `data/acs/e20171us0143000.txt` | 1,378,220 | d1f21c574e54f7bc2a8af2675c9a4c0e21a8a1bb80e2afc98fe1e4d44282ba9d | https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0143000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:57:54Z |
| `data/acs/e20171us0145000.txt` | 1,884,052 | 7321f29445167f1ba3f936e34acd0c34658f7149d3d4d3ab48c422dcf2e969fc | https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0145000.zip | direct | 2026-11-14T14:52:44Z |
| `data/acs/e20181us0152000.txt` | 1,384,521 | cf27883c0fd5eb47bcc4f7c8735ba00941d4d638ec96a348d4636cafcb10f929 | https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0152000.zip | direct | 2026-11-14T02:04:15Z |
| `data/acs/e20181us0154000.txt` | 1,908,771 | b48d93a94d86425b6a3f8dbe0cbe917d119f97ee0bf8de482fd0579de5adc1e3 | https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0154000.zip | direct | 2026-11-14T14:52:49Z |
| `data/acs/e20191us0151000.txt` | 1,373,659 | 27f8d7f196e17ffe6e2ca04928b65a59c6c1093f797703a22c1112ef4bb13382 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0151000.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:49:11Z |
| `data/acs/e20191us0153000.txt` | 1,908,497 | 0c94948f7cd7898aaecd029ec334e8971022a09f90e010b65832d795dca05e86 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0153000.zip | direct | 2026-11-14T14:52:55Z |
| `data/acs/g20061us.txt` | 324,729 | f1c042bbbfa9ec5b2d5092908807ed619c182cc71107a93c3cdd46c44d952054 | https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/g20061us.txt | direct | 2026-11-14T02:04:02Z |
| `data/acs/g20071us.txt` | 332,344 | aaf411a7d3b8dce3199cb888d8b0825f8fcacbd0ae4fbdf597f002bf0b1efdbc | https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/g20071us.txt | direct | 2026-11-14T02:04:02Z |
| `data/acs/g20081us.txt` | 332,345 | a3c98376dee89be5c550e79320bfbef0b464e69f233c3385a40488b85159e7c3 | https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/g20081us.txt | direct | 2026-11-14T02:04:03Z |
| `data/acs/g20091us.txt` | 324,724 | a9ff9999965571f4b3bdf0beab7517ac3325601acbba902984ce7773203fbb0c | https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/g20091us.txt | direct | 2026-11-14T02:04:03Z |
| `data/acs/g20101us.csv` | 161,756 | ff65f55adc0ee315f47b46f52dde4f2ebb43bdc640d9df2671562dafc64eb070 | https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/g20101us.csv | direct | 2026-11-14T02:04:12Z |
| `data/acs/g20111us.csv` | 162,460 | d8d030ca15ccf0c9cc70af5ff6790a8fc075dde9d21fc81af1c8a98bbc5a04f4 | https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/g20111us.csv | direct | 2026-11-14T02:04:12Z |
| `data/acs/g20121us.csv` | 168,689 | 223a2b16ba94e530cf1ce40bb69f8eff6835acf4f39e37d92aec2eee5c08736f | https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/g20121us.csv | direct | 2026-11-14T02:04:13Z |
| `data/acs/g20131us.csv` | 172,234 | 43437cbe1a45c8267557c249810583ea8e7fd4e01c7f2fed754d7d800dd791b5 | https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/g20131us.csv | direct | 2026-11-14T02:04:14Z |
| `data/acs/g20141us.csv` | 172,503 | dc53d7e85e4498a9a2fa9dc7d4c2539ac53e7d5a21d1e675f0d48a31535bc846 | https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/g20141us.csv | direct | 2026-11-14T02:04:14Z |
| `data/acs/g20151us.csv` | 172,986 | 6639a6c9e28ae3bedd3afd6011c1e657519fac07b9a7d3d2b051d6fcf8726f45 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/g20151us.csv | direct | 2026-11-14T02:04:14Z |
| `data/acs/g20161us.csv` | 173,951 | 40d2be3d5f62daf1c2884a0cc02cc91df7f20e582ae8c1c90820744b50438b97 | https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/g20161us.csv | direct | 2026-11-14T02:04:15Z |
| `data/acs/g20171us.csv` | 173,919 | 0a6123de31cb6f16ee3c07ea5b3c9688f3cec63526e903018b4a2928e7666a65 | https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/g20171us.csv | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:57:58Z |
| `data/acs/g20181us.csv` | 174,428 | b1fc6c533d3845290dace40990081a19c1dfa6927d6b95c7129b5965bc4ebde2 | https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/g20181us.csv | direct | 2026-11-14T02:04:15Z |
| `data/acs/g20191us.csv` | 174,436 | 50a9f92f62fc816741f2a6b83b7660385442aa952da392e6bea6134b96a27af2 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/g20191us.csv | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:49:12Z |
| `data/acs/us0000131.2005-1yr.zip` | 1,503,716 | e54d1b1665fba6adb09f63437f515539df2d59842a525a9f487acbadf193e857 | https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000131.2005-1yr.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:23Z |
| `data/acs/us0000131e.2005-1yr` | 1,420,204 | 3f7330b8b6510c72db25cac7c2c5deacac53fc5057c7c1ed4e3bfadce663edeb | https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000131.2005-1yr.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:23Z |
| `data/acs/us0000132.2005-1yr.zip` | 1,652,744 | 54bd413d0376865cd1fe1b106c560918276af58df5857300f6b27c5e1dde9b57 | https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000132.2005-1yr.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:22Z |
| `data/acs/us0000132e.2005-1yr` | 1,506,457 | 1c887775b63b2995cc832f7ebdb7cef5a227a6ee64728858a989f9e5abf3786b | https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000132.2005-1yr.zip | direct (vet download reused, sha256 matched the vet log) | 2026-11-13T10:50:22Z |
| `data/acs/usgeo.2005-1yr` | 238,046 | b31eb15ca45a56eda05b76a52d7e54b79e2c468c4dab63ca336f2cca53560513 | https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/usgeo.2005-1yr | direct | 2026-11-14T02:04:01Z |
| `data/aei_dlm_rent_price_ratio_2018q2.xlsx` | 84,617 | eba71363889d5207a140c1600c3395fc847b2f04bbc148bb45978190207efb9e | https://www.aei.org/wp-content/uploads/2018/10/RENT-PRICE-RATIO.2018q2.xlsx | owner's hand download (browser), copied unchanged; same bytes as Internet Archive capture 20200229184452 (vet p30data/rentprice-verify dl-05) and the vet's direct copy (p30data/rentprice dl-06) | 2026-11-13T23:14:38Z (file time; quarantine record 23:14:40Z) |
| `data/ahs/ahs2005_tab3-13.xls` | 40,448 | c01b2c412da2bb532ee296661249c3311fff1610384b618a97bc8e566f0e988e | https://www2.census.gov/programs-surveys/ahs/2005/tables/tab3-13.xls | direct | 2026-11-13T11:38:41Z |
| `data/ahs/ahs_values.csv` | 10,214 | bd053dbc9ed39abee158f94fb97871515af66f2b6e92f0ecd3808ffa53d987c3 | none (generated) | generated by step 3 (AHS readers) | written 2026-11-14T02:35:17Z |
| `data/ahs/h150-01.pdf` | 9,040,853 | 3acb2a1f3256312388ae0a6a1e6832e0ae1a608a0e74e4e475d1d80a71777e4b | https://www.census.gov/content/dam/Census/library/publications/2002/demo/h150-01.pdf | direct | 2026-11-14T02:10:45Z |
| `data/ahs/h150-03.pdf` | 4,084,806 | 7290bc7aa4ac7cc50ff6681fd44400142a3a14edcf080c29abd47abb3bb54952 | https://www.census.gov/content/dam/Census/library/publications/2004/demo/h150-03.pdf | direct | 2026-11-14T02:10:47Z |
| `data/ahs/h150-05.pdf` | 4,219,908 | 0d650398c6f27bef6bee719fd0f0211e275fcae5b035ba46d3fd43ebff9ba6d4 | https://www.census.gov/content/dam/Census/library/publications/2006/demo/h150-05.pdf | direct | 2026-11-14T02:10:47Z |
| `data/ahs/h150-73C.pdf` | 12,590,068 | 3b09ae95f37928c8902f02e248793f8e04bcd09cc7e442e610dfdb9881b6ea58 | https://www2.census.gov/prod2/ahsscan/h150-73C.pdf | direct | 2026-11-14T01:58:46Z |
| `data/ahs/h150-74C.pdf` | 17,302,907 | 5b5ca1889104e9b5c80b48b3512e70deaaf3185853b43db9623e554c8d615c96 | https://www2.census.gov/prod2/ahsscan/h150-74C.pdf | direct | 2026-11-14T01:58:46Z |
| `data/ahs/h150-75c.pdf` | 11,627,808 | 4a78e44e102e4ba0dbb9ee4fd13becc7368616d92c22b0e7c5084bb0982d93df | https://www2.census.gov/prod2/ahsscan/h150-75c.pdf | direct | 2026-11-13T11:35:52Z |
| `data/ahs/h150-76c.pdf` | 16,760,895 | 70821d0e3dfb36cc0e34b2436a8b2da9d1ed86be15c2a5d9a19dd844aa37d0a8 | https://www2.census.gov/prod2/ahsscan/h150-76c.pdf | direct | 2026-11-14T01:58:47Z |
| `data/ahs/h150-77c.pdf` | 12,786,624 | 67fa042e80b7cc8efcd18a906bd7ac61de722a46ac1f05473e51d41449e47683 | https://www2.census.gov/prod2/ahsscan/h150-77c.pdf | direct | 2026-11-14T01:58:47Z |
| `data/ahs/h150-78c.pdf` | 13,960,375 | de5df29505654408a3a434a4f2f286eae2f442a453910d66156554ffcd377cc2 | https://www2.census.gov/prod2/ahsscan/h150-78c.pdf | direct | 2026-11-14T01:58:54Z |
| `data/ahs/h150-79c.pdf` | 13,987,403 | 9c0b86f639ed575d01511373dc22f70b885088316f11a2b80e961acf112a12bc | https://www2.census.gov/prod2/ahsscan/h150-79c.pdf | direct | 2026-11-14T01:58:55Z |
| `data/ahs/h150-80c.pdf` | 14,658,475 | edee8daca928aad50bb23fac6da138ddb2a12b679d49163f650f047ea85d9e2b | https://www2.census.gov/prod2/ahsscan/h150-80c.pdf | direct | 2026-11-13T11:37:11Z |
| `data/ahs/h150-81c.pdf` | 14,338,243 | a8de836a79740dc2f63f1336108b03988cdeee7821eca9466eee67840ab04f7e | https://www2.census.gov/prod2/ahsscan/h150-81c.pdf | direct | 2026-11-14T01:58:55Z |
| `data/ahs/h150-83c.pdf` | 16,289,434 | e812976483cfccc9cb1deb0b1138f4eff3ef361c7bf2275d21f2ac9c483ec474 | https://www2.census.gov/prod2/ahsscan/h150-83c.pdf | direct | 2026-11-14T01:58:56Z |
| `data/ahs/h150-85.pdf` | 25,035,645 | ce594322f219f8c25ec7545d0d744e7d8cc4022937c80c2fcf107a07efcfaa26 | https://www2.census.gov/prod2/ahsscan/h150-85.pdf | direct | 2026-11-14T01:58:57Z |
| `data/ahs/h150-87.pdf` | 27,093,576 | 4aa9a964223b2f5433d8be483f8451f656f727f9f163281bb86b1cc4fb601202 | https://www2.census.gov/prod2/ahsscan/h150-87.pdf | direct | 2026-11-14T01:58:58Z |
| `data/ahs/h150-89.pdf` | 28,990,127 | f5ae55204c086dfa148b90ac1ea602400c5ea959b1ce1c895c47a8ed172bc34f | https://www2.census.gov/prod2/ahsscan/h150-89.pdf | direct | 2026-11-14T01:58:58Z |
| `data/ahs/h150-91.pdf` | 31,751,720 | a4e901e877bbd86838aeae3b157ae177c69e8acdda6dd5fb040de5c8d245d360 | https://www2.census.gov/prod2/ahsscan/h150-91.pdf | direct | 2026-11-14T01:58:59Z |
| `data/ahs/h150-97.pdf` | 3,189,025 | db3f5afeffaa6fa78388985f7548f25b444f3ae2a1110d5c31c713af7393284a | https://www.census.gov/content/dam/Census/library/publications/1999/demo/h150-97.pdf | direct | 2026-11-14T02:10:43Z |
| `data/ahs/h150-99-rv.pdf` | 4,249,524 | c2ed3215a035ff58a344bee30c84595e1565cd5011c378fbeb5d60e3e56fa4d1 | https://www.census.gov/content/dam/Census/library/publications/2003/demo/h150-99-rv.pdf | direct | 2026-11-14T02:10:44Z |
| `data/ahs/h150_93.pdf` | 4,800,527 | cc886645197b8bfdd25a51a7ef477d0ae742454f7579078647a586451c4d7d7d | https://www.census.gov/content/dam/Census/library/publications/1995/demo/h150_93.pdf | direct | 2026-11-14T02:10:41Z |
| `data/ahs/h150_95rv.pdf` | 4,573,693 | f7e74b356a35b500b7e9df09005e213793bf5129f8b9c8382a638f4faa7d7e45 | https://www.census.gov/content/dam/Census/library/publications/1997/demo/h150_95rv.pdf | direct | 2026-11-14T02:10:42Z |
| `data/bea/bea_fa_section5all_ia20250202204948.xlsx` | 113,046 | afb5988f9cebac83bfc0bd30ca5c0921c5c024363d92231711815058b785844d | https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx | Internet Archive capture 20250202204948 (https://web.archive.org/web/20250202204948id_/https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx); CDX digest ZIXWIECUKU6JOTB3KAAZDLXEVTEV3LOO equals the file's base32 SHA-1 | 2026-11-14T02:04:31Z |
| `data/bea/bea_fa_seriesregister_ia20250207173438.txt` | 588,210 | fc902fc813dfeea585df24435b4a3ea689429d28c366bef6e97925a215b89d4a | https://apps.bea.gov/national/FixedAssets/Release/TXT/SeriesRegister.txt | Internet Archive capture 20250207173438 (https://web.archive.org/web/20250207173438id_/https://apps.bea.gov/national/FixedAssets/Release/TXT/SeriesRegister.txt); CDX digest F2CUKG632INQW6XUO37OSKFWX72CJYFQ equals the file's base32 SHA-1 | 2026-11-14T02:04:29Z |
| `data/bea/bea_fixedassets_ia20250202204946.txt` | 15,446,542 | d880b8dfb5eb92e541f066ba8445a85d0df568bd1e7642a1c9790772ca5721fe | https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt | Internet Archive capture 20250202204946 (https://web.archive.org/web/20250202204946id_/https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt); CDX digest VQAUVFZHPZAFCQK3DZNO2YYKZX6HC375 equals the file's base32 SHA-1 | 2026-11-14T02:04:27Z |
| `data/bea_nipadataa_ia20261020095433.txt` | 11,967,684 | 9f8e96bb72181d14d7b555f3e1b09c71e900fb8de4c305dc9217424de4757f27 | https://apps.bea.gov/national/Release/TXT/NipaDataA.txt | Internet Archive capture 20261020095433 (vet p30data/carrying dl-01; same bytes in p30data/rentprice dl-39) | 2026-11-13T10:36:15Z |
| `data/bls_cu_data_12_ushousing_ia20261029154324.txt` | 2,708,166 | b2ecc4021ea612ee9acf3629f2cbcfc7e1b063338ee5ede5ae10d74512019704 | https://download.bls.gov/pub/time.series/cu/cu.data.12.USHousing | Internet Archive capture 20261029154324, served gzip (389,500 bytes, sha256 220ce77eea98b761a7ebd8cfa80f31d46cdcf737ebdb6f8d2868cc37bb8e5372), stored decompressed; CDX digest KFVZSBXPIB5RBVPSJEUEEYEWLJLL5C4U matches the archived bytes (vet p30data/indexes dl-41) | 2026-11-13T10:40:18Z |
| `data/bls_rcpiurs_allitems_ia20260819.xlsx` | 13,916 | 355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8 | https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx | Internet Archive capture 20260819055403 (Post 29 download, copied from genz-house-chase/data) | 2026-11-10 (UTC, Post 29) |
| `data/census_coh_values_unadj.txt` | 4,479 | 5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6 | https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-values/values-unadj.txt | direct (Post 29 download, copied from genz-house-chase/data) | 2026-11-10 (UTC, Post 29) |
| `data/census_nrs_price_sold_cust.xlsx` | 52,239 | 9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3 | https://www.census.gov/construction/nrs/xls/price_sold_cust.xlsx | direct (Post 29 download, copied from genz-house-chase/data); the vet fetched the same bytes again (p30data/indexes-verify dl-12, 2026-11-13T11:03:55Z) | 2026-11-10 (UTC, Post 29) |
| `data/costs/census_ahs2023_table_specs_puf_estimates.xlsx` | 290,259 | f94af71db86b11562252823f64ffad919e88ec0f6802a9d91dd8c8732b9b9b0e | https://www2.census.gov/programs-surveys/ahs/2023/AHS%202023%20Table%20Specifications%20and%20PUF%20Estimates%20for%20User%20Verification.xlsx | direct | 2026-11-13T11:28:06Z |
| `data/costs/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf` | 2,263,304 | 7aaeadcd06a98abfff9c6c5f957493d2783f19a85752f618efea562867271c58 | https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf | direct | 2026-11-13T10:40:47Z |
| `data/costs/cost_values.csv` | 6,578 | 9b5767862bad96824aa0d608867a8f2e42bc9a04a43831c0ba728c97d267974e | none (generated) | generated by step 3 (scripts/write_cost_values.py); 24 of 24 rows read back from their sources by scripts/verify_cost_values.py | written 2026-11-14T02:05:43Z |
| `data/costs/naic_homeowners_report_dy2021_ia20240217020958.pdf` | 8,117,340 | b1c98f9c1753730593a0c9329f23d6e44168aa0459ba2c020867a94b5d57c638 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20240217020958 (https://web.archive.org/web/20240217020958id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf); CDX digest 6VTDMVSXWBMVTSHP75X554YSXQBEF3YE (first seen 20240217020958) equals the file's base32 SHA-1 | 2026-11-13T11:31:11Z |
| `data/costs/naic_homeowners_report_dy2022_ia20250706013631.pdf` | 6,091,715 | 369718e3f64767077c1639902d8a053c42b3110a2dd0c3cf802ca4658ca69858 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20250706013631 (https://web.archive.org/web/20250706013631id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf); CDX digest XDZIT6XNTIK6IYSNJFQUXE7WNVG22QQB (first seen 20250706013631) equals the file's base32 SHA-1 | 2026-11-13T11:31:09Z |
| `data/costs/naic_homeowners_report_dy2023_ia20261011104807.pdf` | 7,540,197 | b157866e6656e17041416665557867f4effe77b7b124656a747d2833ea9f4739 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20261011104807 (https://web.archive.org/web/20261011104807id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf); CDX digest BTAXEBF5SJPECA4TJT4O3LKEWSQ3UUDS (first seen 20260905065541) equals the file's base32 SHA-1 | 2026-11-13T11:23:25Z |
| `data/fhfa_hpi_at_us_and_census.csv` | 43,679 | 580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba | https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_us_and_census.csv | direct (Post 29 download, copied from genz-house-chase/data); the vet fetched the same bytes again (p30data/indexes-verify dl-04, 2026-11-13T11:01:23Z) | 2026-11-10 (UTC, Post 29) |
| `data/fhfa_hpi_po_us_and_census.txt` | 38,749 | 4776cd3261d1a5ba71701d2fd7c934184d86494b7b2332ba6b20afa63fae1fea | https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_us_and_census.txt | direct | 2026-11-13T10:36:08Z |
| `data/frb_z1_csv_2026-09-11.zip` | 64,219,006 | 83b8eded0bc7f9b74c0269ef503a863cee88312460fd7eef076284b98fc28c06 | https://www.federalreserve.gov/releases/z1/data/FRB_Z1_csv.zip | direct, release of 2026-09-11 (vet p30data/rentprice dl-31; same bytes in p30data/carrying dl-12 at 10:40:31Z) | 2026-11-13T10:40:56Z |
| `data/freddiemac_pmms_historicalweeklydata.xlsx` | 218,952 | 3066c422d5b7ec93038a60078871d4b43c51c9df268afa9a0ac363b18c7e292a | https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx | owner's hand download (browser), copied unchanged; same bytes as the vet's direct copy p30data/mortgage/dl-04 (2026-11-13T10:33:54Z) | 2026-11-13T23:14:32Z (file time; quarantine record 23:14:36Z) |
| `data/french_ff_factors_csv_2026-09-update.zip` | 13,065 | 593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66 | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/09%202026%20Update/ftp/F-F_Research_Data_Factors_CSV.zip | direct (vet p30data/stocks-verify dl-11) | 2026-11-13T11:05:19Z |
| `data/ici_per32_01_data.xlsx` | 142,333 | d6fd8052b5621288194a79665d8e2d74cb977922a6628f03b849c64a3f5c2d70 | https://www.ici.org/files/2026/per32-01-data.xlsx | Internet Archive capture 20260325214944 (vet p30data/stocks dl-38); the same bytes are the gunzipped body of capture 20260328185035 (p30data/stocks dl-37) | 2026-11-13T10:45:09Z |
| `data/z1_owner_occupied_extract.csv` | 71,150 | 6148186b68d2d404e32ac425689eca0c130fa3282c989616f9bec225ae1efab2 | none (generated) | generated by extract_z1.py from data/frb_z1_csv_2026-09-11.zip; regenerated byte-identical by the step-3 critic | written 2026-11-14T01:58:26Z |

## Appendix B. Every stored document in `sources/`

Documents only; each `.txt` or `.gunzipped.txt` extract that the earlier step wrote beside a document is derived from it
and not listed. Where the earlier step stored an Internet Archive capture in the gzip form the archive served, the
transport says so, and its readable extract carries the text.

| File | Bytes | sha256 | URL | Transport | Retrieved (UTC) |
|---|---|---|---|---|---|
| `sources/aei_AEI-Housing-Terms-of-Use_ia20220319235839.pdf` | 491,689 | 632c3a3bbf8a83070538e15d9871494950477bb4f2c503fde1709af13da0d304 | https://www.aei.org/wp-content/uploads/2021/10/AEI.org-Housing-Terms-of-Use-10.6.21-final.pdf | Internet Archive capture 20220319235839 | 2026-11-13T11:26:56Z |
| `sources/aei_LandPriceNotes_October18_ia20200229184449.pdf` | 96,555 | 5189c7e28594a8a1afc9664c795c521c8a39ccfb8b7f175125a371930c0a097c | https://www.aei.org/wp-content/uploads/2018/10/LandPriceNotes_October18.pdf | Internet Archive capture 20200229184449 | 2026-11-13T11:26:52Z |
| `sources/aei_hlpi_page_ia20260927021451.html` | 12,863 | 5f4d8c3117ba2d668e712b500e56677766ad9a8c8c45155c8dc13dba275e83ac | https://www.aei.org/historical-land-price-indicators/ | Internet Archive capture 20260927021451; stored gzip as served | 2026-11-13T11:26:59Z |
| `sources/aei_terms_of_use_ia20261023020130.html` | 14,874 | 8d5996079b5f8ae7cedea5c2e0c1368d8a2f71155e2a48501694710637da7a9e | https://www.aei.org/about/terms-of-use/ | Internet Archive capture 20261023020130; stored gzip as served | 2026-11-13T11:28:19Z |
| `sources/bea_Fixed_Assets_1925_97_ia20251125021830.pdf` | 905,284 | cf86d271951ebe4464e1e1beccaccf5a5c7507c4abffa727e4ef525a5ea4bf3c | https://apps.bea.gov/national/pdf/Fixed_Assets_1925_97.pdf | Internet Archive capture 20251125021830; CDX digest KCMUVU2IECRVDTPKHLNAJ6MSWZSG7C65 matches | 2026-11-14T02:12:15Z |
| `sources/bea_RIPfactsheet.pdf` | 25,002 | 6f40d3466425c81c9b12ee7e9cdf6a0b155166be81b3e49a52efbf488714210c | https://www.bea.gov/sites/default/files/methodologies/RIPfactsheet.pdf | direct | 2026-11-13T11:25:25Z |
| `sources/bea_SeriesRegister_2026-09.txt` | 971,870 | 6d281fcb3a7a891d436a1b86c088415004a62ddd947a450d8af8ed3fec4c2fa6 | https://www.bea.gov/sites/default/files/2026-09/SeriesRegister.txt | direct | 2026-11-13T11:29:33Z |
| `sources/bea_faq_147.html` | 36,801 | 2859a0cc9dd1d466dff8704dbdbcf8dc2d4b4fa58cde3ff7e089cf39129da4a1 | https://www.bea.gov/help/faq/147 | direct | 2026-11-13T11:41:16Z |
| `sources/bea_glossary_cfc.html` | 39,802 | cc3559abd7e0909fc7a5ec1d97d7c02d8c969c88c52ddbbd25709b2542789c53 | https://www.bea.gov/help/glossary/consumption-fixed-capital-cfc | direct | 2026-11-13T11:25:26Z |
| `sources/bea_ia20220703151550_FlatFiles.ZIP` | 18,680,745 | c59d347304100cb1d2fb8ad33e2ee291d0843ad8db3a2d9dfae2f4608c52a527 | https://apps.bea.gov/national/Release/TXT/FlatFiles.ZIP | Internet Archive capture 20220703151550; CDX digest VMPM5VFV3RXCLDWY62TWVCOOBP7DXQNK matches | 2026-11-13T11:18:34Z |
| `sources/bea_ia20220930130325_SeriesRegister_2022.txt` | 1,120,206 | 08612f762fb61e1a39f9543ef0faf99f20170ab3370f467a3cb03cb4b7910392 | https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt | Internet Archive capture 20220930130325 | 2026-11-13T11:15:16Z |
| `sources/bea_ia20251206172244_Section7All_xls.xlsx` | 989,237 | b1b2b2d2375dfa214d9d7baa72e24eb174187945c2a152ec4a10a70724ef013e | https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx | Internet Archive capture 20251206172244; CDX digest 5BJ62KN3B5ERCQVFOHAPHVFSFASJBJMR matches | 2026-11-13T10:36:18Z |
| `sources/bea_ia20251208052150_SeriesRegister.txt` | 204,567 | 3f15b77f98b8a012150358f75c29acc4e9727f6dae57ed68a5f2d7f8ad283aff | https://apps.bea.gov/national/Release/TXT/SeriesRegister.txt | Internet Archive capture 20251208052150; stored gzip as served | 2026-11-13T10:36:17Z |
| `sources/bea_nipa_handbook_chapter-02.pdf` | 757,854 | 82e9efeb46ec54b2d87d2453090457863d9c0527d41ca88c01e5b5dd7a9c30b5 | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-02.pdf | direct | 2026-11-14T02:08:53Z |
| `sources/bea_nipa_handbook_chapter-05.pdf` | 966,361 | 9b60841323cbcb0ab57c92278e8fcd4491403a123c1322ec9760f19732a161ec | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-05.pdf | direct | 2026-11-13T11:31:47Z |
| `sources/bea_nipa_handbook_chapter-06.pdf` | 584,667 | 16ca59e91eb50f3cb88201903cd05bd3988c99ef91543c72bd51d8a82233e109 | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-06.pdf | direct | 2026-11-14T02:08:53Z |
| `sources/bea_nipa_handbook_chapter-12.pdf` | 387,040 | 3241efac841707743fd5ab327d9ad4c0e723abf3307a7053600972c735e138fa | https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-12.pdf | direct | 2026-11-13T11:25:25Z |
| `sources/bea_policies_and_information.html` | 43,104 | 38c2e1b5eb490a31d74883618768088abfede515d6a83d04c108391cbe59ebfe | https://www.bea.gov/about/policies-and-information | direct | 2026-11-13T10:56:36Z |
| `sources/bea_scb_2021-05_housing_services.htm` | 87,703 | 2b62afef4a17f8ebe2390c58fbe658d0870730084492d81c5bfe4f0673131a2c | https://apps.bea.gov/scb/2021/05-may/0521-housing-services.htm | direct | 2026-11-13T11:32:01Z |
| `sources/bea_scb_2023-11_nea_comprehensive_update.htm` | 1,055,842 | 96cdab7da878b3c5dad0d3033ca26b23e3bcf08e06f34c333ac872dc0b9c6f1f | https://apps.bea.gov/scb/issues/2023/11-november/1123-nea-comprehensive-update.htm | direct | 2026-11-13T11:37:23Z |
| `sources/bls_copyright-information_ia20261107031018.htm` | 17,405 | 7e99999ff816e94358df7e0a711968d657e64d376bd97ee5430f45a88ce07855 | https://www.bls.gov/opub/copyright-information.htm | Internet Archive capture 20261107031018; stored gzip as served | 2026-11-13T10:45:21Z |
| `sources/bls_cpi_2025_shutdown_faq_ia20261110081902.htm` | 76,572 | fada646ba27ac327b1719bd2f9c442b2fd1d3d9ae2d062ba8a4f6464398584ca | https://www.bls.gov/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi-faq.htm | Internet Archive capture 20261110081902 | 2026-11-13T10:44:32Z |
| `sources/bls_cu_series_ia20261021074323.txt` | 1,339,447 | 0c15b6db9f3c490baef34c87699da2ecd06c5d277e043004d189450f6ddc8b00 | https://download.bls.gov/pub/time.series/cu/cu.series | Internet Archive capture 20261021074323 | 2026-11-13T10:40:19Z |
| `sources/bls_hom_cpi_calculation_ia20261107234217.htm` | 270,400 | 532914ca230b9140fad645e77f1caf592afc07a8ecf96279d8fd5049a632097e | https://www.bls.gov/opub/hom/cpi/calculation.htm | Internet Archive capture 20261107234217 | 2026-11-13T10:41:36Z |
| `sources/bls_hom_cpi_history_ia20261024112424.htm` | 27,103 | 9da97472c4ea110546a891d555cabb41a5ec1774ebd85be609a31fce94c2f18c | https://www.bls.gov/opub/hom/cpi/history.htm | Internet Archive capture 20261024112424; stored gzip as served | 2026-11-13T10:41:46Z |
| `sources/bls_ia20180623111013_cu.data.0.Current` | 37,386,394 | 8eb6e6b91e501bcf178d69a9e8f5d723345ed3e8b721c2734576de61bf2fa209 | https://download.bls.gov/pub/time.series/cu/cu.data.0.Current | Internet Archive capture 20180623111013; CDX digest 7DYAKLST4U4VSTFEA3GMR67GRKHL2MGS matches | 2026-11-14T02:06:51Z |
| `sources/bls_ia20250802020823_cw.data.12.USHousing` | 2,575,709 | ddec5d78c0ce19db4233c57b9bddf6bd9b271231e8ca3bd5bd6f0c07bea4465f | https://download.bls.gov/pub/time.series/cw/cw.data.12.USHousing | Internet Archive capture 20250802020823; CDX digest W36JT3DS7DAAEUKMSPBEFGSAWJRRZGTI matches | 2026-11-13T11:14:04Z |
| `sources/bls_ia20260819121638_rent-oer-information.htm` | 57,103 | 33f56a28f2f256dc7e8216828725def98f3ff7622569dc93cfe660a1e908a2f5 | https://www.bls.gov/cpi/notices/2024/rent-oer-information.htm | Internet Archive capture 20260819121638 | 2026-11-13T11:17:32Z |
| `sources/bls_ia20260819181438_why-cpi-w-and-cpi-u.htm` | 62,871 | 9051d520e7f58658cc57700221222bc476475418d7dc9a4fad97c86c0e3a8765 | https://www.bls.gov/opub/btn/volume-3/why-does-bls-provide-both-the-cpi-w-and-cpi-u.htm | Internet Archive capture 20260819181438 | 2026-11-13T11:11:53Z |
| `sources/bls_ia20261001052102_cu.footnote` | 107 | 0c39b91a9c5259435555c3aa4bc10b7184f4f39d11dd940f13d0f209c6286b7f | https://download.bls.gov/pub/time.series/cu/cu.footnote | Internet Archive capture 20261001052102; stored gzip as served | 2026-11-13T10:40:30Z |
| `sources/bls_ia20261009030838_cu.txt` | 4,558 | 7668140a6b55af201d9e5d350eb746d14ca5ebdccdeb77f82c1c4c9f57e36a39 | https://download.bls.gov/pub/time.series/cu/cu.txt | Internet Archive capture 20261009030838; stored gzip as served | 2026-11-13T10:40:20Z |
| `sources/bls_ia20261021074323_cu.series` | 89,751 | 50b157c41ffd9898b82891adfca2af3c0b9aad41fc85ce8393384b9bf26e143d | https://download.bls.gov/pub/time.series/cu/cu.series | Internet Archive capture 20261021074323; stored gzip as served | 2026-11-13T10:40:19Z |
| `sources/bls_ia20261107234217_calculation.htm` | 87,022 | cc66087c0117a271c60ec9d8b896e28a61b2f2a6c9f2c8ce228338827643585b | https://www.bls.gov/opub/hom/cpi/calculation.htm | Internet Archive capture 20261107234217; stored gzip as served | 2026-11-13T11:07:17Z |
| `sources/bls_mlr1999_06_art4full_ia20260819075117.pdf` | 110,269 | 7038e9126611757b71eacb10cad36b1de839ed21bd9a7bee5e97ba4bee6b8950 | https://www.bls.gov/opub/mlr/1999/06/art4full.pdf | Internet Archive capture 20260819075117 | 2026-11-13T10:42:57Z |
| `sources/bls_oer_rent_factsheet_ia20261015220925.htm` | 80,893 | 7ce0fb0639e36fa8f5970cf84f1fcd5736f9b5c39a44c6a19f7b5d3400835a78 | https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm | Internet Archive capture 20261015220925 | 2026-11-13T10:42:27Z |
| `sources/bls_r-cpi-u-rs-changes_ia20260819055434.htm` | 64,049 | 5d33b275381515bf7fb071ee322a6d0543fe6515334c92f1e73d161f8157a05e | https://www.bls.gov/cpi/research-series/r-cpi-u-rs-changes.htm | Internet Archive capture 20260819055434 | 2026-11-13T10:42:57Z |
| `sources/bls_r-cpi-u-rs-home_ia20261014233717.htm` | 21,995 | e921857cafedfef64fb2d6063f36cb3575e32d609e6c809eb4732142ebcec6ba | https://www.bls.gov/cpi/research-series/r-cpi-u-rs-home.htm | Internet Archive capture 20261014233717; stored gzip as served | 2026-11-13T10:42:28Z |
| `sources/bls_shutdown-cpi-faq_ia20261110081902.htm` | 28,968 | f78899af367a03e2635514074f2c774c215958835a70188868b57d8b6b901230 | https://www.bls.gov/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi-faq.htm | Internet Archive capture 20261110081902; stored gzip as served | 2026-11-13T10:44:32Z |
| `sources/bls_treatment-owner-occupied-housing_ia20260819123230.htm` | 183,952 | 99c92c955ed660502f25f4dfe55290643945f3110eeb5b129d230149f32f6de5 | https://www.bls.gov/cpi/additional-resources/treatment-owner-occupied-housing.htm | Internet Archive capture 20260819123230 | 2026-11-13T10:44:30Z |
| `sources/census_2007_ACSSubjectDefinitions.pdf` | 413,028 | 4674fae6a2906132c5cad94327cbd455adcec5e201ee40080547ee643c688b06 | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2007_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:58Z |
| `sources/census_2008_ACSSubjectDefinitions.pdf` | 473,226 | a4130bc455e833589db4a5a904ed5625986ad8b6e01a6d5b818a178b0ba7661b | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2008_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:32Z |
| `sources/census_2010_ACSSubjectDefinitions.pdf` | 688,859 | dd016f630ab0435e2e3edfe21ec5aed5ca5a24391e1efb7a5f022d0332336012 | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2010_ACSSubjectDefinitions.pdf | direct | 2026-11-14T02:13:33Z |
| `sources/census_2025_ACSSubjectDefinitions.pdf` | 1,207,867 | c13e11c0994a9339f5e164e4dec1e0557632bcdf4fea64bfda8aed8cdf18d81b | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2025_ACSSubjectDefinitions.pdf | direct | 2026-11-13T11:21:16Z |
| `sources/census_ACS20211YR_Table_Shells.txt` | 7,132,817 | 96271eba7aef8c2ba641b20d691d34e5bc1f02ba8d5014280e761a8fc7ff0345 | https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/ACS20211YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z |
| `sources/census_ACS20221YR_Table_Shells.txt` | 7,165,226 | ebffe6952c7eca126c7583e045a30fec349f6bd977107cedd171c912f7c15b06 | https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/documentation/ACS20221YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z |
| `sources/census_ACS20231YR_Table_Shells.txt` | 7,201,348 | e25ee815917f1b660d0b2c2a86d814ee3c18add086e0d6ac94f35c7ecbfb4711 | https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/documentation/ACS20231YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z |
| `sources/census_ACS20241YR_Table_Shells.txt` | 7,230,781 | 2e4d8a460131be19ca06e87bb478e12ccb4dd44892369245049ee0e463454ad4 | https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/documentation/ACS20241YR_Table_Shells.txt | direct | 2026-11-14T02:04:31Z |
| `sources/census_ACS20251YR_Table_Shells.txt` | 7,242,343 | ff33ade0dad19e66d86027604bcef5f41bbfe1a77ac494735a9f36d693491799 | https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/documentation/ACS20251YR_Table_Shells.txt | direct | 2026-11-13T11:20:56Z |
| `sources/census_acs2005_Chapter_5_tables_summary_list.xls` | 330,240 | f387cff6a03f4ecbad22a88e1e6d6443e3d3941cf8bd24bb466d3e8c8678d73e | https://www2.census.gov/programs-surveys/acs/summary_file/2005/documentation/Chapter_5_tables_summary_list.xls | direct | 2026-11-13T10:50:12Z |
| `sources/census_acs2006_merge_5_6_final.txt` | 1,674,574 | b39ee2cf63c381d835e810e68e1e78aef5e929c6939f82a6657fb8f2ad83441e | https://www2.census.gov/programs-surveys/acs/summary_file/2006/documentation/merge_5_6_final.txt | direct | 2026-11-14T02:01:50Z |
| `sources/census_acs2007_merge_5_6_final.xls` | 4,410,368 | 8246bc4c0d501a5615dbf0a5f6f06f173b9d384182ec0afaea5ff60b8293915d | https://www2.census.gov/programs-surveys/acs/summary_file/2007/documentation/1_year/merge_5_6_final.xls | direct | 2026-11-14T02:01:50Z |
| `sources/census_acs2008_merge_5_6.xls` | 4,064,768 | 4074b43acc6a37e1e1147797976afa76b562b3781e3a3f779592beeaffcb2b7c | https://www2.census.gov/programs-surveys/acs/summary_file/2008/documentation/1_year/user_tools/merge_5_6.xls | direct | 2026-11-14T02:01:51Z |
| `sources/census_acs2009_merge_5_6.txt` | 2,116,794 | edcebf584f18b0af151db5750669c5a0afc04b83ad6f8c36a1f5f408ba454856 | https://www2.census.gov/programs-surveys/acs/summary_file/2009/documentation/1_year/user_tools/merge_5_6.txt | direct | 2026-11-14T02:01:51Z |
| `sources/census_acs2010_Sequence_Number_and_Table_Number_Lookup.txt` | 2,075,282 | 6061be158b19563dfdd88c4d8eb0aab6ae7358935dc93ea8e9ae7bb7c55d8832 | https://www2.census.gov/programs-surveys/acs/summary_file/2010/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-13T10:49:55Z |
| `sources/census_acs2011_Sequence_Number_and_Table_Number_Lookup.txt` | 2,795,890 | 6dce93f44467c9ce5aeb2b0ef4e6edd28f5628b1a6b038e3dfed0fe3d3e08bf9 | https://www2.census.gov/programs-surveys/acs/summary_file/2011/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:51Z |
| `sources/census_acs2012_Sequence_Number_and_Table_Number_Lookup.txt` | 2,132,644 | ca59b70dd6cdea7497d4b37dbbb65ec896159fe44abd8acd8858359a5f2e0197 | https://www2.census.gov/programs-surveys/acs/summary_file/2012/documentation/1_year/user_tools/Sequence_Number_and_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:51Z |
| `sources/census_acs2013_ACS_1yr_Seq_Table_Number_Lookup.txt` | 2,068,726 | f8fbeb1dfbb4ac521938f9022bce6ce5f873e0196108151e3e448223e11bbdc1 | https://www2.census.gov/programs-surveys/acs/summary_file/2013/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z |
| `sources/census_acs2014_ACS_1yr_Seq_Table_Number_Lookup.txt` | 1,907,089 | b66f2b10bb932de964fad4f95466f6bc85190d181ff17578ebcf95eb910085ee | https://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z |
| `sources/census_acs2015_ACS_1yr_Seq_Table_Number_Lookup.txt` | 1,901,019 | ec33e9fadf4febd36864e8e9439cf31339e8bece91b32bdae8cdb7da60282e34 | https://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:49:36Z |
| `sources/census_acs2016_ACS_1yr_Seq_Table_Number_Lookup.txt` | 1,907,695 | 36868b37a395e306a856140e34d4b945bb4a0cb5d6a99d8c8070a6f2b0936874 | https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z |
| `sources/census_acs2017_ACS_1yr_Seq_Table_Number_Lookup.txt` | 2,005,809 | d35a4facf6b39902b4df0008072b8719ef97a195279ad93619ed0b4bc98b7d5b | https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:57:39Z |
| `sources/census_acs2018_ACS_1yr_Seq_Table_Number_Lookup.txt` | 2,120,082 | 36dd6ae97ce97e739a35fe4620a4a6df761b06c4a37d252c316653597e6e64f7 | https://www2.census.gov/programs-surveys/acs/summary_file/2018/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-14T02:01:52Z |
| `sources/census_acs2019_ACS_1yr_Seq_Table_Number_Lookup.txt` | 2,121,821 | b08fe2b87c8720c52bac58146702a732e4d9d281ed0fbec6acf2eabd460d59a0 | https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt | direct | 2026-11-13T10:48:29Z |
| `sources/census_ahs-introduction-history.html` | 346,788 | c739740f94fa8629d1c1afe82dbc7beedb723fc97db3f3cfff32e3c89ff6565c | https://www.census.gov/programs-surveys/ahs/about/ahs-introduction-history.html | direct | 2026-11-14T02:23:26Z |
| `sources/census_ahs2023_definitions.pdf` | 951,112 | dc037d61fcae13571215c86e02b9c6f8ca5145bae4c9062648bbd412d5b95f46 | https://www2.census.gov/programs-surveys/ahs/2023/2023%20AHS%20Definitions.pdf | direct | 2026-11-13T11:28:06Z |
| `sources/census_citation.html` | 369,394 | e3ae437d0edb60bcfe244529e433a06aaca71ecaa8d883577456276e6a9b8286 | https://www.census.gov/about/policies/citation.html | direct | 2026-11-13T10:37:33Z |
| `sources/census_coh_values.html` | 337,548 | 9b01c5a692316a869b500c6a6bcb5535631aeb7bf7aa9e62135fe2e806e6b78e | https://www.census.gov/data/tables/time-series/dec/coh-values.html | direct | 2026-11-10T00:13:34Z |
| `sources/census_cpi_2005.pdf` | 189,538 | d358bbe410c793720059d13f62fdf834ff6be20e95df0abcb5d655d4fe77a28b | https://www.census.gov/construction/pdf/cpi_2005.pdf | direct | 2026-11-13T10:38:32Z |
| `sources/census_cpi_faqs.html` | 65,129 | 97397b93934563e92efc23735130f0aaa8492dcf35e3f0e32dd698c1e8a4dcf3 | https://www.census.gov/construction/cpi/faqs.html | direct | 2026-11-13T10:38:26Z |
| `sources/census_descpi_sold.pdf` | 59,188 | 87af6bcb1f6847cbed7f7fa53049c635f164776c5186e1b1dae0e772edf871b0 | https://www.census.gov/construction/cpi/pdf/descpi_sold.pdf | direct | 2026-11-13T10:37:32Z |
| `sources/census_generalinformationaboutpriceindexes.pdf` | 92,537 | a95d2dc3012f3ed896f99a73dfa063756b9695fa6c1b05e706fb80065987f306 | https://www.census.gov/construction/cpi/pdf/generalinformationaboutpriceindexes.pdf | direct | 2026-11-13T10:37:32Z |
| `sources/census_open_gov.html` | 325,233 | 382083d5f3ea2168194620046bd7c34aec767eb66c5bb55aa4e1c547fa9b6cb0 | https://www.census.gov/about/policies/open-gov.html | direct | 2026-11-13T10:37:32Z |
| `sources/census_priceindexregressionmodel.pdf` | 21,927 | 100dc3c0f90cfa13e99e1b25ca9ab560a2f27a08c410fc38bcaea7001a53ca06 | https://www.census.gov/construction/cpi/pdf/priceindexregressionmodel.pdf | direct | 2026-11-13T10:38:26Z |
| `sources/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf` | 2,263,304 | 7aaeadcd06a98abfff9c6c5f957493d2783f19a85752f618efea562867271c58 | https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf | direct | 2026-11-13T10:40:47Z |
| `sources/cfpb_reg_c_1003_3.html` | 219,224 | ecb3db5a92aec5c2b778f12077d8599b122a716bd536e2b71c41006a6ca0d804 | https://www.consumerfinance.gov/rules-policy/regulations/1003/3/ | direct | 2026-11-13T11:23:13Z |
| `sources/cfpb_reg_c_1003_4.html` | 428,292 | 51df8fa6a3788f63b859fd8a37ae2ab2386fc7f0bef1cb103dae54495fc23f39 | https://www.consumerfinance.gov/rules-policy/regulations/1003/4/ | direct | 2026-11-13T10:41:47Z |
| `sources/cfpb_website_privacy_policy_legal_notices.html` | 159,054 | 0a7d67237a638ecfbb5f5f59522fef8463e6c88bd6e5914b9de49a071d6c381a | https://www.consumerfinance.gov/privacy/website-privacy-policy/ | direct | 2026-11-13T10:42:16Z |
| `sources/cox_followill_page.html` | 105,651 | 2aba739036778637f044e0d5cb0a25aeb88ccb138748f8c4f60d212fbfdac2b1 | https://www.financialplanningassociation.org/article/journal/MAY18-rent-or-buy-30-year-perspective | direct | 2026-11-13T11:09:41Z |
| `sources/crossref_10.1086_376953.json` | 4,844 | 025b08c7042945a7d8884393c78305e4cee734cb75aae67c3679a136e20d0fcd | https://api.crossref.org/works/10.1086/376953 | direct | 2026-11-13T11:20:15Z |
| `sources/crossref_10.1111_j.1475-4991.2008.00274.x.json` | 4,659 | 34476a27375c40350511b424c040147a28643bcf3d7d3992d379f6486aba136f | https://api.crossref.org/works/10.1111/j.1475-4991.2008.00274.x | direct | 2026-11-14T02:06:04Z |
| `sources/crossref_beracha-johnson-2012_work.json` | 6,983 | 929ce0d8e3778076dcb0b9357b14eaf9424da9334b45706dfda5a74f0cd54564 | https://api.crossref.org/works/10.1111/j.1540-6229.2011.00321.x | direct | 2026-11-13T11:07:29Z |
| `sources/crossref_beracha-skiba-johnson-2017_work.json` | 3,052 | 96b52e01499decc5283eedd17a3e64c936d73113d4ddd07c9f06eaa01e35fd66 | https://api.crossref.org/works/10.1080/10835547.2017.12092125 | direct | 2026-11-13T11:07:40Z |
| `sources/crsp_us_stock_databases.html` | 955,840 | 82244a4f5bb871164c6de15d247d622a6de105d6ac24dd6e525aed279c7b0a5b | https://indexes.morningstar.com/research-data-products/crsp-us-stock-databases | direct | 2026-11-13T11:01:41Z |
| `sources/dlm_roiw_2008-13.pdf` | 81,730 | 5d94feb5195f49a7975cc875ddfb5d5f41bb5169a5202d1ed4b5bc32b24dbaed | http://www.roiw.org/2008/2008-13.pdf | direct | 2026-11-13T11:25:57Z |
| `sources/entrepreneur_terms.html` | 122,620 | fa6fb5c46bec1600570893e4733b3479fec9af25bc397125ea02ae86e0ac800b | https://www.entrepreneur.com/terms-of-service | direct | 2026-11-13T11:04:04Z |
| `sources/fhfa_faqs_hpi.html` | 133,851 | ea600ca68179a72f3a46df0fda5b0e8bdc68509415f38332ceb6d90fe564cc79 | https://www.fhfa.gov/faqs/hpi | direct | 2026-11-13T10:35:18Z |
| `sources/fhfa_hpi-technical-description.pdf` | 78,095 | 1d78a08feadd9977b5dd09f45e84c79b05855b02af8b9da055a727a5e6347e06 | https://www.fhfa.gov/document/d/hpi/hpi-technical-description | direct | 2026-11-13T10:36:09Z |
| `sources/fhfa_hpi_datasets.html` | 550,219 | 679ad59073fe01e294c7b06a1fc3e019a51cac848da3c5c2b2e89c1806078c71 | https://www.fhfa.gov/data/hpi/datasets | direct | 2026-11-13T10:35:17Z |
| `sources/fhfa_hpi_dictionary.xlsx` | 17,456 | 388ac3dbc639f7d2dab5a44bb05d7ec2b1a894e6612e2aa036bc915108970084 | https://www.fhfa.gov/document/d/hpi/hpi_dictionary.xlsx | direct | 2026-11-13T10:36:08Z |
| `sources/fhfa_hpi_faqs_2026-11-13.html` | 133,851 | ea600ca68179a72f3a46df0fda5b0e8bdc68509415f38332ceb6d90fe564cc79 | https://www.fhfa.gov/faqs/hpi | direct | 2026-11-13T10:35:18Z |
| `sources/fhfa_hpi_technical_description_1996.pdf` | 78,095 | 1d78a08feadd9977b5dd09f45e84c79b05855b02af8b9da055a727a5e6347e06 | https://www.fhfa.gov/document/d/hpi/hpi-technical-description | direct | 2026-11-13T10:36:09Z |
| `sources/fhfa_ia20180917224523_HPI_PO_summary.xls` | 64,512 | 16cec8f2864b08263a708f50c8050a0fd1669c5a5fc8da438f309a5c274bcc4b | https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_PO_summary.xls | Internet Archive capture 20180917224523; CDX digest Y5J2PA3OOXPTLB7BJ7TENLRR63NAS5PP matches | 2026-11-14T02:06:00Z |
| `sources/fhfa_website_privacy_policy.html` | 99,730 | 7b88250e8d25af3832e777cd85c0aad598e9ba58714871237f1f14398b1dc248 | https://www.fhfa.gov/about/fhfa-policies/website-privacy-policy | direct | 2026-11-13T10:35:18Z |
| `sources/fm_202210-Note-PMMS-07_ia20230513054834.pdf` | 368,980 | 2d788a3ba7a8966628227b4bcf4020117a7e1b2b042ce42655e02521d70e76bf | https://www.freddiemac.com/research/pdf/202210-Note-PMMS-07.pdf | Internet Archive capture 20230513054834 | 2026-11-14T02:05:42Z |
| `sources/fm_202210-Note-PMMS-12_ia20250819015623.pdf` | 398,131 | dcd50a8f4d57fa37f6ce85ed2aaba3029064b2d08cd180a23eef3d5eeb53ac05 | https://www.freddiemac.com/research/pdf/202210-Note-PMMS-12.pdf | Internet Archive capture 20250819015623 | 2026-11-14T02:05:40Z |
| `sources/fm_freddiemac_content_use_ia20260614201536.html` | 103,406 | 1f78f82623e47d9b0c9b025bbef6bcf2a4c19bd15ee4cb406c79ddc7bd366cca | https://www.freddiemac.com/terms/content-use | Internet Archive capture 20260614201536 | 2026-11-13T10:38:21Z |
| `sources/fm_freddiemac_terms_ia20261019233334.html` | 25,951 | 3f1011c921d7798bb98917fcf227f4c7401f06fc08cb10469fa86e8b294af334 | https://www.freddiemac.com/terms | Internet Archive capture 20261019233334; stored gzip as served | 2026-11-13T11:04:31Z |
| `sources/fm_pmms_definitions_ia20260412130140.html` | 85,461 | d866b1faaf167208ce90815068c74cd7a3ecdaaed9a79d5c9be2c5f7db0d7543 | https://www.freddiemac.com/pmms/weightings/weightings_series_011 | Internet Archive capture 20260412130140 | 2026-11-13T11:04:33Z |
| `sources/fm_pmms_ia20261112180833.html` | 20,451 | 1944e49ba10b5a4fd525896ceae9e25a6bcb21e55fdf27a75692ecfd2b7a2757 | https://www.freddiemac.com/pmms | Internet Archive capture 20261112180833; stored gzip as served | 2026-11-13T11:04:34Z |
| `sources/fm_pmms_note_2019_explained_ia20251012225852.html` | 105,880 | 32aad63a2c60d46e29bf1288d2bc1ed3e3875797ec495fe28ce3b8fbd5278036 | https://www.freddiemac.com/research/insight/20190614-mortgage-rate-survey-explained | Internet Archive capture 20251012225852 | 2026-11-13T10:35:03Z |
| `sources/fpa_FPA_Terms_of_Service_2025.pdf` | 97,778 | 440914a280c300df1386647df78c6d6a3f4283de96243b89a82ea7d50426a7c1 | https://www.financialplanningassociation.org/sites/default/files/FPA_Terms_of_Service_2025.pdf | direct | 2026-11-13T11:10:33Z |
| `sources/frb_disclaimer.htm` | 85,306 | 55424b86691fd059b5ff64370219b27ff6e10def9ed63f352f5080cf82b304a3 | https://www.federalreserve.gov/disclaimer.htm | direct | 2026-11-13T11:41:17Z |
| `sources/frb_feds_note_accessible_20250512.htm` | 82,285 | 353d60a1816e85479e988281248b5f06e287fe5016ab9bd6f8c0f6c70a37d0f6 | https://www.federalreserve.gov/econres/notes/feds-notes/commissions-and-omissions-trends-in-real-estate-broker-compensation-accessible-20250512.htm | direct | 2026-11-13T11:09:29Z |
| `sources/frb_feds_note_commissions_20250512.html` | 128,406 | deac5652b5fccb5d405e4329d990c1546838c49027662bab9a32828a92f2b931 | https://www.federalreserve.gov/econres/notes/feds-notes/commissions-and-omissions-trends-in-real-estate-broker-compensation-20250512.html | direct | 2026-11-13T11:09:29Z |
| `sources/frb_fof_series_FL155035013.html` | 87,579 | 9ed7ad267572d7841d75632a654260bc2db85f54fb4c14ee9637be3194cc34b9 | https://www.federalreserve.gov/apps/fof/SeriesAnalyzer.aspx?s=FL155035013&t= | direct | 2026-11-13T11:40:44Z |
| `sources/frb_fof_series_FL155035015.html` | 84,524 | 4a5ca8c72382b3701478212b6e300749c9acb283efd16013686a413e36f08d7e | https://www.federalreserve.gov/apps/fof/SeriesAnalyzer.aspx?s=FL155035015&t= | direct | 2026-11-13T10:42:46Z |
| `sources/frb_fof_series_LM155035015_v2.html` | 81,262 | 604c99aaa6a6a221289a1b0006c89fe44ae8c3ded0ee6c759b99beb7ad711cb5 | https://www.federalreserve.gov/apps/fof/SeriesAnalyzer.aspx?s=LM155035015&t= | direct | 2026-11-13T10:42:40Z |
| `sources/frb_z1_current_S14_b.htm` | 132,856 | 6da045e6189fe171796769971b39ba97770402ff5f7926708076d994b9eeee43 | https://www.federalreserve.gov/releases/z1/current/html/S14_b.htm | direct | 2026-11-13T11:31:05Z |
| `sources/french_data_library.html` | 245,761 | dd48316327898aea2e3ad3dd070b34c3325ce3b25ced7f719245efd5ad36146a | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html | direct | 2026-11-13T10:34:34Z |
| `sources/french_f-f_factors.html` | 17,018 | 9a851fe8e34edef5ef2b7039cd296fb20892fce1ba3de5deca53481e034988af | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html | direct | 2026-11-13T10:34:34Z |
| `sources/french_f-f_factors_archive.html` | 18,977 | 147ed35c5957128428ecc3942dfab8ba08d8b9823868442084e5cec134a7ff07 | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors_archive.html | direct | 2026-11-13T11:05:05Z |
| `sources/hm2003_moretti_real-estate19.pdf` | 309,636 | 28954859ddadef701dbeb10125f7d6e1ad54acf45ef884d70670350e2cdb2f78 | https://eml.berkeley.edu/~moretti/real-estate19.pdf | direct | 2026-11-13T11:20:38Z |
| `sources/ia_terms_metadata_ia-page-terms.json` | 21,345 | b4bceb2d384b79ca841dbf8a0911ca8afbb8fd90838cc1bd721ba8549d97f1ed | https://archive.org/metadata/ia-page-terms | direct | 2026-11-13T10:45:37Z |
| `sources/ici_copyright_linking_ia20260514103053.html` | 337,208 | 6714157443d67205556bcfc05b87f8280bc289326211ada27fbd8abc2c81601a | https://www.ici.org/copyright-and-linking-policies | Internet Archive capture 20260514103053 | 2026-11-13T10:46:19Z |
| `sources/ici_per32-01_ia20261103124156.pdf` | 1,098,280 | 6875768b0b2436044e98d0373b317bdfd2570eff2423e047a27be432bd4c21fd | https://www.ici.org/system/files/2026-03/per32-01.pdf | Internet Archive capture 20261103124156 | 2026-11-13T10:41:30Z |
| `sources/ici_permissions_ia20260602125954.html` | 46,239 | 04a232bbafed33a6cb4546985145796d50f8bc66748bf07e6a2c6794fa61a793 | https://www.ici.org/permissions | Internet Archive capture 20260602125954; stored gzip as served | 2026-11-13T10:43:56Z |
| `sources/kcfed_ia20260930093421_disclaimer.html` | 611,001 | 5973d10f65c0367d3cf001ce69c9ae1ec7c4b702063d3a010da4992c975acf48 | https://www.kansascityfed.org/about-us/disclaimer/ | Internet Archive capture 20260930093421 | 2026-11-13T11:21:06Z |
| `sources/kiyosaki_ia20160528151441_page.html` | 49,900 | a15b95f2eb8c240b2979119e5fbf9dd9235ce4a2a033582662f5abeb4d01fb8d | https://www.entrepreneur.com/article/276512 | Internet Archive capture 20160528151441 | 2026-11-13T11:03:50Z |
| `sources/kiyosaki_page.html` | 217,679 | e5b4adbf8e12bf11b718c7e0f8a0641168c8da58f204c21bd4931ef001bf19b5 | https://www.entrepreneur.com/money-finance/true-financial-literacy-starts-with-questioning-traditional/276512 | direct | 2026-11-13T11:02:33Z |
| `sources/naic2021_naic_hmr_ia20240217020958.pdf` | 8,117,340 | b1c98f9c1753730593a0c9329f23d6e44168aa0459ba2c020867a94b5d57c638 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20240217020958 | 2026-11-13T11:31:11Z |
| `sources/naic2022_naic_hmr_ia20250706013631.pdf` | 6,091,715 | 369718e3f64767077c1639902d8a053c42b3110a2dd0c3cf802ca4658ca69858 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20250706013631 | 2026-11-13T11:31:09Z |
| `sources/naic2023_naic_hmr_zu_homeowners_report_ia20261011104807.pdf` | 7,540,197 | b157866e6656e17041416665557867f4effe77b7b124656a747d2833ea9f4739 | https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf | Internet Archive capture 20261011104807 | 2026-11-13T10:53:01Z |
| `sources/rappaport_ia20251115193619_PDF-10q4Rappaport.pdf` | 628,189 | 79d422b6e81e14f189ade53d426f7de3e05c93971d7d0f5c1216c78dff604231 | https://www.kansascityfed.org/documents/379/PDF-10q4Rappaport.pdf | Internet Archive capture 20251115193619 | 2026-11-13T11:17:40Z |
| `sources/tandf_ia20240228204601_page.html` | 17,925 | 981f3b1c805e9425895a45ff6953969a9c4d03aa2b5871e84046d0d9cbb4eeb5 | https://www.tandfonline.com/doi/abs/10.1080/10835547.2017.12092125 | Internet Archive capture 20240228204601; stored gzip as served | 2026-11-13T11:10:59Z |
| `sources/vanguard_50_facts.html` | 142,642 | 827f49d038781a9bbf1e1288b1b7a560e7ff1f824f75dfe71106edfd5de3e914 | https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/50-years-50-facts-indexing-since-1976.html | direct | 2026-11-13T10:39:31Z |
| `sources/vanguard_press_500_50th.html` | 51,910 | 058cbfb430b0a8f2f8bba741f968184af81621011c9507d79960baa8c24acb9a | https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are/pressroom/press-release-50th-anniversary-vanguard-500-index-fund-083126.html | direct | 2026-11-13T10:39:16Z |
| `sources/vanguard_terms_of_use.html` | 29,569 | 7887275ab31a9254cdd2efadb113a069ad4120dc8476738aa65412f979ef192f | https://corporate.vanguard.com/content/corporatesite/us/en/corp/terms-of-use.html | direct | 2026-11-13T10:40:03Z |
| `sources/wiley_ia20200221224323_page.html` | 70,452 | 95c0af43f5e14b5d518b65008bc587856e6137c3af959165ad2770c580315e4a | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6229.2011.00321.x | Internet Archive capture 20200221224323 | 2026-11-13T11:09:16Z |
