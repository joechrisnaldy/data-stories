# Data for Post 28

The data files are not committed. Each downloaded file below is frozen by its `sha256` hash, which `profile_data.py` checks before reading it (run `python3 profile_data.py` from the post folder); the same script prints each file's coverage, gaps and key columns and, for each file the analysis uses, the exact rows it reads. A fresh download may differ and then needs a new vet. The built file, `jht_rates.csv`, is made by `extract_jht.py`, which checks the documents it reads instead. The blog is non-commercial. The block under each source gives the file, its hash, when it was fetched and the command that fetches it again. The documents behind the definitions and licences below are stored in `sources/` and listed, with their hashes, in `docs/provenance-audit.md`.

## Sources

### The JHT rate: `jht_rates.csv`

- **What it is.** A row for each figure the design reads from the documents of PT Jamsostek and its successor, BPJS Ketenagakerjaan: the rate credited to JHT balances in each year of the window (kind `base`, or `yearend_reported` for the year with no annual decree), the bonuses rule `R3` names (kinds `incentive` and `oneoff`), and the JHT fund's published investment yield (kind `yield`), which is not what members are credited. Columns: `year`, `kind`, `value_pct` (percent a year, as the document prints it), `applies_to` (the balance the figure is applied to, as the design reads it) and `document` (the stored copy it comes from).
- **How it is made.** It is built, not downloaded. `extract_jht.py` writes it from `docs/jht-manifest.csv`, which holds a row for each figure with the stored document, its `sha256`, the page, a verbatim quote and a note, and from the stored documents in `sources/jht/`. For each row the script checks the document's hash, that the quote occurs once on the cited page and starts and ends on whole words, and that the percentage the quote prints equals `value_pct`. It also checks coverage: a single credited rate for each year of the window, no credited rate after it, no second yield in any year, and exactly the bonus rows `R3` lists. `test_extract_jht.py` corrupts the manifest in the ways those checks are meant to catch and confirms each corruption stops the script.
- **What the manifest's notes record.** Where each rate comes from: the notes to the financial statements for the earlier years with an annual decree, and for 2016 to 2020 the reports' narrative sections, as design amendment `A1` records. They also record which column a table-row quote stops at, and that reading the window's last `base` figure as the rate for balances is an inference; the balances the 2009 incentive and the 2013 payouts were paid on are inferences too, recorded in design amendment `A1` and `docs/provenance-audit.md`, section C. `docs/provenance-audit.md`, sections A to D, reads each row's defining sentence.
- **Gaps.** No credited rate after the window: BPJS has not published those rates. A year inside the yield span has no yield row, since no stored document with a text layer gives it; `extract_jht.py` prints which.
- **Licence and credit.** BPJS Ketenagakerjaan publishes no terms of use, so its reports are quoted under Indonesia's Copyright Law, `Pasal 44 ayat (1) huruf a`, with the source cited in full (`docs/provenance-audit.md`, section K). The year-end figure for the year with no decree comes from a BPJS news release read through an Internet Archive capture, while BPJS's robots file refuses the `ia_archiver` crawler; the audit flags this for the owner. Credit: PT Jamsostek (Persero) and BPJS Ketenagakerjaan.

```
file      data/jht_rates.csv
sha256    4a6ab8b769536e5c66aa0bbbc657563bfde91f58b12fcbfd38b8014f7f37351f
made by   python3 extract_jht.py   (run from the post folder; needs poppler's pdftotext)
reads     docs/jht-manifest.csv
          and the 20 documents in sources/jht/, each pinned by its sha256 in the manifest
check     rebuilt 2026-10-22 from the same manifest and documents: byte-identical
tests     python3 -m unittest test_extract_jht   (17 tests, OK on 2026-10-22)
```

### Stock and bond returns: `damodaran_histretSP.xls`

- **What it is.** Aswath Damodaran (NYU Stern School of Business), Historical Returns on Stocks, Bonds and Bills, the workbook behind the historical returns page of Damodaran Online. The analysis reads the sheet `Returns by year`, column B, headed `S&P 500 (includes dividends)`, and column E, headed `US T. Bond (10-year)`: annual returns as decimal fractions, not percent.
- **What the series are**, by the workbook's own notes (sheet `Explanations and FAQ`). The stock return is the index's price change plus its dividends, over the index level at the start of the year; years before the S&P index existed are back-filled with other large-company indices. The bond return is computed from constant-maturity Treasury yields, which the workbook takes from FRED, by repricing a bond issued at par at the previous year-end yield, with the maturity held constant: a modelled return, not a fund's. This post reads Damodaran's computed returns and does not fetch from FRED.
- **Licence and credit.** The Usage Rules on Damodaran's data history page set no licence terms; acknowledgement is welcome and not required. Credit him as the compiler anyway, and name his inputs: Damodaran, A., Historical Returns on Stocks, Bonds and Bills, NYU Stern School of Business, compiled from the `S&P 500` index (a mark of S&P Dow Jones Indices) and its dividends, and from the constant-maturity yields of the `10-year` US Treasury bond (via FRED). The same section asks that the data not be used in public policy debates. That is a request, not a licence term, and the owner should weigh it before publishing, since the post makes a case about a public scheme.
- **Quirks in the final year of this edition** (outside the window, recorded here for whoever reads the workbook next):
  - The workbook's stock return for that year (`Returns by year`, cell `B118`) and the HTML table's figure differ in the second decimal place. Recomputing it from the sheet `S&P 500 & Raw Data` (index levels and dividends) gives the workbook's figure, so the workbook is the copy read.
  - That year's figure on the sheet `Inflation Rate` is CPI-U November over November, not December over December (checked against the Bureau of Labor Statistics' historical CPI-U table). The analysis takes no inflation from this workbook.
  - The Treasury yield for that year on `S&P 500 & Raw Data` differs from the yield on `T. Bond yield & return`; column E's return is what repricing at the latter gives.
  - The cell labelled `Date updated:` on `Returns by year` is stored in the workbook's own date system (`xlrd` reports `datemode = 1`, the Mac system) and reads as a date in the same January as the HTML page's Updated line. Read in the other date system it looks years stale, which is how the source vet's check read it.

```
file      data/damodaran_histretSP.xls
sha256    28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69
source    https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
page      https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html ("Updated: January 5, 2026")
terms     https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html (Usage Rules)
fetched   2026-10-21 at the source vet; the same URL served identical bytes at 2026-10-22T13:37Z
again     curl -o damodaran_histretSP.xls "https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls"
          Damodaran updates the workbook each January; a later download will carry a new hash.
```

### Consumer prices: `imf_cpi_idn_m.csv` and `imf_cpi_usa_m.csv`

- **What they are.** International Monetary Fund, Consumer Price Index (CPI) dataset, `IMF.STA:CPI(5.0.0)`, as SDMX-CSV with the IMF's metadata columns. The analysis reads the headline index, monthly: rows with `COICOP_1999 = _T`, `TYPE_OF_TRANSFORMATION = IX` and `FREQUENCY = M`. December values are read as published; annual averages of the monthly values, inflation rates and real values are the author's calculations.
- **Indonesia.** Copied unchanged from the previous post (`msci-fear-chain/data/imf_cpi_idn_m.csv`, the same hash as that post's vetted file), which downloaded it from the IMF data portal; the portal query was not recorded. Its headline series is the CPI of BPS-Statistics Indonesia, which links its base years by overlap (IMF DSBB metadata, quoted in `msci-fear-chain/docs/provenance-audit.md`); reference period `2022A`. The API query below returns the same headline monthly values, month for month, with different rows and bytes, so a re-download needs a new hash. In the window, the index's December-to-December change differs from BPS's published December year-on-year inflation (Bank Indonesia's Data Inflasi, below) for `Desember 2008`, `Desember 2013` and `Desember 2020`. The linking is the likely source: the file itself is consistent (its own year-on-year series equals the change in its index), and the headline rows carry the IMF's overlap flag `OL`, whose description says estimates of the same indicator can differ across IMF datasets, among other reasons through splicing series for continuity (the code list is copied to `sources/provenance/imf/imf_api_cpi_codes_extract.txt`; the previous post's provenance audit quotes it). Design amendment `A1` keeps the IMF index for `R5` and `R6`; the year-by-year chart also shows, in some years, JHT's rate against BPS's published December rate.
- **United States.** Fetched for this post from the IMF's SDMX API in the same format. Its headline index is the US Bureau of Labor Statistics' `CPI-U: U.S. city average, all items`, rebased by the IMF to reference period `2010A`: over the months the analysis reads, the IMF index divided by the published CPI-U is constant to machine precision (checked against BLS's historical CPI-U workbook, `historical-cpi-u-202512.xlsx`, an Internet Archive copy kept by the source vet). A month is missing, `2025-M10`, the month BLS did not publish during the lapse in appropriations; it is outside the window.
- **Licence and credit.** The IMF's Copyright and Usage terms, checked for the previous post (`msci-fear-chain/docs/provenance-audit.md`, IMF section), let users download, copy, transform and publish IMF data, provided it carries attribution to the IMF as the source and any material transformation is stated. The IMF's suggested citation, from the files' `SUGGESTED_CITATION` column, reads `International Monetary Fund. Consumer Price Index (CPI),   https://data.imf.org/en/datasets/IMF.STA:CPI. Accessed on [current date].` Charts and notes credit the IMF, name the national compiler BPS-Statistics Indonesia and label annual averages, inflation rates and real values as the author's calculations. The IMF's terms bar training language models on its content without permission; they do not bar reading or quoting it.

```
file      data/imf_cpi_idn_m.csv
sha256    b3ba15f60d304316b78adedd37229ff945c8669b67321f9284196e564071c20b
source    copied from ../msci-fear-chain/data/imf_cpi_idn_m.csv
          (IMF data portal download at that post's vet, 2026-10-16; PUBLICATION_DATE 2026-10-16T06:48:22Z)
again     curl -H "Accept: application/vnd.sdmx.data+csv;version=1.0.0" -o imf_cpi_idn_m.csv \
            "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/IDN.CPI._T..M"
          run 2026-10-22: headline IX monthly values equal the stored file's (705 of 705); other rows differ

file      data/imf_cpi_usa_m.csv
sha256    9789f725405061e7d38fcc1d78fe7cbf7daf9254e13c1f185733f7850f900c17
fetched   2026-10-22T13:30:03Z, HTTP 200, PUBLICATION_DATE 2026-10-22T06:47:02Z
command   curl -H "Accept: application/vnd.sdmx.data+csv;version=1.0.0" -o imf_cpi_usa_m.csv \
            "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/USA.CPI._T..M"
check     its headline IX rows equal the API's XML for USA.CPI._T.IX.M, fetched the same minute
          (860 months, 0 differences); without the Accept header the API answers in XML
check     IMF index / BLS CPI-U constant over 2004-01 to 2020-12 (204 months), BLS file from
          https://web.archive.org/web/20260929081709id_/https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202512.xlsx
          (sha256 1010f74a32661f1fc70aba1871efc202ae8e7865e4776e7f894384128a12e954)
```

### BPS's published inflation: `bi_data_inflasi.xlsx`

- **What it is.** Bank Indonesia's Data Inflasi page (bi.go.id, Statistik, Indikator), saved as a workbook with a single sheet, `Data Inflasi`, with the columns `No`, `Periode` and `Data Inflasi` and a row for each month, each value a percent string in Indonesian notation. The values are BPS's headline consumer price inflation, year on year, as Bank Indonesia reports it; Bank Indonesia's inflation page says the calculation is done by BPS (`sources/provenance/bi/bi_inflasi_definisi.txt`). The file's last row, `Desember 2002`, holds a placeholder value rather than a rate; the reader leaves it out and stops if it ever changes.
- **Why it is here.** Design amendment `A1`: the IMF index stays the measure for `R5` and `R6`, and the year-by-year chart also shows, in some years, JHT's rate against BPS's published December rate (see the Indonesia note above).
- **How it was obtained.** The owner downloaded it by hand from the page below for the previous post, which pins it by the same hash (`msci-fear-chain/build_analysis.py`, key `bi_inflasi`); it is copied here unchanged under a new name. That post cross-checked December values for a sample of years against a second Bank Indonesia publication, its Target Inflasi page, and found them equal.
- **What the analysis reads.** The December row of each year, as `profile_data.py` prints it. The reader is the previous post's `household.read_published_inflation`, reused with its checks: the known placeholder, no repeated month, and an unbroken run of months.
- **Licence and credit.** Bank Indonesia's data policy, Peraturan Bank Indonesia `Nomor 12 Tahun 2024`, `Pasal 21 ayat (4)`, requires external users of its data to name Bank Indonesia as the source (`sources/provenance/rights/bi_pbi_12_2024_data_policy.pdf`; quoted in `docs/provenance-audit.md`, section K). Credit: Bank Indonesia, with BPS-Statistics Indonesia as the compiler. BPS's own site is not used: its robots file blocks Anthropic's crawler (the design's data section).

```
file      data/bi_data_inflasi.xlsx
sha256    5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217
source    copied from ../msci-fear-chain/data/Data Inflasi.xlsx (same sha256, checked before and after
          copying on 2026-10-22)
page      https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx
fetched   2026-10-17, downloaded by hand by the owner in a browser (that post's design, amendment 8.7)
again     download the workbook from the page above by hand; a later download covers later months
          and needs a new hash
policy    https://www.bi.go.id/id/publikasi/peraturan/Pages/PBI_122024.aspx (PBI 12/2024, Pasal 21 ayat (4))
```

### Singapore's CPF rates: `cpf_contribution_rates.csv` and `cpf_allocation_rates.csv`

- **What they are.** The Central Provident Fund Board's datasets CPF contribution rates (`d_98ffa142ae0dec40391f78f81d26aca9`) and CPF allocation rates (`d_97ec9a2ce15cbf253128e48779a3fba0`), published on data.gov.sg. Contribution rates are by effective month, age group and party (employer or employee), for private-sector and non-pensionable public-sector employees, and apply to the top wage band (the dataset's description). Allocation rates split the contribution across the Ordinary, Special, MediSave and Retirement accounts.
- **Units differ between the files.** `contribution_rate` is in whole percent of wages, although the dataset's description says `Percentages are expressed as a number out of 1.`; `allocation_rate` is a fraction of the contribution.
- **Account change.** From `effective_from = 2025-01`, the age groups from `Above 55 - 60 years` up have `Retirement` rows in place of `Special` rows; the allocation dataset's description ties this to the closure of those members' Special Account. The age groups the analysis reads, `35 years & below` to `Above 50 - 55 years`, keep `Special`.
- **What the analysis reads.** From the contribution file, for those age groups, the rows of their last effective date on or before `effective_from = 2026-01` (the rates in force on that date).
- **Licence and credit.** Singapore Open Data Licence: use is allowed whether commercially or non-commercially. The licence requires a conspicuous notice acknowledging the source, with a link to the licence; its example notice, used below, names the dataset and the access date. It also bars any use that suggests official status or an agency's endorsement. The notice, in the form of the licence's example:

```
Contains information from CPF contribution rates and CPF allocation rates accessed on 21 October 2026
from data.gov.sg (Central Provident Fund Board) which is made available under the terms of the
Singapore Open Data Licence version 1.0 https://data.gov.sg/open-data-licence
```

```
file      data/cpf_contribution_rates.csv
sha256    c4529a8e3cb1fb364dcb7d1279dbaf8ee1f73212b7e335d8b711ef735925d2f2
page      https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view

file      data/cpf_allocation_rates.csv
sha256    4cb1fc28020c2b41ed12c8bcc64983a185db54c227352328f070ffe3e1c03b04
page      https://data.gov.sg/datasets/d_97ec9a2ce15cbf253128e48779a3fba0/view

fetched   2026-10-21 about 20:39Z at the source vet; fetched again 2026-10-22 with the steps below,
          byte-identical (same SHA-256 for both)
again     for each dataset id:
            curl "https://api-open.data.gov.sg/v1/public/api/datasets/<id>/initiate-download"
            curl "https://api-open.data.gov.sg/v1/public/api/datasets/<id>/poll-download"
          then fetch the signed URL in data.url once data.status is DOWNLOAD_SUCCESS.
          Without an API key the API rate-limits calls (HTTP 429: try again after ten seconds).
licence   https://data.gov.sg/open-data-licence
```

### Indonesian employment: `ilo_idn_employment_by_status.csv`

- **What it is.** International Labour Organization, ILOSTAT, employment by sex and status in employment, ILO modelled estimates (indicator `EMP_2EMP_SEX_STE_NB_A`, the dataflow named `Employment by sex and status in employment -- ILO modelled estimates, Nov. 2025` on the ILO's SDMX server), Indonesia, both sexes, persons, scaled as the file's `UNIT_MULT` column says (`3: Thousands`). `profile_data.py` reads the rows with `STE: Status in employment` equal to `STE_AGGREGATE_EES: Employees`. These are modelled estimates, not survey counts; some years carry the status flag `A: Adjusted`.
- **How it was fetched.** The source vet pulled this indicator from ILOSTAT's API host, `rplumber.ilo.org`, with `timefrom=2020`, so the vet copy starts there. When this file was built, that host answered repeated requests, its robots file included, with empty responses over several minutes, so the series was fetched instead from the ILO's own SDMX API, `sdmx.ilo.org` (its robots file returns `HTTP 404`, so it sets no rules; no challenge was served). Both serve ILOSTAT's modelled estimates of the same vintage. Checks in the block below tie this file to the vet copy and to a second source: over the years the vet copy covers, the copies agree row for row, on the aggregate and the `ICSE-93` rows, values and status flags alike; and employees derived from the World Bank's World Development Indicators agree with this file's `Employees` rows in each year read. The World Bank's series are themselves built on ILO estimates, so the second check is a second route to the same model, not an independent count.
- **Licence and credit.** The ILO's Rights and permissions page places ILO databases and datasets under the Creative Commons Attribution licence (`CC BY 4.0`) for datasets published from its cut-off date on, which this vintage was; the licence excludes microdata restricted to the ILO's own use. Credit: International Labour Organization, ILOSTAT, ILO modelled estimates (`Nov. 2025` vintage).

```
file      data/ilo_idn_employment_by_status.csv
sha256    73572b2829c2fae8e24396d0580fb9f838d707e66cfc3e03d08b9c221396cdb6
fetched   2026-10-22T13:36:43Z, HTTP 200
command   curl -H "Accept: application/vnd.sdmx.data+csv;labels=both" -o ilo_idn_employment_by_status.csv \
            "https://sdmx.ilo.org/rest/data/ILO,DF_EMP_2EMP_SEX_STE_NB,1.0/IDN.A..SEX_T.?startPeriod=2015"
key       REF_AREA.FREQ.MEASURE.SEX.STE (from the dataflow's data structure, EMP_2EMP_SEX_STE_NB)
check     the source vet's rplumber copy (timefrom=2020, so 2020 to 2025): 48 of 48 rows equal this
          file's in value and status flag, the ICSE-93 rows included (re-checked 2026-10-22)
check     World Bank WDI, Indonesia, from the vet's stored API responses (lastupdated 2026-10-08):
          SL.TLF.TOTL.IN x (1 - SL.UEM.TOTL.ZS / 100) x SL.EMP.WORK.ZS / 100, in thousands, is within
          0.45 thousand persons of this file's Employees row in each year 2015 to 2025 (11 years)
untested  the vet's rplumber URL with timefrom changed from 2020 to 2015; not tested, since the host
          returned empty HTTP 200 responses on 2026-10-22 (the vet's own URL used timefrom=2020):
          https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_STE_NB_A&ref_area=IDN&sex=SEX_T&timefrom=2015&type=label&format=.csv
rights    https://www.ilo.org/rights-and-permissions
```

## Traps hit while building

- The ILO's API host returned empty responses while this folder was built; see the employment section.
- The IMF API serves SDMX-CSV when asked for it with the Accept header shown and SDMX-ML otherwise; the source vet saw it fail with `HTTP 500` when asked for generic SDMX-ML by name.
- The CPF contribution file's description and its numbers disagree on units; read each file's unit separately.
- Damodaran's workbook keeps dates in the Mac date system; a reader that assumes the other system misdates them.
- The IMF's Indonesian index is BPS's CPI linked across base years, and its December-to-December change differs from BPS's published December rate in some window years (the Indonesia note above).
- The IMF files' `FULL_DESCRIPTION` field holds line breaks inside quotes, so a text line is not a record; read the files with a CSV parser.
- The Data Inflasi workbook ends with a placeholder row (`Desember 2002`) that is not a published rate.
