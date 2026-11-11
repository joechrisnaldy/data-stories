# Data for Post 29

The data files are not committed. Each file below is frozen by its `sha256` hash, which `profile_data.py` checks (run `python3 profile_data.py` from the post folder). The script then prints the coverage of each series the analysis reads, and the cross-checks it runs; the code lists, titles and footnote files are kept for reference. A fresh download may differ and then needs a new vet. The definitions behind each variable, quoted from the defining documents, are in `docs/provenance-audit.md`. The downloads used a generic user agent, and the robots file of each host was read and kept with the stored documents.

## Home prices

- **New homes.** U.S. Census Bureau and U.S. Department of Housing and Urban Development, Survey of Construction: the median sales price of new houses sold in the United States, annual, in current dollars, lot included. The constant-quality (Laspeyres) price index of new houses sold and the median floor area of new houses sold come from the same survey. Census publishes these as open data; cite the Census Bureau and HUD.
- **Existing homes.** FHFA House Price Index, all-transactions, United States, quarterly and not seasonally adjusted; the build takes the mean of each year's four quarters. FHFA's terms ask for the attribution and the notice: this product uses FHFA data but is neither endorsed nor certified by FHFA.
- **Anchors.** The median value of specified owner-occupied homes in the census year the existing-home check is anchored to, and the median value of owner-occupied units in the American Community Survey.

```
data/census_nrs_price_cust.xlsx            d543bbad67384a30292f64a4965b33c62a03b7340425e0d37b3c2cde3f119237
  https://www.census.gov/construction/nrs/xls/price_cust.xlsx   (sheet Annual: median and average, 1963 to 2025)
data/census_nrs_price_sold_cust.xlsx       9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3
  https://www.census.gov/construction/nrs/xls/price_sold_cust.xlsx   (sheet Price Index, column Annual index, 2005 = 100)
data/census_chars_soldsquarefeet_cust.xls  b3e24b4beef8026c423ecad7b438d2eb0985f0b13751c06c5087aa09304cd34e
  https://www.census.gov/construction/chars/xls/soldsquarefeet_cust.xls   (sheet SoldMedAvgSF, 1978 to 2025)
data/fhfa_hpi_at_us_and_census.csv         580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba
  https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_us_and_census.csv   (rows USA, 1975Q1 to 2026Q2; release of 2026-10-27)
data/census_coh_values_unadj.txt           5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6
  https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-values/values-unadj.txt
data/census_acs_b25077_2025.dat            7ab895b182348af2e79cb31e45717be5fdcc38ab1e1ad959cb4e0e7e9393b772
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25077.dat
retrieved 2026-11-10 (UTC)
```

## Incomes and homeownership

- **Incomes.** U.S. Census Bureau, Current Population Survey, Annual Social and Economic Supplement, Table H-10: median household income by age of householder, current dollars. Where Census publishes an alternate row for a year, the build uses the row Census marks for comparison with later years; the alternate is a check.
- **Homeownership.** U.S. Census Bureau, Current Population Survey and Housing Vacancy Survey, annual statistics, Table 17: homeownership rates by age of householder. The final year averages eleven months.

```
data/census_h10ar.xlsx         fe3041e6445323518e6919b02d82461c15777037391108d23420b094f17d1d53
  https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h10ar.xlsx   (release of 2026-09-15)
data/census_hvs_ann25t_17.xlsx c9f6e22b5bce78b657cae7cd2fa69e592916e1a3acfe9055c3425ac9851da194
  https://www.census.gov/housing/hvs/files/annual25/ann25t_17.xlsx
retrieved 2026-11-10 (UTC)
```

## Interest

Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, the whole package from the Data Download Program; the build reads series `RIFSGFSM03_N.A`, the 3-month Treasury bill secondary market rate, discount basis, annual. The Board's site places its information in the public domain unless otherwise indicated and asks to be cited.

```
data/frb_h15_package.zip   295b4e17daf1d2ae6fdd215d5aa2c9d4e9cce98eaddad40e18749cd345e3dc3a
  https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&filetype=zip   (retrieved 2026-11-10T01:54:40Z)
```

## Pay, prices and spending (Bureau of Labor Statistics)

Every BLS file here is an Internet Archive copy of the official file, and its content matches the archive's own record. The archive's terms ask that it be listed in the bibliography. BLS data are public domain; cite BLS and do not use its emblem.

- **Pay.** Median usual weekly earnings of full-time wage and salary workers, annual averages, series `LEU0252888500` (ages 25 to 34). The archived copy of the current file stops partway through, after the rows the build reads; a complete copy of an earlier release is kept to check them, and the years they share are identical. The final year averages eleven months.
- **Prices.** The consumer price index retroactive series using current methods, `R-CPI-U-RS`, annual average, and the CPI-U, `CUUR0000SA0`, as a check.
- **Spending.** Consumer Expenditure Surveys, LABSTAT database, means by age of reference person: average annual expenditures, food away from home, entertainment, personal care products and services, and snacks and nonalcoholic beverages bought away from home. The printed tables for the first and last years check the database.

```
data/bls_le_data_alldata_ia20260512.txt   a4585d4f14097762deb6f4988196f353474029d889a5292992d09a3541d81598
  https://web.archive.org/web/20260512154323id_/https://download.bls.gov/pub/time.series/le/le.data.1.AllData
data/bls_le_data_alldata_ia20250802.txt   daad9793a5dbbf03947deed1d9f85d710db0840e15968c5c68852f255df067ec   (complete, earlier release; check)
data/bls_le_series.txt                    137e0d9a6ba1e2bc1b39cc77409483bc4a198e6b7ab0dbdb27454db276810a0f
data/bls_rcpiurs_allitems_ia20260819.xlsx 355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8
  https://web.archive.org/web/20260819055403id_/https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx
data/bls_cu_data_allitems.txt             f3c22c8592d9134fa5ab305fa2df6e37dfd2388f10168985fdbc84082deb4ff0
  https://web.archive.org/web/20261029091858id_/https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems
data/bls_cx_data_alldata.txt              eb080c52b0d213d2f891c1658cd3c5d0860bd3826558e8c07a41108fa4d2cfdd
  https://web.archive.org/web/20260613202524id_/download.bls.gov/pub/time.series/cx/cx.data.1.AllData
data/bls_cx_series.txt                    9755a92a6605d05bae92ca34080b4214500603dd487c37090e0e1ed95b8432f2
data/bls_cx_item.txt                      6c2bcd8c37c8de2f2092376c6a3501e707c0b251c064ffc51485edd298a32e98
data/bls_cx_characteristics.txt           a264f45122a82fc3a56f8304c17bab015b5fad3c45c01eae4b137f9d7fd4d666
data/bls_cx_demographics.txt              ea97efd13956cbc61a63455af584e05cff7f67621e753192ee9ff84424c6809a
data/bls_cx_footnote.txt                  3f32756911577e6df3c007b6400c495c08cdeaa1089988401789f8128b2e0cb5
data/bls_ce_age_1984.pdf                  dd2abcd23013052e846c4f1e232f4225e40b565d6cbdad74cf9d8977d2bd511f
data/bls_ce_age_2024.xlsx                 0abaa86afa5d2b226c21952ff958a2c5300287b2b1fefc115a452f361a55ba86
retrieved 2026-11-10 (UTC), each from its Internet Archive capture
```

## Recent college graduates

Federal Reserve Bank of New York, The Labor Market for Recent College Graduates, https://nyfed.org/collegelabor (the bank's own citation form), monthly unemployment rates, seasonally adjusted three-month moving averages, plotted as published, with the bank's own source line: U.S. Census Bureau and U.S. Bureau of Labor Statistics, Current Population Survey (IPUMS). The bank's terms license reuse with its source identifiers kept and changes labelled; it does not endorse this post.

```
data/nyfed_college_labor_unemployment.csv   f7a508bb5d8091b2d67a3ab1266526cf0b39fc424ad9bd6c2278c3785b55dae7
  https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-unemployment-data.csv
  release of 2026-11-02, retrieved 2026-11-10 (UTC)
```

## Indonesia

- **House prices.** Bank Indonesia, Survei Harga Properti Residensial, the national composite residential property price index for the primary market. The build reads the generic data-series file, which held an older release that starts earlier, and checks it against the newer release. Bank Indonesia's data policy asks users to name it as the source: Sumber: Bank Indonesia, Survei Harga Properti Residensial. The workbooks themselves are not redistributed.
- **Pay.** International Labour Organization, ILOSTAT, median monthly earnings of employees, Indonesia, by age and by area type, from the ILO's processing of the national labour force survey. Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); the post transforms them into growth rates.

```
data/bi_shpr_2018eq100_tw3_2025.xlsx   1f1b7d967c4fa6fd0750b6e67e9eaa333bb3eee045e42fc74c45596ffcc8a4dc
  https://www.bi.go.id/id/publikasi/laporan/Documents/SHPR.zip   (the generic file, as served on 2026-11-10)
data/bi_shpr_tw3_2026.xlsx             153980dd12efc1992de8b2cbb77f23f81c93e8caf92ddc867526e4414d4c62c9
  the data-series file released with the report of 2026-11-06
data/ilo_ear_emtm_sex_age_idn.csv      6aa994d63fba35a328909056ab03975ead57f4e4e8c10a6076bbaf0d2af46b2c
  https://rplumber.ilo.org/data/indicator/?id=EAR_EMTM_SEX_AGE_NB_A&ref_area=IDN&format=.csv&type=label
data/ilo_ear_emtm_sex_geo_idn.csv      1d316f3a6d6eaedc84081783c908d7e540d5b2c6e6651f96a539984435772f61
retrieved 2026-11-10 (UTC)
```

## Not used

FRED; NAR's existing-home prices (its terms bar automated access and storage); FHFA's mortgage interest rate survey (a convenience sample); Bank Indonesia's older index series (superseded; the Internet Archive keeps a copy); and the BLS API, whose robots file disallows all automated agents.
