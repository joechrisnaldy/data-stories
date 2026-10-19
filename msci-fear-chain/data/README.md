# Data for Post 27

The data files are not committed. Each data file `build_analysis.py` reads is frozen by its SHA-256, which it checks before reading it; a fresh download may differ and then needs a new vet. The blog is non-commercial. Source documents and licence terms are in `docs/provenance-audit.md`.

## Sources

- **IHSG month-end close.** Bank Indonesia, SEKI Table III.3, "Transaksi dan indeks harga saham di Bursa Efek Indonesia" (bi.go.id, statistics, SEKI), used from December 2005. Bank Indonesia's data policy requires its data to be credited to Bank Indonesia. Before that: Bapepam's weekly capital market statistics (Statistik Pasar Modal), read from an Internet Archive copy of the OJK archive file by `extract_bapepam_2004_2005.py`. Six months are corrected to the Indonesia Stock Exchange's own statistics or Bapepam-LK's statistics by `extract_ihsg_corrections.py` (Indonesia Stock Exchange files cited with their access date, as its terms require).
- **Rupiah per US dollar, daily.** Bank for International Settlements, US dollar exchange rates (data.bis.org, topic XRU, series for Indonesia), with its national sources: the US Federal Reserve, then the European Central Bank. Days after the last BIS update use the European Central Bank's reference rates (rupiah per euro divided by dollars per euro), computed by the author.
- **Foreign equity flows, quarterly.** International Monetary Fund, Balance of Payments: Indonesia, portfolio investment liabilities, equity and investment fund shares, net incurrence, US dollars. Sums are the author's calculations.
- **Consumer prices, monthly.** International Monetary Fund, Consumer Price Index: Indonesia, headline index, compiled by BPS-Statistics Indonesia. Inflation rates are the author's calculations.
- **Context.** OJK's Portal Data SJK Terintegrasi: the daily IHSG and weekly foreign trading on the exchange.
- **Deposit, loan and policy rates, monthly.** Bank Indonesia, SEKI Tables I.28 (rupiah time-deposit rates) and I.26 (rupiah loan rates), commercial banks as a whole, and I.25.A (policy and money-market rates) (bi.go.id, statistics, SEKI); credited to Bank Indonesia. Each was checked against an earlier edition of the same table archived by the Internet Archive.
- **BPS's published inflation, monthly.** Bank Indonesia's Data Inflasi page (bi.go.id, statistics, indicators), which reports BPS's year-on-year headline inflation; downloaded by hand.
- **Deposit interest tax.** Government Regulations PP 131/2000 and PP 51/1994, from peraturan.bpk.go.id; PP 131/2000's rate is bound to a stored quote in `docs/sources.json`.
- **Fuel price changes.** Government regulations and official notices from peraturan.bpk.go.id, the Ministry of Energy and Mineral Resources (esdm.go.id, migas.esdm.go.id, its legal documentation site) and Pertamina, many through Internet Archive copies; `extract_fuel.py` checks each passage in `docs/fuel-manifest.csv` against the stored document and writes `fuel_price_changes.csv`.
- **The October fall.** Indonesia Stock Exchange, IDX Daily Statistics for 16 October 2026 and the trading day before (idx.co.id, Market Data, Statistical Reports, Daily), downloaded by hand and read by `extract_idx_daily.py`; cited with the access date, as the exchange's terms require. October has no monthly or quarterly file from the exchange yet.

## How the index series was checked

Bank Indonesia's month-ends were compared, month by month, with the Indonesia Stock Exchange's statistics books, Bapepam and OJK statistics and OJK's daily index; the comparison tables are in `docs/ihsg-checks/`. Months where they disagree use the exchange's figure first, then Bapepam's or OJK's. Bank Indonesia's closes before 2004 are not used: they failed this check.

## Traps hit while vetting

- OECD's monthly share price series for Indonesia names a commercial website as its source and averages daily closes, so it was not used.
- Bank Indonesia's table places the year label on the first month of each year in older sheets and on the last month in recent years; the reader groups each year's months instead of carrying the label forward.
- The Indonesia Stock Exchange's terms forbid scraping; its statistics were read from individual documents.
- MSCI's terms bar use of its content with language models without a licence, so MSCI's own documents were not used; its announcement is reported from the press.
- BPS's site blocks Anthropic's crawler in its robots file, so BPS's own pages and tables were not used, and the unemployment test could not be run: no other official source with BPS's round-by-round figures could be used. Kompas was not used.
- Bank Indonesia's rate tables spread each series over several sheets, label the year on a few months in newer sheets, and Table I.26 repeats December 2018 (the first copy empty); `seki.py` checks each case.
- From 2015 the Premium price the government set applied outside Java, Madura and Bali; the Java price was verified for January 2016 alone, so the other Premium rows from 2015 on are listed as size not verified.
