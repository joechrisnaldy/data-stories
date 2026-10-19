# Provenance audit: Post 27 (msci-fear-chain)

Every definition, licence term and external fact the post leans on, with the stored copy of its
defining document (in `sources/`, gitignored) and that copy's SHA-256. Generated 2026-10-17 from
checked entries: each quote occurs exactly once in its stored copy. Data publishers' definitions
and terms are quoted; press articles are listed with a locator only, because their terms do not
grant quotation (design 8.6). No MSCI document is used (design 8.5).

## Rupiah: BIS daily rates and the ECB cross rate (and the rejected OECD share series)

- **OECD share prices, Indonesia (DSD_STES@DF_FINMARK, MEASURE SHARE): monthly average or month-end**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, Indonesia, Share prices, Index*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row REF_AREA=IDN, MEASURE=SHARE, UNIT_MEASURE=IX; attribute DATA_COMP (Data compilation). Raw CSV as fetched: downloads/oecd_finmark_refmeta_idn_share.csv, sha256 f184b0c3ddcecf076f826e99df63afc2920ae68dea14e54017082e833ac512f0.
  Quote: "Monthly data are averages of daily closing figures."
  Establishes: Each monthly value of OECD's Indonesia share price series is the average of that month's daily closes, not an end-of-month value. The same row says quarterly and annual values are averages of monthly figures. So the 10% shock-month rule compares monthly averages, which smooths a crash that happens late in a month. The rupiah rules (L2, L4) use month-end values instead, and the post should say so.

- **OECD share prices, Indonesia: what the index measures (coverage)**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, Indonesia, Share prices, Index*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row REF_AREA=IDN, MEASURE=SHARE, UNIT_MEASURE=IX; attribute COVERAGE (Coverage).
  Quote: "The index covers all companies whose shares are traded on the JSX."
  Establishes: OECD describes Indonesia's series as an all-share index of the Jakarta Stock Exchange (JSX): it covers every listed company, not a narrow blue-chip basket.

- **OECD share prices, Indonesia: index construction and national index named**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, Indonesia, Share prices, Index*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row REF_AREA=IDN, MEASURE=SHARE, UNIT_MEASURE=IX; attribute STAT_CONC_DEF (Statistical concepts and definitions), first sentence.
  Quote: "The index is calculated as the sum of the regular closing price multiplied by the number of shares and divided by the base value."
  Establishes: The underlying index is weighted by market capitalisation (closing price times shares, divided by a base value). The same paragraph calls it the CSPI, first set to 100 on August 10, 1982 and later rebased to August 14, 1991 = 100. OECD then republishes it rebased to 2015=100. Read with the general SHARE row, it is a price index and does not include dividends.

- **OECD share prices, Indonesia: underlying source OECD names**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, Indonesia, Share prices, Index*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row REF_AREA=IDN, MEASURE=SHARE, UNIT_MEASURE=IX; attribute DISS_ORG (Dissemination agency); the English and French values are identical, and only the English value is kept in the text file so the quote occurs once.
  Quote: "Singapore Yahoo Finance"
  Establishes: For Indonesia, OECD names Singapore Yahoo Finance as the dissemination agency, not the Indonesia Stock Exchange or a central bank. The national index is the JSX composite (see the COVERAGE and STAT_CONC_DEF entries). The credit line should read OECD, with the index originally from the Jakarta exchange and the source as OECD names it. Under OECD's terms, the user must check any third-party rights (see the OECD terms entries).

- **OECD share prices, Indonesia: base 2015=100**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, dataflow level*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row 'dataflow level (all series)'; attribute STAT_CONC_DEF (Statistical concepts and definitions), last sentence.
  Quote: "All data are available monthly, and are presented as either an index (where the year 2015 is the base year) or as a level depending on which measure is seen as the most appropriate and/or useful in the economic analysis context."
  Establishes: Indexed series in the dataflow use 2015 as the base year. In the stored data file (data/oecd_share_prices_idn_m.csv, sha256 a7988564668b2af51f9217b2defeca693c08af16a55a2eddbca54f6ef271b25f), every row has UNIT_MEASURE=IX and BASE_PER=2015. Its twelve 2015 monthly values average 100.000004 (computed with python3 -I in this run). That confirms 2015=100, with the 2015 annual average set to 100.

- **OECD share prices (all countries): MEI target definition, simple averages of daily closes**
  OECD (Organisation for Economic Co-operation and Development); OECD Statistics and Data Directorate, short-term economic statistics (SDMX agency OECD.SDD.STES); n.d. (the DATE_LAST_UPDATE field is empty in the metadata). *Financial market (DSD_STES@DF_FINMARK, version 4.0): SDMX reference metadata, Share prices, Index (all countries)*. https://sdmx.oecd.org/public/rest/v2/data/dataflow/OECD.SDD.STES/DSD_STES@DF_FINMARK/4.0/IDN.M.SHARE.*.*.*.*.*.*?attributes=msd&measures=none (Accept: application/vnd.sdmx.data+csv;version=2.0.0;labels=both)
  Stored: `sources/provenance/oecd-bis-ecb/oecd_finmark_refmeta_idn_share.txt` (SHA-256 `66b370e879b0b4caa3547b1d3b38457bac282d51d0442875c081ae0142df4440`), fetched 2026-10-17; Metadata row MEASURE=SHARE, UNIT_MEASURE=IX (all countries); attribute STAT_CONC_DEF, first sentence.
  Quote: "The Main Economic Indicator share indices are targeted to be national, all-share or broad, price indices and use the closing daily values for the monthly data, normally expressed as simple arithmetic averages of the daily data."
  Establishes: This general OECD definition matches the Indonesia-specific note. The monthly values are simple arithmetic averages of daily closing values, and the indices are price indices with no dividends reinvested.

- **OECD reuse terms for data (permitted use)**
  OECD (Organisation for Economic Co-operation and Development); OECD; 2024-07-01 (page footer: 'Last updated on 1 July 2024'). *Terms & Conditions (section 3, Data: Permitted Use)*. https://www.oecd.org/en/about/terms-conditions.html
  Stored: `sources/provenance/oecd-bis-ecb/oecd_terms_conditions_data.txt` (SHA-256 `8a14c4fa8c3346e000e9f7bba72c85bcd3f7ce4fa463b54a57063ecc42400859`), fetched 2026-10-17; Section 3 'Data', accordion 'Permitted Use', first sentence. The excerpt was taken in the Claude Browser pane (curl got HTTP 403 from Cloudflare). The page loaded normally with no challenge. The browser-side SHA-256 of the excerpt body, cdf474d4da97a142008011cabb552d240010faf0f5bffdba7eb01e82b610a107, matches the saved body..
  Quote: "Except where additional restrictions apply as stated above, you can extract from, download, copy, adapt, print, distribute, share and embed Data for any purpose, even for commercial use."
  Establishes: OECD data may be reused and adapted, for example rebased, charted or used to compute shock months, on a non-commercial blog. This holds unless additional restrictions apply (see the third-party caveat entry).

- **OECD reuse terms for data (attribution format)**
  OECD (Organisation for Economic Co-operation and Development); OECD; 2024-07-01 (page footer: 'Last updated on 1 July 2024'). *Terms & Conditions (section 3, Data: Permitted Use)*. https://www.oecd.org/en/about/terms-conditions.html
  Stored: `sources/provenance/oecd-bis-ecb/oecd_terms_conditions_data.txt` (SHA-256 `8a14c4fa8c3346e000e9f7bba72c85bcd3f7ce4fa463b54a57063ecc42400859`), fetched 2026-10-17; Section 3 'Data', accordion 'Permitted Use', second sentence.
  Quote: "You must give appropriate credit to the OECD by using the citation associated with the relevant Data, or, if no specific citation is available, you must cite the source information using the following format: OECD (year), (dataset name),(data source) DOI or URL (accessed on (date))."
  Establishes: Attribution is required. Use the dataset's own citation if it has one; otherwise use the format 'OECD (year), Financial market, (data source) URL (accessed on date)'. Credits in the method notes, chart footers and data/README.md should follow this format.

- **OECD reuse terms for data (third-party ownership caveat)**
  OECD (Organisation for Economic Co-operation and Development); OECD; 2024-07-01 (page footer: 'Last updated on 1 July 2024'). *Terms & Conditions (section 3, Data)*. https://www.oecd.org/en/about/terms-conditions.html
  Stored: `sources/provenance/oecd-bis-ecb/oecd_terms_conditions_data.txt` (SHA-256 `8a14c4fa8c3346e000e9f7bba72c85bcd3f7ce4fa463b54a57063ecc42400859`), fetched 2026-10-17; Section 3 'Data', introductory paragraph, second sentence.
  Quote: "Data may be subject to restrictions beyond the scope of these Terms and Conditions, either because specific terms apply to those Data or because third parties may have ownership interests."
  Establishes: OECD does not warrant that it owns every series. The next sentence makes the user responsible for checking third-party ownership in the metadata. For Indonesia's share prices, the metadata names the Jakarta exchange index and Singapore Yahoo Finance, so the owner should record this caveat in the rights notes.

- **BIS US dollar exchange rates (WS_XRU): definition**
  Bank for International Settlements (BIS); Bank for International Settlements, BIS statistics; n.d.. *Bilateral exchange rates (BIS Data Portal metadata report, topic XRU)*. https://data.bis.org/api/v0/categories/XRU/metadata_report (the API behind https://data.bis.org/topics/XRU)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xru_metadata_report.txt` (SHA-256 `af5ddeaae972a685a73048be6e5a70f5cd733e9655b98f399d5d90a657ebc642`), fetched 2026-10-17; JSON field introLong, first paragraph, second sentence (the raw JSON is downloads/bis_xru_metadata_report.json, sha256 e4eb2025bfcd068135493760e80dec57c483a4fa2a3f3ca80e82f07354920ca2).
  Quote: "They record the nominal value of one US dollar (USD) relative to a given currency."
  Establishes: Each WS_XRU value is units of the national currency per one US dollar. For Indonesia that means rupiah per US dollar. The same paragraph says a decrease means appreciation and an increase means depreciation, so a higher line is a weaker rupiah, as chart 2 requires.

- **BIS WS_XRU series D.ID.IDR.A: identity and units (rupiah per US dollar)**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-10-15 (JSON field last_updated). *Exchange rates against USD, Indonesia, IDR/USD (BIS Data Portal series metadata, D.ID.IDR.A)*. https://data.bis.org/api/v0/dataflows/BIS,WS_XRU,1.0/timeseries/D.ID.IDR.A (the API behind https://data.bis.org/topics/XRU/BIS%2CWS_XRU%2C1.0/D.ID.IDR.A)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xru_series_D.ID.IDR.A.txt` (SHA-256 `77bd53f48a7fa808596a7b5763d7e95bc50462339414d7a15b0fcb087b1dc8ab`), fetched 2026-10-17; JSON field title (the raw JSON is downloads/bis_xru_series_D.ID.IDR.A.json, sha256 7b1020c651d106d504611ba3ab625c6b1bee086a01660b00b56a2c36c7276a93).
  Quote: "Exchange rates against USD, Indonesia, IDR/USD"
  Establishes: Series D.ID.IDR.A is the daily rupiah per US dollar rate (IDR/USD). The same JSON gives start_date 1988-01-01, end_date 2026-10-13, last_updated 2026-10-15, end_value 17880.648 and collection code A. Those match the stored data/bis_idr_usd_daily.csv (sha256 7002a7c243f9c09bb7597e2abc1b279b835eea99447760d9dd26e4c03bd9183b): 10,020 rows from 1988-01-01 to 2026-10-13, last value 17880.64891.

- **BIS WS_XRU series D.ID.IDR.A: unit and multiplier**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-10-15 (JSON field last_updated). *Exchange rates against USD, Indonesia, IDR/USD (BIS Data Portal series metadata, D.ID.IDR.A)*. https://data.bis.org/api/v0/dataflows/BIS,WS_XRU,1.0/timeseries/D.ID.IDR.A
  Stored: `sources/provenance/oecd-bis-ecb/bis_xru_series_D.ID.IDR.A.txt` (SHA-256 `77bd53f48a7fa808596a7b5763d7e95bc50462339414d7a15b0fcb087b1dc8ab`), fetched 2026-10-17; JSON fields unit_code and unit (followed by unit_multiplier "Units").
  Quote: "unit_code":"IDR","unit":"Rupiah"
  Establishes: The values are in rupiah, with unit multiplier Units (UNIT_MULT 0), so they are not scaled by thousands. A value of 17880.648 means 17,880.648 rupiah per US dollar.

- **BIS WS_XRU Indonesia: national source and period, 1988 to January 1999**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-09-24 (PDF: 'Last updated 24 September 2026'). *Long series on US dollar bilateral nominal exchange rates: data documentation (title as printed has an en dash where the colon is shown)*. https://www.bis.org/statistics/xrusd/xrusd_doc.pdf (redirects to https://www.bis.org/pages/statistics/xrusd-documentation.pdf)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xrusd_doc_layout.txt` (SHA-256 `775fec81d4c1f0134b45590720a7ad29eaac2407aa49c2f9a12992acd68efd43`), fetched 2026-10-17; PDF page 4, country table, row 'ID Indonesia, Compilation/Source'. Row membership was confirmed from pdftotext word coordinates: the Indonesia block sits at y = 641.4, 652.7 and 664.0 pt, between Hungary (617.8) and Ireland (693.3). The PDF as fetched is downloads/bis_xrusd_doc.pdf, sha256 0cdbc7ceb74f66bb97dfe6c7a5d76e6884c7d2b0520925fe018534d83beb04e5..
  Quote: "From 1 Jan 1988 to 4 Jan 1999: US Federal Reserve System."
  Establishes: BIS's documented source for the Indonesian daily rate from 1 January 1988 to 4 January 1999 is the US Federal Reserve. This period covers the 1997 float and the 1997 to 1998 crisis segment. The same row gives IMF International Financial Statistics before January 1988, which falls outside the daily file.

- **BIS WS_XRU Indonesia: national source and period, from January 1999**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-09-24 (PDF: 'Last updated 24 September 2026'). *Long series on US dollar bilateral nominal exchange rates: data documentation (title as printed has an en dash where the colon is shown)*. https://www.bis.org/statistics/xrusd/xrusd_doc.pdf (redirects to https://www.bis.org/pages/statistics/xrusd-documentation.pdf)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xrusd_doc_layout.txt` (SHA-256 `775fec81d4c1f0134b45590720a7ad29eaac2407aa49c2f9a12992acd68efd43`), fetched 2026-10-17; PDF page 4, country table, row 'ID Indonesia, Compilation/Source', first line of the block (y = 641.4 pt, confirmed from word coordinates).
  Quote: "From 5 Jan 1999 onwards: ECB."
  Establishes: From 5 January 1999 BIS's documented source is the ECB. The credit line can say: BIS, from US Federal Reserve data to early January 1999 and ECB data since then. See the unresolved note on the one-day mismatch with the stored data.

- **BIS WS_XRU daily data: quotation times by source**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-09-24 (PDF: 'Last updated 24 September 2026'). *Long series on US dollar bilateral nominal exchange rates: data documentation (title as printed has an en dash where the colon is shown)*. https://www.bis.org/statistics/xrusd/xrusd_doc.pdf (redirects to https://www.bis.org/pages/statistics/xrusd-documentation.pdf)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xrusd_doc_flow.txt` (SHA-256 `38c5c10185b8476c22c2bdb8d44dc2006d630f55da7fc91200a8f0ce89abbe8c`), fetched 2026-10-17; PDF page 1, paragraph beginning 'For the most recent periods, daily data from the ECB is the main source'. This file is whitespace-collapsed pdftotext output, so the sentence reads on one line..
  Quote: "Exchange rates are measured at 13:15 GMT for the ECB data and 17:00 GMT for the Federal Reserve."
  Establishes: The timing of each source: ECB-based days are quoted in the European early afternoon, and Federal Reserve days at 17:00 GMT. So the switch at the start of 1999 also changes the quotation time. Neither time is Jakarta's market close.

- **BIS WS_XRU: ECB-based values are cross rates (method for the post's ECB fill)**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-09-24 (PDF: 'Last updated 24 September 2026'). *Long series on US dollar bilateral nominal exchange rates: data documentation (title as printed has an en dash where the colon is shown)*. https://www.bis.org/statistics/xrusd/xrusd_doc.pdf (redirects to https://www.bis.org/pages/statistics/xrusd-documentation.pdf)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xrusd_doc_flow.txt` (SHA-256 `38c5c10185b8476c22c2bdb8d44dc2006d630f55da7fc91200a8f0ce89abbe8c`), fetched 2026-10-17; PDF page 1, section 'Additional information', second sentence.
  Quote: "The BIS series based on ECB data are calculated from the national currency/EUR and the EUR/USD cross rates."
  Establishes: BIS builds its post-1999 rupiah series as IDR per EUR divided by USD per EUR, the same method design 8.4 uses for days after BIS's last observation. I checked this against the stored files in this run. For 2026-10-13, BIS has 17880.64891 and ECB gives 20004.87 / 1.1188 = 17880.648910. For 1999-01-04, BIS has 8002.044279 and ECB gives 9433.61 / 1.1789 = 8002.044279. So the ECB fill continues the BIS series exactly.

- **BIS attribution request (national source to be quoted)**
  Bank for International Settlements (BIS); Bank for International Settlements; 2026-09-24 (PDF: 'Last updated 24 September 2026'). *Long series on US dollar bilateral nominal exchange rates: data documentation (title as printed has an en dash where the colon is shown)*. https://www.bis.org/statistics/xrusd/xrusd_doc.pdf (redirects to https://www.bis.org/pages/statistics/xrusd-documentation.pdf)
  Stored: `sources/provenance/oecd-bis-ecb/bis_xrusd_doc_flow.txt` (SHA-256 `38c5c10185b8476c22c2bdb8d44dc2006d630f55da7fc91200a8f0ce89abbe8c`), fetched 2026-10-17; PDF page 2, last paragraph before the country table.
  Quote: "Series may be downloaded, reproduced and disseminated as long as the appropriate national source is quoted and the BIS terms and conditions are observed."
  Establishes: BIS asks that the national source be credited alongside BIS. For Indonesia, those are the US Federal Reserve (1988 to January 1999) and the ECB (since January 1999), as in the page 4 row.

- **BIS reuse terms for statistics (citation requirement)**
  Bank for International Settlements (BIS); Bank for International Settlements; n.d.. *Legal: Terms of permitted use of BIS statistics (BIS Data Portal)*. https://data.bis.org/help/legal
  Stored: `sources/provenance/oecd-bis-ecb/bis_data_help_legal.txt` (SHA-256 `830947922e176d565943c9b9dade6b129aec6b3f8fb790d52625c6337d4f5a9f`), fetched 2026-10-17; Section 'Terms of permitted use of BIS statistics', first condition after 'The use of the statistics is unrestricted, provided that:' (text file line 32). The raw HTML is downloads/bis_data_help_legal.html, sha256 eba9123ace81e8ab70d6c23522f73058aafb89c2de4c7ee2d1ca004dee5883e0..
  Quote: "if the statistics are reproduced, the BIS must be cited in your publication or product as the source of the statistics;"
  Establishes: Using BIS statistics is unrestricted provided BIS is cited as the source. The other conditions: a translation must say it is not an official BIS translation; the use must not imply BIS endorsement; there is no extra charge in a commercial product; BIS gives no warranty; and the statistics are not investment advice.

- **BIS general terms defer to the Data Portal terms for statistics**
  Bank for International Settlements (BIS); Bank for International Settlements; n.d.. *Terms and conditions (BIS website, Copyright and permissions)*. https://www.bis.org/terms_conditions.htm (redirects to https://www.bis.org/about/terms-conditions)
  Stored: `sources/provenance/oecd-bis-ecb/bis_terms_conditions.txt` (SHA-256 `b9466e654ef53dacb76ab9b9615b9b9dbd5d126e9cdc152a351af61e6d0e7d11`), fetched 2026-10-17; Copyright and permissions section, paragraph after the 'limited extract' rule (text file line 815). The raw HTML is downloads/bis_terms_conditions.html, sha256 6409625485be1b91e830f230dcd289ffd2af571da7f781d4939ba2bd99e243d4..
  Quote: "Users may use the statistics published in the BIS Data Portal in accordance with the terms set out under the heading "About BIS statistics"."
  Establishes: The statistics are governed by the Data Portal terms (the entry above). Other BIS material, such as the documentation PDF's text, falls under the limited-extract rule on the same page: cite BIS, at most 400 words or two tables or graphs. Short quotes from the documentation fit that rule.

- **ECB euro foreign exchange reference rates: daily concertation time**
  European Central Bank (ECB); European Central Bank; n.d. (when fetched, the page showed reference rates for 16 October 2026). *Euro foreign exchange reference rates*. https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html
  Stored: `sources/provenance/oecd-bis-ecb/ecb_eurofxref_index.txt` (SHA-256 `a6dc3cc07b0da5897eb70a6fb2b477d7ade80b5f3a9e520b06522df3b1cada30`), fetched 2026-10-17; Introductory paragraphs above the rate table (text file line 1060). The raw HTML is downloads/ecb_eurofxref_index.html, sha256 23df5ec1b33baec84516747e2af0660d8c4dc62ba28f8c93c05a049886303bdb..
  Quote: "They are based on the daily concertation procedure between central banks across Europe, which normally takes place around 14:10 CET."
  Establishes: ECB reference rates come from a daily concertation between central banks at about 14:10 CET. The line before says they are usually updated at around 16:00 CET on working days, except TARGET closing days. Cross-check in this run: the page's 16 October 2026 rates (USD 1.1253, IDR 20290.28) match the last rows of data/ecb_idr_usd_per_eur_daily.csv exactly.

- **ECB euro foreign exchange reference rates: for information purposes only**
  European Central Bank (ECB); European Central Bank; n.d. (when fetched, the page showed reference rates for 16 October 2026). *Euro foreign exchange reference rates*. https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html
  Stored: `sources/provenance/oecd-bis-ecb/ecb_eurofxref_index.txt` (SHA-256 `a6dc3cc07b0da5897eb70a6fb2b477d7ade80b5f3a9e520b06522df3b1cada30`), fetched 2026-10-17; Introductory paragraphs above the rate table (text file line 1060), last two sentences.
  Quote: "The reference rates are published for information purposes only. Using the rates for transaction purposes is strongly discouraged."
  Establishes: The ECB rates are for information only, not for transactions. The method notes should say the computed cross rate is indicative.

- **ECB reuse terms (attribution)**
  European Central Bank (ECB); European Central Bank; n.d.. *Disclaimer & copyright*. https://www.ecb.europa.eu/services/disclaimer/html/index.en.html (redirects to https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html)
  Stored: `sources/provenance/oecd-bis-ecb/ecb_disclaimer.txt` (SHA-256 `666ec9a28c4f32b1ead302e1d9aafcf3def1d29d2652c459d5fbc6c1486d63a2`), fetched 2026-10-17; Section 'Copyright', first condition (text file line 1096). The raw HTML is downloads/ecb_disclaimer.html, sha256 75181309fa61bab35e6ad4cda0dd65dcfa28b70a497746410e1516b0fa3aa449..
  Quote: "When such information is distributed or reproduced, it must appear accurately and the ECB must be cited as the source."
  Establishes: Information from the ECB website may be used freely if it is reproduced accurately and the ECB is cited. The ECB Data Portal, where the series was downloaded, links to this same page: its 'Disclaimer & Copyright' menu item points to it (downloads/ecb_data_portal_home.html, sha256 5de0fde88fef77d93d8d5feaa7815307357b8e5856bc236923d048e223fdc25d).

- **ECB reuse terms (modified data must be stated)**
  European Central Bank (ECB); European Central Bank; n.d.. *Disclaimer & copyright*. https://www.ecb.europa.eu/services/disclaimer/html/index.en.html (redirects to https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html)
  Stored: `sources/provenance/oecd-bis-ecb/ecb_disclaimer.txt` (SHA-256 `666ec9a28c4f32b1ead302e1d9aafcf3def1d29d2652c459d5fbc6c1486d63a2`), fetched 2026-10-17; Section 'Copyright', third condition (text file line 1100).
  Quote: "If the information is modified by the user (e.g. by seasonal adjustment of statistical data or calculation of growth rates) this must be stated explicitly."
  Establishes: Computing rupiah per US dollar from the two ECB euro rates is a modification, and the post must say so explicitly. Design 8.4 already plans to say 'stated as computed'.

## IMF balance of payments and consumer prices

- **IMF BOP, Indonesia, portfolio investment liabilities, equity and investment fund shares (USD): meaning of 'net incurrence of liabilities'**
  International Monetary Fund; International Monetary Fund; 2009 (title page: '© 2009 International Monetary Fund'). *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 3.31 (Chapter 3, Types of accounting entries), printed p. 35, PDF page 54. Normalized pypdf text; raw PDF saved as imf_bpm6.pdf (SHA-256 4731d6cf731f3272169170e9fd1a689dcccfdb08db5432b3ccd360bf6ad5973a), raw extraction imf_bpm6_text.txt (SHA-256 7b28fe19149b17bca22b4861b8759f788240bdbc799f6de78ddd1a1edca4e174).
  Quote: "In the case of transactions in financial assets and liabilities, the terms “net acquisition of financial assets” and “net incurrence of liabilities” are used."
  Establishes: 'Net incurrence of liabilities' is BPM6's term for financial account transactions in liabilities, the entry type of the series (BOP_ACCOUNTING_ENTRY L_NIL_T).

- **IMF BOP portfolio equity liabilities: 'net' means purchases less sales within the quarter**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 3.31, printed p. 35, PDF page 54.
  Quote: "Financial account items are recorded on a net basis separately for each financial asset and liability (i.e., they reflect changes due to all credit and debit entries during an accounting period)."
  Establishes: Each quarterly value nets all transactions in the instrument during the quarter, so it is a net flow, not gross selling.

- **IMF BOP portfolio equity liabilities: sign convention (negative = decrease in liabilities)**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 3.31, printed p. 35, PDF page 54 (the raw extraction breaks the last word as 'liabili-' + 'ties'; normalization joined it).
  Quote: "A positive change indicates an increase in assets or liabilities and a negative change indicates a decrease in assets or liabilities."
  Establishes: A negative value of the series is a net decrease in Indonesia's portfolio equity liabilities through transactions in that quarter.

- **IMF BOP: liabilities are positions toward nonresidents (who the counterparties are)**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 8.1 (Chapter 8, Financial Account, A. Concepts and Coverage), printed p. 133, PDF page 152.
  Quote: "The financial account records transactions that involve financial assets and liabilities and that take place between residents and nonresidents"
  Establishes: The flows are only resident to nonresident transactions, so Indonesia's liability flows are transactions with non-resident investors.

- **IMF BOP: equity is a liability of the issuer (Indonesian shares held abroad are Indonesia's liabilities)**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 5.21 (Chapter 5, a. Equity), printed p. 83, PDF page 102.
  Quote: "Equity is treated as a liability of the issuing institutional unit (a corporation or other unit)."
  Establishes: Shares issued by Indonesian companies and held by nonresidents are Indonesian liabilities; with 8.1 and 3.31, a negative value means non-residents' holdings fell through net transactions (net selling or withdrawal).

- **IMF BOP: definition of portfolio investment (excludes direct investment)**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 6.54 (Chapter 6, C. Portfolio Investment), printed p. 110, PDF page 129 (the source text then has ' .' after 'assets'; quote ends at 'assets').
  Quote: "Portfolio investment is defined as cross-border transactions and positions involving debt or equity securities, other than those included in direct investment or reserve assets"
  Establishes: The series covers cross-border equity securities holdings below the direct-investment threshold, i.e. foreign portfolio investors, not foreign direct investors.

- **IMF BOP: transactions exclude price changes (a market fall alone does not make the flow negative)**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 2.21, printed p. 11, PDF page 30.
  Quote: "The financial account shows the net acquisition of financial assets and net incurrence of liabilities during the specified period. In contrast, the other changes in financial assets and liabilities account shows flows that do not result from balance of payments transactions."
  Establishes: Revaluations (share price and exchange rate moves) are recorded outside the financial account, so the series measures investor transactions, not the fall in value of foreign holdings.

- **IMF BOP portfolio equity liabilities: caveat, issuer buybacks also reduce the liability**
  International Monetary Fund; International Monetary Fund; 2009. *Balance of Payments and International Investment Position Manual, Sixth Edition (BPM6)*. https://www.imf.org/external/pubs/ft/bop/2007/pdf/bpm6.pdf
  Stored: `sources/provenance/imf/imf_bpm6_text_normalized.txt` (SHA-256 `e6645739697647a2cb3d97c9efff67b17b3594e0e61e85f73f5ab2a918193eb5`), fetched 2026-10-17T08:14:52Z; para. 8.32 (Share and debt buybacks), printed p. 137, PDF page 156.
  Quote: "If a corporation buys its own shares, the transaction is classified as being a reduction in the equity liability, rather than an acquisition of an asset."
  Establishes: A negative value can include buybacks from non-resident holders, so 'net selling or withdrawal by non-residents' is the accurate gloss, not 'open-market selling' alone.

- **IMF BOP series code BOP_ACCOUNTING_ENTRY=L_NIL_T in imf_bop_portfolio_equity_liab_q.xml**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:BOP(21.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/BOP/21.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_bop_codes_extract.txt` (SHA-256 `e134fa2b6f50f9e38404cc1089cae9d8fcf42a288f2a2168caa16d9de683b25e`), fetched 2026-10-17T08:15:56Z; codelist CL_BOP_ACCOUNTING_ENTRY(3.3.0), code L_NIL_T (extract line 2; full response saved as imf_api_bop_dataflow_structure_all.xml.txt, SHA-256 e231ddb1a72b1aa57c99b635fb9c4bab642908df263bcb324f3ecaeca51766dc).
  Quote: "CL_BOP_ACCOUNTING_ENTRY(3.3.0) code L_NIL_T | en name: Liabilities, Net incurrence of liabilities"
  Establishes: The IMF data portal's own label for the file's entry code L_NIL_T is 'Liabilities, Net incurrence of liabilities'.

- **IMF BOP series code INDICATOR=P_F5 in imf_bop_portfolio_equity_liab_q.xml**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:BOP(21.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/BOP/21.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_bop_codes_extract.txt` (SHA-256 `e134fa2b6f50f9e38404cc1089cae9d8fcf42a288f2a2168caa16d9de683b25e`), fetched 2026-10-17T08:15:56Z; codelist CL_BOP_INDICATOR(10.0.0), code P_F5 (extract line 3).
  Quote: "CL_BOP_INDICATOR(10.0.0) code P_F5 | en name: Portfolio investment, Equity and investment fund shares"
  Establishes: The file's indicator P_F5 is portfolio investment in equity and investment fund shares.

- **IMF BOP series attribute SCALE=6 (unit multiplier)**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:BOP(21.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/BOP/21.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_bop_codes_extract.txt` (SHA-256 `e134fa2b6f50f9e38404cc1089cae9d8fcf42a288f2a2168caa16d9de683b25e`), fetched 2026-10-17T08:15:56Z; codelist CL_UNIT_MULT(1.0.2), code 6 (extract line 5).
  Quote: "CL_UNIT_MULT(1.0.2) code 6 | en name: Millions"
  Establishes: SCALE=6 is labelled Millions, yet OBS_VALUE figures are already in US dollar units (see unresolved); the analysis must not multiply by 10^6.

- **IMF BOP series key and attributes for Indonesia (same series as the project data file)**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T19:36:48Z (PUBLICATION_DATE attribute). *IMF SDMX data response, BOP series IDN.L_NIL_T.P_F5.USD.Q*. https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP,21.0.0/IDN.L_NIL_T.P_F5.USD.Q
  Stored: `sources/provenance/imf/imf_api_bop_idn_L_NIL_T_P_F5_USD_Q.xml.txt` (SHA-256 `8bf4c3be5ce9f62a87dbfdca17294726c015af5ba5d891e81a1afa995c1223c8`), fetched 2026-10-17T08:20:09Z; Series element attributes (the single Series element in the response).
  Quote: "Series COUNTRY="IDN" BOP_ACCOUNTING_ENTRY="L_NIL_T" INDICATOR="P_F5" UNIT="USD" FREQUENCY="Q" SCALE="6" METHODOLOGY="BPM6"
  Establishes: Series is Indonesia, net incurrence of liabilities, portfolio equity and investment fund shares, US dollars, quarterly, BPM6. All 182 observations (1981-Q1 to 2026-Q2) are identical to /Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog/msci-fear-chain/data/imf_bop_portfolio_equity_liab_q.xml (SHA-256 39dc6a2eda9ff82bcfe766593e0fabe2b0ee7611e9e7902e76613038cd0fe9bf), 0 mismatches.

- **IMF CPI, Indonesia (imf_cpi_idn_m.csv): headline series key columns**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T06:48:22Z (PUBLICATION_DATE column). *IMF Consumer Price Index (CPI) dataset, Indonesia, project data file imf_cpi_idn_m.csv: metadata columns of the headline series*. https://data.imf.org/en/datasets/IMF.STA:CPI (dataset named in the file's SUGGESTED_CITATION; original download URL not recorded in the file)
  Stored: `sources/provenance/imf/imf_cpi_idn_m_headline_metadata_extract.txt` (SHA-256 `845d3958ccd08ceccc9256bc5dd3e35dd796749e5d438f13593a01c38390f92e`), fetched CSV downloaded at the vet (2026-10-16), not refetched; metadata extracted 2026-10-17T08:24:16Z; headline values confirmed identical to the IMF API series fetched 2026-10-17T08:20:10Z; extract line 3 (short columns in CSV order) for the 705 rows with COICOP_1999 _T, TYPE_OF_TRANSFORMATION IX, FREQUENCY M; source CSV SHA-256 b3ba15f60d304316b78adedd37229ff945c8669b67321f9284196e564071c20b.
  Quote: "INDEX_TYPE=CPI COICOP_1999=_T TYPE_OF_TRANSFORMATION=IX FREQUENCY=M"
  Establishes: The series used is the all-items (headline) CPI as an index, monthly; the file also holds CP01 (food), SRP_IX and year-on-year series that must be filtered out.

- **IMF CPI, Indonesia: reference period of the headline index (file metadata)**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T06:48:22Z (PUBLICATION_DATE column). *IMF Consumer Price Index (CPI) dataset, Indonesia, project data file imf_cpi_idn_m.csv: metadata columns of the headline series*. https://data.imf.org/en/datasets/IMF.STA:CPI (dataset named in the file's SUGGESTED_CITATION)
  Stored: `sources/provenance/imf/imf_cpi_idn_m_headline_metadata_extract.txt` (SHA-256 `845d3958ccd08ceccc9256bc5dd3e35dd796749e5d438f13593a01c38390f92e`), fetched CSV downloaded at the vet (2026-10-16), not refetched; metadata extracted 2026-10-17T08:24:16Z; extract line 3, columns DERIVATION_TYPE to COMMON_REFERENCE_PERIOD.
  Quote: "DERIVATION_TYPE=O OVERLAP=OL REFERENCE_PERIOD=2022A COMMON_REFERENCE_PERIOD=2022A"
  Establishes: The headline index's reference period is the year 2022 (2022A), reported official data (O), flagged as overlapping other IMF datasets (OL).

- **IMF CPI, Indonesia: source attribution in the file's own metadata**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T06:48:22Z (PUBLICATION_DATE column). *IMF Consumer Price Index (CPI) dataset, Indonesia, project data file imf_cpi_idn_m.csv: metadata columns of the headline series*. https://data.imf.org/en/datasets/IMF.STA:CPI (dataset named in the file's SUGGESTED_CITATION)
  Stored: `sources/provenance/imf/imf_cpi_idn_m_headline_metadata_extract.txt` (SHA-256 `845d3958ccd08ceccc9256bc5dd3e35dd796749e5d438f13593a01c38390f92e`), fetched CSV downloaded at the vet (2026-10-16), not refetched; metadata extracted 2026-10-17T08:24:16Z; extract line 4, column SHORT_SOURCE_CITATION (the SOURCE column is empty, see extract line 3).
  Quote: "SHORT_SOURCE_CITATION=Country Authorities; Organisation for Economic Cooperation and Development; Eurostat; National Summary Data Pages (NSDPs); IMF Staff Calculations"
  Establishes: The file cites country authorities and National Summary Data Pages as sources; it does not name BPS anywhere.

- **IMF CPI dataset: how national CPIs are sourced**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T06:48:22Z (PUBLICATION_DATE column). *IMF Consumer Price Index (CPI) dataset, Indonesia, project data file imf_cpi_idn_m.csv: metadata columns of the headline series*. https://data.imf.org/en/datasets/IMF.STA:CPI (dataset named in the file's SUGGESTED_CITATION)
  Stored: `sources/provenance/imf/imf_cpi_idn_m_headline_metadata_extract.txt` (SHA-256 `845d3958ccd08ceccc9256bc5dd3e35dd796749e5d438f13593a01c38390f92e`), fetched CSV downloaded at the vet (2026-10-16), not refetched; metadata extracted 2026-10-17T08:24:16Z; extract, column FULL_DESCRIPTION (second paragraph).
  Quote: "The statistics are sourced from national authorities (central banks, national statistical institutes, ministries of finance) and collected using the IMF's Consumer Price Index Report Form."
  Establishes: The IMF CPI values come from national authorities such as national statistical institutes; for Indonesia that institute is BPS (see the DSBB entries).

- **IMF CPI dataset: citation format the IMF asks for**
  International Monetary Fund; International Monetary Fund, Statistics Department (DEPARTMENT=STA); 2026-10-16T06:48:22Z (PUBLICATION_DATE column). *IMF Consumer Price Index (CPI) dataset, Indonesia, project data file imf_cpi_idn_m.csv: metadata columns of the headline series*. https://data.imf.org/en/datasets/IMF.STA:CPI
  Stored: `sources/provenance/imf/imf_cpi_idn_m_headline_metadata_extract.txt` (SHA-256 `845d3958ccd08ceccc9256bc5dd3e35dd796749e5d438f13593a01c38390f92e`), fetched CSV downloaded at the vet (2026-10-16), not refetched; metadata extracted 2026-10-17T08:24:16Z; extract, column SUGGESTED_CITATION (note three spaces before the URL, verbatim).
  Quote: "SUGGESTED_CITATION=International Monetary Fund. Consumer Price Index (CPI),   https://data.imf.org/en/datasets/IMF.STA:CPI"
  Establishes: The IMF's suggested citation for the CPI dataset, usable for the APA 7 reference and chart footers.

- **IMF CPI, Indonesia: headline series key and common reference period, fetched fresh from the IMF API**
  International Monetary Fund; International Monetary Fund, Statistics Department; 2026-10-16T06:48:22Z (PUBLICATION_DATE attribute). *IMF SDMX data response, CPI series IDN.CPI._T.IX.M*. https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/IDN.CPI._T.IX.M
  Stored: `sources/provenance/imf/imf_api_cpi_idn_T_IX_M.xml.txt` (SHA-256 `26816f36977eed4c857b0b61931a2a68f1d0dd5ebd98a2cdd66ceff2bfc436c7`), fetched 2026-10-17T08:20:10Z; Series element attributes (single Series element).
  Quote: "Series COUNTRY="IDN" INDEX_TYPE="CPI" COICOP_1999="_T" TYPE_OF_TRANSFORMATION="IX" FREQUENCY="M" IFS_FLAG="true" COMMON_REFERENCE_PERIOD="2022A"
  Establishes: Fresh IMF pull of the same headline series with reference period 2022; all 705 monthly values (1968-M01 to 2026-M09) equal the CSV's headline IX values, 0 mismatches.

- **IMF CPI code COICOP_1999=_T (headline, all items)**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`), fetched 2026-10-17T08:18:55Z; codelist CL_COICOP_1999(1.1.1), code _T (extract line 3; full response imf_api_cpi_dataflow_structure_all.xml.txt, SHA-256 17cd7f123da51b1847c66793397ff7d15e2c2ec9e411be5efeb647f9ce39badd).
  Quote: "CL_COICOP_1999(1.1.1) code _T | en name: All Items"
  Establishes: _T is the all-items CPI, i.e. headline inflation.

- **IMF CPI code SRP_IX (not the series used): 2010=100 rebased variant**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`), fetched 2026-10-17T08:18:55Z; codelist CL_CPI_TYPE_OF_TRANSFORMATION(5.0.0), code SRP_IX (extract line 5).
  Quote: "CL_CPI_TYPE_OF_TRANSFORMATION(5.0.0) code SRP_IX | en name: Standard reference period (2010=100), Index"
  Establishes: The CSV's SRP_IX rows are an IMF 2010=100 rebasing; the IX rows (reference period 2022A) are the national-base index the design calls 2022=100.

- **IMF CPI derivation type O (reported official data)**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`), fetched 2026-10-17T08:18:55Z; codelist CL_DERIVATION_TYPE(1.2.1), code O (extract line 7); the BOP series also carries DERIVATION_TYPE O.
  Quote: "CL_DERIVATION_TYPE(1.2.1) code O | en name: Reported official data | en description: Official data reported to the IMF by country authorities without any modifications or adjustments made by IMF staff."
  Establishes: Both IMF series are flagged as official data reported by Indonesia's authorities, not IMF estimates.

- **IMF CPI overlap flag OL: IMF and national figures can differ**
  International Monetary Fund; International Monetary Fund, Statistics Department (agency IMF.STA); not stated in the structure response. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), all referenced codelists*. https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`), fetched 2026-10-17T08:18:55Z; codelist CL_OVERLAP(1.0.0), code OL description (extract line 8).
  Quote: "differences can occur due to variations in sources and methods, splicing series to preserve time-series continuity, and timing differences in the collection, processing and publication of the indicator"
  Establishes: Supports design 8.3's rule to show BPS's published year-on-year rates alongside and say where they differ: IMF series may be spliced.

- **IMF CPI, Indonesia: compiling agency is BPS (IMF DSBB SDDS record)**
  International Monetary Fund (Dissemination Standards Bulletin Board); IMF DSBB record for Indonesia; agency field names Badan Pusat Statistik (BPS); 2025-02-05 (BasePageUpdatedDate field of the record). *Dissemination Standards Bulletin Board, SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00), base page info*. https://dsbb.imf.org/api/report/getBasepageInfo?CategoryCode=CPI00&CountryCode=IDN&clientLocPath=https:%2F%2Fdsbb.imf.org%2Fsdds%2Fdqaf-base%2Fcountry%2FIDN%2Fcategory%2FCPI00&contactType=4&countryType=SDDS
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_basepageinfo.json.txt` (SHA-256 `25ae9468d1d9b51f9337e37c8e00e3db9cfd700777925ef51d62fbe97776c8d4`), fetched 2026-10-17T08:18:34Z; JSON field Natl_Description (data behind the page https://dsbb.imf.org/sdds/dqaf-base/country/IDN/category/CPI00).
  Quote: "Badan Pusat Statistik (BPS) - Statistics Indonesia"
  Establishes: The IMF's own standards board records BPS as the national agency for Indonesia's consumer price index.

- **IMF CPI, Indonesia: BPS publishes the CPI (IMF DSBB metadata)**
  International Monetary Fund (Dissemination Standards Bulletin Board); IMF DSBB record for Indonesia (agency Statistics Indonesia); 2025-02-05 (BasePageUpdatedDate of the same record). *Dissemination Standards Bulletin Board, SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00), DQAF indicators*. https://dsbb.imf.org/api/report/getDQAFIndicators?CategoryCode=CPI00&CountryCode=IDN&clientLocPath=https:%2F%2Fdsbb.imf.org%2Fsdds%2Fdqaf-base%2Fcountry%2FIDN%2Fcategory%2FCPI00&contactType=4&countryType=SDDS
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` (SHA-256 `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4`), fetched 2026-10-17T08:18:34Z; DQAF item 0.1.1 Responsibility for collecting, processing, and disseminating statistics (TextDetails).
  Quote: "The consumer prices data are published by BPS as a service to the public."
  Establishes: BPS is the publisher of Indonesia's consumer price data that countries report to the IMF.

- **IMF CPI, Indonesia: national index base 2022=100 (IMF DSBB metadata)**
  International Monetary Fund (Dissemination Standards Bulletin Board); IMF DSBB record for Indonesia (agency Statistics Indonesia); 2025-02-05 (BasePageUpdatedDate of the same record). *Dissemination Standards Bulletin Board, SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00), DQAF indicators*. https://dsbb.imf.org/api/report/getDQAFIndicators?CategoryCode=CPI00&CountryCode=IDN&clientLocPath=https:%2F%2Fdsbb.imf.org%2Fsdds%2Fdqaf-base%2Fcountry%2FIDN%2Fcategory%2FCPI00&contactType=4&countryType=SDDS
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` (SHA-256 `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4`), fetched 2026-10-17T08:18:34Z; DQAF item 5.1.1 Statistical presentation (TextDetails).
  Quote: "Data are disseminated on the Consumer Price Index (2022=100) covering 150 regency/municipality throughout Indonesia."
  Establishes: BPS's CPI is published on a 2022=100 base, matching the file's REFERENCE_PERIOD 2022A; the same record says the 2022 base replaced 2018 from January 2024.

- **IMF CPI, Indonesia: how base changes are linked (IMF DSBB metadata)**
  International Monetary Fund (Dissemination Standards Bulletin Board); IMF DSBB record for Indonesia (agency Statistics Indonesia); 2025-02-05 (BasePageUpdatedDate of the same record). *Dissemination Standards Bulletin Board, SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00), DQAF indicators*. https://dsbb.imf.org/api/report/getDQAFIndicators?CategoryCode=CPI00&CountryCode=IDN&clientLocPath=https:%2F%2Fdsbb.imf.org%2Fsdds%2Fdqaf-base%2Fcountry%2FIDN%2Fcategory%2FCPI00&contactType=4&countryType=SDDS
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` (SHA-256 `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4`), fetched 2026-10-17T08:18:34Z; DQAF item 3.3.2 Other statistical procedures (TextDetails).
  Quote: "In case of using a new CPI index, linking reweighted index to historical index is made by the overlap index = 100 and recalculate the rest."
  Establishes: Older base periods are linked to the current one by overlap, which is why a single 2022-based series can reach back decades (the 'linked' wording in design 8.3).

- **IMF copyright and terms: permission to reuse IMF statistical data**
  International Monetary Fund; International Monetary Fund; Effective October 11, 2024 (stated on the page). *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`), fetched 2026-10-17T08:23:22Z (browser-rendered page; section text hash-verified); special terms for published statistical data (section DIV innerText, 2685 chars; browser SHA-256 of section 26bb62d8e98f7b789b007ccd8a7ba93ab9df89728b7c27321bd2448f42054612 matched before saving).
  Quote: "You may download, extract, copy, create derivative works, publish, distribute, and use Data obtained from IMF Sites, subject to the following conditions"
  Establishes: The IMF permits reuse and derivative works from its statistical data (BOP and CPI are covered), subject to conditions.

- **IMF copyright and terms: attribution condition**
  International Monetary Fund; International Monetary Fund; Effective October 11, 2024 (stated on the page). *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`), fetched 2026-10-17T08:23:22Z (browser-rendered page; section text hash-verified); special terms for published statistical data, first condition.
  Quote: "when Data is distributed or reproduced in any manner, it must appear accurately with attribution to the IMF as the source"
  Establishes: Charts and notes must credit the IMF as source; the page's example format is 'Source: International Monetary Fund, Database Name, <link to the dataset>'.

- **IMF copyright and terms: condition on materially transformed data**
  International Monetary Fund; International Monetary Fund; Effective October 11, 2024 (stated on the page). *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`), fetched 2026-10-17T08:23:22Z (browser-rendered page; section text hash-verified); special terms for published statistical data, second condition.
  Quote: "If the Data is materially transformed by the User, this must be stated explicitly along with the required source citation."
  Establishes: Derived figures (two-quarter sums of BOP flows, 12-month inflation computed from the index) must be labelled as the author's calculations next to the IMF citation.

- **IMF copyright and terms: third-party information in IMF statistical products**
  International Monetary Fund; International Monetary Fund; Effective October 11, 2024 (stated on the page). *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`), fetched 2026-10-17T08:23:22Z (browser-rendered page; section text hash-verified); special terms for published statistical data, Note.
  Quote: "Some statistical products may incorporate information from third parties and may have separate terms and conditions for usage."
  Establishes: Data originating with BPS or Bank Indonesia may carry their own terms in addition to the IMF's.

- **IMF copyright and terms: language-model clause**
  International Monetary Fund; International Monetary Fund; Effective October 11, 2024 (stated on the page). *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_llm_clause.txt` (SHA-256 `36a0859f5364b9f13ce65d6b272d55cd77345463e8e3c45a8b59dd9d4c345c92`), fetched 2026-10-17T08:23:45Z (browser-rendered page; element text hash-verified); Prohibitions list (UL innerText, 129 chars; browser SHA-256 0217fe4ddac6b292a1391a725bb9915e1c8c9fcede1082c3c13c540c2f2e25e0 matched).
  Quote: "The IMF does not permit use of its Content or Sites for the training of large language models (LLMs) without explicit permission."
  Establishes: The IMF bars LLM training without permission; unlike the MSCI rule in design 8.5, it does not bar reading or quoting IMF material with a language model.

- **IMF copyright and terms: effective date (for the APA reference)**
  International Monetary Fund; International Monetary Fund; October 11, 2024. *IMF Copyright and Usage*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_effective_date.txt` (SHA-256 `a30fa4d76a920266772dba8c2fe99fba42492fb2add109caa232c2494534f31f`), fetched 2026-10-17T08:23:45Z (browser-rendered page; element text hash-verified); P element under the 'Copyright and Usage' heading (27 chars; browser SHA-256 1081e51fae45b5ca04ed00f002fef765cbb6e6da1474c7e5be8bd539ce8d9d76 matched).
  Quote: "Effective: October 11, 2024"
  Establishes: Date for the terms page's APA 7 reference.

- **IMF copyright and terms: variant served to non-browser clients (wording differs)**
  International Monetary Fund; International Monetary Fund; not stated in this variant. *IMF Copyright and Usage (machine-readable variant served to curl)*. https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms.html` (SHA-256 `5f1954f78e78a0c8e80ad896035f8dae5d17ffab18aa0dd122c6303746a70273`), fetched 2026-10-17T08:14:52Z (curl, HTTP 200, saved as fetched with a header line); Special Terms for Statistical Data, list item 3.
  Quote: "If material transformation occurs, it must be stated explicitly along with the required source citation."
  Establishes: Same condition in condensed wording; recorded only to document that this variant differs from the browser page. Quote the browser-rendered text in the post.

## OJK, BPS, Bank Indonesia and IDX: definitions and terms

- **OJK Portal Data dataset behind data/ojk_ihsg_daily_2023on.xml: 'Indeks & Kapitalisasi Pasar' (MetricID 274), its cube, measures and dimensions**
  Otoritas Jasa Keuangan (OJK), Departemen Pengelolaan Data dan Statistik; Otoritas Jasa Keuangan (OJK); n.d. (XMLA metadata: cube PPM_IndeksKapitalisasiPasar LAST_DATA_UPDATE 2026-10-16T18:11:59). *Dataset: Indeks & Kapitalisasi Pasar (Portal Data OJK, Pasar Modal > Produk Pasar Modal > Kinerja Pasar)*. https://data.ojk.go.id/SJKPublic/Dataset/Dataset/Dataset/274
  Stored: `sources/provenance/ojk-bps/ojk_dataset_274_indeks_kapitalisasi_pasar.txt` (SHA-256 `4a387e873574190325fa25b59805da607ffa464a6cf450af80f155e989f81fce`), fetched 2026-10-17 (curl, raw page dl/ds_page_274.html); Dataset page breadcrumb (visible text); SCRIPT EXCERPTS section for cube and fields.
  Quote: "Produk Pasar Modal > Kinerja Pasar > Indeks & Kapitalisasi Pasar"
  Establishes: The daily IHSG file comes from the OJK Portal Data dataset 'Indeks & Kapitalisasi Pasar'. The page source binds it to XMLA catalog PORTALSJKCUBE_PM, cube PPM_IndeksKapitalisasiPasar, measures [Measures].[Nilai Indeks] and [Measures].[Kapitalisasi Pasar], dimensions [Jenis Indeks] and [Harian]. These are exactly the field names inside data/ojk_ihsg_daily_2023on.xml (sha256 33e4eb3e941634c471069adf3b6eed24f6b8fce2e64cf0531f426ecf904ed4f3): CubeName PPM_IndeksKapitalisasiPasar, Axis0 measures 'Nilai Indeks' and 'Kapitalisasi Pasar', Axis1 hierarchies [Harian].[Harian] (captions such as 2023-01-02) and [Jenis Indeks].[Jenis Indeks] (only member COMPOSITE). The portal API lists this dataset as MetricID 274 with the name 'Indeks  & Kapitalisasi Pasar' (two spaces; raw dl/ds_metric_276.json).

- **OJK definition of IHSG (the COMPOSITE member, measure 'Nilai Indeks'): what it measures and its unit**
  Otoritas Jasa Keuangan (OJK), Portal Data; Otoritas Jasa Keuangan (OJK); 2025-03-24 ("Update terakhir" on the catalog entry). *Katalog Data: IHSG (Indeks Harga Saham Gabungan)*. https://data.ojk.go.id/SJKPublic/Dataset/KatalogData/PopupDetail/467
  Stored: `sources/provenance/ojk-bps/ojk_katalog_467_ihsg.txt` (SHA-256 `cc10e30e8e3069180d4828987bb1ae896f1abff4ba689253b1747ba35cda8292`), fetched 2026-10-17 (curl, raw dl/katalog_popup_467.html); Catalog entry 467, field 'Definisi Data'.
  Quote: "IHSG (Indeks Harga Saham Gabungan) adalah Indeks yang mengukur kinerja harga semua saham yang tercatat di Papan Utama, Papan Pengembangan, Papan Akselerasi, dan Papan Pemantauan Khusus Bursa Efek Indonesia"
  Establishes: OJK defines IHSG as a price index covering all stocks listed on IDX's Main, Development, Acceleration and Special Monitoring boards; Sumber Data: PT Bursa Efek Indonesia; dimensions include Harian. 'Nilai Indeks' is therefore an index level in points, not a currency amount. The entry is attached to the sibling metric 'Indeks' (RefMetricID 272) in the same Kinerja Pasar group; none of the 378 catalog entries is attached to MetricID 274 itself (checked in dl/katalog_grid.json).

- **OJK definition of market capitalisation (measure 'Kapitalisasi Pasar') and its unit**
  Otoritas Jasa Keuangan (OJK), Portal Data; Otoritas Jasa Keuangan (OJK); 2025-03-27 ("Update terakhir" on the catalog entry). *Katalog Data: Kapitalisasi*. https://data.ojk.go.id/SJKPublic/Dataset/KatalogData/PopupDetail/744
  Stored: `sources/provenance/ojk-bps/ojk_katalog_744_kapitalisasi.txt` (SHA-256 `ab5a29db7ee9147fb74f1c8abbe9b109b1d8000c5edbb4816e1976e0c54557f4`), fetched 2026-10-17 (curl, raw dl/katalog_popup_744.html); Catalog entry 744, field 'Definisi Data' (Formula Data: 'Harga saham x jumlah saham beredar').
  Quote: "Nilai Kapitalisasi Saham adalah hasil perkalian antara jumlah saham yang dicatatkan dengan harga saham di Bursa untuk Perusahaan Tercatat"
  Establishes: Market capitalisation is listed shares times exchange price, a rupiah value. In the XML it is stored in full rupiah (2024-10-18: 1.2960436666505866E16, i.e. Rp 12,960.44 trillion). This catalog entry belongs to the issuer area (Emiten dan Perusahaan Publik, RefMetricID 76), not to MetricID 274, so it is OJK's general definition rather than the dataset's own metadata. The post does not use this measure.

- **OJK Portal Data dataset behind data/ojk_foreign_trading_weekly.xml: 'Nilai Perdagangan Saham di Bursa' (MetricID 404), cube, measures, dimensions**
  Otoritas Jasa Keuangan (OJK), Departemen Pengelolaan Data dan Statistik; Otoritas Jasa Keuangan (OJK); n.d. (XMLA metadata: cube INV_BursaSaham LAST_DATA_UPDATE 2026-10-16T18:12:18). *Dataset: Nilai Perdagangan Saham di Bursa (Portal Data OJK, Pasar Modal > Investor > Informasi Transaksi)*. https://data.ojk.go.id/SJKPublic/Dataset/Dataset/Dataset/404
  Stored: `sources/provenance/ojk-bps/ojk_dataset_404_nilai_perdagangan_saham.txt` (SHA-256 `8a91e3cde2b603aaca193323bf09d72ee7cb41c1dac7302c466b369785936c23`), fetched 2026-10-17 (curl, raw dl/ds_page_404.html); Dataset page breadcrumb (visible text); SCRIPT EXCERPTS section for cube and fields.
  Quote: "Investor > Informasi Transaksi > Nilai Perdagangan Saham di Bursa"
  Establishes: The weekly foreign-trading file comes from 'Nilai Perdagangan Saham di Bursa'. The page source binds it to cube INV_BursaSaham (catalog PORTALSJKCUBE_PM) with measures [Measures].[Net Buy Sell], [Measures].[Nilai Jual], [Measures].[Nilai Beli], [Measures].[Kontribusi Investor] and dimensions [Tipe Investor], [Bulan], [Minggu]. These match data/ojk_foreign_trading_weekly.xml (sha256 b6b7df7eb2bb18bf3a334cc223d868f80be690d3c944d5eed9d07d89ea46e32f): CubeName INV_BursaSaham, the same four measures, Axis1 [Minggu].[Minggu] with captions such as '2023-01 Minggu 1' and [Tipe Investor].[Tipe Investor] with members 'Asing' (foreign) and 'Lokal' (domestic).

- **OJK Portal Data display unit for both datasets**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); n.d.. *Dataset: Nilai Perdagangan Saham di Bursa (Portal Data OJK), page source*. https://data.ojk.go.id/SJKPublic/Dataset/Dataset/Dataset/404
  Stored: `sources/provenance/ojk-bps/ojk_dataset_404_nilai_perdagangan_saham.txt` (SHA-256 `8a91e3cde2b603aaca193323bf09d72ee7cb41c1dac7302c466b369785936c23`), fetched 2026-10-17 (curl, raw dl/ds_page_404.html); SCRIPT EXCERPTS: default value of the page variable 'satuan'.
  Quote: "Angka (Satuan penuh)"
  Establishes: The default unit is full numbers (no scaling); GetListSatuanData for metrics 274 and 404 offers the same alternatives Ribu, Juta, Miliar, Triliun (raw dl/ds_satuan_274.json, dl/ds_satuan_404.json). The portal never names a currency on these pages; that the values are rupiah is established by the exact match to OJK's weekly statistics in Rp miliar (entries below).

- **OJK definition of 'Kontribusi Investor' and aggregation of 'Net Buy Sell', 'Nilai Jual', 'Nilai Beli' in cube INV_BursaSaham**
  Otoritas Jasa Keuangan (OJK), Portal Data XMLA data source; Otoritas Jasa Keuangan (OJK); n.d. (cube LAST_SCHEMA_UPDATE 2025-12-15T06:39:42). *XMLA Discover MDSCHEMA_MEASURES response, catalog PORTALSJKCUBE_PM, cube INV_BursaSaham*. https://data.ojk.go.id/SJKPublic/datasource/
  Stored: `sources/provenance/ojk-bps/ojk_xmla_measures_INV_BursaSaham.txt` (SHA-256 `7a11c29bf0ebf29c37fede2f16cddf6ccd5dffe6f3d9a88b42baddfbd97966ad`), fetched 2026-10-17 (curl POST of an XMLA Discover request to the endpoint the portal's own pivot grid uses; raw dl/xmla_measures_INV_BursaSaham.xml); Row MEASURE_NAME=Kontribusi Investor, field EXPRESSION.
  Quote: "([Measures].[Nilai Jual] + [Measures].[Nilai Beli]) / (( ([Tipe Investor].[Tipe Investor].[Lokal], [Measures].[Nilai Beli]) + ([Tipe Investor].[Tipe Investor].[Asing], [Measures].[Nilai Beli]) )*2)*100"
  Establishes: Kontribusi Investor is an investor type's share, in percent, of two-sided trading value: (its sell + its buy) divided by twice the total buy value (Lokal + Asing). Net Buy Sell, Nilai Jual and Nilai Beli are stored measures with MEASURE_AGGREGATOR 1 (sum) and no description. OJK gives no wording for Net Buy Sell; the data show it equals Nilai Beli minus Nilai Jual (2024-10 Minggu 3, Asing: 20,957,362,101,440 minus 19,740,226,877,115 = 1,217,135,224,325), with Asing and Lokal net values equal and opposite.

- **Units of the weekly foreign trading series: OJK's own publication of the same table in Rp miliar**
  Otoritas Jasa Keuangan (OJK), Departemen Pengelolaan Data dan Statistik; Otoritas Jasa Keuangan (OJK); October 2024 (covers 14 to 18 October 2024). *Statistik Mingguan Pasar Modal 2024, Minggu ke-3 Oktober 2024 (14 s.d. 18 Oktober 2024)*. https://www.ojk.go.id/id/kanal/pasar-modal/data-dan-statistik/statistik-pasar-modal/Documents/3.%20STATISTIK%20MINGGU%20KE-3%20OKTOBER%202024.pdf
  Stored: `sources/provenance/ojk-bps/ojk_statistik_mingguan_14-18okt2024.txt` (SHA-256 `4e2bfcc32b37cc3b650dbbfbf2c6771e49da94dfdd46ada987509d517588de5f`), fetched 2026-10-17 (curl, raw dl/ojk_statistik_mingguan_okt2024_mg3.pdf); PDF page 20 (printed 'Hal 7'), table title and unit line.
  Quote: "REKAPITULASI NILAI PERDAGANGAN SAHAM BERDASARKAN TIPE INVESTOR dalam Rp Miliar"
  Establishes: OJK publishes the investor-type trading table (Domestik and Asing buy and sell, 'Net Beli Asing', 'Kontribusi Investor (%)') in rupiah billions; the English page labels it 'in IDR Billion' and 'Foreign Net Buy (Sell)'. Its 'Total Nilai' column equals the sum of buys (one side of trading).

- **Cross-check of data/ojk_foreign_trading_weekly.xml against OJK's weekly statistics (units, sign, week labels)**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); October 2024. *Statistik Mingguan Pasar Modal 2024, Minggu ke-3 Oktober 2024 (14 s.d. 18 Oktober 2024)*. https://www.ojk.go.id/id/kanal/pasar-modal/data-dan-statistik/statistik-pasar-modal/Documents/3.%20STATISTIK%20MINGGU%20KE-3%20OKTOBER%202024.pdf
  Stored: `sources/provenance/ojk-bps/ojk_statistik_mingguan_14-18okt2024.txt` (SHA-256 `4e2bfcc32b37cc3b650dbbfbf2c6771e49da94dfdd46ada987509d517588de5f`), fetched 2026-10-17 (curl, raw dl/ojk_statistik_mingguan_okt2024_mg3.pdf); PDF page 20 (printed 'Hal 7'), row '14 - 18 Okt' (columns: Total Nilai, Domestik Beli, Domestik Jual, Asing Beli, Asing Jual, Net Beli Asing, Kontribusi Domestik %, Kontribusi Asing %).
  Quote: "14 - 18 Okt 54.620,36 33.663,00 34.880,13 20.957,36 19.740,23 1.217,14 62,75 37,25"
  Establishes: The portal XML row ('2024-10 Minggu 3', 'Asing') holds Net Buy Sell 1,217,135,224,325, Nilai Jual 19,740,226,877,115, Nilai Beli 20,957,362,101,440, Kontribusi Investor 37.255: identical to the PDF's Rp miliar figures times 10^9. So the XML values are full rupiah, positive Net Buy Sell means foreign net buying, and Kontribusi is a percent. Also '2024-10 Minggu 1' Asing (-4,878,632,514,676) matches the PDF row '30 Sept - 4 Okt' ((4.878,63)), so a week spanning two months carried the later month's label in this instance.

- **Cross-check of data/ojk_ihsg_daily_2023on.xml COMPOSITE 'Nilai Indeks' against OJK's published IHSG close**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); October 2024. *Statistik Mingguan Pasar Modal 2024, Minggu ke-3 Oktober 2024 (14 s.d. 18 Oktober 2024)*. https://www.ojk.go.id/id/kanal/pasar-modal/data-dan-statistik/statistik-pasar-modal/Documents/3.%20STATISTIK%20MINGGU%20KE-3%20OKTOBER%202024.pdf
  Stored: `sources/provenance/ojk-bps/ojk_statistik_mingguan_14-18okt2024.txt` (SHA-256 `4e2bfcc32b37cc3b650dbbfbf2c6771e49da94dfdd46ada987509d517588de5f`), fetched 2026-10-17 (curl, raw dl/ojk_statistik_mingguan_okt2024_mg3.pdf); PDF page 8 (printed page 1), table 'INDEKS HARGA SAHAM GABUNGAN', daily row '18 Okt' (columns Tertinggi, Terendah, Akhir).
  Quote: "18 Okt 7.790,71 7.718,68 7.760,06"
  Establishes: OJK's published IHSG close (Akhir) for 18 October 2024 is 7.760,06, equal to the portal XML value 7760.06 for 2024-10-18 COMPOSITE; 14 October also agrees (PDF 7.559,66, XML 7559.655). The portal's daily 'Nilai Indeks' is the closing level in index points.

- **OJK terms for reuse of Portal Data (portal's own statement)**
  Otoritas Jasa Keuangan (OJK), Portal Data; Otoritas Jasa Keuangan (OJK); 2022-12-22 (CreatedDatetime of FAQ 46). *FAQ, Portal Data SJK Terintegrasi: FAQ 46 (Aksesibilitas)*. https://data.ojk.go.id/SJKPublic/Master/FAQ (content served by https://data.ojk.go.id/SJKPublic/Master/FAQ/GetGridData)
  Stored: `sources/provenance/ojk-bps/ojk_portal_faq.txt` (SHA-256 `cbd8d4df81009970aeaec9b2f346bb70586bfd57c96f33eabd98cbdbe1a95b06`), fetched 2026-10-17 (curl, raw dl/faq_grid.json); FAQ 46, answer.
  Quote: "Seluruh masyarakat dapat melakukan akses dan menggunakan data dan informasi SJK Terintegrasi yang telah dipublikasikan oleh OJK. Penggunaan Data dari Portal Data SJK Terintegrasi OJK harus dilakukan secara bertanggungjawab"
  Establishes: The portal states that the whole public may access and use the published data, and that use must be responsible. No account is needed (FAQ 47). FAQ 45 says the portal has no API yet; the data files are responses from the XMLA endpoint the portal's pivot grid calls, which the FAQ does not address. The portal has no separate terms-of-use page.

- **Copyright notice on OJK Portal Data pages**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); n.d. (footer year 2025). *Dataset: Indeks & Kapitalisasi Pasar (Portal Data OJK), page footer*. https://data.ojk.go.id/SJKPublic/Dataset/Dataset/Dataset/274
  Stored: `sources/provenance/ojk-bps/ojk_dataset_274_indeks_kapitalisasi_pasar.txt` (SHA-256 `4a387e873574190325fa25b59805da607ffa464a6cf450af80f155e989f81fce`), fetched 2026-10-17 (curl, raw dl/ds_page_274.html); Page footer (visible text).
  Quote: "Copyrights © Otoritas Jasa Keuangan 2025 All Rights Reserved"
  Establishes: Portal pages carry an all-rights-reserved notice alongside FAQ 46's grant of public use; the credit line should name OJK as the rights holder. The same footer is on the 404 dataset page.

- **OJK website terms (Syarat dan Kondisi): reuse and citation rule, Indonesian**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); n.d. (page footer: Copyright Otoritas Jasa Keuangan 2024). *Syarat dan Kondisi*. https://www.ojk.go.id/id/Pages/syarat-dan-kondisi.aspx
  Stored: `sources/provenance/ojk-bps/ojk_syarat_dan_kondisi_id.txt` (SHA-256 `c7b9eb2441a0c6005146114412035ffc029d4c96d2ac74aa11ba19702e202ee5`), fetched 2026-10-17 (curl, raw dl/ojk_syarat_id.html); 'SYARAT DAN KONDISI', first condition.
  Quote: "Informasi yang diperoleh atau diunduh akan dipergunakan oleh pengguna yang bersangkutan secara bertanggung jawab. Pengutipan diizinkan dengan menyebutkan sumbernya secara lengkap"
  Establishes: On OJK's website, information obtained or downloaded must be used responsibly and quoting is allowed with the complete source cited. The page governs 'website Otoritas Jasa Keuangan (OJK) ini' (www.ojk.go.id); that it also covers the data.ojk.go.id subdomain is an inference, not stated.

- **OJK website terms (Disclaimer): reuse and citation rule, English**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); n.d. (page footer: Copyright Otoritas Jasa Keuangan 2024). *Disclaimer*. https://www.ojk.go.id/en/Pages/syarat-dan-kondisi.aspx
  Stored: `sources/provenance/ojk-bps/ojk_disclaimer_en.txt` (SHA-256 `ebceb615e136d1268191fedcd61d4a880d14f7cac532403a4f42719b3138f22f`), fetched 2026-10-17 (curl, raw dl/ojk_syarat_en.html); 'DISCLAIMER', first condition.
  Quote: "Users will use information that is gained and downloaded responsibly. Quoting is allowed as long as it cites the complete source"
  Establishes: English version of the same rule: responsible use, quoting allowed with the complete source cited. Non-commercial use is not singled out; there is no commercial restriction in the text.

- **OJK caveat that capital market data on its site may be provisional**
  Otoritas Jasa Keuangan (OJK); Otoritas Jasa Keuangan (OJK); n.d. (page footer: Copyright Otoritas Jasa Keuangan 2024). *Syarat dan Kondisi*. https://www.ojk.go.id/id/Pages/syarat-dan-kondisi.aspx
  Stored: `sources/provenance/ojk-bps/ojk_syarat_dan_kondisi_id.txt` (SHA-256 `c7b9eb2441a0c6005146114412035ffc029d4c96d2ac74aa11ba19702e202ee5`), fetched 2026-10-17 (curl, raw dl/ojk_syarat_id.html); 'SYARAT DAN KONDISI', condition on capital market data and statistics.
  Quote: "data yang ditampilkan bisa saja merupakan data sementara"
  Establishes: OJK warns that its capital market data may be provisional because of collection lag and will be revised later; the latest weeks and days in the OJK files should be described as possibly provisional.

- **BPS terms of use: citation requirement (Indonesian, latest archived copy)**
  Badan Pusat Statistik (BPS); archived by the Internet Archive Wayback Machine; Badan Pusat Statistik (BPS); n.d. (Wayback snapshot 2026-10-05 11:27:29 UTC of https://www.bps.go.id/assets/term-of-use). *Syarat dan Ketentuan (Ketentuan Penggunaan), Badan Pusat Statistik*. https://web.archive.org/web/20261005112729id_/https://www.bps.go.id/assets/term-of-use
  Stored: `sources/provenance/ojk-bps/bps_term_of_use_id_wayback_20261005.txt` (SHA-256 `3bdc1e42c47a5e268a752d4936debe60f1db7fc84f21d1395f8a22a35162896c`), fetched 2026-10-17 (curl from web.archive.org; live www.bps.go.id refused the connection; raw gzip dl/bps_tou_assets_20261005.html, decompressed dl/bps_tou_assets_20261005.decompressed.html); Section 'Syarat Penggunaan', list of obligations, second item.
  Quote: "memberikan kutipan atau kredit kepada BPS. Kutipan harus mencantumkan judul konten, tanggal akses, penulis (jika ada), dan tautan langsung ke konten asli di website"
  Establishes: Anyone reusing BPS content must credit BPS, and the citation must give the content title, access date, author if any, and a direct link to the original content. BPS tables the owner downloads by hand should be cited with all four.

- **BPS terms of use: permission to reuse statistics (commercial and non-commercial)**
  Badan Pusat Statistik (BPS); archived by the Internet Archive Wayback Machine; Badan Pusat Statistik (BPS); n.d. (Wayback snapshot 2026-10-05 11:27:29 UTC). *Syarat dan Ketentuan (Ketentuan Penggunaan), Badan Pusat Statistik*. https://web.archive.org/web/20261005112729id_/https://www.bps.go.id/assets/term-of-use
  Stored: `sources/provenance/ojk-bps/bps_term_of_use_id_wayback_20261005.txt` (SHA-256 `3bdc1e42c47a5e268a752d4936debe60f1db7fc84f21d1395f8a22a35162896c`), fetched 2026-10-17 (curl from web.archive.org); Section 'Syarat Penggunaan', grant paragraph.
  Quote: "Konten yang tersedia di website ini diberikan kepada Anda secara gratis, di seluruh dunia, terus-menerus, dan non-eksklusif untuk tujuan (i) penggunaan data, baik untuk kepentingan komersial maupun nonkomersial"
  Establishes: BPS content is licensed free, worldwide, continuing and non-exclusive, including use of the data for commercial and non-commercial purposes, plus copying, distribution and derivative extraction, subject to the obligations (citation, lawful use, no false endorsement). The content itself remains subject to copyright held by the Government of Indonesia, BPS and statutory bodies.

- **BPS terms of use: citation requirement (English)**
  BPS-Statistics Indonesia; archived by the Internet Archive Wayback Machine; BPS-Statistics Indonesia; n.d. (Wayback snapshot 2026-05-14 20:58:05 UTC of https://www.bps.go.id/en/term-of-use). *Term of Use, BPS-Statistics Indonesia*. https://web.archive.org/web/20260514205805id_/https://www.bps.go.id/en/term-of-use
  Stored: `sources/provenance/ojk-bps/bps_term_of_use_en_wayback_20260514.txt` (SHA-256 `3c83f5ec962ef3e7fdaa308540a004ed65c7aff1727b2dfcce053134885b470f`), fetched 2026-10-17 (curl from web.archive.org; raw dl/bps_tou_en_20260514.html); Section 'Condition of Use', list of obligations, second item.
  Quote: "provide proper citation or credit to BPS-Statistics Indonesia. The citation should include the title of the content, accessed date, the author (if applicable), and a direct link to the original content on the Website"
  Establishes: English wording of the same citation duty; the same page grants use 'for both commercial and non-commercial purposes'.

- **BPS definition of inflation (inflasi)**
  Badan Pusat Statistik (BPS); archived by the Internet Archive Wayback Machine; Badan Pusat Statistik (BPS); n.d. (Wayback snapshot 2023-10-04 03:56:51 UTC of https://www.bps.go.id/subject/3/inflasi.html). *Inflasi (subject page, tab Konsep), Badan Pusat Statistik*. https://web.archive.org/web/20231004035651id_/https://www.bps.go.id/subject/3/inflasi.html
  Stored: `sources/provenance/ojk-bps/bps_subject_inflasi_wayback_20231004.txt` (SHA-256 `59cd809d5670ae80544f2a9f68f7ae88150c172aa31fb869528e791179927025`), fetched 2026-10-17 (curl from web.archive.org; raw dl/bps_subject3_20231004.raw); 'Konsep' section, entry 'Inflasi:'.
  Quote: "Inflasi adalah kecenderungan naiknya harga barang dan jasa pada umumnya yang berlangsung secara terus menerus"
  Establishes: BPS's own definition: inflation is the tendency of prices of goods and services in general to rise continuously; the page adds it can also be read as a fall in the value of money. This snapshot predates 2024 and describes the 2018=100 base then in force.

- **BPS definition of the consumer price index (IHK)**
  Badan Pusat Statistik (BPS); archived by the Internet Archive Wayback Machine; Badan Pusat Statistik (BPS); n.d. (Wayback snapshot 2023-10-04 03:56:51 UTC). *Inflasi (subject page, tab Konsep), Badan Pusat Statistik*. https://web.archive.org/web/20231004035651id_/https://www.bps.go.id/subject/3/inflasi.html
  Stored: `sources/provenance/ojk-bps/bps_subject_inflasi_wayback_20231004.txt` (SHA-256 `59cd809d5670ae80544f2a9f68f7ae88150c172aa31fb869528e791179927025`), fetched 2026-10-17 (curl from web.archive.org); 'Konsep' section, entry 'Indeks Harga konsumen (IHK):'.
  Quote: "Indeks Harga konsumen (IHK): Indeks yang menghitung rata-rata perubahan harga dari suatu paket barang dan jasa yang dikonsumsi oleh rumah tangga dalam kurun waktu tertentu"
  Establishes: BPS defines the CPI as an index of the average price change of a basket of goods and services consumed by households over a period; the page continues that the IHK is the indicator used to measure inflation and its change over time gives inflation or deflation.

- **CPI base 2022=100 introduced January 2024 (Bank Indonesia table citing BPS)**
  Bank Indonesia; Bank Indonesia (SEKI); 2026-10-01 (PDF creation date; data to September 2026). *Statistik Ekonomi dan Keuangan Indonesia (SEKI), Tabel VIII.1 Indeks Harga Konsumen Gabungan di 150 Kota*. https://www.bi.go.id/SEKI/tabel/TABEL8_1.pdf
  Stored: `sources/provenance/ojk-bps/bi_seki_tabel8_1_ihk.txt` (SHA-256 `38cceeec10f465702fee5cb29e78105160b753fd6b32a563904f31794655dde2`), fetched 2026-10-17 (curl, raw dl/bi_seki_TABEL8_1.pdf); PDF page 1, footnote 6 below the table.
  Quote: "Sejak bulan Januari 2024, IHK dihitung berdasarkan tahun dasar 2022 (2022=100) di 150 kota"
  Establishes: Since January 2024 the CPI has been computed on base year 2022 (2022=100) across 150 cities; footnote 5 records the previous 2018=100 base (90 cities) from January 2020. The table's source line names BPS (next entry).

- **Source attribution of BI's CPI table to BPS**
  Bank Indonesia; Bank Indonesia (SEKI); 2026-10-01 (PDF creation date). *Statistik Ekonomi dan Keuangan Indonesia (SEKI), Tabel VIII.1 Indeks Harga Konsumen Gabungan di 150 Kota*. https://www.bi.go.id/SEKI/tabel/TABEL8_1.pdf
  Stored: `sources/provenance/ojk-bps/bi_seki_tabel8_1_ihk.txt` (SHA-256 `38cceeec10f465702fee5cb29e78105160b753fd6b32a563904f31794655dde2`), fetched 2026-10-17 (curl, raw dl/bi_seki_TABEL8_1.pdf); PDF page 1, source line below the table.
  Quote: "Sumber : Badan Pusat Statistik"
  Establishes: BI states that the CPI figures and base-year notes in Table VIII.1 come from BPS, so the 2022=100 statement is a Bank Indonesia publication quoting BPS, as the task allows.

- **CPI base 2022=100 introduced January 2024 (English wording)**
  Bank Indonesia; Bank Indonesia (SEKI); 2026-10-01 (PDF creation date). *SEKI Table VIII.1 Composite Consumer Price Index of 150 Cities*. https://www.bi.go.id/SEKI/tabel/TABEL8_1.pdf
  Stored: `sources/provenance/ojk-bps/bi_seki_tabel8_1_ihk.txt` (SHA-256 `38cceeec10f465702fee5cb29e78105160b753fd6b32a563904f31794655dde2`), fetched 2026-10-17 (curl, raw dl/bi_seki_TABEL8_1.pdf); PDF page 2, NOTES, footnote 6 (source line 'Source : Statistics Indonesia').
  Quote: "Since January 2024, CPI has been calculated from 150 cities based on 2022 = 100"
  Establishes: English statement of the January 2024 switch to 2022=100 (150 cities), attributed to Statistics Indonesia.

- **Bank Indonesia's definition of inflation (for comparison with BPS's wording)**
  Bank Indonesia; Bank Indonesia; n.d.. *Inflasi (Fungsi Utama > Moneter > Inflasi), Bank Indonesia*. https://www.bi.go.id/id/fungsi-utama/moneter/inflasi/default.aspx
  Stored: `sources/provenance/ojk-bps/bi_inflasi_definisi.txt` (SHA-256 `97fb182a8cd9af90afa930d82a570a6855aabc41371264d4a300c482f942c292`), fetched 2026-10-17 (curl, raw dl/bi_inflasi_default.html); Section 'Definisi Inflasi', first sentence.
  Quote: "Inflasi adalah kenaikan harga barang dan jasa secara umum dan terus menerus dalam jangka waktu tertentu"
  Establishes: BI's definition, worded differently from BPS's ('kecenderungan naiknya harga ... pada umumnya ... secara terus menerus'). If the post defines inflation in BPS's terms, use the BPS wording; BI's is a usable plain-language alternative attributed to BI.

- **Bank Indonesia statement that BPS computes Indonesia's inflation**
  Bank Indonesia; Bank Indonesia; n.d.. *Inflasi (Fungsi Utama > Moneter > Inflasi), Bank Indonesia*. https://www.bi.go.id/id/fungsi-utama/moneter/inflasi/default.aspx
  Stored: `sources/provenance/ojk-bps/bi_inflasi_definisi.txt` (SHA-256 `97fb182a8cd9af90afa930d82a570a6855aabc41371264d4a300c482f942c292`), fetched 2026-10-17 (curl, raw dl/bi_inflasi_default.html); Section 'Definisi Inflasi', fourth sentence.
  Quote: "Perhitungan inflasi dilakukan oleh Badan Pusat Statistik (BPS) di Indonesia"
  Establishes: BI confirms BPS is the agency that calculates inflation; the page also says the IHK is grouped into 11 COICOP 2018 expenditure groups and that BPS publishes core, volatile food and administered price disaggregations.

- **BPS's own January 2024 release labelled with the 2022=100 base (regional office)**
  Badan Pusat Statistik Kota Bandar Lampung (hosted on ppid.bps.go.id); Badan Pusat Statistik Kota Bandar Lampung; 2024-02-01. *Berita Resmi Statistik, Kota Bandar Lampung, inflasi Januari 2024 (bahan tayang)*. https://ppid.bps.go.id/upload/doc/Bahan_Tayang_Inflasi_Januari_2024_1706778222.pdf
  Stored: `sources/provenance/ojk-bps/bps_bandarlampung_brs_jan2024_slides.txt` (SHA-256 `d221c8ba480c38fdfedaa9392899f00889b7931d193e7e5b157466a222531fdc`), fetched 2026-10-17 (curl, raw dl/bps_bahan_tayang_jan2024.pdf); PDF page 2, title slide.
  Quote: "KOTA BANDAR LAMPUNG (Tahun Dasar 2022 = 100) No. 02/02/1871/Th. V, 1 Februari 2024"
  Establishes: A BPS release for January 2024 data is labelled 'Tahun Dasar 2022 = 100' and describes the SBH 2022 commodity package, consistent with the switch starting with January 2024 data. It is a city-level release, not the national one; it also quotes the national figures 0,04 % m-to-m and 2,57 % y-on-y.

- **BPS national January 2024 inflation release (first month on the 2022=100 base): headline values for cross-checking the IMF CPI series**
  Badan Pusat Statistik (BPS); archived by the Internet Archive Wayback Machine; Badan Pusat Statistik (BPS); 2024-02-01 (Tanggal Rilis); Wayback snapshot 2024-12-04 10:19:43 UTC. *Inflasi year-on-year (y-on-y) pada Januari 2024 sebesar 2,57 persen ... (Berita Resmi Statistik, release page)*. `https://web.archive.org/web/20241204101943id_/https://www.bps.go.id/id/pressrelease/2024/02/01/2300/inflasi-year-on-year--y-on-y--pada-januari-2024-sebesar-2-57-persen--inflasi-provinsi-tertinggi-terjadi-di-provinsi-papua-tengah-sebesar-4-76-persen-dan-inflasi-kabupaten-kota-tertinggi-terjadi-di-kab-toli-toli-sebesar-6-76-persen-.html`
  Stored: `sources/provenance/ojk-bps/bps_pressrelease_2300_jan2024_wayback_20241204.txt` (SHA-256 `bd9d0d5709a3860c5795da47dd07bc68bf26df244554bb79101d350ba9ecc473`), fetched 2026-10-17 (curl from web.archive.org; raw dl/bps_pr_2300_id_20241204.raw); 'Abstraksi', first sentence.
  Quote: "Pada Januari 2024 terjadi inflasi year on year (y-on-y) sebesar 2,57 persen dengan Indeks Harga Konsumen (IHK) sebesar 105,19"
  Establishes: National CPI for January 2024 is 105,19 with 2,57 percent y-on-y and 0,04 percent m-to-m (same abstract). An index near 105 two years after 2022 fits a 2022=100 base (the December 2023 figure on the old base, per BI SEKI, was 116.56). The abstract itself does not name the base year.

- **IDX terms of use: non-commercial citation clause (Indonesian, live)**
  PT Bursa Efek Indonesia (Indonesia Stock Exchange, IDX); PT Bursa Efek Indonesia; n.d. (live page). *Syarat Penggunaan, Bursa Efek Indonesia*. https://www.idx.id/id/syarat-penggunaan
  Stored: `sources/provenance/ojk-bps/idx_syarat_penggunaan_id_live.txt` (SHA-256 `4b133dd4c3fc9d6ace8ad2605193b050eeec225c39245b6374d57392d621a68a`), fetched 2026-10-17 (curl; www.idx.co.id returned HTTP 403 to automated requests; raw dl/idx_syarat_penggunaan_live.html); Syarat Penggunaan, paragraph on use of Informasi and data (first part of the sentence).
  Quote: "Penggunaan Informasi dan atau data termasuk pengutipan Informasi dan atau data bukan untuk tujuan komersial diperbolehkan dengan menyebutkan sumbernya secara lengkap yang disertai tanggal akses Pengguna mengutip Informasi dan atau data tersebut pada Website"
  Establishes: Non-commercial use and citation of IDX website information and data is permitted if the full source and the user's access date are given. The non-commercial blog must cite IDX daily closes with source and access date.

- **IDX terms of use: no-scraping clause (Indonesian, live)**
  PT Bursa Efek Indonesia (IDX); PT Bursa Efek Indonesia; n.d. (live page). *Syarat Penggunaan, Bursa Efek Indonesia*. https://www.idx.id/id/syarat-penggunaan
  Stored: `sources/provenance/ojk-bps/idx_syarat_penggunaan_id_live.txt` (SHA-256 `4b133dd4c3fc9d6ace8ad2605193b050eeec225c39245b6374d57392d621a68a`), fetched 2026-10-17 (curl, raw dl/idx_syarat_penggunaan_live.html); Syarat Penggunaan, same sentence, closing clause.
  Quote: "tidak diperkenankan menggunakan metode web scrapping/crawling"
  Establishes: The permission for non-commercial use is conditional on not using web scraping or crawling (IDX's spelling 'scrapping'); IDX data must be taken by hand (the page's own download button), as design section 8.1 already provides.

- **IDX terms of use: commercial use needs written permission (Indonesian, live)**
  PT Bursa Efek Indonesia (IDX); PT Bursa Efek Indonesia; n.d. (live page). *Syarat Penggunaan, Bursa Efek Indonesia*. https://www.idx.id/id/syarat-penggunaan
  Stored: `sources/provenance/ojk-bps/idx_syarat_penggunaan_id_live.txt` (SHA-256 `4b133dd4c3fc9d6ace8ad2605193b050eeec225c39245b6374d57392d621a68a`), fetched 2026-10-17 (curl, raw dl/idx_syarat_penggunaan_live.html); Syarat Penggunaan, sentence preceding the citation clause.
  Quote: "Pengguna dilarang menggunakan atau menyebarluaskan Informasi dan atau data yang diperoleh dari Website kepada pihak lain untuk tujuan komersial tanpa izin tertulis terlebih dahulu dari Bursa Efek Indonesia"
  Establishes: Commercial use or redistribution needs prior written permission from IDX (or the original owner of the data); the blog relies on being non-commercial.

- **Link between the idx.id page and idx.co.id**
  PT Bursa Efek Indonesia (IDX); PT Bursa Efek Indonesia; n.d. (live page). *Syarat Penggunaan, Bursa Efek Indonesia (page source)*. https://www.idx.id/id/syarat-penggunaan
  Stored: `sources/provenance/ojk-bps/idx_syarat_penggunaan_id_live.txt` (SHA-256 `4b133dd4c3fc9d6ace8ad2605193b050eeec225c39245b6374d57392d621a68a`), fetched 2026-10-17 (curl, raw dl/idx_syarat_penggunaan_live.html); PAGE SOURCE EXCERPT: canonical link element.
  Quote: "rel="canonical" href="https://www.idx.co.id/id/syarat-penggunaan""
  Establishes: The page served at www.idx.id declares www.idx.co.id/id/syarat-penggunaan as its canonical address, so the terms read at idx.id are IDX's idx.co.id terms; cite the idx.co.id URL in the post.

- **IDX terms of use: non-commercial citation and no-scraping clause (English, live)**
  PT Bursa Efek Indonesia (IDX); Indonesia Stock Exchange; n.d. (live page). *Terms of Use, Indonesia Stock Exchange*. https://www.idx.id/en/terms-of-use
  Stored: `sources/provenance/ojk-bps/idx_terms_of_use_en_live.txt` (SHA-256 `62f68bca69455f51a41ecdc97b0d850591f49e682d69e9d1a52def427a885c22`), fetched 2026-10-17 (curl, raw dl/idx_terms_of_use_en_live.html); Terms of Use, paragraph on use of Information and data.
  Quote: "The use of Information, including information and or data citation not for commercial purposes is permitted by mentioning the complete source accompanied with the date of Users access citing such information and or data on Website and do not use the web scrapping/crawling method"
  Establishes: English wording of both clauses in one sentence: non-commercial citation allowed with complete source and access date, and no web scraping or crawling.

- **IDX terms of use: commercial restriction (English, live)**
  PT Bursa Efek Indonesia (IDX); Indonesia Stock Exchange; n.d. (live page). *Terms of Use, Indonesia Stock Exchange*. https://www.idx.id/en/terms-of-use
  Stored: `sources/provenance/ojk-bps/idx_terms_of_use_en_live.txt` (SHA-256 `62f68bca69455f51a41ecdc97b0d850591f49e682d69e9d1a52def427a885c22`), fetched 2026-10-17 (curl, raw dl/idx_terms_of_use_en_live.html); Terms of Use, sentence preceding the citation clause.
  Quote: "Users are prohibited from using or disseminating Information and or data obtained from Website to other parties for commercial purpose without prior written consent from Indonesia Stock Exchange and or the original owner of such Information and or data"
  Establishes: English wording of the commercial-use restriction.

- **IDX terms of use on the idx.co.id domain (archived English copy)**
  PT Bursa Efek Indonesia (IDX); archived by the Internet Archive Wayback Machine; Indonesia Stock Exchange; n.d. (Wayback snapshot 2024-04-06 13:28:34 UTC of https://www.idx.co.id/en/terms-of-use/). *Terms of Use, Indonesia Stock Exchange (www.idx.co.id)*. https://web.archive.org/web/20240406132834id_/https://www.idx.co.id/en/terms-of-use/
  Stored: `sources/provenance/ojk-bps/idx_co_id_terms_of_use_en_wayback_20240406.txt` (SHA-256 `01decd9b349d72ab0e0db50b19914c3d0e5f9bad799e34b37128c25271a73a47`), fetched 2026-10-17 (curl from web.archive.org; raw gzip dl/idx_co_id_terms_en_20240406.raw, decompressed dl/idx_co_id_terms_en_20240406.html); Terms of Use, paragraph on use of Information and data.
  Quote: "The use of Information, including information and or data citation not for commercial purposes is permitted by mentioning the complete source accompanied with the date of Users access citing such information and or data on Website and do not use the web scrapping/crawling method"
  Establishes: The same clause stood on www.idx.co.id in April 2024, so the rule is not new and matches the live idx.id text word for word.

## Press sources for the MSCI announcement and market facts (no quotes)

- **MSCI consultation of 15 Oct 2026 (US time): the proposal to move Indonesia from Emerging to Standalone**
  The Jakarta Post (Reuters wire copy); Reuters (no individual reporter named on the Jakarta Post copy); 2026-10-16T07:24:28+07:00. *MSCI weighs downgrading Indonesia to standalone-market status*. https://www.thejakartapost.com/business/2026/10/16/msci-weighs-downgrading-indonesia-to-standalone-market-status
  Stored: `sources/provenance/press-msci/jakpost_2026-10-16_msci-weighs.txt` (SHA-256 `acdba54701111dc30f88fa63b2a9ff68793bbf0dd42ef74b2758c7d25f2ac646`), fetched 2026-10-17; VISIBLE TEXT, lead paragraph, line 169 (the drop-cap M of [text] sits alone on line 168); raw HTML downloads/jakpost_2026-10-16_msci-weighs.html.

- **MSCI consultation: Frontier considered and rejected**
  The Jakarta Post (Reuters wire copy); Reuters (no individual reporter named on the Jakarta Post copy); 2026-10-16T07:24:28+07:00. *MSCI weighs downgrading Indonesia to standalone-market status*. https://www.thejakartapost.com/business/2026/10/16/msci-weighs-downgrading-indonesia-to-standalone-market-status
  Stored: `sources/provenance/press-msci/jakpost_2026-10-16_msci-weighs.txt` (SHA-256 `acdba54701111dc30f88fa63b2a9ff68793bbf0dd42ef74b2758c7d25f2ac646`), fetched 2026-10-17; VISIBLE TEXT, line 189 (paragraph after the newsletter box).

- **MSCI consultation: feedback deadline 30 April 2027**
  Jakarta Globe; Thresa Sandra Desfika, Ria Fortuna Wijaya; 2026-10-16T12:48:00+07:00. *Indonesia Could Join Zimbabwe, Palestine in MSCI Standalone Market Downgrade*. https://jakartaglobe.id/business/indonesia-could-join-zimbabwe-palestine-in-msci-standalone-market-downgrade
  Stored: `sources/provenance/press-msci/jakartaglobe_join-zimbabwe-palestine.txt` (SHA-256 `3bcfd9c83b67c0ca869bf0d3e65d47e0bacdcaf94c9935c7877bbd645300f3e6`), fetched 2026-10-17; VISIBLE TEXT, line 86 (penultimate article paragraph).

- **MSCI consultation: final decision no later than 30 June 2027**
  CNBC Indonesia; Romys Binekasri; 2026-10-16T16:14:38+07:00. *Terhantam Badai MSCI, IHSG Ambruk 11,57% ke Level 5.185*. https://www.cnbcindonesia.com/market/20261016161146-17-776961/terhantam-badai-msci-ihsg-ambruk-1157-ke-level-5185
  Stored: `sources/provenance/press-msci/cnbcindonesia_776961_ihsg-ambruk-close.txt` (SHA-256 `db3e643462c68e56d13e4dc032d209e3b28debed19563cef3fc275fcaf9eef85`), fetched 2026-10-17; VISIBLE TEXT, line 65.

- **MSCI's stated reasons (ownership opacity, suspected coordinated trading)**
  Euronews; Doloresz Katanich; 2026-10-16T10:13:31+02:00. *Indonesian stocks plunge 11% as MSCI proposes emerging market downgrade*. https://www.euronews.com/2026/10/16/indonesian-stocks-plunge-11-as-msci-proposes-emerging-market-downgrade
  Stored: `sources/provenance/press-msci/euronews_2026-10-16_indonesian-stocks-plunge.txt` (SHA-256 `5d73f3aef41b8126b630c36ba4c0048a293c37d3cae8b21160006579540b97af`), fetched 2026-10-17; VISIBLE TEXT, line 308, the sentence right after Euronews quotes MSCI's statement on investability concerns.

- **Hook: economic development counts only for Developed status**
  Jakarta Globe; Faisal Maliki Baskoro; 2026-10-16T11:38:00+07:00. *Explainer: What Is MSCI Market Classification and Why Does It Matter for Indonesia?*. https://jakartaglobe.id/business/explainer-what-is-msci-market-classification-and-why-does-it-matter-for-indonesia
  Stored: `sources/provenance/press-msci/jakartaglobe_explainer-msci-classification.txt` (SHA-256 `c8b7ea05f377f0464e516c01bfdb6614e13932e592c2fe0c9952a9b02a5746eb`), fetched 2026-10-17; VISIBLE TEXT, line 73, under [text]. The line starts with the label [text], which [text] refers to; lines 74 and 75 give size and liquidity and market accessibility.

- **What a Standalone market is**
  Jakarta Globe; Faisal Maliki Baskoro; 2026-10-16T11:38:00+07:00. *Explainer: What Is MSCI Market Classification and Why Does It Matter for Indonesia?*. https://jakartaglobe.id/business/explainer-what-is-msci-market-classification-and-why-does-it-matter-for-indonesia
  Stored: `sources/provenance/press-msci/jakartaglobe_explainer-msci-classification.txt` (SHA-256 `c8b7ea05f377f0464e516c01bfdb6614e13932e592c2fe0c9952a9b02a5746eb`), fetched 2026-10-17; VISIBLE TEXT, line 86, the Standalone paragraph under [text].

- **Current Standalone markets (press), Euronews list**
  Euronews; Doloresz Katanich; 2026-10-16T10:13:31+02:00. *Indonesian stocks plunge 11% as MSCI proposes emerging market downgrade*. https://www.euronews.com/2026/10/16/indonesian-stocks-plunge-11-as-msci-proposes-emerging-market-downgrade
  Stored: `sources/provenance/press-msci/euronews_2026-10-16_indonesian-stocks-plunge.txt` (SHA-256 `5d73f3aef41b8126b630c36ba4c0048a293c37d3cae8b21160006579540b97af`), fetched 2026-10-17; VISIBLE TEXT, line 306.

- **Current Standalone markets (press), CNN Indonesia list, Americas**
  CNN Indonesia; No named author; staff initials (fln/pta); 2026-10-16T11:51:09+07:00. *Apa Itu Standalone Market di Tengah Riuh Pengumuman MSCI?*. https://www.cnnindonesia.com/ekonomi/20261016085631-92-1415988/apa-itu-standalone-market-di-tengah-riuh-pengumuman-msci
  Stored: `sources/provenance/press-msci/cnnindonesia_apa-itu-standalone.txt` (SHA-256 `caf6163d642e6dcccb868af0a25db74704fb14a5a42832ef4186970977662aa7`), fetched 2026-10-17; VISIBLE TEXT, line 113.

- **Current Standalone markets (press), CNN Indonesia list, EMEA; whether Zimbabwe is named**
  CNN Indonesia; No named author; staff initials (fln/pta); 2026-10-16T11:51:09+07:00. *Apa Itu Standalone Market di Tengah Riuh Pengumuman MSCI?*. https://www.cnnindonesia.com/ekonomi/20261016085631-92-1415988/apa-itu-standalone-market-di-tengah-riuh-pengumuman-msci
  Stored: `sources/provenance/press-msci/cnnindonesia_apa-itu-standalone.txt` (SHA-256 `caf6163d642e6dcccb868af0a25db74704fb14a5a42832ef4186970977662aa7`), fetched 2026-10-17; VISIBLE TEXT, line 114.

- **January 2026 MSCI freeze: announcement date (Tuesday 27 January)**
  Fortune Indonesia (fortuneidn.com); Bonaventura Sigit; 2026-01-28T10:18:15+07:00. *MSCI Bekukan Rebalancing, Saham Indonesia Masuk Interim Freeze*. https://www.fortuneidn.com/market/msci-bekukan-rebalancing-saham-indonesia-masuk-interim-freeze-d7w03-00-dz73p-hrlsxj
  Stored: `sources/provenance/press-msci/fortuneidn_msci-bekukan-interim-freeze.txt` (SHA-256 `ddf00610364f41feef4fd96c56bcc7cc092f1e496aa2a22d3ad3b80ef900e085`), fetched 2026-10-17; VISIBLE TEXT, line 54, third paragraph.

- **January 2026 MSCI freeze: what was announced**
  Fortune Indonesia (fortuneidn.com); Bonaventura Sigit; 2026-01-28T10:18:15+07:00. *MSCI Bekukan Rebalancing, Saham Indonesia Masuk Interim Freeze*. https://www.fortuneidn.com/market/msci-bekukan-rebalancing-saham-indonesia-masuk-interim-freeze-d7w03-00-dz73p-hrlsxj
  Stored: `sources/provenance/press-msci/fortuneidn_msci-bekukan-interim-freeze.txt` (SHA-256 `ddf00610364f41feef4fd96c56bcc7cc092f1e496aa2a22d3ad3b80ef900e085`), fetched 2026-10-17; VISIBLE TEXT, line 52, lead paragraph.

- **IHSG fall of 28 January 2026**
  Databoks (Katadata); Nabilah Muhamad; editor Adi Ahdiat; 2026-01-28T17:33:12+07:00. *IHSG Ditutup Melemah 7,35% Usai Pengumuman MSCI (Rabu, 28 Januari 2026)*. https://databoks.katadata.co.id/pasar/statistik/6979df85991ed/ihsg-ditutup-melemah-735-usai-pengumuman-msci-rabu-28-januari-2026
  Stored: `sources/provenance/press-msci/databoks_6979df85991ed_ihsg-ditutup-735.txt` (SHA-256 `7d6995105e82a07db8b6fb72617c94655116da49c5adcee5c3bea62183314827`), fetched 2026-10-17; VISIBLE TEXT, line 210, first article sentence, which opens with [text].

- **IHSG fall of 28 January 2026 linked to the MSCI freeze**
  Databoks (Katadata); Nabilah Muhamad; editor Adi Ahdiat; 2026-01-28T17:33:12+07:00. *IHSG Ditutup Melemah 7,35% Usai Pengumuman MSCI (Rabu, 28 Januari 2026)*. https://databoks.katadata.co.id/pasar/statistik/6979df85991ed/ihsg-ditutup-melemah-735-usai-pengumuman-msci-rabu-28-januari-2026
  Stored: `sources/provenance/press-msci/databoks_6979df85991ed_ihsg-ditutup-735.txt` (SHA-256 `7d6995105e82a07db8b6fb72617c94655116da49c5adcee5c3bea62183314827`), fetched 2026-10-17; VISIBLE TEXT, line 211, second sentence.

- **IHSG close on 16 October 2026**
  CNBC Indonesia; Romys Binekasri; 2026-10-16T16:14:38+07:00. *Terhantam Badai MSCI, IHSG Ambruk 11,57% ke Level 5.185*. https://www.cnbcindonesia.com/market/20261016161146-17-776961/terhantam-badai-msci-ihsg-ambruk-1157-ke-level-5185
  Stored: `sources/provenance/press-msci/cnbcindonesia_776961_ihsg-ambruk-close.txt` (SHA-256 `db3e643462c68e56d13e4dc032d209e3b28debed19563cef3fc275fcaf9eef85`), fetched 2026-10-17; VISIBLE TEXT, line 54, lead paragraph.

- **IHSG close on 16 October 2026 (second outlet)**
  Jakarta Globe; Ria Fortuna Wijaya, Arnoldus Kristianus; 2026-10-16T16:04:00+07:00. *Indonesian Stocks End at 2026 Low After Losing 11.57% on MSCI Warning*. https://jakartaglobe.id/business/indonesian-stocks-end-at-2026-low-after-losing-1157-on-msci-warning
  Stored: `sources/provenance/press-msci/jakartaglobe_stocks-end-2026-low-1157.txt` (SHA-256 `6f26a937e6695b4d7ea28a96b0346e038c0d7b11d4cf4aca9161a7c158410e1d`), fetched 2026-10-17; VISIBLE TEXT, line 65, lead paragraph.

- **Largest one-day fall since 1998 (close-based, Refinitiv)**
  CNBC Indonesia (Research); Elaine Tairio; 2026-10-16T17:42:01+07:00. *IHSG Ambruk 11,57%: Terburuk Sejak Krisis 1998*. https://www.cnbcindonesia.com/research/20261016171956-128-776996/ihsg-ambruk-1157-terburuk-sejak-krisis-1998
  Stored: `sources/provenance/press-msci/cnbcindonesia_776996_terburuk-sejak-1998.txt` (SHA-256 `80635f61dbb9f1361a7b111f68185bb87ef238dc1f8a201dc0534e00965e9db9`), fetched 2026-10-17; VISIBLE TEXT, line 57, fourth paragraph. The sentence opens with [text]; line 56 says the ranking uses Refinitiv data.

- **Largest one-day fall in 28 years (Euronews)**
  Euronews; Doloresz Katanich; 2026-10-16T10:13:31+02:00. *Indonesian stocks plunge 11% as MSCI proposes emerging market downgrade*. https://www.euronews.com/2026/10/16/indonesian-stocks-plunge-11-as-msci-proposes-emerging-market-downgrade
  Stored: `sources/provenance/press-msci/euronews_2026-10-16_indonesian-stocks-plunge.txt` (SHA-256 `5d73f3aef41b8126b630c36ba4c0048a293c37d3cae8b21160006579540b97af`), fetched 2026-10-17; VISIBLE TEXT, line 301, first body paragraph, after [text].

## The IHSG month-end series (design 8.6)

- **Bank Indonesia, SEKI Table III.3** (`data/bi_seki_table_iii3_ihsg_monthend.xls`, SHA-256
  `da0c63edff686f6292b41326006c3fcd4b37d35880de86dfb43a443e77436364`): IHSG month-end close, used from
  December 2005. Credit required by Bank Indonesia's data policy, PBI 12/2024, Article 21(4)
  (`sources/bi_pbi_12_2024_data_policy.pdf`, SHA-256
  `0053dd26eafa80893ef67875b6f1af8702e3fa11d9f99875557d54cd19f263ee`).
- **Bapepam, Statistik Pasar Modal, 28 November to 2 December 2005, Table 8, column Akhir**
  (`sources/bapepam_statistik_pasar_modal_2005-11_week4.pdf`, SHA-256
  `95921cd7bb5d8f53398d4053ffcd17329b90f136e79afd259415716a9231480d`), extracted by
  `extract_bapepam_2004_2005.py` into `data/bapepam_ihsg_monthend_2004_2005.csv`: January 2004 to
  November 2005. It matches Bank Indonesia for December 2004. December 2005 (Akhir 1.162,63, equal to Bank
  Indonesia's 1162.63) is from the next issue's Table 8, page 16
  (`sources/bapepam_statistik_pasar_modal_2006-01_week4.pdf`, SHA-256
  `6a54be58efbcfb305bc9ccac93dab9081ff6ca6ae7731c87da162bed59b27664`); corrected in round 2.
- **Corrections** (`extract_ihsg_corrections.py` into `data/ihsg_monthend_corrections.csv`): the six
  months where Bank Indonesia disagrees with the exchange's own publications or Bapepam's, using the
  exchange's figure first, then Bapepam's or OJK's: 2006-01, 2006-02, 2006-08 (Bapepam), 2006-09,
  2009-03, 2021-04 (IDX).
- **Checks:** 2008, all 12 months match IDX's 2008 statistics book; 2006 to 2016, 127 of 132 months
  match IDX books or Bapepam/OJK; 2017 to 2022, 71 of 72 match OJK or IDX; 2023 to August 2026, all 44
  match OJK's daily index. Tables: `docs/ihsg-checks/`.
- **Not used: 1995 to 2003.** Bank Indonesia's older sheet disagreed with the exchange's own files in
  9 of 85 checked months and with Bapepam in 7 more (`docs/ihsg-checks/comparison_1995_2003.csv`).
- **Rejected: OECD share prices.** OECD's metadata names Singapore Yahoo Finance as the dissemination
  agency and its monthly values are averages of daily closes (entries above).


## October 2026: IDX Daily Statistics (design 8.1)

- **IDX Daily Statistics, 15 and 16 October 2026** (DS261015, DS261016), page 1, block "IDX Composite
  Index (IHSG)": close, change and previous close. Downloaded by the owner on 2026-10-17 from idx.co.id,
  Market Data, Statistical Reports, Daily (https://www.idx.co.id/Media/bfsctwrv/ds_261015.pdf and
  https://www.idx.co.id/Media/bndpqsus/ds_261016.pdf), not scraped. Stored: `sources/ds_261015.pdf`
  (SHA-256 `5a424eea2f52688cb71119f426d5a82dc60b9c444d7d26fa17f04b2383d9dbe3`) and
  `sources/ds_261016.pdf` (SHA-256 `08e80f11ec5fb466e6a34e430f9cc7bc60f756efe458c0dae1bf6d9b9d4c3608`);
  extracted by `extract_idx_daily.py` into `data/idx_ihsg_daily_2026-10.csv` (SHA-256
  `48f360ad8f6d8908eda7a9f9c635488b4887f66f82212652d17e749d1ecb54ec`).
- **Why daily reports, not the quarterly file named in 8.1:** on 2026-10-17 IDX's Digital Statistic
  listed 2026 only to Q3 (quarterly) and September (monthly); the daily reports are the same
  publisher's file for the same closes. No rule changes.
- **Checks:** the 16 October previous close equals the 15 October close (5,863.780); close minus
  previous equals the printed change (minus 678.675) in both reports; the build's fall rounds to the
  printed minus 11.57%. It matches the press figures above (11.57% to 5,185). OJK's daily index ends
  2 October 2026, so it cannot check these two days; its 31 August close matches Bank Indonesia's
  August month-end within 0.01, and its 30 September close is the bridge drawn dotted in chart 1.
- **Terms:** non-commercial use with full source and access date (IDX terms entries above); the post
  cites Indonesia Stock Exchange (2026) with the retrieval date.

## Amendment 8.7: Bank Indonesia rate tables, what their notes say (recorded before any value was read)

Copies fetched from bi.go.id/SEKI/tabel/ on 2026-10-17 by the source vet (Bank Indonesia saved them on
2026-10-05); bi.go.id refused further connections from this machine later that day, so these copies are used.
Only text cells were printed (labels and notes, `seki_text_cells.py` in the session scratchpad); no value was read.

- **Table I.28, rupiah time-deposit rates by bank group and maturity** (`data/bi_seki_table_i28_deposit_rates.xls`,
  SHA-256 `4b19af0c8cbc3ed0ed3093a53062d5db66062491be3a8f30982e8f2f1909e69c`). Unit: "(Percent Per Annum)".
  Rows: 1, 3, 6, 12 and 24 months for each bank group and for "Bank Umum / Commercial Banks". Notes: the
  August 2017 change in coverage of national private and government banks; the January 2025 reclassification of
  foreign-bank offices (integrated commercial bank report); "* Data sementara / Provisional Figures". The notes do
  NOT say whether the rate is a weighted or simple average, on new or outstanding deposits, or a month average or
  month end; the post says so.
- **Table I.26, rupiah loan rates by bank group and type** (`data/bi_seki_table_i26_loan_rates.xls`, SHA-256
  `d437c35c64b72be1d76d16a152fd8eab8ee44e44e0e9662517b671c883c7b83c`). Unit: "(Percent Per Annum)". Rows: working
  capital, investment and "Pinjaman Konsumsi Yang Diberikan / Consumer Loans" for each bank group and for
  commercial banks. Same notes as I.28. The notes do NOT say whether the rate is weighted, on new or outstanding
  loans, or a month average or month end; the post says so.
- **Table I.25.A (sheets titled I.30 "Suku bunga, diskonto, imbalan"), policy and money-market rates**
  (`data/bi_seki_table_i25a_policy_rate.xls`, SHA-256
  `aae221bd92d1365237c850a13e4e58a8f98dcb8b83a5045533e744079e658058`). Unit: "(Percent Per Annum)" (the
  1990 to 2003 sheet is mislabelled "(Billions of Rp)"). Rows include "BI Rate", "Sertifikat Bank Indonesia, 1
  Month" and, from 2010, "Policy Rate". Footnote 1: "Data akhir periode / End of period data".
- **Exposure while reading the layout (2026-10-17).** A layout check of I.28's sheet "1.28" printed its first
  rows, including the 1-month and 3-month time-deposit rates of state banks (Bank Persero) for January 2025 to
  August 2026. These months lie outside every slide window; they enter only the last windows of L5's share of
  all windows, which uses the all-bank series, not the state-bank rows. No other value was printed.
- **Layout (headers and row labels only):** sheets "Th 1990-2008" and "Th 2009-2018" carry a year on every
  month column with a blank column between years ("Th 2009-2018" runs to March 2019); "Th 2010-2024" carries a
  year label only on some months (2010 on January, 2024 on December, 2025 on March) and runs to March 2025;
  "1.28" covers January 2025 to August 2026 with a blank column after December 2025. Bank Umum, 1 Bulan is the
  row after the "Bank Umum" label in each sheet.
- **Cross-checks (8.7), run before any window value was read; tolerance 0.05 points.** Second publications:
  earlier editions of the same SEKI tables archived on web.archive.org (I.28 and I.26: 2011 edition snapshot
  20110815, 2019 edition 20190529, 2024 edition 20240705; I.25: 2011, 2019 and 2024 editions), and Bank
  Indonesia's SEKI July 2023 edition (zip from bi.go.id) for the June 2023 consumer-loan rate; the IMF's
  monetary policy rate (MFS_IR) also matches the three policy-rate values. Results, current file against second
  publication: 1-month deposit rate, all commercial banks, June 2010 6.79 / 6.79, June 2017 6.30 / 6.30, June 2023
  4.20 / 4.20; consumer-loan rate June 2010 14.99 / 14.99, June 2017 13.21 / 13.21, June 2023 10.29 / 10.29;
  policy rate June 2010 6.50 / 6.50, June 2017 4.75 / 4.75, June 2023 5.75 / 5.75. All pass (difference 0.00).
  The IMF's own deposit and lending rates use other definitions and were not used.
- **Reader checks (`seki.py`):** I.28 and I.26 have no missing month from January 2004 to August 2026; the 111
  months where "Th 2009-2018" and "Th 2010-2024" overlap agree exactly; for January to March 2025 the newest sheet
  supersedes (3 months differ in each table). I.26's "Th 2009-2018" sheet has two December 2018 columns, the first
  empty; the filled one equals "Th 2010-2024". I.25.A: the one-month SBI rate runs from December 2003, the BI Rate
  from October 2005 (earlier months are zero placeholders), the Policy Rate row from January 2010, with no gap.
- **July 2005 BI Rate:** not found in any Bank Indonesia document searched (the BI-Rate history page starts in
  2016; press-release and report searches on bi.go.id found nothing for July 2005), so the policy-rate note for the
  August 2005 slide is "not available", as 8.7's rule requires.
- **Data Inflasi (BPS's published rates, via Bank Indonesia):** `data/Data Inflasi.xlsx`; 284 months, January 2003
  to August 2026, plus the "Desember 2002, 0,00 %" placeholder, which the reader excludes. Cross-check against a
  second publication, Bank Indonesia's Target Inflasi page (actual inflation by year, December year on year,
  viewed 2026-10-17): December 2010 6.96 / 6.96, December 2017 3.61 / 3.61, December 2023 2.61 / 2.61; all pass.
  **Exposure:** that page lists December inflation for every year from 2001 to 2025, including years inside the
  slide windows; the author saw it while taking the three check values. No slide-month value is on it. Web search
  summaries during the search for the July 2005 BI Rate also showed the author the 2005 December figure and a
  September 2006 BI Rate cut.

## Amendment 8.8: BPS's own site excluded (2026-10-17)

bps.go.id's robots file names ClaudeBot with "Disallow: /" (`sources/provenance/rights-87/bps_robots_wayback_20260507.txt`,
SHA-256 `f590050bbb0f7bc991fa9fe21086cfa49d18b8ad946f495b2474b6318cb1f1fd`). The five archived BPS page copies listed
above under "OJK, BPS, Bank Indonesia and IDX" (BPS terms in Indonesian and English, the BPS inflation subject page,
the Bandar Lampung January 2024 slides and the national January 2024 release) were moved out of `sources/` on
2026-10-17; their entries above are EXCLUDED (8.8) and nothing in the post rests on them. The CPI's compiling agency
and base year rest on the IMF's DSBB record. The search for another unemployment source, and its rights files, are
in `sources/provenance/rights-88/`; no source passed.

## Amendment 8.7: deposit interest tax and fuel prices

- **PP No. 131 Tahun 2000** (`sources/tax/pp_131_2000.pdf`, peraturan.bpk.go.id Download/43363, SHA-256
  `7e46c646cde1d1ba7dec04a9c81c811c4f77d3d798d6161e93edf242c5acce5e`). Page 2, Pasal 2 huruf a: "dikenakan pajak final
  sebesar 20% (dua puluh persen) dari jumlah bruto, terhadap Wajib Pajak dalam negeri dan bentuk usaha tetap." Page 4,
  Pasal 7: in force 1 January 2001; Pasal 6 revokes PP 51/1994. Page 3, Pasal 3: deposits not above Rp 7,500,000 are
  not taxed (not modelled). BPK's archived record lists one amendment, PP 123/2015, which lowers the rate only for
  deposits funded by export proceeds and keeps 20% for others (`sources/tax/pp_123_2015.pdf`, page 4, Pasal 2 huruf c
  angka 1).
- **PP No. 51 Tahun 1994** (`sources/tax/pp_51_1994.pdf`, BPK Download/46751, SHA-256
  `c8718465b8c8035a9590a424c50e9bf49db60bc59e18c2ab6e6aeb24a0d5256f`). Page 3, Pasal 3: 15% of the gross amount; page
  6, Pasal 8: in force 1 January 1995. Used for the 1997 slide.
- **Fuel price changes** (`extract_fuel.py`, `docs/fuel-manifest.csv`, `data/fuel_price_changes.csv`; 19 official
  documents in `sources/fuel/`, each with its URL, hash and fetch date in `sources/fuel/provenance.tsv`). Every row's
  passages are checked by script (hash, exactly one occurrence, the only date printed is the effective date, the old
  price equals the previous verified new price). From 2015 the government-set Premium price applied outside
  Java-Madura-Bali; the Java price was verified only for 5 January 2016, so the other 2015 to 2016 Premium
  rows are "size not verified". The Cabinet Secretariat (setkab.go.id) serves a security page in place of its robots
  file, so its posts are not used.

## Amendment 8.7: independent recomputation (2026-10-17, before drafting)

Two agents that did not write the rules recomputed L5, L6, the policy-rate note, both all-window shares, the
published-rate comparison and the fuel list from the amendment text and the frozen files alone, one with pandas and
one without (scripts and outputs in the session scratchpad, `recompute-87/a` and `/b`). Both match `results.json` on
every slide (after-tax returns to 0.01, loan-rate changes to 0.005, every status), on the shares (L5 90 of 261, L6 10
of 260) and on the largest published-rate gap (0.81). Readings they raised: the deposit timing r(s+1) to r(s+12)
instead of the registered r(s) to r(s+11) leaves every slide's outcome unchanged and gives an L5 share of 92 of 260;
8.7's text ("read as the rate earned over month m + 1") decides it, so the registered reading stands. "Edge month" can
mean the outer edges or all four window edges; the build flags all four, and the post prints no edge flag.
