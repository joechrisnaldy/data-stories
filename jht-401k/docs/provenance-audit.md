# Provenance audit: Post 28 (jht-401k)

Every variable the analysis leans on and every external figure the post cites, with the document that defines it,
the stored copy of that document and its SHA-256, the page, and a verbatim quote that defines it. Generated
2026-10-22 from checked entries (scripts and run logs in the session scratchpad, `post28-build/prov`), and
regenerated the same day by Task D, after the copies in section M, from `post28-build/fix-D/prov-gen`. No rule
result was computed or read for this audit: the figures below are inputs (rates, balances, definitions), and the
only arithmetic is on inputs, labelled where it appears.

Note (2026-10-22, later the same day): sections A (its table) and J are as checked at the audit's first run, when
`docs/sources.json` held 30 records. The review fixes then added two quote-only records (`vanguard_glide_age65`,
`has_estimation_method`) and edited notes and locators; the file now holds 32, each checked by the fix round's
own script. Evidence later copied into the post folder is listed with its SHA-256 in
`sources/provenance/ADDED_SHA256SUMS.txt`: the 2020 and 2021 one-page summaries behind the 2020 note, and the
ILO and World Bank files behind the data README's two employment checks.

How the quotes were checked. Each quote occurs exactly once in its unit and starts and ends on whole words, after
whitespace is collapsed: for a PDF the unit is the cited page as `pdftotext -layout -f P -l P` prints it (the rule
`extract_jht.py` uses), or, where marked "reading order", the same page from `pdftotext` without `-layout`
(used where a two-column page interleaves in layout mode); for an HTML page, the page text with scripts and styles
dropped (the same parser as `extract_jht.py`); for a text file, the whole file; for a workbook, the cited cell;
for a JSON file, the cited field; for a CSV, the cited column, which must take one value over the cited rows; for an
SDMX structure file, the English Description. Where a PDF quote also occurs on other pages, the entry says so. A
mutation run changed one character in every quote and confirmed each check then fails (136 of 136). Two
documents have no text layer; their entries are marked "transcribed, not machine-checked" and only their SHA-256
is checked. Quotes from copyrighted documents are kept short and are cited, not reproduced; regulations carry no
copyright (section K).

Where the copies are. Every stored copy cited below is in this post folder: paths start `sources/` or `data/`.
The copies first stored outside it, in the session scratchpad or in Post 27's folder, were copied in on
2026-10-22 and each SHA-256 was checked before and after copying; section M lists where each came from.

The builders' records were re-checked read-only: all 30 records in `docs/sources.json` and all 31 rows of
`docs/jht-manifest.csv` match their files' SHA-256, and every quote occurs once on its cited page (three
`sources.json` records are reading-order extractions by design, as their `extracted_with` field says).

## What the owner or the analysis must act on

1. **The JHT rule the vet summarised is not the one in force in the window.** Peraturan BPJS 3/2020 (credit on
   1 January, realized income, deposit floor) took effect on 7 January 2021, after the 2005 to 2020 window. The
   2015 to 2020 year-end rates were set under Peraturan BPJS 4/2015 (image-only; transcribed in section A), which
   has the same realized-income rule and floor but sets the annual rate each 31 December from the annual
   financial report. Before 2015 the rate was a Board decree. The post should describe the mechanism by period.
2. **R2's crediting rule matches the documents only for part of the window.** The half-rate formula
   (`Y = X%.A + 0.5.X%.IJHT`) is printed for 2006 and 2007 and for "off-line" records in 2008. "On-line" records
   from 2008, and all records from 2010 to 2013, are credited day by day from each contribution's receipt date;
   from 2015 BPJS uses time-weighted balances. Half a year is a reasonable stand-in for monthly contributions, but
   it is an approximation from 2008 on, and the post should say so.
3. **The March 2013 payout may not be a rate on the opening 2013 balance.** The audited note says only
   "equivalent to 6.50%". Dividing the payout by 6.50% gives Rp86.67 trillion, near the end-2011 JHT balance
   (Rp85.61 trillion), not the end-2012 balance (Rp100.74 trillion) that R3 applies it to; the August payout does
   match the end-2012 balance (section C). The owner should rule whether R3 stands (it is a pre-registered rule;
   any change is a dated amendment).
4. **The 2009 incentive's base is not stated** (section C). R3's "added to that year's rate" is an inference.
5. **The deposit floor is law only from 1 July 2015** (PP 46/2015 Pasal 37). No stored document gives a legal floor
   for 2005 to mid-2015; design section 7's floor sentence should be dated.
6. **The published yield changes basis.** 2014 is labelled gross ("bruto"), 2015 to 2022 carry no gross or net
   label, and 2023 to 2025 are labelled net ("Neto"). No stored document defines the denominator or says whether
   unrealized gains count (section D). Chart 4 should not present the series as one consistent measure.
7. **The 401(k) comparison figure excludes nonparticipants** and covers Vanguard-recordkept plans only, with 2025
   estimated by extrapolation (section G). P5 compares a statutory rate for all covered workers with an average
   over people who chose to contribute.
8. **JP is a share of wages only up to a ceiling** (Rp7 million a month in 2015, indexed each year); JHT has none
   (section G). R7's "shares of wages" holds for JHT and JP only below the ceiling.
9. **The 0.08% expense ratio is the January 2026 figure**, charged in every year 2005 to 2020 by R4 (section H).
10. **ILO "employees" is wider than JHT's legal coverage** (any paid employment job, including government and
    household employers, section I).
11. **The US CPI's identity rests on a numerical check**, not an IMF document: the IMF file names no national
    compiler (section F).
12. **Rights flags** (section K): BPJS's robots file refuses `ia_archiver` while the 2015 release is an Internet
    Archive capture; Damodaran asks that his data not be used in public policy debates (a request); Vanguard
    licenses content for personal and noncommercial use only; BPJS has no terms of use, so its reports are used
    under Copyright Law Pasal 44(1)(a) with full citations; the ICSE-93 resolution predates the ILO's open-access
    date and is quoted briefly, not reproduced.
13. **Design section 3 says the 2016 to 2020 rates come from audited notes; they do not.** They come from the
    reports' management discussion and narrative (manifest notes); the 2018 audited notes give only monthly claim
    rates. The design's data paragraph needs a dated amendment, or the post should say where the figures come from.

## A. The JHT credited rate: what it is

The law and the rules that define the rate credited to JHT balances, and how each era credits it. The year's rate itself is in `docs/jht-manifest.csv`, one checked row per figure; the table at the end of this section says what each row's defining sentence names.

- **PP 46/2015 Pasal 22(2): what a JHT balance is**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 15, Pasal 22 ayat (2).
  Quote: "Besarnya manfaat JHT adalah sebesar nilai akumulasi seluruh Iuran yang telah disetor ditambah hasil pengembangannya yang tercatat dalam rekening perorangan Peserta"
  Establishes: A member's JHT is the sum of every contribution paid in plus the returns credited to the member's individual account. The 'JHT rate' in this post is the rate at which those returns are credited.

- **PP 46/2015 Pasal 27(1): the annual rate comes from the annual financial report**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 17, Pasal 27 ayat (1).
  Quote: "yang diberikan kepada Peserta oleh BPJS Ketenagakerjaan berdasarkan hasil pengembangan program JHT sesuai laporan keuangan tahunan"
  Establishes: The return credited to members follows the JHT program's result in the annual financial report.

- **PP 46/2015 Pasal 27(2): members who claim get a monthly rate**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 18, Pasal 27 ayat (2).
  Quote: "ditetapkan berdasarkan laporan keuangan bulanan pada periode bulan sebelumnya"
  Establishes: Members who claim during the year are paid at a rate set from the previous month's financial report, not at the annual rate. This is why the audited notes list monthly 'claim rates' (see the IR 2015 and IR 2018 entries).

- **PP 46/2015 Pasal 27(3): the floor under the credited rate**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 18, Pasal 27 ayat (3).
  Quote: "paling sedikit sebesar rata-rata bunga deposito counter rate bank pemerintah untuk jangka waktu 1 (satu) tahun"
  Establishes: Both the annual and the monthly rate must be at least the average one-year counter rate on deposits at state banks. This is the floor the design cites in section 7 (sources.json key pp46_rate_floor holds the longer quote).

- **PP 46/2015 Pasal 37: in force from 1 July 2015**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 22, Pasal 37.
  Quote: "Peraturan Pemerintah ini mulai berlaku pada tanggal 1 Juli 2015"
  Establishes: The statutory floor exists from 1 July 2015. For 2005 to mid-2015 no stored document states a legal floor; the Jamsostek-era rate was set by Board decree (entries below).

- **Peraturan BPJS 4/2015: the rule in force for 2015 to 2020 (image-only scan)**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2015 No. 1329; ditetapkan 29 July 2015, diundangkan 3 September 2015 (read from the page renders). *Peraturan BPJS Ketenagakerjaan Nomor 4 Tahun 2015 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan hari tua* (salinan, scanned). https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/05022016_110020_PER%20BPJSTK%20NOMOR%2004%20TAHUN%202015.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_4_2015.pdf` (SHA-256 `b682477a437148f3309439f73fe16996e3cd461324ed92f237546272f4aaeb4a`); fetched 2026-10-21 (source vet); PDF pages 3 to 5 (no text layer; read from 80 dpi renders made by this audit). Pasal 2(4), 2(6), 4(1), 5(1); page 5 dates.
  Transcription (not machine-checked): Pasal 4(1): Penetapan tingkat pengembangan JHT secara tahunan dilakukan setiap tanggal 31 Desember untuk membentuk saldo awal tahun berikutnya.
  Establishes: Pasal 2(4) gives the annual rate from the annual financial report; Pasal 2(6) repeats the deposit floor; Pasal 4(1) sets the annual rate each 31 December to form the next year's opening balance; Pasal 5(1) distributes it proportionally every 31 December to members who have not claimed. Ditetapkan 29 Juli 2015, diundangkan 3 September 2015, Berita Negara 2015 No. 1329. This is the regulation that Peraturan BPJS 3/2020 Pasal 8 revokes, so it governed the 2015 to 2020 year-end rates.

- **Peraturan BPJS 3/2020 Pasal 1 angka 3: definition of Hasil Pengembangan**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 3, Pasal 1 angka 3.
  Quote: "Hasil Pengembangan adalah hasil investasi DJS Hari Tua dan pendapatan dari sumber lainnya yang dapat didistribusikan kepada peserta setelah dikurangi dana operasional dan biaya lainnya"
  Establishes: What is credited is investment income net of the operating fund and other costs, not the fund's gross yield.

- **Peraturan BPJS 3/2020 Pasal 2(5): the credited balance becomes the 1 January opening balance**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 4, Pasal 2 ayat (5).
  Quote: "yang dicatat sebagai Saldo Awal peserta pada tanggal 1 Januari tahun berikutnya"
  Establishes: For members who have not fully claimed by 31 December, the opening balance plus contributions plus the year's returns is recorded as the next year's opening balance on 1 January.

- **Peraturan BPJS 3/2020 Pasal 2(6): the annual rate is set from the November report**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 4, Pasal 2 ayat (6).
  Quote: "Hasil Pengembangan program JHT diberikan setiap tahun berdasarkan Tingkat Pengembangan tahunan sesuai laporan keuangan bulanan pada periode November tahun berjalan"
  Establishes: From 2021 the annual rate is set from the November monthly accounts of the same year, before the year ends.

- **Peraturan BPJS 3/2020 Pasal 2(7): claimants get the monthly rate**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 4, Pasal 2 ayat (7).
  Quote: "Tingkat Pengembangan bulanan sesuai laporan keuangan bulanan pada periode bulan sebelumnya"
  Establishes: Members who claim (in full under ayat (1), or partly under ayat (2)) are credited at the monthly rate from the previous month's accounts.

- **Peraturan BPJS 3/2020 Pasal 2(8): the same deposit floor**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 4, Pasal 2 ayat (8).
  Quote: "ditetapkan paling sedikit sebesar rata-rata bunga deposito (counter rate) Bank Pemerintah jangka waktu satu tahun"
  Establishes: Annual and monthly rates are floored at the average one-year state-bank counter rate, restating PP 46/2015 Pasal 27(3).

- **Peraturan BPJS 3/2020 Pasal 3(1): how the rate is computed**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 5, Pasal 3 ayat (1).
  Quote: "berdasarkan Hasil Pengembangan dibagi dengan penjumlahan dari Saldo Awal tertimbang ditambah total iuran tertimbang dikurangi total klaim sebagian tertimbang"
  Establishes: The rate is net investment result divided by time-weighted balances (opening balance plus weighted contributions less weighted partial claims). It is a ratio of what can be distributed, not a market return.

- **Peraturan BPJS 3/2020 Pasal 3(2): only realized income counts**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 5, Pasal 3 ayat (2).
  Quote: "dihitung berdasarkan hasil investasi bersih JHT yang direalisasikan ditambah pendapatan dari sumber lainnya dikurangi dana operasional dan biaya lainnya"
  Establishes: Unrealized gains and losses do not enter the credited rate. Peraturan BPJS 4/2015 Pasal 3(2) has the same wording (page render).

- **Peraturan BPJS 3/2020 Pasal 4(2): the monthly claim periods**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 6, Pasal 4 ayat (2).
  Quote: "berlaku untuk klaim pada tanggal 20 bulan berjalan sampai dengan tanggal 19 bulan berikutnya"
  Establishes: A monthly rate applies to claims from the 20th of one month to the 19th of the next, which is why the audited notes list periods such as '20 Desember 2015 s.d 19 Januari 2016' (section B). Peraturan BPJS 4/2015 Pasal 4(2) has the same periods (page render).

- **Peraturan BPJS 3/2020 Pasal 4(4): the January claim rate is the deposit rate**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 6, Pasal 4 ayat (4).
  Quote: "ditetapkan sebesar rata-rata bunga deposito (counter rate) Bank Pemerintah jangka waktu satu tahun periode Desember tahun sebelumnya"
  Establishes: Claims from 1 January to 19 February are credited at the previous December's counter rate, a mechanical rule, not a fund result.

- **Peraturan BPJS 3/2020 Pasal 5(1): distribution on 1 January**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 6, Pasal 5 ayat (1).
  Quote: "dilakukan secara proporsional setiap tanggal 1 Januari berdasarkan Tingkat Pengembangan tahunan"
  Establishes: The annual rate is credited proportionally to members who have not fully claimed, every 1 January.

- **Peraturan BPJS 3/2020 Pasal 9: in force on promulgation**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 7, Pasal 9 (Pasal 8 on the same page revokes Peraturan BPJS 4/2015, Berita Negara 2015 No. 1329).
  Quote: "Peraturan Badan ini mulai berlaku pada tanggal diundangkan"
  Establishes: The regulation takes effect on its promulgation date (next entry).

- **Peraturan BPJS 3/2020: promulgated 7 January 2021**
  BPJS Ketenagakerjaan (Direktur Utama); Berita Negara Republik Indonesia 2021 No. 4; ditetapkan 28 December 2020, diundangkan 7 January 2021. *Peraturan BPJS Ketenagakerjaan Nomor 3 Tahun 2020 tentang mekanisme penetapan dan distribusi hasil pengembangan dana jaminan sosial hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf
  Stored: `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` (SHA-256 `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a`); fetched 2026-10-21 (source vet; re-fetched hash-identical by the vet's checker); PDF page 8, promulgation block.
  Quote: "Diundangkan di Jakarta pada tanggal 7 Januari 2021"
  Establishes: Peraturan BPJS 3/2020 governs 2021 onward, after the design's 2005 to 2020 window. It describes the mechanism the vet summarised, but the window's year-end rates were set under Peraturan BPJS 4/2015 and PERDIR/143/102015 (2015 to 2020) or Board decrees (2005 to 2014).

- **Jamsostek era: crediting formula with half the rate on the year's contributions (2006)**
  PT Jamsostek (Persero); 2007. *Laporan Tahunan 2006* (annual report with audited consolidated financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140411_anual_06.pdf
  Stored: `sources/jht/jamsostek_ar_2006.pdf` (SHA-256 `604e14f42f25e49d08e2049b953b7d80dce6530a82f4645db784f9b79ca5c7bb`); fetched 2026-10-21 (source vet); PDF page 116, audited notes, accounting policy on Hutang JHT (English on PDF page 145).
  Quote: "Y = X%.A + 0.5.X%.IJHT Y = bagian peserta atas hasil investasi JHT X% = besaran tarif bunga JHT per tahun yang ditetapkan Perusahaan"
  Establishes: The member's share is the year's rate X% on the opening balance plus half of X% on the year's contributions. X% is a rate set by the company (the Board decree in jht-manifest.csv), not an investment yield. This is the crediting rule R2 adopts.

- **Jamsostek era: the terms of the formula (2006)**
  PT Jamsostek (Persero); 2007. *Laporan Tahunan 2006* (annual report with audited consolidated financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140411_anual_06.pdf
  Stored: `sources/jht/jamsostek_ar_2006.pdf` (SHA-256 `604e14f42f25e49d08e2049b953b7d80dce6530a82f4645db784f9b79ca5c7bb`); fetched 2026-10-21 (source vet); PDF page 116, same note.
  Quote: "A = saldo hutang JHT awal tahun IJHT = iuran JHT yang diterima selama tahun berjalan"
  Establishes: A is the opening JHT balance and IJHT the contributions received during the year.

- **Jamsostek era: what is not credited goes to the development fund**
  PT Jamsostek (Persero); 2007. *Laporan Tahunan 2006* (annual report with audited consolidated financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140411_anual_06.pdf
  Stored: `sources/jht/jamsostek_ar_2006.pdf` (SHA-256 `604e14f42f25e49d08e2049b953b7d80dce6530a82f4645db784f9b79ca5c7bb`); fetched 2026-10-21 (source vet); PDF page 116, same note.
  Quote: "maka sisa tersebut menjadi dana pengembangan JHT"
  Establishes: Investment income left after crediting members becomes the JHT development fund (dana pengembangan JHT). The 2008 incentive and the 2013 one-off payouts were paid out of this fund (section C).

- **Jamsostek era: the same half-rate formula (2007)**
  PT Jamsostek (Persero); 2008. *Laporan Tahunan 2007*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140427_anual_07.pdf
  Stored: `sources/jht/jamsostek_ar_2007.pdf` (SHA-256 `86942918b27af30a7620070c54a7937852c6c4177f68f55476561e188d8d7580`); fetched 2026-10-21 (source vet); PDF page 153, audited notes. The same words also occur on PDF page 184.
  Quote: "Y = X%.A + 0.5.X%.IJHT"
  Establishes: 2007 uses the same crediting formula as 2006 (English on PDF page 184).

- **2008: two formulas, day-weighted for on-line records and half-rate for off-line records**
  PT Jamsostek (Persero); 2009. *Laporan Tahunan 2008 / 2008 Annual Report*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140427_anual_08.pdf
  Stored: `sources/jht/jamsostek_ar_2008.pdf` (SHA-256 `7f8fea46d9b92818cba922569ed7dd8da5fe3136d0e428415aae12236059f69a`); fetched 2026-10-21 (source vet); PDF page 211, audited notes, policy p (Utang JHT dan bagian peserta atas hasil investasi JHT). The same words also occur on PDF page 257.
  Quote: "Off-line Y = X%.A + 0.5.X%.IJHT"
  Establishes: From 2008 the notes give two methods: 'On-line' records credit each month's contribution from its receipt date (Ht = Hs + Hi, with Jhn days in the month and Ti the receipt date), 'Off-line' records keep the half-rate formula. R2's half-rate rule is the off-line formula; for contributions spread evenly through the year the on-line formula credits about the same (an approximation this audit states, not a document).

- **2010: only the day-weighted formula is printed**
  PT Jamsostek (Persero); 2011. *Laporan Tahunan 2010*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/26032015_134549_AR%20JAMSOSTEK%20LOWRESS%20PLENO%2010711.pdf
  Stored: `sources/jht/jamsostek_ar_2010.pdf` (SHA-256 `ba9b9628e3e59dfc28cad2e74d06690c2980d7e6b0378731fe93475cc22f84fe`); fetched 2026-10-21 (source vet); PDF page 288, audited notes, policy t (two-column bilingual page).
  Quote: "Ti : Tanggal Iuran Diterima"
  Establishes: The 2010 notes print only the day-weighted formula (Ht = Hs + Hi, Hs = Sa x i%, Hi summed over months with the receipt date Ti); no off-line half-rate formula appears. The 2011 (PDF page 396), 2012 (PDF page 508) and 2013 (PDF page 334) notes print the same day-weighted formula. So from 2010 the documented crediting is day-weighted, and R2's half-year rule is an approximation of it.

- **2013: the day-weighted formula still in force**
  PT Jamsostek (Persero), published by BPJS Ketenagakerjaan; 2014. *Laporan Tahunan 2013*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/26032015_133805_ARA%20BPJS%20Ketenagakerjaan%202013.pdf
  Stored: `sources/jht/jamsostek_ar_2013.pdf` (SHA-256 `5ffe934e8611cba133db3007eb5bccd9e32e838284c9daba05ef2dea868a8c3d`); fetched 2026-10-21 (source vet); PDF page 334, audited notes (stamped 'D1/January 30, 2014'). The same words also occur on PDF pages 454, 587.
  Quote: "Ti : Tanggal Iuran Diterima"
  Establishes: Same day-weighted formula for 2013.

- **BPJS era: what hasil pengembangan is (2014 and 2015 notes)**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 316, audited DJS JHT notes, note 3.t.
  Quote: "Hasil pengembangan adalah akumulasi hasil investasi Jaminan Hari Tua yang telah dikurangi dengan beban pengelolaan Program JHT yang akan dikembalikan kepada peserta"
  Establishes: The credited return is investment income after the JHT program's management costs, returned to members.

- **BPJS era: from 1 January 2015 the rate is set monthly at claim**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 315, note 3.t, citing KEP/94/032015 amending KEP/392/122014.
  Quote: "penghitungan dana pengembangan Jaminan Hari Tua per 1 Januari 2015 dilakukan secara bulanan pada saat klaim yang ditetapkan oleh tim khusus"
  Establishes: In 2015 the development result was computed monthly at the time of claim by a special team. This is why 2015 has a list of monthly settings and no single annual decree (section B).

- **BPJS era: PERDIR/143/102015 hands the rate to a working team**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 315, note 3.t, citing PERDIR/143/102015 of 14 September 2015.
  Quote: "Tingkat Pengembangan Jaminan Hari Tua dihitung oleh Tim Kerja yang ditunjuk melalui Surat Perintah"
  Establishes: From October 2015 the rate is computed by an appointed working team. The 2016 to 2018 year-end rates in jht-manifest.csv are described as set by 'Tim JHT'; the 2019 and 2020 rows are worded differently (their manifest notes). PERDIR/143/102015 itself is not stored and was not found.

- **2018: the audited notes list only monthly claim rates**
  BPJS Ketenagakerjaan; 2019. *Integrated report 2018* (file BPJS19_LO23_FS.pdf, with the DJS JHT financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS19_LO23_FS.pdf
  Stored: `sources/jht/bpjs_ir_2018.pdf` (SHA-256 `db96187f92c805328f161943fc72bcfbedb8c5b0fddcf54781f147d440e15886`); fetched 2026-10-21 (source vet); PDF page 470, DJS JHT notes, note 5 (Hasil Pengembangan), table of rates by period.
  Quote: "12 20 Desember s.d 31 Desember 2018 6,23%"
  Establishes: The 2018 audited notes give twelve monthly claim rates, the last being 6.23% for 20 to 31 December. The year-end rate of 6.26% in jht-manifest.csv comes from the same report's narrative (PDF pages 22 and 120), not from these notes.

- **2018: distributions come from realized income only**
  BPJS Ketenagakerjaan; 2019. *Integrated report 2018* (file BPJS19_LO23_FS.pdf, with the DJS JHT financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS19_LO23_FS.pdf
  Stored: `sources/jht/bpjs_ir_2018.pdf` (SHA-256 `db96187f92c805328f161943fc72bcfbedb8c5b0fddcf54781f147d440e15886`); fetched 2026-10-21 (source vet); PDF page 501, DJS JHT notes.
  Quote: "distribusi hasil pengembangan JHT kepada peserta bersumber dari hasil investasi realized"
  Establishes: BPJS states, under PERDIR/143/102015, that what members are credited comes from realized investment income only.

- **2018: the consequence when markets fall**
  BPJS Ketenagakerjaan; 2019. *Integrated report 2018* (file BPJS19_LO23_FS.pdf, with the DJS JHT financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS19_LO23_FS.pdf
  Stored: `sources/jht/bpjs_ir_2018.pdf` (SHA-256 `db96187f92c805328f161943fc72bcfbedb8c5b0fddcf54781f147d440e15886`); fetched 2026-10-21 (source vet); PDF page 501, same note.
  Quote: "Pola distribusi hasil pengembangan JHT yang hanya membagikan hasil realized saja"
  Establishes: The same note explains that crediting realized results only can distribute more than the fund's total result when unrealized results are negative, as in 2018 (it reports an unfunded gap for that year). The credited rate and the fund's market return are different measures.

### The rows of `docs/jht-manifest.csv`, by what their sentence names

Values and quotes are the manifest's own (re-checked for this audit: SHA-256 and one occurrence on the cited page for all 31 rows). The last column is this audit's reading of each row's defining sentence.

| Year | Kind | Value (%) | Document, PDF page | What the defining sentence names |
|---|---|---|---|---|
| 2005 | base | 8.00 | `sources/jht/jamsostek_ar_2006.pdf` p.116 | opening balance and contributions of 2005 (Board decree KEP/283/122005) |
| 2006 | base | 10.50 | `sources/jht/jamsostek_ar_2006.pdf` p.116 | opening balance and contributions of 2006 (KEP/262/122006) |
| 2007 | base | 9.50 | `sources/jht/jamsostek_ar_2007.pdf` p.153 | opening balance and contributions of 2007 (KEP/40/022008) |
| 2008 | base | 8.00 | `sources/jht/jamsostek_ar_2008.pdf` p.212 | opening balance and contributions of 2008 (KEP/390/122008) |
| 2008 | incentive | 2.10 | `sources/jht/jamsostek_ar_2008.pdf` p.225 | 2.1% of the 2007 PSJHT balance, from the development fund (section C) |
| 2009 | base | 9.00 | `sources/jht/jamsostek_ar_2010.pdf` p.288 | a 9.00% development result; no base named (KEP/363/122009) |
| 2009 | incentive | 1.60 | `sources/jht/jamsostek_ar_2010.pdf` p.288 | a 1.60% JHT incentive; no base named (section C) |
| 2010 | base | 10.60 | `sources/jht/jamsostek_ar_2010.pdf` p.288 | opening balance and contributions of 2010 (KEP/330/122010) |
| 2011 | base | 10.10 | `sources/jht/jamsostek_ar_2011.pdf` p.396 | opening balance and contributions of 2011 (KEP/363/122011) |
| 2012 | base | 9.10 | `sources/jht/jamsostek_ar_2012.pdf` p.508 | opening balance (Indonesian); the English column adds contributions (KEP/477/122012) |
| 2013 | base | 8.68 | `sources/jht/jamsostek_ar_2013.pdf` p.335 | opening balance only (KEP/444/122013) |
| 2013 | oneoff | 6.50 | `sources/jht/jamsostek_ar_2013.pdf` p.387 | 'equivalent to' a rate, paid to all members who had not withdrawn; no base named (section C) |
| 2013 | oneoff | 0.81 | `sources/jht/jamsostek_ar_2013.pdf` p.387 | 'equivalent to' a rate, paid to all members who had not withdrawn; no base named (section C) |
| 2014 | base | 10.55 | `sources/jht/bpjs_ir_2015.pdf` p.316 | the development result 'for 2014'; no base named (KEP/391/122014) |
| 2015 | yearend_reported | 6.89 | `sources/jht/bpjs_news_6489.html` p.1 | the return BPJS 'could give' members after deductions; a release, not a decree (section B) |
| 2016 | base | 7.19 | `sources/jht/bpjs_ar_2017.pdf` p.166 | year-end rate set by Tim JHT (management discussion) |
| 2017 | base | 7.83 | `sources/jht/bpjs_ar_2017.pdf` p.165 | year-end rate set by Tim JHT (management discussion) |
| 2018 | base | 6.26 | `sources/jht/bpjs_ir_2018.pdf` p.22 | rate set by Tim JHT (narrative); the audited notes give monthly claim rates only |
| 2019 | base | 6.08 | `sources/jht/bpjs_ir_2019.pdf` p.67 | 'hasil pengembangan DJS ... khususnya Program JHT' (management discussion) |
| 2020 | base | 5.59 | `sources/jht/bpjs_ir_2020.pdf` p.52 | 'terendah yang ditetapkan Badan'; read as the JHT rate by inference |
| 2014 | yield | 13.80 | `sources/jht/bpjs_ar_2014.pdf` p.118 | YOI, labelled bruto (gross) |
| 2015 | yield | 8.76 | `sources/jht/bpjs_ir_2015.pdf` p.100 | YOI, no gross or net label |
| 2016 | yield | 9.49 | `sources/jht/bpjs_ir_2016.pdf` p.117 | YOI, no label |
| 2018 | yield | 8.11 | `sources/jht/bpjs_ir_2018.pdf` p.120 | investment result, no label |
| 2019 | yield | 7.23 | `sources/jht/bpjs_ir_2019.pdf` p.67 | investment result, no label |
| 2020 | yield | 7.39 | `sources/jht/bpjs_ir_2020.pdf` p.52 | investment result, no label |
| 2021 | yield | 6.95 | `sources/jht/bpjs_ir_2021.pdf` p.43 | investment result, no label |
| 2022 | yield | 6.81 | `sources/jht/bpjs_ir_2022.pdf` p.49 | investment result, no label |
| 2023 | yield | 7.04 | `sources/jht/bpjs_ir_2023.pdf` p.48 | investment result (Neto) |
| 2024 | yield | 6.86 | `sources/jht/bpjs_ir_2024.pdf` p.104 | investment result (Neto) |
| 2025 | yield | 6.97 | `sources/jht/bpjs_ir_2025.pdf` p.66 | investment result (Neto) |

## B. 2015: a year-end figure, not a decree

Why the 2015 row is labelled `yearend_reported` and what supports it.

- **2015: the last monthly setting of the year**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 315, table under PERDIR/143/102015 (Oktober s.d Desember 2015), row 3.
  Quote: "20 Desember 2015 s.d 19 Januari 2016 6,89"
  Establishes: The audited note's last 2015 setting, 6.89%, covers claims from 20 December 2015. The eleven 2015 settings run from 6.25 to 9.28. This row corroborates the 2015 figure but is a claim rate, not a year-end decree.

- **2015: BPJS's own year-end statement of the return to members**
  BPJS Ketenagakerjaan; posted 19 February 2016 (no media byline). *BPJS Ketenagakerjaan Targetkan Dana Kelolaan Rp246 T Tahun Ini* (news item 6489), Internet Archive capture 20170919194042. https://web.archive.org/web/20170919194042id_/http://www.bpjsketenagakerjaan.go.id:80/berita/6489/BPJS-Ketenagakerjaan-Targetkan-Dana-Kelolaan-Rp246-T-Tahun-Ini.html
  Stored: `sources/jht/bpjs_news_6489.html` (SHA-256 `f08514b85132df42a49b1f5e2a62d6981956f7d0905c82d81df60af704c9fc3e`); fetched 2026-10-21 (gap search; re-fetched byte-identical by its checker); News item 6489, paragraph quoting Irvansyah Utoh Banja (single HTML page; the whole page text).
  Quote: "BPJS Ketenagakerjaan dapat memberikan imbal hasil sebesar 6,89% yang lebih besar dari rata-rata suku bunga deposito Bank Pemerintah"
  Establishes: BPJS's own release says 6.89% is the return it could give members for 2015. It does not use the word 'credited', so the manifest labels the row yearend_reported.

- **2015: what was deducted to reach 6.89%**
  BPJS Ketenagakerjaan; posted 19 February 2016 (no media byline). *BPJS Ketenagakerjaan Targetkan Dana Kelolaan Rp246 T Tahun Ini* (news item 6489), Internet Archive capture 20170919194042. https://web.archive.org/web/20170919194042id_/http://www.bpjsketenagakerjaan.go.id:80/berita/6489/BPJS-Ketenagakerjaan-Targetkan-Dana-Kelolaan-Rp246-T-Tahun-Ini.html
  Stored: `sources/jht/bpjs_news_6489.html` (SHA-256 `f08514b85132df42a49b1f5e2a62d6981956f7d0905c82d81df60af704c9fc3e`); fetched 2026-10-21 (gap search; re-fetched byte-identical by its checker); News item 6489, same paragraph.
  Quote: "setelah dikurangi pencairan klaim JHT, dana operasional dan beban investasi"
  Establishes: The 6.89% is stated as the result after JHT claim payouts, the operating fund and investment costs.

- **2015: the gross development result in the same release**
  BPJS Ketenagakerjaan; posted 19 February 2016 (no media byline). *BPJS Ketenagakerjaan Targetkan Dana Kelolaan Rp246 T Tahun Ini* (news item 6489), Internet Archive capture 20170919194042. https://web.archive.org/web/20170919194042id_/http://www.bpjsketenagakerjaan.go.id:80/berita/6489/BPJS-Ketenagakerjaan-Targetkan-Dana-Kelolaan-Rp246-T-Tahun-Ini.html
  Stored: `sources/jht/bpjs_news_6489.html` (SHA-256 `f08514b85132df42a49b1f5e2a62d6981956f7d0905c82d81df60af704c9fc3e`); fetched 2026-10-21 (gap search; re-fetched byte-identical by its checker); News item 6489, earlier paragraph.
  Quote: "hasil pengembangan program Jaminan Hari Tua (JHT) mencapai 9,14%"
  Establishes: The release's 9.14% is the program's development result before those deductions, a different measure from the 6.89% and from the report's YOI of 8.76% (section D).

- **2015: posting date**
  BPJS Ketenagakerjaan; posted 19 February 2016 (no media byline). *BPJS Ketenagakerjaan Targetkan Dana Kelolaan Rp246 T Tahun Ini* (news item 6489), Internet Archive capture 20170919194042. https://web.archive.org/web/20170919194042id_/http://www.bpjsketenagakerjaan.go.id:80/berita/6489/BPJS-Ketenagakerjaan-Targetkan-Dana-Kelolaan-Rp246-T-Tahun-Ini.html
  Stored: `sources/jht/bpjs_news_6489.html` (SHA-256 `f08514b85132df42a49b1f5e2a62d6981956f7d0905c82d81df60af704c9fc3e`); fetched 2026-10-21 (gap search; re-fetched byte-identical by its checker); News item 6489, header.
  Quote: "Posted: 19 Feb 2016"
  Establishes: The release was posted on 19 February 2016, after the year closed.

- **2015: the market-value return on JHT net assets (not used)**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 353, DJS JHT notes, market-risk table (columns 2015, 2014).
  Quote: "Aset Neto Hasil Pengembangan 2,73% 10,55%"
  Establishes: The 2.73% for 2015 is a return on JHT net assets; the gap search's checker reads it as including unrealized losses (note 31 offsets realized income with unrealized losses). It is neither the credited rate nor the YOI and is not used.

- **2015 and 2016: BPJS's one-page 2016 summary (image only)**
  BPJS Ketenagakerjaan; 2017. *Laporan Keuangan 2016 BPJS Ketenagakerjaan* (one-page summary of the 2016 financial statements, image only; linked on BPJS's site in 2019 as laporan-keuangan-audit-2016.png). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_keuangan/Laporan_Keuangan_2016_BPJS_Ketenagakerjaan.png
  Stored: `sources/provenance/jht/lk_2016_summary.png` (SHA-256 `cedcab52bf88021340ada64d19a8198498ba326bf763f7f4dd6271d25599dc2a`); fetched 2026-10-21 (gap search; re-fetched identical 2026-10-22); Single image, panel 'PERBANDINGAN HASIL PENGEMBANGAN JHT DENGAN DEPOSITO BANK PEMERINTAH' (crop viewed by this audit).
  Transcription (not machine-checked): Legend: Hasil pengembangan JHT, tanpa potongan pajak (dalam persentase); bars 2016 7,19% and 2015 6,89%
  Establishes: BPJS's one-page summary of its 2016 financial statements labels 6.89% (2015) and 7.19% (2016) as the JHT development result before tax deductions, beside the state-bank deposit rate (4.5% and 5.06%). It corroborates the 2015 and 2016 rows; it cannot be quote-checked.

## C. Incentives and one-off payouts: rate, money and balance

What R3's bonuses were, where the money came from, and what balance each was measured on.

- **2008 incentive: rate and the balance it applied to**
  PT Jamsostek (Persero); 2009. *Laporan Tahunan 2008 / 2008 Annual Report*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140427_anual_08.pdf
  Stored: `sources/jht/jamsostek_ar_2008.pdf` (SHA-256 `7f8fea46d9b92818cba922569ed7dd8da5fe3136d0e428415aae12236059f69a`); fetched 2026-10-21 (source vet); PDF page 225, audited notes, paragraph before note 37.
  Quote: "setara dengan tingkat bunga 2,1% dari saldo PSJHT tahun 2007 yang sumber dananya dari dana pengembangan JHT"
  Establishes: The 2008 incentive equals 2.1% of the 2007 PSJHT balance (the balance per members' balance statements at end-2007), paid from the JHT development fund. This matches R3.

- **2008 incentive: what PSJHT is**
  PT Jamsostek (Persero); 2009. *Laporan Tahunan 2008 / 2008 Annual Report*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140427_anual_08.pdf
  Stored: `sources/jht/jamsostek_ar_2008.pdf` (SHA-256 `7f8fea46d9b92818cba922569ed7dd8da5fe3136d0e428415aae12236059f69a`); fetched 2026-10-21 (source vet); PDF page 224, note 34 (Utang JHT sesuai PSJHT).
  Quote: "Akun ini merupakan akumulasi penerimaan iuran JHT berikut hasil pengembangannya yang jumlahnya telah sesuai dengan nilai yang tercantum dalam Pernyataan Saldo Jaminan Hari Tua (PSJHT)"
  Establishes: PSJHT balances are members' contributions plus credited returns as shown in their balance statements.

- **2008 incentive: the end-2007 PSJHT balance**
  PT Jamsostek (Persero); 2009. *Laporan Tahunan 2008 / 2008 Annual Report*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/02022015_140427_anual_08.pdf
  Stored: `sources/jht/jamsostek_ar_2008.pdf` (SHA-256 `7f8fea46d9b92818cba922569ed7dd8da5fe3136d0e428415aae12236059f69a`); fetched 2026-10-21 (source vet); PDF page 224, note 34.
  Quote: "Saldo akun ini pada akhir tahun 2008 dan 2007 masing-masing berjumlah Rp51.773.949.368.626 dan Rp.42.754.319.048.333"
  Establishes: End-2007 PSJHT balance: Rp42.75 trillion. The incentive amount (Rp941.736.126.775, page 225) divided by 2.1% is Rp44.84 trillion, about 5% above it (this audit's arithmetic). The document names the base, so R3's reading stands; the 5% difference is unexplained.

- **2009 incentive: rate given, base not stated**
  PT Jamsostek (Persero); 2011. *Laporan Tahunan 2010*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/26032015_134549_AR%20JAMSOSTEK%20LOWRESS%20PLENO%2010711.pdf
  Stored: `sources/jht/jamsostek_ar_2010.pdf` (SHA-256 `ba9b9628e3e59dfc28cad2e74d06690c2980d7e6b0378731fe93475cc22f84fe`); fetched 2026-10-21 (source vet); PDF page 288, audited notes, policy t, English column.
  Quote: "development yield is 9.00% and 1.60% for JHT"
  Establishes: Decree KEP/363/122009 gave a 9.00% development result and a 1.60% JHT incentive for 2009 (Indonesian column: '9,00 % dan insentif JHT sebesar 1,60%', the manifest's quote). Neither column says what balance the 1.60% applied to. R3 adds it to the 2009 rate, an inference; the source vet's checker reports that the 2013 report's chart (PDF page 83, not quote-checked here) shows 10.6 for 2009, consistent with base plus incentive.

- **2013 one-off payouts: source of the money**
  PT Jamsostek (Persero), published by BPJS Ketenagakerjaan; 2014. *Laporan Tahunan 2013*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/26032015_133805_ARA%20BPJS%20Ketenagakerjaan%202013.pdf
  Stored: `sources/jht/jamsostek_ar_2013.pdf` (SHA-256 `5ffe934e8611cba133db3007eb5bccd9e32e838284c9daba05ef2dea868a8c3d`); fetched 2026-10-21 (source vet); PDF page 387, audited notes, before note 39. The same words also occur on PDF page 500.
  Quote: "Dari saldo Dana Pengembangan JHT per 31 Desember 2012 sebesar Rp 8.272.781.992.143 telah didistribusikan pada bulan Maret 2013"
  Establishes: The March 2013 payout came out of the development fund as it stood at 31 December 2012.

- **2013 one-off payouts: the March rate and who received it**
  PT Jamsostek (Persero), published by BPJS Ketenagakerjaan; 2014. *Laporan Tahunan 2013*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/26032015_133805_ARA%20BPJS%20Ketenagakerjaan%202013.pdf
  Stored: `sources/jht/jamsostek_ar_2013.pdf` (SHA-256 `5ffe934e8611cba133db3007eb5bccd9e32e838284c9daba05ef2dea868a8c3d`); fetched 2026-10-21 (source vet); PDF page 387, same paragraph. The same words also occur on PDF page 500.
  Quote: "atau setara dengan tingkat bunga 6,50% kepada seluruh peserta yang belum mengambil JHT"
  Establishes: The March payout (Rp5.633.678.560.310) is described as equivalent to 6.50% for all members who had not withdrawn their JHT. The sentence does not say which balance the 6.50% was measured on; the August payout (0.81%, Rp818.594.165.600) is worded the same way.

- **2013 one-off payouts: the JHT balances at end-2012 and end-2011**
  PT Jamsostek (Persero); 2013. *Laporan Tahunan 2012*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/25032015_214934_AR%20JAMSOSTEK%202012.pdf
  Stored: `sources/jht/jamsostek_ar_2012.pdf` (SHA-256 `ea1a71164d75f154a9c579042d069f81eccb2d849458aa0fb6430d9600a87f8a`); fetched 2026-10-21 (source vet); PDF page 471, consolidated statement of financial position (columns 31 Dec 2012, 2011, 2010).
  Quote: "Liabilitas Jaminan Hari Tua Sesuai RSJHT 3.t, 35 100,744,721,448,886 85,606,383,728,617"
  Establishes: JHT balances per members' balance records were Rp100.74 trillion at end-2012 and Rp85.61 trillion at end-2011. By this audit's arithmetic, the August payout divided by 0.81% is Rp101.06 trillion (the end-2012 balance, as R3 assumes), but the March payout divided by 6.50% is Rp86.67 trillion, close to the end-2011 balance and 14% below the opening 2013 balance. So the March 6.50% is not confirmed as a rate on the opening 2013 balance (see the gaps).

## D. What BPJS's published investment yield measures

The yield rows in `docs/jht-manifest.csv` (2014 to 2025) are the JHT fund's investment yield, not what members were credited. Their labels change over the years.

- **2014 yield: labelled gross**
  BPJS Ketenagakerjaan; 2015. *Laporan Tahunan 2014*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/15072015_080550_AR%20BPJS%20TK%202014.pdf
  Stored: `sources/jht/bpjs_ar_2014.pdf` (SHA-256 `2f22e5108208dd0433ffa5614f5cbe0c191ebc7d24347fd4bb41b3693a579a1c`); fetched 2026-10-21 (source vet); PDF page 26, Board report, item c (reading-order text; the two-column layout text interleaves).
  Quote: "Yield on Investment (YOI) bruto masing-masing DJS yaitu untuk JKK sebesar 16,12%, JKM 14,89%, JHT 13,80%"
  Establishes: The 2014 JHT yield (13.80%) is a gross YOI by the report's own label.

- **2015 yield: YOI with no gross or net label**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 100, investment overview (reading-order text; the English column interleaves after these words).
  Quote: "Yield on Investment (YOI) pada tahun 2015 untuk Dana Jaminan"
  Establishes: The 2015 figure (8.76%) is called YOI without saying gross or net.

- **2016 yield: YOI table, no label**
  BPJS Ketenagakerjaan; 2017. *Integrated report covering 2016* (pages headed '2017 Integrated Report'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS%20Ketenagakerjaan%20IR%202016.pdf
  Stored: `sources/jht/bpjs_ir_2016.pdf` (SHA-256 `d6640da40395dc20c7c574e9d21bb45f8e3e03bd3081affbe259eaec1f6bc081`); fetched 2026-10-21 (source vet); PDF page 117, table title.
  Quote: "Yield of Investment (YOI) Tahun 2016 (%)"
  Establishes: The 2016 figure (9.49) comes from a YOI table without a gross or net label.

- **2018 yield: the table that holds 2018 to 2025 yields**
  BPJS Ketenagakerjaan; 2019. *Integrated report 2018* (file BPJS19_LO23_FS.pdf, with the DJS JHT financial statements). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS19_LO23_FS.pdf
  Stored: `sources/jht/bpjs_ir_2018.pdf` (SHA-256 `db96187f92c805328f161943fc72bcfbedb8c5b0fddcf54781f147d440e15886`); fetched 2026-10-21 (source vet); PDF page 120, table title (reading-order text).
  Quote: "Tingkat Hasil Pengembangan Investasi Dana Kelola Dan Perbandingan Terhadap Tingkat Bunga Deposito Bank Pemerintah"
  Establishes: From 2018 the yield comes from a table comparing each program's investment result with the state-bank deposit rate.

- **2022 yield: column header still without a net label**
  BPJS Ketenagakerjaan; 2023. *Laporan Tahunan Terintegrasi 2022*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/BPJS_2022_LO19-_(1).pdf
  Stored: `sources/jht/bpjs_ir_2022.pdf` (SHA-256 `54c879ae464b01b9396cb72253fa48dac576baa0c10efb47a341a783ec19cf4b`); fetched 2026-10-21 (source vet); PDF page 49, table header (reading-order text).
  Quote: "Tingkat Hasil Investasi Tingkat Bunga Deposito Selisih"
  Establishes: In 2018 to 2022 the column is headed only 'Tingkat Hasil Investasi' (checked on PDF pages 120, 67, 52, 43 and 49 of the 2018 to 2022 reports).

- **2023 yield: the column is first labelled net**
  BPJS Ketenagakerjaan; 2024. *Integrated Report 2023*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Integrated_Report_2023.pdf
  Stored: `sources/jht/bpjs_ir_2023.pdf` (SHA-256 `84307fef8d3139d6bea1e0432f4645c9e28c1f1551d2faa2e576924aa5357236`); fetched 2026-10-21 (source vet); PDF page 48, table header (reading-order text).
  Quote: "Tingkat Hasil Investasi (Neto)"
  Establishes: From 2023 (also 2024 PDF page 104 and 2025 PDF page 66) the column reads '(Neto)'. Whether the 2018 to 2022 figures are on the same net basis is not stated.

- **2025 yield: net, and the funds pay no tax on investment income**
  BPJS Ketenagakerjaan; 2026. *2025 Laporan Terintegrasi / Integrated Report 2025*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/IR_2025.pdf
  Stored: `sources/jht/bpjs_ir_2025.pdf` (SHA-256 `fb2c05e48895a35c9e9e3be498c41655d1b3070fb8320ca569b92708fe451bc0`); fetched 2026-10-21 (source vet); PDF page 66, text beside the table (reading-order text).
  Quote: "program DJS lainnya yang hasil investasinya tidak dikenakan pajak"
  Establishes: Apart from JKP, the social security funds' investment income is not taxed, so net here means net of costs, not of tax.

- **BPJS's own term for a realized yield**
  BPJS Ketenagakerjaan; 2016. *Laporan Tahunan 2015* (integrated annual report; the DJS JHT notes are stamped 'Draft/April 23, 2016'). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Laporan_Tahunan_2015.pdf
  Stored: `sources/jht/bpjs_ir_2015.pdf` (SHA-256 `c499618ed45ad965cbad49c0fd126041fec9eaadc9086ff166bdade9a52ae14e`); fetched 2026-10-21 (source vet); PDF page 519, DJS JP notes, claim-rate formula (Jaminan Pensiun, not JHT).
  Quote: "YOI_realized : yield on investment (tingkat hasil investasi yang direalisasikan)"
  Establishes: In its pension-program formula BPJS uses 'YOI_realized' for the realized investment yield. No stored document says whether the published JHT yields are realized only or include unrealized changes.

- **The 'lowest yield' sentence names the lowest program in the table (2021)**
  BPJS Ketenagakerjaan; 2022. *Integrated Report 2021*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/Integrated_Report_2021.pdf
  Stored: `sources/jht/bpjs_ir_2021.pdf` (SHA-256 `d7f9aa06e2862bcb80d39185d681884e71b774b2acc5040a209a25c10638f4e3`); fetched 2026-10-21 (source vet); PDF page 43, right-hand column read line by line: 'Tingkat imbal hasil investasi terendah yang / ditetapkan BPJAMSOSTEK adalah 6,88% untuk / Program JKP atau selisih 3,67% ...'; the quote is the middle line, which stays contiguous in the two-column layout text.
  Quote: "ditetapkan BPJAMSOSTEK adalah 6,88% untuk"
  Establishes: In 2021 the same boilerplate that IR 2020 uses for 5.59% (jht-manifest.csv, 2020 base row) names the lowest program yield in the table (JKP). In 2020, 5.59% matches no table value, which is why reading it as the rate set for JHT balances stays an inference.

## E. US returns: Damodaran's definitions

The workbook `data/damodaran_histretSP.xls` defines its own series on the sheet `Explanations and FAQ`.

- **S&P 500 with dividends: index used and back-fill**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Sheet 'Explanations and FAQ', cell B4 (Stocks (Large Cap)).
  Quote: "I use the S&P 500, which was created in 1957, and then back fill the data"
  Establishes: The stock series is the S&P 500 from 1957 and other large-company indices before it. The window (2005 to 2020) is all S&P 500.

- **S&P 500 with dividends: how the annual return is computed**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Same cell, worked example.
  Quote: "my annual return = (1080-1000+5)/1000 = 8.5%"
  Establishes: Annual return = (end level minus start level plus the year's dividends) over the start level: price change plus dividends.

- **Column the analysis reads for stocks**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Sheet 'Returns by year', cell B20 (column header).
  Quote: "S&P 500 (includes dividends)"
  Establishes: Column B is the total-return series, as decimal fractions.

- **10-year T-bond: the yield behind the return**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Sheet 'Explanations and FAQ', cell B6 (US T.Bond); the workbook's own spelling.
  Quote: "I use the yields on a constant-maturrity 10-year bond, which can be found on FRED"
  Establishes: The bond return is built from constant-maturity 10-year Treasury yields that Damodaran takes from FRED. The post reads his computed returns and fetches nothing from FRED.

- **10-year T-bond: repriced at par each year**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Same cell.
  Quote: "issued at par at the prior year's yield"
  Establishes: Each year's return reprices a par bond bought at the previous year-end yield at the new yield, plus the coupon.

- **10-year T-bond: constant maturity**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Same cell.
  Quote: "while keeping the maturity constant at 10 years"
  Establishes: The maturity is reset to 10 years every year: a modelled return, not a fund's (the FAQ on row 20 explains why).

- **Column the analysis reads for bonds**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Sheet 'Returns by year', cell E20 (column header).
  Quote: "US T. Bond (10-year)"
  Establishes: Column E is the 10-year bond return used in the 90/10 mix (R4).

- **Damodaran's inflation series (not used)**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026 (the HTML page's Updated line). *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (workbook histretSP.xls). https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
  Stored: `data/damodaran_histretSP.xls` (SHA-256 `28b8110916a15a4dcc11c87c6422510704608ddedcdfa67a1298abdc22e49c69`); fetched 2026-10-21 (source vet); identical bytes 2026-10-22; Sheet 'Explanations and FAQ', cell B11 (Inflation Rate).
  Quote: "I use the CPI for all urban consumers, reported on FRED."
  Establishes: His inflation is CPI-U from FRED, non-seasonally adjusted (same cell). The analysis takes no inflation from this workbook; it uses the IMF CPI (R5, R6), so his CPI source does not reach any result.

- **Edition date**
  Damodaran, A.; NYU Stern School of Business; January 5, 2026. *Historical Returns on Stocks, Bonds and Bills: 1928-2025* (HTML table). https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html
  Stored: `sources/provenance/us/damodaran_histretSP.html` (SHA-256 `127c772f0fea8763391dbf2c1c7d3ecd3a07ca2b23f81ab47af58b529e2b5647`); fetched 2026-10-21 (source vet); HTML table page, header.
  Quote: "Updated: January 5, 2026"
  Establishes: The edition is the January 2026 update covering 1928 to 2025. The XLS cell labelled 'Date updated:' is stored in the Mac date system (data-README).

## F. Prices: the IMF CPI series

Code meanings come from the IMF's SDMX structure stored by Post 27; the file metadata come from the post's own data files.

- **IMF CPI: COICOP_1999 = _T is all items**
  International Monetary Fund, Statistics Department; n.d. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), referenced codelists* (code extract stored by Post 27). https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`); fetched 2026-10-17 (Post 27); Code extract line 3 (codelist CL_COICOP_1999(1.1.1)).
  Quote: "CL_COICOP_1999(1.1.1) code _T | en name: All Items"
  Establishes: The rows read (COICOP_1999 = _T) are the headline, all-items CPI.

- **IMF CPI: TYPE_OF_TRANSFORMATION = IX is the index**
  International Monetary Fund, Statistics Department; n.d. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), referenced codelists* (code extract stored by Post 27). https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`); fetched 2026-10-17 (Post 27); Code extract line 4 (codelist CL_CPI_TYPE_OF_TRANSFORMATION(5.0.0)).
  Quote: "code IX | en name: Index"
  Establishes: IX is the index level relative to its reference period (not a percent change); SRP_IX, a 2010=100 rebasing, is a different code the analysis does not read.

- **IMF CPI: FREQUENCY = M is monthly**
  International Monetary Fund, Statistics Department; n.d. *IMF SDMX structure for dataflow IMF.STA:CPI(5.0.0), referenced codelists* (code extract stored by Post 27). https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/CPI/5.0.0?references=all
  Stored: `sources/provenance/imf/imf_api_cpi_codes_extract.txt` (SHA-256 `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0`); fetched 2026-10-17 (Post 27); Code extract line 6 (codelist CL_FREQ(1.2.0)).
  Quote: "CL_FREQ(1.2.0) code M | en name: Monthly"
  Establishes: Annual averages (R2) and December values (R5, R6) are taken from the monthly index.

- **Indonesia: reference period of the index read**
  International Monetary Fund; 2026-10-16 (PUBLICATION_DATE column). *Consumer Price Index (CPI), Indonesia* (SDMX-CSV, IMF.STA:CPI(5.0.0)). https://data.imf.org/en/datasets/IMF.STA:CPI
  Stored: `data/imf_cpi_idn_m.csv` (SHA-256 `b3ba15f60d304316b78adedd37229ff945c8669b67321f9284196e564071c20b`); downloaded 2026-10-16 at Post 27's vet; copied unchanged; Column REFERENCE_PERIOD over the headline monthly index rows.
  Quote: "2022A"
  Establishes: Indonesia's headline index is on BPS's 2022 base, the same value on every row read.

- **Indonesia: BPS publishes the CPI the IMF reports**
  International Monetary Fund (Dissemination Standards Bulletin Board); record for Indonesia, agency Statistics Indonesia; 2025-02-05. *SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00)* (stored by Post 27). https://dsbb.imf.org/sdds/dqaf-base/country/IDN/category/CPI00
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` (SHA-256 `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4`); fetched 2026-10-17 (Post 27); DSBB DQAF item 0.1.1 (TextDetails), stored by Post 27.
  Quote: "The consumer prices data are published by BPS as a service to the public."
  Establishes: The Indonesian series is BPS's CPI as reported to the IMF. The post uses the IMF copy because bps.go.id blocks Anthropic's crawler.

- **Indonesia: older bases linked by overlap**
  International Monetary Fund (Dissemination Standards Bulletin Board); record for Indonesia, agency Statistics Indonesia; 2025-02-05. *SDDS DQAF view: Indonesia, Price index: consumer prices (CPI00)* (stored by Post 27). https://dsbb.imf.org/sdds/dqaf-base/country/IDN/category/CPI00
  Stored: `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` (SHA-256 `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4`); fetched 2026-10-17 (Post 27); DSBB DQAF item 3.3.2 (TextDetails), stored by Post 27.
  Quote: "linking reweighted index to historical index is made by the overlap index = 100"
  Establishes: One 2022-based series reaches back across BPS's earlier bases by overlap linking, so 2005 to 2020 can be read from a single series.

- **Indonesia: BPS's published inflation, the Data Inflasi file (amendment A1)**
  Bank Indonesia; data compiled by BPS-Statistics Indonesia; downloaded 2026-10-17. *Data Inflasi* (Statistik, Indikator; workbook saved from the page). https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx
  Stored: `data/bi_data_inflasi.xlsx` (SHA-256 `5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217`); downloaded by hand by the owner on 2026-10-17 for Post 27; copied unchanged 2026-10-22 (Task D); Sheet 'Data Inflasi', header row (Excel row 5), column C heading.
  Quote: "Data Inflasi"
  Establishes: Bank Indonesia's Data Inflasi page, downloaded by hand by the owner on 2026-10-17 for Post 27 and copied here unchanged (the SHA-256 Post 27 pins in build_analysis.py, key bi_inflasi). The column holds BPS's published headline inflation, year on year, percent, by month: 284 months, January 2003 to August 2026, plus a last row 'Desember 2002, 0,00 %' that is a placeholder; profile_data.py excludes it with Post 27's reader (household.read_published_inflation) and its checks. Post 27 cross-checked the file against a second publication, Bank Indonesia's Target Inflasi page (actual inflation by year, December year on year, viewed 2026-10-17): December 2010 6.96 / 6.96, December 2017 3.61 / 3.61, December 2023 2.61 / 2.61; all equal. Under amendment A1 R5 and R6 keep the IMF index, and chart 2 shows, in some years, JHT's rate against these December rates. Exposure: profile_data.py prints the December rates 2004 to 2020 as inputs, and the Task B check and Task D compared them with the IMF index's December-to-December change (Task D printed only the years that differ); no rule result was computed.

- **Bank Indonesia: BPS calculates Indonesia's inflation**
  Bank Indonesia; n.d. *Inflasi* (Fungsi Utama, Moneter, Inflasi; page text extract stored by Post 27). https://www.bi.go.id/id/fungsi-utama/moneter/inflasi/default.aspx
  Stored: `sources/provenance/bi/bi_inflasi_definisi.txt` (SHA-256 `97fb182a8cd9af90afa930d82a570a6855aabc41371264d4a300c482f942c292`); fetched 2026-10-17 (Post 27); copied unchanged 2026-10-22 (Task D); Page text, section 'Definisi Inflasi', fourth sentence (Post 27's extract).
  Quote: "Perhitungan inflasi dilakukan oleh Badan Pusat Statistik (BPS) di Indonesia"
  Establishes: Bank Indonesia states that BPS computes Indonesia's inflation, so the Data Inflasi figures are BPS's published rates as Bank Indonesia reports them. They are credited to Bank Indonesia (section K) and to BPS. The post uses Bank Indonesia's copy because bps.go.id blocks Anthropic's crawler.

- **United States: reference period of the index read**
  International Monetary Fund; 2026-10-22 (PUBLICATION_DATE column). *Consumer Price Index (CPI), United States* (SDMX-CSV, IMF.STA:CPI(5.0.0)). https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/USA.CPI._T..M
  Stored: `data/imf_cpi_usa_m.csv` (SHA-256 `9789f725405061e7d38fcc1d78fe7cbf7daf9254e13c1f185733f7850f900c17`); fetched 2026-10-22T13:30:03Z; Column REFERENCE_PERIOD over the headline monthly index rows.
  Quote: "2010A"
  Establishes: The US headline index is expressed with 2010 as the reference period.

- **United States: the file names no national compiler**
  International Monetary Fund; 2026-10-22 (PUBLICATION_DATE column). *Consumer Price Index (CPI), United States* (SDMX-CSV, IMF.STA:CPI(5.0.0)). https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/USA.CPI._T..M
  Stored: `data/imf_cpi_usa_m.csv` (SHA-256 `9789f725405061e7d38fcc1d78fe7cbf7daf9254e13c1f185733f7850f900c17`); fetched 2026-10-22T13:30:03Z; Column SHORT_SOURCE_CITATION over the headline monthly index rows.
  Quote: "Country Authorities; Organisation for Economic Cooperation and Development; Eurostat; National Summary Data Pages (NSDPs); IMF Staff Calculations"
  Establishes: The IMF file does not name the Bureau of Labor Statistics. That the US series is BLS's CPI-U rests on the build's check (data-README: the IMF index over published CPI-U is constant over 2004-01 to 2020-12), not on an IMF document.

- **United States: what CPI-U is (check file)**
  U.S. Bureau of Labor Statistics; 2026. *Historical CPI-U, December 2025* (historical-cpi-u-202512.xlsx), Internet Archive capture 20260929081709. https://web.archive.org/web/20260929081709id_/https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202512.xlsx
  Stored: `sources/provenance/us/bls_historical-cpi-u-202512.xlsx` (SHA-256 `1010f74a32661f1fc70aba1871efc202ae8e7865e4776e7f894384128a12e954`); fetched 2026-10-21 (source vet); Sheet 'Index Levels', cell B1 (title).
  Quote: "Historical Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, all items, by month"
  Establishes: The series the IMF index was checked against is BLS's all-items CPI-U, US city average, monthly. This file is a check copy, not an input.

- **IMF CPI: the citation the IMF asks for**
  International Monetary Fund; 2026-10-22 (PUBLICATION_DATE column). *Consumer Price Index (CPI), United States* (SDMX-CSV, IMF.STA:CPI(5.0.0)). https://api.imf.org/external/sdmx/2.1/data/IMF.STA,CPI,5.0.0/USA.CPI._T..M
  Stored: `data/imf_cpi_usa_m.csv` (SHA-256 `9789f725405061e7d38fcc1d78fe7cbf7daf9254e13c1f185733f7850f900c17`); fetched 2026-10-22T13:30:03Z; Column SUGGESTED_CITATION (the file has three spaces before the URL; whitespace normalised).
  Quote: "International Monetary Fund. Consumer Price Index (CPI), https://data.imf.org/en/datasets/IMF.STA:CPI. Accessed on [current date]."
  Establishes: Citation format for the APA reference and chart footers.

## G. What goes in: contribution definitions (JHT, JP, 401(k), CPF)

What each contribution rate in R7 is a share of, and for whom.

- **JHT contribution: who pays what**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 11, Pasal 16 ayat (1) (sources.json key pp46_jht_contribution holds the full sentence).
  Quote: "a. 2% (dua persen) ditanggung oleh Pekerja; dan b. 3,7% (tiga koma tujuh persen) ditanggung oleh Pemberi Kerja"
  Establishes: JHT is 5.7% of wages for wage earners of non-state employers: 2% from the worker, 3.7% from the employer.

- **JHT contribution: the wage it is a share of**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015 (ditetapkan and diundangkan 30 June 2015). *Peraturan Pemerintah Nomor 46 Tahun 2015 tentang penyelenggaraan program jaminan hari tua*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2046%20Tahun%202015.pdf
  Stored: `sources/text/pp_46_2015.pdf` (SHA-256 `ad90a60ea58d6a4197f60ac3891821f3f22e205b3824e32846e23338bbb2214c`); fetched 2026-10-21 (source vet); PDF page 11, Pasal 17 ayat (2).
  Quote: "terdiri atas Upah pokok dan tunjangan tetap"
  Establishes: The JHT wage base is basic wage plus fixed allowances, with no ceiling in PP 46/2015. A 401(k) deferral rate is a share of pay as each plan defines it, so the shares compare like-for-like only roughly.

- **JP contribution: who pays what**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015. *Peraturan Pemerintah Nomor 45 Tahun 2015 tentang penyelenggaraan program jaminan pensiun*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2045%20Tahun%202015.pdf
  Stored: `sources/text/pp_45_2015.pdf` (SHA-256 `f48fe9157c56176edbecfcfc267dc0ba0d4b27a246fe96d1fad6a31e1807bdd4`); fetched 2026-10-21 (source vet); PDF page 20, Pasal 28 ayat (3) (sources.json key pp45_jp_split).
  Quote: "a. 2% (dua persen) dari upah ditanggung oleh Pemberi Kerja selain penyelenggara negara; dan b. 1% (satu persen) dari upah ditanggung oleh Peserta"
  Establishes: Jaminan Pensiun is 3% of wages: 2% employer, 1% worker. It is a pension, shown apart from JHT (R7).

- **JP contribution: a wage ceiling**
  Pemerintah Republik Indonesia; BPJS Ketenagakerjaan's copy; 2015. *Peraturan Pemerintah Nomor 45 Tahun 2015 tentang penyelenggaraan program jaminan pensiun*. https://www.bpjsketenagakerjaan.go.id/assets/uploads/peraturan/15122015_104556_PP%2045%20Tahun%202015.pdf
  Stored: `sources/text/pp_45_2015.pdf` (SHA-256 `f48fe9157c56176edbecfcfc267dc0ba0d4b27a246fe96d1fad6a31e1807bdd4`); fetched 2026-10-21 (source vet); PDF page 21, Pasal 29 ayat (2).
  Quote: "Batas paling tinggi Upah yang digunakan sebagai dasar perhitungan Iuran Jaminan Pensiun untuk tahun 2015 ditetapkan sebesar Rp7.000.000,00 (tujuh juta rupiah) setiap bulan"
  Establishes: JP's 3% applies to wages up to a ceiling (Rp7 million a month in 2015), raised each year by GDP growth under ayat (3). For a worker paid above the ceiling, JP is less than 3% of the full wage; JHT has no such ceiling.

- **401(k): what the deferral rate counts**
  Vanguard; June 2026. *How America Saves 2026* (25th ed.). https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  Stored: `sources/text/vanguard_how_america_saves_2026.pdf` (SHA-256 `df79916eaa0664923bb15c99c4cc1481019a9f97c55a90b6fc880d99ae758c79`); fetched 2026-10-21 (source vet); PDF page 36, 'Employee deferrals' (reading-order text).
  Quote: "Vanguard deferral rates are drawn from recordkeeping data and exclude eligible employees"
  Establishes: The deferral rate is the employee's own contribution as a share of pay, among participants only; eligible employees who do not contribute are left out (the same sentence continues).

- **401(k): what the total contribution rate counts**
  Vanguard; June 2026. *How America Saves 2026* (25th ed.). https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  Stored: `sources/text/vanguard_how_america_saves_2026.pdf` (SHA-256 `df79916eaa0664923bb15c99c4cc1481019a9f97c55a90b6fc880d99ae758c79`); fetched 2026-10-21 (source vet); PDF page 45, 'Aggregate contributions' (reading-order text).
  Quote: "Considering both employee and employer contributions, the average total participant contribution rate"
  Establishes: The total contribution rate is employee plus employer contributions as a share of pay. This is the 401(k) figure P5 compares with JHT's 5.7% (sources.json key has_total_contribution).

- **401(k): participants only**
  Vanguard; June 2026. *How America Saves 2026* (25th ed.). https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  Stored: `sources/text/vanguard_how_america_saves_2026.pdf` (SHA-256 `df79916eaa0664923bb15c99c4cc1481019a9f97c55a90b6fc880d99ae758c79`); fetched 2026-10-21 (source vet); PDF page 45, same paragraph.
  Quote: "These rates exclude eligible nonparticipants."
  Establishes: The total contribution rate leaves out eligible employees who do not join. The same page gives a lower rate with nonparticipants counted at 0%; the post should say which one it uses. JHT's 5.7% is a statutory rate for every covered worker.

- **401(k): the sample is Vanguard's own recordkeeping clients**
  Vanguard; June 2026. *How America Saves 2026* (25th ed.). https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  Stored: `sources/text/vanguard_how_america_saves_2026.pdf` (SHA-256 `df79916eaa0664923bb15c99c4cc1481019a9f97c55a90b6fc880d99ae758c79`); fetched 2026-10-21 (source vet); PDF page 109, Methodology.
  Quote: "for which Vanguard directly provides recordkeeping services"
  Establishes: How America Saves covers plans Vanguard recordkeeps (more than 1,300 plans, the same sentence says), not all US plans; participation and deferral rates come from a subset tested for nondiscrimination (sources.json key has_sample).

- **401(k): the 2025 figures are estimates**
  Vanguard; June 2026. *How America Saves 2026* (25th ed.). https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  Stored: `sources/text/vanguard_how_america_saves_2026.pdf` (SHA-256 `df79916eaa0664923bb15c99c4cc1481019a9f97c55a90b6fc880d99ae758c79`); fetched 2026-10-21 (source vet); PDF page 109, Methodology, last paragraph.
  Quote: "The estimations use a combination of linear extrapolation and subjective estimation."
  Establishes: The 2025 participation and deferral figures (asterisked on PDF page 6) are extrapolated and partly judgemental.

- **CPF: the dataset's unit and coverage**
  Central Provident Fund Board, via data.gov.sg; last updated 2026-03-26. *CPF contribution rates* (dataset d_98ffa142ae0dec40391f78f81d26aca9, metadata JSON from the data.gov.sg API; the request URL was not recorded). https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view
  Stored: `sources/provenance/cpf/meta_d_98ffa142ae0dec40391f78f81d26aca9.json` (SHA-256 `26daef4b772c35797bb6148e33bcacfbf2494df087c419644e9e97d62821540b`); fetched 2026-10-21 (source vet); Metadata field data.description, first sentence.
  Quote: "As a proportion of wage, for private sector employees and public sector non-pensionable employees."
  Establishes: CPF contribution rates are shares of wage for private-sector and non-pensionable public-sector employees.

- **CPF: the highest wage band**
  Central Provident Fund Board, via data.gov.sg; last updated 2026-03-26. *CPF contribution rates* (dataset d_98ffa142ae0dec40391f78f81d26aca9, metadata JSON from the data.gov.sg API; the request URL was not recorded). https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view
  Stored: `sources/provenance/cpf/meta_d_98ffa142ae0dec40391f78f81d26aca9.json` (SHA-256 `26daef4b772c35797bb6148e33bcacfbf2494df087c419644e9e97d62821540b`); fetched 2026-10-21 (source vet); Metadata field data.description, third sentence.
  Quote: "The CPF contribution rates are applicable for the highest wage band."
  Establishes: The rates are for the top wage band only (the next sentence gives wages of $750 or more a month for January 2014); lower-wage bands are not in this dataset.

- **CPF: the unit statement the file contradicts**
  Central Provident Fund Board, via data.gov.sg; last updated 2026-03-26. *CPF contribution rates* (dataset d_98ffa142ae0dec40391f78f81d26aca9, metadata JSON from the data.gov.sg API; the request URL was not recorded). https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view
  Stored: `sources/provenance/cpf/meta_d_98ffa142ae0dec40391f78f81d26aca9.json` (SHA-256 `26daef4b772c35797bb6148e33bcacfbf2494df087c419644e9e97d62821540b`); fetched 2026-10-21 (source vet); Metadata field data.description, second sentence.
  Quote: "Percentages are expressed as a number out of 1."
  Establishes: The contribution CSV holds whole percents despite this sentence (data-README); the allocation CSV holds fractions.

- **CPF: age group read (youngest)**
  Central Provident Fund Board, via data.gov.sg. *CPF contribution rates* (CSV). https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view
  Stored: `data/cpf_contribution_rates.csv` (SHA-256 `c4529a8e3cb1fb364dcb7d1279dbaf8ee1f73212b7e335d8b711ef735925d2f2`); fetched 2026-10-21; re-fetched byte-identical 2026-10-22; CSV row prefix (effective_from, age_grp, contributing_party).
  Quote: "2026-01,35 years & below,Employer"
  Establishes: R7's 'aged 55 and under' is four of the dataset's own age groups: '35 years & below', 'Above 35 - 45 years', 'Above 45 - 50 years' and 'Above 50 - 55 years'. Each has rows effective from 2026-01, the rates in force on 1 January 2026.

- **CPF: age group read (oldest)**
  Central Provident Fund Board, via data.gov.sg. *CPF contribution rates* (CSV). https://data.gov.sg/datasets/d_98ffa142ae0dec40391f78f81d26aca9/view
  Stored: `data/cpf_contribution_rates.csv` (SHA-256 `c4529a8e3cb1fb364dcb7d1279dbaf8ee1f73212b7e335d8b711ef735925d2f2`); fetched 2026-10-21; re-fetched byte-identical 2026-10-22; CSV row prefix.
  Quote: "2026-01,Above 50 - 55 years,Employer"
  Establishes: 'Above 50 - 55 years' is the oldest group read; the next group, 'Above 55 - 60 years', is left out.

- **CPF: the allocation dataset and the Special Account closure**
  Central Provident Fund Board, via data.gov.sg; last updated 2026-03-26. *CPF allocation rates* (dataset d_97ec9a2ce15cbf253128e48779a3fba0, metadata JSON). https://data.gov.sg/datasets/d_97ec9a2ce15cbf253128e48779a3fba0/view
  Stored: `sources/provenance/cpf/meta_d_97ec9a2ce15cbf253128e48779a3fba0.json` (SHA-256 `5ec6b51629e066aaceb5f585718d50e3202b18d89bde839f85c4608240a0ed00`); fetched 2026-10-21 (source vet); Metadata field data.description.
  Quote: "From 2025 onwards, upon the closure of Special Account, the contributions for members aged 55 and above will be fully allocated to the Retirement Account (RA)"
  Establishes: The account change affects only members aged 55 and above, outside the groups read.

## H. The 401(k) lines: glide path and cost (R4)

- **Glide path: 90% stocks early in a career**
  Vanguard; n.d. *Target-date fund glide path* (Target Retirement Trust page). https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html
  Stored: `sources/text/vanguard_tdf_glide_path.html` (SHA-256 `d48cb74b2499014f02caf8cf8de0caa320223559c007afbbfeefd320704d1626`); fetched 2026-10-21 (source vet); Glide path section, heading 'Age 20: Phase 1, early career' (sources.json key vanguard_glide_age20).
  Quote: "younger investors can likely afford to take more risks with a 90% stock allocation"
  Establishes: Vanguard's glide path holds 90% stocks in phase 1.

- **Glide path: the stock share starts to fall at 40**
  Vanguard; n.d. *Target-date fund glide path* (Target Retirement Trust page). https://workplace.vanguard.com/investment/strategies/tdf-glide-path.html
  Stored: `sources/text/vanguard_tdf_glide_path.html` (SHA-256 `d48cb74b2499014f02caf8cf8de0caa320223559c007afbbfeefd320704d1626`); fetched 2026-10-21 (source vet); Heading 'Age 40: Beginning of phase 2, midcareer' (sources.json key vanguard_glide_age40).
  Quote: "We start to gradually reduce stock exposure"
  Establishes: A saver aged 25 in 2005 is 40 in 2020, so R4's constant 90/10 mix covers the whole window.

- **Prospectus chart: 90% stocks at 50 and 25 years before retirement**
  Vanguard; January 28, 2026, with a supplement dated May 20, 2026. *Vanguard Target Retirement Funds, Prospectus, Investor Shares* (p308). https://personal.vanguard.com/pub/Pdf/p308.pdf
  Stored: `sources/text/vanguard_target_retirement_prospectus_p308.pdf` (SHA-256 `cd35c5f75fe2db3335037989a57ccc0bc07b4829081425f345fe8521e28b3015`); fetched 2026-10-21 (source vet); PDF page 114 (printed page 111), chart 'An example of how fund asset allocations change over time' (sources.json key vanguard_tr_glide_chart).
  Quote: "Stocks 90% 90% 50% 30%"
  Establishes: The mutual-fund prospectus gives the same 90% for the years up to 25 years before retirement (age 40 if retiring at 65).

- **Expense ratio: 0.08%, the 2026 figure**
  Vanguard; January 28, 2026, with a supplement dated May 20, 2026. *Vanguard Target Retirement Funds, Prospectus, Investor Shares* (p308). https://personal.vanguard.com/pub/Pdf/p308.pdf
  Stored: `sources/text/vanguard_target_retirement_prospectus_p308.pdf` (SHA-256 `cd35c5f75fe2db3335037989a57ccc0bc07b4829081425f345fe8521e28b3015`); fetched 2026-10-21 (source vet); PDF page 58 (printed page 55), Target Retirement 2045 Fund, fees table (sources.json key vanguard_tr2045_expenses). The same words also occur on PDF pages 4, 13, 22, 31, 40, 49, 67, 76, 85, 94, 103.
  Quote: "Acquired Fund Fees and Expenses 0.08% Total Annual Fund Operating Expenses 0.08%"
  Establishes: The 0.08% is the expense ratio in the January 2026 prospectus, all of it the underlying funds' costs. No stored document gives the funds' expense ratios for 2005 to 2020, so charging 0.08% in every year of the window (R4) uses today's cost, not the historical one.

- **Prospectus date**
  Vanguard; January 28, 2026, with a supplement dated May 20, 2026. *Vanguard Target Retirement Funds, Prospectus, Investor Shares* (p308). https://personal.vanguard.com/pub/Pdf/p308.pdf
  Stored: `sources/text/vanguard_target_retirement_prospectus_p308.pdf` (SHA-256 `cd35c5f75fe2db3335037989a57ccc0bc07b4829081425f345fe8521e28b3015`); fetched 2026-10-21 (source vet); PDF page 2, cover.
  Quote: "January 28, 2026 Prospectus"
  Establishes: Dates the fee and glide-path figures (the supplement dated May 20, 2026 is PDF page 1).

## I. Coverage: active JHT members and ILO employees

- **BPJS: what 'active member' means**
  BPJS Ketenagakerjaan; 2026. *2025 Laporan Terintegrasi / Integrated Report 2025* (copy in sources/text, same hash as sources/jht/bpjs_ir_2025.pdf). https://www.bpjsketenagakerjaan.go.id/assets/uploads/laporan_tahunan/IR_2025.pdf
  Stored: `sources/text/bpjs_ir_2025.pdf` (SHA-256 `fb2c05e48895a35c9e9e3be498c41655d1b3070fb8320ca569b92708fe451bc0`); fetched 2026-10-21 (source vet); PDF page 55, membership section (reading-order text).
  Quote: "Peserta aktif merupakan peserta PU, BPU, Jakon dan PMI yang masih membayar iuran dan belum dilaporkan berhenti"
  Establishes: Active members are those still paying contributions; nonactive members have stopped but not claimed their JHT (same paragraph). The JHT count the post uses (end-2024, sources.json key bpjs_ir2024_jht_active, from the 2024 report) is a count of active members, under the definition the 2025 report states, not of everyone with a JHT balance.

- **ILO: the series is modelled, and imputed values are uncertain**
  International Labour Organization; dataflow last update 02/12/2025 (LAST_UPDATE annotation). *Employment by sex and status in employment, ILO modelled estimates, Nov. 2025* (SDMX dataflow DF_EMP_2EMP_SEX_STE_NB). https://sdmx.ilo.org/rest/dataflow/ILO/DF_EMP_2EMP_SEX_STE_NB/latest
  Stored: `sources/provenance/ilo/dataflow_DF_EMP_2EMP_SEX_STE_NB.xml` (SHA-256 `463ed53262c5c2cc8e11b929d3b8cf55080b909f15de10999f64380e605749ab`); fetched 2026-10-22T14:10Z by this audit, HTTP 200; Dataflow DF_EMP_2EMP_SEX_STE_NB, English Description.
  Quote: "Imputed observations are not based on national data, are subject to high uncertainty"
  Establishes: The employee counts are ILO modelled estimates; the post labels them so.

- **ILO: definitions used**
  International Labour Organization; dataflow last update 02/12/2025 (LAST_UPDATE annotation). *Employment by sex and status in employment, ILO modelled estimates, Nov. 2025* (SDMX dataflow DF_EMP_2EMP_SEX_STE_NB). https://sdmx.ilo.org/rest/dataflow/ILO/DF_EMP_2EMP_SEX_STE_NB/latest
  Stored: `sources/provenance/ilo/dataflow_DF_EMP_2EMP_SEX_STE_NB.xml` (SHA-256 `463ed53262c5c2cc8e11b929d3b8cf55080b909f15de10999f64380e605749ab`); fetched 2026-10-22T14:10Z by this audit, HTTP 200; Same Description.
  Quote: "This series is based on the 13th ICLS definitions."
  Establishes: The same Description says status in employment follows ICSE-93 (next entry).

- **ICSE-93: who counts as an employee**
  International Labour Organization, Fifteenth International Conference of Labour Statisticians; adopted 28 January 1993. *Resolution concerning the International Classification of Status in Employment (ICSE)*. https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@stat/documents/normativeinstrument/wcms_087562.pdf
  Stored: `sources/provenance/ilo/icse93_resolution.pdf` (SHA-256 `06ce8eb42b3d1ad79a0507d630ab6ee61e7a61b0d794ea04e04f32686cbd5157`); fetched 2026-10-22T14:10Z by this audit, HTTP 200; PDF page 2, paragraph 8 (group 1).
  Quote: "Employees are all those workers who hold the type of job defined as"
  Establishes: Employees are workers in 'paid employment jobs' (paragraph 6, next entry).

- **ICSE-93: what a paid employment job is**
  International Labour Organization, Fifteenth International Conference of Labour Statisticians; adopted 28 January 1993. *Resolution concerning the International Classification of Status in Employment (ICSE)*. https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@stat/documents/normativeinstrument/wcms_087562.pdf
  Stored: `sources/provenance/ilo/icse93_resolution.pdf` (SHA-256 `06ce8eb42b3d1ad79a0507d630ab6ee61e7a61b0d794ea04e04f32686cbd5157`); fetched 2026-10-22T14:10Z by this audit, HTTP 200; PDF page 2, paragraph 6.
  Quote: "which is not directly dependent upon the revenue of the unit for which they work"
  Establishes: A paid employment job gives a basic remuneration not tied to the employer's revenue, under a written, oral or implicit contract, with a corporation, non-profit, government unit or household (same paragraph). The ILO 'employees' count is therefore wider than the wage earners of non-state employers whose contribution PP 46/2015 Pasal 16 sets; a ratio of active JHT members to ILO employees is a rough coverage measure, not a share of those legally covered.

- **ILO data file: the rows read**
  International Labour Organization; Nov. 2025 vintage. *Employment by sex and status in employment, ILO modelled estimates* (SDMX-CSV, Indonesia). https://sdmx.ilo.org/rest/data/ILO,DF_EMP_2EMP_SEX_STE_NB,1.0/IDN.A..SEX_T.?startPeriod=2015
  Stored: `data/ilo_idn_employment_by_status.csv` (SHA-256 `73572b2829c2fae8e24396d0580fb9f838d707e66cfc3e03d08b9c221396cdb6`); fetched 2026-10-22T13:36:43Z; Column 'UNIT_MULT: Unit multiplier' over the rows with STE_AGGREGATE_EES: Employees.
  Quote: "3: Thousands"
  Establishes: Employee counts in the file are in thousands of persons.

## J. The builders' stored quotes (`docs/sources.json`)

Each record holds its own verbatim quote, document, SHA-256 and page; all 30 were re-checked for this audit (SHA-256 of the stored text, one occurrence in it, and one occurrence on the cited PDF page or HTML page). They define the external figures the prose uses: contribution rates, withdrawal rules, the glide path and fee, How America Saves' rates, IRS and DOL rules, BPJS's member and app counts and its simulator's 5% assumption.

| Key | Document, page | What it defines | Rights |
|---|---|---|---|
| `pp46_jht_contribution` | `sources/text/pp_46_2015.txt` p.11 | Pasal 16 ayat (1): JHT contribution for wage earners whose employer is not a state organ | regulation, no copyright (K) |
| `pp46_rate_floor` | `sources/text/pp_46_2015.txt` p.18 | Pasal 27 ayat (3): floor on the return credited to JHT balances (average one-year state-bank deposit counter rate) | regulation, no copyright (K) |
| `pp46_balance_information` | `sources/text/pp_46_2015.txt` p.15 | Pasal 22 ayat (7): BPJS must tell members their JHT balance and its returns once a year | regulation, no copyright (K) |
| `pp45_jp_total` | `sources/text/pp_45_2015.txt` p.20 | Pasal 28 ayat (2): Jaminan Pensiun (JP) contribution, a monthly share of wages | regulation, no copyright (K) |
| `pp45_jp_split` | `sources/text/pp_45_2015.txt` p.20 | Pasal 28 ayat (3) huruf a and b: how the 3% JP contribution is split between employer and worker | regulation, no copyright (K) |
| `pp60_benefit_payable` | `sources/text/pp_60_2015_kemnaker.txt` p.3 | Pasal I, new Pasal 26 ayat (1) of PP 46/2015: when the JHT benefit must be paid | regulation, no copyright (K) |
| `pp60_stopping_work` | `sources/text/pp_60_2015_kemnaker.txt` p.6 | Penjelasan (elucidation), Pasal I, Pasal 26 ayat (1) huruf a: reaching pension age includes members who stop working | regulation, no copyright (K) |
| `permenaker4_resign_wait` | `sources/text/permenaker_4_2022_kemnaker.txt` p.6 | Pasal 8 (Bagian Ketiga, members who resign): the JHT of a member who resigns, paid in cash after a one-month wait | regulation, no copyright (K) |
| `permenaker4_layoff_wait` | `sources/text/permenaker_4_2022_kemnaker.txt` p.6 | Pasal 10 (Bagian Keempat, members who are laid off): the JHT of a member whose employment is terminated, paid in cash after a one-month wait | regulation, no copyright (K) |
| `vanguard_glide_age20` | `sources/text/vanguard_tdf_glide_path.txt` (web page) | Glide path section, heading 'Age 20: Phase 1, early career' and the sentence under it | Vanguard terms (K) |
| `vanguard_glide_age40` | `sources/text/vanguard_tdf_glide_path.txt` (web page) | Glide path section, heading 'Age 40: Beginning of phase 2, midcareer' and the sentence under it (the stock share starts to fall at 40) | Vanguard terms (K) |
| `vanguard_glide_final` | `sources/text/vanguard_tdf_glide_path.txt` (web page) | Glide path section, under the heading 'Age 72: Phase 4, withdrawal': the glide path's final allocation | Vanguard terms (K) |
| `vanguard_tr_glide_chart` | `sources/text/vanguard_target_retirement_prospectus_p308.txt` p.114 | More on the Funds (printed page 111), chart 'An example of how fund asset allocations change over time': row 'Stocks' under the columns '50 Years Before Retirement', '25 Years Before Retirement', 'At Retirement' and '25 Years After Retirement'; with retirement at 65 the first two columns are ages 15 and 40 | Vanguard terms (K) |
| `vanguard_tr2045_expenses` | `sources/text/vanguard_target_retirement_prospectus_p308.txt` p.58 | Fund summary for Vanguard Target Retirement 2045 Fund (printed page 55): investment objective and the fees and expenses table. Every fund in this prospectus prints the same table (Total Annual Fund Operating Expenses 0.08%), so the quote starts at the fund's own name to occur once; 2045 is the target year of a saver aged 25 in 2005 retiring at 65 | Vanguard terms (K) |
| `has_participation_rate` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, row 'Plan-weighted participation rate' (body text page 31); columns 2021, 2022, 2023, 2024, 2025; the 2025 cell carries the asterisk for an estimate | Vanguard terms (K) |
| `has_average_deferral` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, row 'Average participant deferral rate' (body text page 36); columns 2021, 2022, 2023, 2024, 2025; the 2025 cell carries the asterisk for an estimate | Vanguard terms (K) |
| `has_median_deferral` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, row 'Median participant deferral rate' (body text page 36); columns 2021, 2022, 2023, 2024, 2025; the 2025 cell carries the asterisk for an estimate | Vanguard terms (K) |
| `has_total_contribution` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, row 'Average total contribution rate (participant and employer)' (body text page 45); columns 2021, 2022, 2023, 2024, 2025; the 2025 cell carries the asterisk for an estimate | Vanguard terms (K) |
| `has_auto_enrollment` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, row 'Plans with automatic enrollment' (body text page 27); columns 2021, 2022, 2023, 2024, 2025; this row has no estimate asterisk | Vanguard terms (K) |
| `has_2025_estimates` | `sources/text/vanguard_how_america_saves_2026.txt` p.6 | Highlights at a glance, footnote to the asterisk | Vanguard terms (K) |
| `has_sample` | `sources/text/vanguard_how_america_saves_2026.txt` p.109 | Methodology, 'Vanguard participation and deferral rates': the sample is Vanguard's own recordkeeping clients | Vanguard terms (K) |
| `irs_deferral_limit_2026` | `sources/text/irs_401k_contribution_limits.txt` (web page) | Section on elective deferral limits: the 2026 limit on employee elective deferrals | IRS: not subject to copyright (K) |
| `irs_early_additional_tax` | `sources/text/irs_topic_558.txt` (web page) | First paragraph: the additional tax on early distributions | IRS: not subject to copyright (K) |
| `irs_early_age` | `sources/text/irs_topic_558.txt` (web page) | First paragraph: which distributions count as early (before age 59 and a half) | IRS: not subject to copyright (K) |
| `dol_fab_quarterly_statements` | `sources/text/dol_fab_2006-03.txt` p.1 | Field Assistance Bulletin No. 2006-03 (December 20, 2006), Background: ERISA section 105 as amended by the Pension Protection Act of 2006 requires a statement at least once each quarter for participant-directed individual account plans | DOL public domain (K) |
| `bpjs_ir2024_jht_active` | `sources/text/bpjs_ir_2024.txt` p.92 | Membership section, list headed 'Rincian peserta aktif per program adalah sebagai berikut' (active members by program, position to December 2024), item 2: JHT, with wage earners (PU) and non-wage earners (BPU) | BPJS: Copyright Law Pasal 44(1)(a) (K) |
| `bpjs_ir2024_active_list_heading` | `sources/text/bpjs_ir_2024.txt` p.92 | Membership section: the heading of the list that holds the JHT count, which marks those counts as active members | BPJS: Copyright Law Pasal 44(1)(a) (K) |
| `bpjs_ir2025_jmo_users` | `sources/text/bpjs_ir_2025.txt` p.99 | JMO (Jamsostek Mobile) table under the header row 'Keterangan 2025 2024 2023', row 'Pengguna JMO' (users of the JMO app by year; the table does not say how many of them checked a balance) | BPJS: Copyright Law Pasal 44(1)(a) (K) |
| `bpjs_ir2022_brand_awareness` | `sources/text/bpjs_ir_2022.txt` p.88 | Table 'Tantangan dan Solusi Perluasan Kepesertaan', column 'Kendala' (obstacles to wider membership), first row | BPJS: Copyright Law Pasal 44(1)(a) (K) |
| `bpjs_simulator_assumed_return` | `sources/text/bpjs_tetap_sejahtera.txt` (web page) | JHT simulator ('Simulasikan Manfaat JHT Disini'), list of assumptions under 'Perhitungan simulasi di atas dengan asumsi' | BPJS: Copyright Law Pasal 44(1)(a) (K) |

## K. Rights basis by source

Robots lines are quoted from the stored robots files; terms clauses from the stored terms pages. None of the 16 stored robots files names ClaudeBot, Claude-User, Claude-SearchBot, Claude-Web or anthropic-ai (checked for this audit), and sdmx.ilo.org has no robots file (HTTP 404, 2026-10-22). Hosts the design excludes (bps.go.id, kwsp.gov.my, peraturan.bpk.go.id, FRED) and the press sites the task names were not fetched.

- **BPJS site robots: all agents allowed**
  https://www.bpjsketenagakerjaan.go.id/robots.txt
  Stored: `sources/provenance/robots/www.bpjsketenagakerjaan.go.id.txt` (SHA-256 `8ddd4eb2b36e0c6269ef1d83f5c8d6db4e4649a6041b4b7e5a5f2dcefaad5f65`); fetched 2026-10-21 (source vet; re-fetched byte-identical by its checker); robots.txt, first group.
  Quote: "User-agent: * Disallow: User-agent: Googlebot Disallow:"
  Establishes: The '*' group has an empty Disallow, so every path is allowed to agents not named; no Anthropic agent is named.

- **BPJS site robots: the Internet Archive's crawler is refused**
  https://www.bpjsketenagakerjaan.go.id/robots.txt
  Stored: `sources/provenance/robots/www.bpjsketenagakerjaan.go.id.txt` (SHA-256 `8ddd4eb2b36e0c6269ef1d83f5c8d6db4e4649a6041b4b7e5a5f2dcefaad5f65`); fetched 2026-10-21 (source vet; re-fetched byte-identical by its checker); robots.txt, ia_archiver group.
  Quote: "User-agent: ia_archiver Disallow: /"
  Establishes: The site asks ia_archiver not to crawl. The 2015 release (news item 6489) is an Internet Archive capture from 2017-09-19. This audit could not establish whether the rule existed when the capture was made; the owner should weigh it.

- **Copyright Law: no copyright in regulations**
  Mahkamah Konstitusi Republik Indonesia; 2025. *Undang-Undang Nomor 28 Tahun 2014 tentang Hak Cipta, Anotasi 2025* (OCR text layer). https://s.mkri.id/public/content/infoumum/undang/pdf/Anotasi_185_UU%2028%202014%20Hak%20Cipta.pdf
  Stored: `sources/provenance/rights/uu_28_2014_anotasi_2025.pdf` (SHA-256 `6fada279bc2688b76ef52acb35bc73d4f4bf5360261692a81c777eb9ba3bc3ed`); fetched 2026-10-21 (source vet; 50.6 MB); PDF page 28 (printed 21), Pasal 42 huruf b (OCR text layer).
  Quote: "b. peraturan perundang-undangan;"
  Establishes: PP 45/2015, PP 46/2015, PP 60/2015, Permenaker 4/2022 and the Peraturan BPJS carry no copyright (Pasal 42: 'Tidak ada Hak Cipta atas hasil karya berupa').

- **Copyright Law: citation basis for BPJS reports**
  Mahkamah Konstitusi Republik Indonesia; 2025. *Undang-Undang Nomor 28 Tahun 2014 tentang Hak Cipta, Anotasi 2025* (OCR text layer). https://s.mkri.id/public/content/infoumum/undang/pdf/Anotasi_185_UU%2028%202014%20Hak%20Cipta.pdf
  Stored: `sources/provenance/rights/uu_28_2014_anotasi_2025.pdf` (SHA-256 `6fada279bc2688b76ef52acb35bc73d4f4bf5360261692a81c777eb9ba3bc3ed`); fetched 2026-10-21 (source vet; 50.6 MB); PDF page 29 (printed 22), Pasal 44 ayat (1) huruf a, with its closing condition.
  Quote: "pendidikan, penelitian, penulisan karya ilmiah, penyusunan laporan, penulisan kritik atau tinjauan suatu masalah dengan tidak merugikan kepentingan yang wajar dari Pencipta atau Pemegang Hak Cipta"
  Establishes: Use for research, report writing, criticism or review is not infringement if the source is cited in full and the rights holder's reasonable interests are not harmed. BPJS's site has no terms of use (vet: eight likely terms URLs return 404), so reuse of its reports rests on this: full citations, figures only, no reproduced charts or images.

- **Copyright Law: the full-citation condition**
  Mahkamah Konstitusi Republik Indonesia; 2025. *Undang-Undang Nomor 28 Tahun 2014 tentang Hak Cipta, Anotasi 2025* (OCR text layer). https://s.mkri.id/public/content/infoumum/undang/pdf/Anotasi_185_UU%2028%202014%20Hak%20Cipta.pdf
  Stored: `sources/provenance/rights/uu_28_2014_anotasi_2025.pdf` (SHA-256 `6fada279bc2688b76ef52acb35bc73d4f4bf5360261692a81c777eb9ba3bc3ed`); fetched 2026-10-21 (source vet; 50.6 MB); PDF page 29, Pasal 44 ayat (1), lead-in.
  Quote: "jika sumbernya disebutkan atau dicantumkan secara lengkap untuk keperluan:"
  Establishes: The condition is a complete citation.

- **Kemnaker JDIH robots: all allowed**
  https://jdih.kemnaker.go.id/robots.txt
  Stored: `sources/provenance/robots/jdih.kemnaker.go.id.txt` (SHA-256 `16ceb5ee3e0dc13aa9adf31a3ebbe45a1d965b8c2b9f72eaf84e5911e140ed95`); fetched 2026-10-21 (source vet); robots.txt, whole file.
  Quote: "User-agent: * Allow: /"
  Establishes: PP 60/2015 and Permenaker 4/2022 came from this host.

- **Kemnaker JDIH: footer covers the site, not the statutes**
  Kementerian Ketenagakerjaan, JDIH; n.d. *Record: Peraturan Pemerintah Nomor 60 Tahun 2015* (detail page 622). https://jdih.kemnaker.go.id/peraturan/detail/622
  Stored: `sources/provenance/rights/jdih_kemnaker_detail_622.html` (SHA-256 `636fa19b475a74ea98c0b929144c058d87afea8f9e37731b900e9cc011ab6eb1`); fetched 2026-10-21 (source vet); Record page 622 (PP 60/2015), footer.
  Quote: "© 2026 JDIH Kementerian Ketenagakerjaan RI. All Rights Reserved."
  Establishes: The notice covers the site; the statute texts have no copyright (Pasal 42 huruf b). The same page records PP 60/2015 as 'Berlaku'.

- **Constitutional Court host robots**
  https://s.mkri.id/robots.txt
  Stored: `sources/provenance/robots/s.mkri.id.txt` (SHA-256 `c00c30db3392bdf92714f71e661e312ee9d5542e015e3c56a9b30bda5a83400e`); fetched 2026-10-21 (source vet); robots.txt, '*' group.
  Quote: "User-agent: * Disallow: /bak/"
  Establishes: The '*' group disallows a list of directories, none of them /public/, where the Copyright Law copy sits; no Anthropic agent is named.

- **Internet Archive: web.archive.org has no robots file**
  https://web.archive.org/robots.txt (HTTP 404 page)
  Stored: `sources/provenance/robots/web.archive.org.txt` (SHA-256 `d465172175d35d493fb1633e237700022bd849fa123164790b168b8318acb090`); fetched 2026-10-21 (source vet); Response to /robots.txt.
  Quote: "<title>404 Not Found</title>"
  Establishes: No rules apply to web.archive.org captures (2015 release, DOL bulletin, BLS file).

- **Internet Archive: archive.org robots**
  https://archive.org/robots.txt
  Stored: `sources/provenance/robots/archive.org.txt` (SHA-256 `83e00f46c71e9fa872694af73fa9c15a615b9052b2f10820a3d146bc506c6161`); fetched 2026-10-21 (source vet); robots.txt.
  Quote: "User-agent: * Disallow: /control/ Disallow: /report/"
  Establishes: archive.org disallows only two admin paths; no Anthropic agent is named.

- **Damodaran: host robots**
  https://pages.stern.nyu.edu/robots.txt
  Stored: `sources/provenance/robots/pages.stern.nyu.edu.txt` (SHA-256 `b6c31d61cdbe840d46c0f8b71cdebdc404cd5f282c689acdb681c72ccb4af01d`); fetched 2026-10-21 (source vet; live copy re-checked identical); robots.txt, whole file.
  Quote: "User-agent: * Disallow: /~tang/aboutus/recruiters/"
  Establishes: Only a recruiters path is disallowed; the data paths are allowed and no Anthropic agent is named.

- **Damodaran: no strings attached**
  Damodaran, A.; NYU Stern School of Business; n.d. *Data history* (sections History & Philosophy and Usage Rules). https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html
  Stored: `sources/provenance/rights/damodaran_datahistory.html` (SHA-256 `6d8ccb3d77715d951c8fa1ccf76654396fbf4f4bbcf8cb87487ac26656bb04aa`); fetched 2026-10-21 (source vet; re-fetched byte-identical by its checker); Data history page, History & Philosophy.
  Quote: "I hope you find this data useful and there are no strings attached"
  Establishes: Damodaran sets no licence terms on his data.

- **Damodaran: acknowledgement optional**
  Damodaran, A.; NYU Stern School of Business; n.d. *Data history* (sections History & Philosophy and Usage Rules). https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html
  Stored: `sources/provenance/rights/damodaran_datahistory.html` (SHA-256 `6d8ccb3d77715d951c8fa1ccf76654396fbf4f4bbcf8cb87487ac26656bb04aa`); fetched 2026-10-21 (source vet; re-fetched byte-identical by its checker); Usage Rules, Acknowledgements.
  Quote: "If not, I will not lose any sleep"
  Establishes: Acknowledgement is welcome, not required; the post credits him anyway.

- **Damodaran: the public policy request**
  Damodaran, A.; NYU Stern School of Business; n.d. *Data history* (sections History & Philosophy and Usage Rules). https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html
  Stored: `sources/provenance/rights/damodaran_datahistory.html` (SHA-256 `6d8ccb3d77715d951c8fa1ccf76654396fbf4f4bbcf8cb87487ac26656bb04aa`); fetched 2026-10-21 (source vet; re-fetched byte-identical by its checker); Usage Rules, Public policy debates.
  Quote: "this data was never meant for public policy debates"
  Establishes: A request, not a licence term. The post argues about a public scheme, so the owner should weigh it (data-README says the same).

- **IMF: reuse permitted**
  International Monetary Fund; effective October 11, 2024. *IMF Copyright and Usage* (special terms for statistical data; browser-rendered section stored by Post 27). https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`); fetched 2026-10-17 (Post 27); Special terms for statistical data, opening sentence (Post 27 copy).
  Quote: "You may download, extract, copy, create derivative works, publish, distribute, and use Data obtained from IMF Sites"
  Establishes: IMF CPI data may be reused and transformed.

- **IMF: attribution required**
  International Monetary Fund; effective October 11, 2024. *IMF Copyright and Usage* (special terms for statistical data; browser-rendered section stored by Post 27). https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`); fetched 2026-10-17 (Post 27); First condition.
  Quote: "it must appear accurately with attribution to the IMF as the source"
  Establishes: Charts and notes must credit the IMF.

- **IMF: transformations must be stated**
  International Monetary Fund; effective October 11, 2024. *IMF Copyright and Usage* (special terms for statistical data; browser-rendered section stored by Post 27). https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` (SHA-256 `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a`); fetched 2026-10-17 (Post 27); Second condition.
  Quote: "If the Data is materially transformed by the User, this must be stated explicitly along with the required source citation."
  Establishes: Annual averages, inflation rates and real values are labelled the author's calculations.

- **IMF: language-model clause**
  International Monetary Fund; effective October 11, 2024. *IMF Copyright and Usage* (Prohibitions list; stored by Post 27). https://www.imf.org/en/about/copyright-and-terms
  Stored: `sources/provenance/imf/imf_copyright_and_terms_browser_llm_clause.txt` (SHA-256 `36a0859f5364b9f13ce65d6b272d55cd77345463e8e3c45a8b59dd9d4c345c92`); fetched 2026-10-17 (Post 27); Prohibitions list.
  Quote: "for the training of large language models (LLMs) without explicit permission"
  Establishes: Bars training on IMF content, not reading or quoting it.

- **IMF robots (archived copy)**
  Internet Archive capture (2026-09-15) of https://www.imf.org/robots.txt (the live host answers scripts with Akamai 403)
  Stored: `sources/provenance/robots/www.imf.org.wayback20260915.txt` (SHA-256 `c58f6dd5fdc0471b883844e048cb91cd3f9d9aa200861d8a883f9d3e2c164bbe`); fetched 2026-10-21 (source vet); robots.txt as captured 2026-09-15.
  Quote: "User-agent: * Disallow: /external/country/"
  Establishes: Only listed /external/ and other paths are disallowed; no Anthropic agent is named. The API host returned 502 for its robots file and data.imf.org's archived file allows all (next entry).

- **IMF data host robots (archived copy)**
  Internet Archive capture (2025-03-16) of https://data.imf.org/robots.txt
  Stored: `sources/provenance/robots/data.imf.org.wayback20250316.txt` (SHA-256 `9133ceedd6bece0761cc791489df7a3fdbfaaa32d6316d98b92e6f8ff76e397a`); fetched 2026-10-21 (source vet); robots.txt as captured 2025-03-16.
  Quote: "User-agent: * Disallow:"
  Establishes: Allows everything.

- **Vanguard workplace site robots**
  https://institutional.vanguard.com/robots.txt (serves the workplace.vanguard.com file)
  Stored: `sources/provenance/robots/workplace.vanguard.com.txt` (SHA-256 `fd0833682f1b57c1bf1b805058efd3b44bdff2126f8aeb33f5200893fe91e2c6`); fetched 2026-10-21 (source vet); robots.txt for workplace.vanguard.com.
  Quote: "# robots.txt for https://workplace.vanguard.com User-agent: *"
  Establishes: The '*' group disallows only stylesheet, image, script, unavailable-page and seven fact-sheet paths, none of them /content/dam/ (How America Saves) or /investment/ (glide-path page); no Anthropic agent is named.

- **Vanguard personal site robots**
  https://personal.vanguard.com/robots.txt
  Stored: `sources/provenance/robots/personal.vanguard.com.txt` (SHA-256 `c47befa7c174a485a302850f0b4c8923c657fba602c2586c499b247a14d34c67`); fetched 2026-10-21 (source vet); robots.txt for personal.vanguard.com.
  Quote: "# robots.txt for http://www.vanguard.com/ User-agent: *"
  Establishes: None of the listed Disallow paths covers /pub/Pdf/ (the prospectus); no Anthropic agent is named.

- **Vanguard terms: personal and noncommercial use**
  The Vanguard Group, Inc.; revised October 12, 2020. *Terms of Use*. https://corporate.vanguard.com/content/corporatesite/us/en/corp/terms-of-use.html
  Stored: `sources/provenance/rights/vanguard_terms_of_use.html` (SHA-256 `ed57ab205b36d4c4255681636e2e59bba4f5062a2b9a5b3aff69f01000a2ec79`); fetched 2026-10-21 (source vet); Terms of Use, licence clause.
  Quote: "solely for your personal and noncommercial use or as expressly authorized by Vanguard in writing"
  Establishes: The blog is non-commercial; the post cites Vanguard's facts (rates, percentages) with attribution and reproduces none of its charts or tables (design section 3).

- **IRS robots**
  https://www.irs.gov/robots.txt
  Stored: `sources/provenance/robots/www.irs.gov.txt` (SHA-256 `a847662017650507cb5ed22919ab668944eebb40abdd67da197a1bb3cf915b0b`); fetched 2026-10-21 (source vet); robots.txt, the only User-agent line.
  Quote: "User-agent: *"
  Establishes: One '*' group; its disallowed paths do not cover /retirement-plans/ or /taxtopics/; no Anthropic agent is named.

- **IRS: no copyright in federal content**
  Internal Revenue Service; n.d. *Use of content from IRS.gov*. https://www.irs.gov/about-irs/use-of-content-from-irsgov
  Stored: `sources/provenance/rights/irs_use_of_content.html` (SHA-256 `d0946716e5927bf9a3be656a394f4e6360fdf434f3bdaa3e9a071eb55974d14e`); fetched 2026-10-21 (source vet); Use of content from IRS.gov, copyright notice.
  Quote: "is not subject to copyright and may be freely copied. Credit is requested."
  Establishes: IRS pages may be quoted; credit the IRS.

- **DOL robots (archived copy)**
  Internet Archive capture (2026-05-16) of https://www.dol.gov/robots.txt (the live host answers scripts with Access Denied)
  Stored: `sources/provenance/robots/www.dol.gov.wayback20260516.txt` (SHA-256 `773fb8d35bb9a39d35335ee6db8dc5c912d2aacbfb823152d9c61cd647dd902d`); fetched 2026-10-21 (source vet); robots.txt as captured 2026-05-16.
  Quote: "User-agent: * # CSS, JS, Images"
  Establishes: One '*' group whose Disallows cover admin, search and user paths, not /sites/ or /agencies/; no Anthropic agent is named. The FAB PDF is an Internet Archive capture (references-draft.md).

- **DOL: public domain, no implied endorsement**
  U.S. Department of Labor; n.d. *Public Domain, Copyright, Trademark and Patent Information* (Internet Archive capture of 2026-10-19). https://www.dol.gov/general/aboutdol/copyright
  Stored: `sources/provenance/rights/dol_copyright.html` (SHA-256 `168bd96441dbadb6b6c03589305f5aa374d14b19f25b95d42bfbca10c3fbb8c5`); fetched 2026-10-21 (source vet); Public Domain page.
  Quote: "such materials may not be used in a manner that implies any affiliation or endorsement by the DOL"
  Establishes: DOL material is public domain; credit DOL and imply no endorsement.

- **BLS (check file only): public domain**
  U.S. Bureau of Labor Statistics; n.d. *BLS Copyright Information* (Internet Archive capture of 2026-10-17). https://www.bls.gov/opub/copyright-information.htm
  Stored: `sources/provenance/rights/bls_copyright.htm` (SHA-256 `93b73a7df1d66de966702f1ebe76ad42d3dcf5ca38741b4fcbf610f885021be2`); fetched 2026-10-21 (source vet); BLS Copyright Information.
  Quote: "You are free to use our public domain material without specific permission"
  Establishes: The BLS CPI-U file is used only to check the IMF series; BLS asks to be cited as the source.

- **data.gov.sg robots**
  https://data.gov.sg/robots.txt
  Stored: `sources/provenance/robots/data.gov.sg.txt` (SHA-256 `44f3f8eafdf064cf69acb05f23ee4dfc9ab5b3d67d81c64246bc29f7e438789a`); fetched 2026-10-21 (source vet; re-fetched identical by its checker); robots.txt, whole file.
  Quote: "User-agent: * Allow: /"
  Establishes: Allows everything; the API host has no robots file (next entry).

- **data.gov.sg API host: no robots file**
  https://api-production.data.gov.sg/robots.txt (JSON 404)
  Stored: `sources/provenance/robots/api-production.data.gov.sg.txt` (SHA-256 `13e90134f4419294d86340b489651b6f00100edccb2a4471a1aadbcc50953367`); fetched 2026-10-21 (source vet); Response to /robots.txt.
  Quote: "Resource not found."
  Establishes: No rules on the API hosts the CPF files came through (the vet's checker found api-open.data.gov.sg also answers 404 JSON).

- **Singapore Open Data Licence: use permitted**
  Government of Singapore (data.gov.sg); n.d. *Singapore Open Data Licence, version 1.0*. https://data.gov.sg/open-data-licence
  Stored: `sources/provenance/rights/datagovsg_open-data-licence.html` (SHA-256 `0c59cb5cf4fb97e38a8e1c5d0dd6f842ecf088ae51060aaa09aedbe6810c2926`); fetched 2026-10-21 (source vet); What you can do.
  Quote: "whether commercially or non-commercially"
  Establishes: The CPF datasets may be used, copied, modified and adapted.

- **Singapore Open Data Licence: attribution**
  Government of Singapore (data.gov.sg); n.d. *Singapore Open Data Licence, version 1.0*. https://data.gov.sg/open-data-licence
  Stored: `sources/provenance/rights/datagovsg_open-data-licence.html` (SHA-256 `0c59cb5cf4fb97e38a8e1c5d0dd6f842ecf088ae51060aaa09aedbe6810c2926`); fetched 2026-10-21 (source vet); Additional conditions, Attribution.
  Quote: "a conspicuous notice acknowledging the source of the datasets and including a link to the most recent version of this Licence"
  Establishes: The notice in data-README's form must appear with any chart or figure from the CPF datasets.

- **Singapore Open Data Licence: no implied endorsement**
  Government of Singapore (data.gov.sg); n.d. *Singapore Open Data Licence, version 1.0*. https://data.gov.sg/open-data-licence
  Stored: `sources/provenance/rights/datagovsg_open-data-licence.html` (SHA-256 `0c59cb5cf4fb97e38a8e1c5d0dd6f842ecf088ae51060aaa09aedbe6810c2926`); fetched 2026-10-21 (source vet); Limitations.
  Quote: "You must not use the datasets in a way that suggests any official status"
  Establishes: The post must not suggest that CPF Board or the Singapore Government endorses it.

- **ILO site robots**
  https://www.ilo.org/robots.txt
  Stored: `sources/provenance/robots/www.ilo.org.txt` (SHA-256 `7b3366a38b51ccd03706a0e2be961a22d51069f784bc8429f4cf51cc3a387c7a`); fetched 2026-10-22T14:09Z by this audit; robots.txt, '*' group, Content-Signal line (the same group sets Crawl-delay: 10).
  Quote: "Content-Signal: search=yes,ai-input=yes,ai-train=no,use=reference"
  Establishes: www.ilo.org names no Anthropic agent; its content signal allows AI input and reference use and refuses training, and the same group sets a 10-second crawl delay. This audit made one request to www.ilo.org after reading the robots file (the ICSE-93 resolution), minutes later. sdmx.ilo.org answered HTTP 404 with an empty body for its robots file on 2026-10-22, so it sets no rules.

- **ILOSTAT front end robots (archived copy)**
  Internet Archive capture (2026-10-12) of https://ilostat.ilo.org/robots.txt (the live host serves a bot challenge)
  Stored: `sources/provenance/robots/ilostat.ilo.org.wayback20261012.txt` (SHA-256 `390c43c6812e8ebd45cf41567da101f30f47d7b862423042c7e310278b0ad9eb`); fetched 2026-10-21 (source vet); robots.txt as captured 2026-10-12.
  Quote: "User-agent: * Disallow:"
  Establishes: Allows everything; the live front end serves a bot challenge, which neither the vet nor the build tried to pass.

- **ILO: datasets under CC BY 4.0**
  International Labour Organization; n.d. *Rights and permissions*. https://www.ilo.org/rights-and-permissions
  Stored: `sources/provenance/rights/ilo_rights_permissions.html` (SHA-256 `69d01e6ce11e855f67ed1261774e46d7cb2a0f8eaeb6ae198b2e77107f2a5a64`); fetched 2026-10-21 (source vet; re-fetched by its checker); Rights and permissions, Data, 'Published as of 3 May 2023'.
  Quote: "As of 3 May 2023, databases and datasets together with the accompanying referential metadata are covered by the Creative Commons CC BY 4.0 licence."
  Establishes: The Nov. 2025 modelled estimates and their SDMX metadata are CC BY 4.0: credit the ILO. The ICSE-93 resolution (1993) predates the policy, so it is cited and briefly quoted, not reproduced.

- **Bank Indonesia's data policy: name Bank Indonesia as the source**
  Bank Indonesia; ditetapkan 31 December 2024. *Peraturan Bank Indonesia Nomor 12 Tahun 2024 tentang kebijakan data dan informasi Bank Indonesia*. https://www.bi.go.id/id/publikasi/peraturan/Pages/PBI_122024.aspx
  Stored: `sources/provenance/rights/bi_pbi_12_2024_data_policy.pdf` (SHA-256 `0053dd26eafa80893ef67875b6f1af8702e3fa11d9f99875557d54cd19f263ee`); stored by Post 27 on 2026-10-16 (file date; its audit records no fetch note); copied unchanged 2026-10-22 (Task D); PDF page 6, Pasal 21 ayat (4).
  Quote: "Pihak eksternal yang menggunakan Data dan Informasi sebagaimana dimaksud pada ayat (3) harus mencantumkan Bank Indonesia sebagai sumber materi"
  Establishes: External users of the data and information Bank Indonesia disseminates (ayat (3): through channels open to the public, or on request) must name Bank Indonesia as the source. This is Post 27's rights basis for its Bank Indonesia data, adapted: the Data Inflasi file is credited to Bank Indonesia, with BPS as the compiler (section F). The file was downloaded by hand from bi.go.id, not crawled.

## L. What could not be defined from a primary document

- **PERDIR/143/102015**, the Board regulation under which the 2015 to 2020 rates were computed, is not stored and
  was not found; it is known only through the audited notes (IR 2015 p.315, IR 2018 pp.470 and 501).
- **Peraturan BPJS 4/2015** has no text layer. Its provisions are transcribed from page renders, not quote-checked.
- **A legal floor before 1 July 2015.** No stored document states one for 2005 to mid-2015.
- **The base of the 2009 incentive (1.60%)** and **of the 2013 one-off payouts (6.50%, 0.81%)**. The documents give
  the rates and amounts, not the balance; the March 2013 amount does not fit the opening 2013 balance (section C).
- **Day weighting versus R2.** The documents define the 2008 on-line and 2010 to 2013 crediting as day-weighted;
  no document gives a JHT-wide figure showing how far the half-year rule departs from it.
- **The 2016 to 2020 base rates as audited figures.** They come from management discussion and narrative; the
  2018 audited notes give only monthly claim rates, and 2016, 2017, 2019 and 2020 have no text-layer audited JHT
  notes. The 2016 and 2015 figures are corroborated by BPJS's image-only 2016 summary.
- **2020's 5.59% as the credited rate.** The only text-layer sentence calls it the lowest yield set by the Agency;
  the same wording in 2021 to 2025 names the lowest program yield, and 5.59% matches no 2020 table value. It stays
  an inference (manifest note).
- **The credited rate for 2021 to 2025.** BPJS has not published it (vet and gap search).
- **What the published JHT yield measures.** No document defines its denominator, whether unrealized gains count,
  or whether 2015 to 2022 are gross or net. 2017 has no yield in any stored text-layer document.
- **The US CPI's compiler in IMF metadata.** No stored IMF document names BLS for the US series; the link rests on
  the build's ratio check (data-README).
- **Historical Target Retirement expense ratios for 2005 to 2020.** Only the January 2026 prospectus is stored.
- **What the JHT annual statement shows** (whether it states the year's credited rate). PP 46/2015 Pasal 22(7)
  requires yearly balance information, but no document shows the statement; the app needs a login (vet).
- **A JHT-specific active-member count for years other than end-2024 in text form.** End-2025 exists only as an
  image (vet); the post uses end-2024 (sources.json).

## M. Copies made into this post folder

Every file this audit relies on that was first stored outside the post folder, copied in on 2026-10-22 by Task D with its SHA-256 checked before and after copying (`post28-build/fix-D/scripts/copy_files.py`, which read each expected hash from this section's earlier table, Post 27's FILES table or Post 27's audit). `SCRATCH` is the session scratchpad, `/private/tmp/claude-501/-Users-jonathanchrisnaldy-Claude-Workspace/7a1b9d4a-a613-4eb1-a1d2-f4d11a2b1ecc/scratchpad`, which is not durable; `../msci-fear-chain/` is Post 27's folder. The entries above cite the copies only.

| Copied from | Now at | SHA-256 (checked after copying) |
|---|---|---|
| `SCRATCH/post28-vet/jht/regs/Peraturan_BPJS_Ketenagakerjaan_Nomor_3_Tahun_2020_tentang_Mekanisme_Penetapan_dan_Distribusi_Hasil_Pengembangan_Dana_JHT.pdf` | `sources/provenance/rules/peraturan_bpjs_3_2020.pdf` | `3c32dc964061aacb32127d08319b1769e348b8bbd4e7aad390a34b9570073d7a` |
| `SCRATCH/post28-vet/jht/regs/05022016_110020_PER_BPJSTK_NOMOR_04_TAHUN_2015.pdf` | `sources/provenance/rules/peraturan_bpjs_4_2015.pdf` | `b682477a437148f3309439f73fe16996e3cd461324ed92f237546272f4aaeb4a` |
| `SCRATCH/post28-gap/jamsostek/bpjs/img/LK_2016.png` | `sources/provenance/jht/lk_2016_summary.png` | `cedcab52bf88021340ada64d19a8198498ba326bf763f7f4dd6271d25599dc2a` |
| `SCRATCH/post28-vet/us/damodaran/histretSP.html` | `sources/provenance/us/damodaran_histretSP.html` | `127c772f0fea8763391dbf2c1c7d3ecd3a07ca2b23f81ab47af58b529e2b5647` |
| `SCRATCH/post28-vet/us/damodaran/page_datahistory.html` | `sources/provenance/rights/damodaran_datahistory.html` | `6d8ccb3d77715d951c8fa1ccf76654396fbf4f4bbcf8cb87487ac26656bb04aa` |
| `../msci-fear-chain/sources/provenance/imf/imf_api_cpi_codes_extract.txt` | `sources/provenance/imf/imf_api_cpi_codes_extract.txt` | `3292b9253cd4dcbd432ffcb44d6fa1176b35eac40442107c7172cc0a8a5618c0` |
| `../msci-fear-chain/sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` | `sources/provenance/imf/imf_dsbb_idn_cpi_dqaf.json.txt` | `3489b63a139e345c8a5a3bd5cd35bd01d730aaccde579714d39741fc6b6121f4` |
| `../msci-fear-chain/sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` | `sources/provenance/imf/imf_copyright_and_terms_browser_data_section.txt` | `ada830edad348b1a378c2d22b73670108aa603ea0b8263c0460e1ffbc746430a` |
| `../msci-fear-chain/sources/provenance/imf/imf_copyright_and_terms_browser_llm_clause.txt` | `sources/provenance/imf/imf_copyright_and_terms_browser_llm_clause.txt` | `36a0859f5364b9f13ce65d6b272d55cd77345463e8e3c45a8b59dd9d4c345c92` |
| `SCRATCH/post28-vet/us/bls/historical-cpi-u-202512.xlsx` | `sources/provenance/us/bls_historical-cpi-u-202512.xlsx` | `1010f74a32661f1fc70aba1871efc202ae8e7865e4776e7f894384128a12e954` |
| `SCRATCH/post28-vet/us/vanguard/corp_terms.html` | `sources/provenance/rights/vanguard_terms_of_use.html` | `ed57ab205b36d4c4255681636e2e59bba4f5062a2b9a5b3aff69f01000a2ec79` |
| `SCRATCH/post28-vet/neighbours/datagovsg/meta_d_98ffa142ae0dec40391f78f81d26aca9.json` | `sources/provenance/cpf/meta_d_98ffa142ae0dec40391f78f81d26aca9.json` | `26daef4b772c35797bb6148e33bcacfbf2494df087c419644e9e97d62821540b` |
| `SCRATCH/post28-vet/neighbours/datagovsg/meta_d_97ec9a2ce15cbf253128e48779a3fba0.json` | `sources/provenance/cpf/meta_d_97ec9a2ce15cbf253128e48779a3fba0.json` | `5ec6b51629e066aaceb5f585718d50e3202b18d89bde839f85c4608240a0ed00` |
| `SCRATCH/post28-vet/neighbours/datagovsg/datagovsg_open-data-licence.html` | `sources/provenance/rights/datagovsg_open-data-licence.html` | `0c59cb5cf4fb97e38a8e1c5d0dd6f842ecf088ae51060aaa09aedbe6810c2926` |
| `SCRATCH/post28-vet/us/irs/use-of-content.html` | `sources/provenance/rights/irs_use_of_content.html` | `d0946716e5927bf9a3be656a394f4e6360fdf434f3bdaa3e9a071eb55974d14e` |
| `SCRATCH/post28-vet/us/dol/dol-copyright.html` | `sources/provenance/rights/dol_copyright.html` | `168bd96441dbadb6b6c03589305f5aa374d14b19f25b95d42bfbca10c3fbb8c5` |
| `SCRATCH/post28-vet/us/bls/bls-copyright.htm` | `sources/provenance/rights/bls_copyright.htm` | `93b73a7df1d66de966702f1ebe76ad42d3dcf5ca38741b4fcbf610f885021be2` |
| `SCRATCH/post28-build/prov/fetch/ilo/df_emp_2emp.xml` | `sources/provenance/ilo/dataflow_DF_EMP_2EMP_SEX_STE_NB.xml` | `463ed53262c5c2cc8e11b929d3b8cf55080b909f15de10999f64380e605749ab` |
| `SCRATCH/post28-build/prov/fetch/ilo/icse93_wcms_087562.pdf` | `sources/provenance/ilo/icse93_resolution.pdf` | `06ce8eb42b3d1ad79a0507d630ab6ee61e7a61b0d794ea04e04f32686cbd5157` |
| `SCRATCH/post28-vet/awareness/ilo/ilo_rights_permissions.html` | `sources/provenance/rights/ilo_rights_permissions.html` | `69d01e6ce11e855f67ed1261774e46d7cb2a0f8eaeb6ae198b2e77107f2a5a64` |
| `SCRATCH/post28-vet/jht/law/Anotasi_185_UU_28_2014_Hak_Cipta.pdf` | `sources/provenance/rights/uu_28_2014_anotasi_2025.pdf` | `6fada279bc2688b76ef52acb35bc73d4f4bf5360261692a81c777eb9ba3bc3ed` |
| `SCRATCH/post28-vet/jht/raw/kemdet_622.html` | `sources/provenance/rights/jdih_kemnaker_detail_622.html` | `636fa19b475a74ea98c0b929144c058d87afea8f9e37731b900e9cc011ab6eb1` |
| `SCRATCH/post28-vet/jht/robots/www.bpjsketenagakerjaan.go.id.txt` | `sources/provenance/robots/www.bpjsketenagakerjaan.go.id.txt` | `8ddd4eb2b36e0c6269ef1d83f5c8d6db4e4649a6041b4b7e5a5f2dcefaad5f65` |
| `SCRATCH/post28-vet/jht/robots/jdih.kemnaker.go.id.txt` | `sources/provenance/robots/jdih.kemnaker.go.id.txt` | `16ceb5ee3e0dc13aa9adf31a3ebbe45a1d965b8c2b9f72eaf84e5911e140ed95` |
| `SCRATCH/post28-vet/jht/robots/s.mkri.id.txt` | `sources/provenance/robots/s.mkri.id.txt` | `c00c30db3392bdf92714f71e661e312ee9d5542e015e3c56a9b30bda5a83400e` |
| `SCRATCH/post28-vet/jht/robots/web.archive.org.txt` | `sources/provenance/robots/web.archive.org.txt` | `d465172175d35d493fb1633e237700022bd849fa123164790b168b8318acb090` |
| `SCRATCH/post28-vet/jht/robots/archive.org.txt` | `sources/provenance/robots/archive.org.txt` | `83e00f46c71e9fa872694af73fa9c15a615b9052b2f10820a3d146bc506c6161` |
| `SCRATCH/post28-vet/us/robots/pages.stern.nyu.edu.txt` | `sources/provenance/robots/pages.stern.nyu.edu.txt` | `b6c31d61cdbe840d46c0f8b71cdebdc404cd5f282c689acdb681c72ccb4af01d` |
| `SCRATCH/post28-vet/us/robots/institutional.vanguard.com.txt` | `sources/provenance/robots/workplace.vanguard.com.txt` | `fd0833682f1b57c1bf1b805058efd3b44bdff2126f8aeb33f5200893fe91e2c6` |
| `SCRATCH/post28-vet/us/robots/personal.vanguard.com.txt` | `sources/provenance/robots/personal.vanguard.com.txt` | `c47befa7c174a485a302850f0b4c8923c657fba602c2586c499b247a14d34c67` |
| `SCRATCH/post28-vet/us/robots/www.irs.gov.txt` | `sources/provenance/robots/www.irs.gov.txt` | `a847662017650507cb5ed22919ab668944eebb40abdd67da197a1bb3cf915b0b` |
| `SCRATCH/post28-vet/us/robots/wb_dol.txt` | `sources/provenance/robots/www.dol.gov.wayback20260516.txt` | `773fb8d35bb9a39d35335ee6db8dc5c912d2aacbfb823152d9c61cd647dd902d` |
| `SCRATCH/post28-vet/neighbours/robots/www.imf.org.wayback20260915.txt` | `sources/provenance/robots/www.imf.org.wayback20260915.txt` | `c58f6dd5fdc0471b883844e048cb91cd3f9d9aa200861d8a883f9d3e2c164bbe` |
| `SCRATCH/post28-vet/neighbours/robots/data.imf.org.wayback20250316.txt` | `sources/provenance/robots/data.imf.org.wayback20250316.txt` | `9133ceedd6bece0761cc791489df7a3fdbfaaa32d6316d98b92e6f8ff76e397a` |
| `SCRATCH/post28-vet/neighbours/robots/data.gov.sg.robots.txt` | `sources/provenance/robots/data.gov.sg.txt` | `44f3f8eafdf064cf69acb05f23ee4dfc9ab5b3d67d81c64246bc29f7e438789a` |
| `SCRATCH/post28-vet/neighbours/robots/api-production.data.gov.sg.robots.txt` | `sources/provenance/robots/api-production.data.gov.sg.txt` | `13e90134f4419294d86340b489651b6f00100edccb2a4471a1aadbcc50953367` |
| `SCRATCH/post28-build/prov/fetch/ilo/robots_www.ilo.org.txt` | `sources/provenance/robots/www.ilo.org.txt` | `7b3366a38b51ccd03706a0e2be961a22d51069f784bc8429f4cf51cc3a387c7a` |
| `SCRATCH/post28-vet/awareness/robots/ilostat.ilo.org.wayback20261012.txt` | `sources/provenance/robots/ilostat.ilo.org.wayback20261012.txt` | `390c43c6812e8ebd45cf41567da101f30f47d7b862423042c7e310278b0ad9eb` |
| `../msci-fear-chain/data/Data Inflasi.xlsx` | `data/bi_data_inflasi.xlsx` | `5c79086509b6c19f90c5e3e835c5dcc40a02d322087d94e1c2a30a17e0280217` |
| `../msci-fear-chain/sources/provenance/ojk-bps/bi_inflasi_definisi.txt` | `sources/provenance/bi/bi_inflasi_definisi.txt` | `97fb182a8cd9af90afa930d82a570a6855aabc41371264d4a300c482f942c292` |
| `../msci-fear-chain/sources/bi_pbi_12_2024_data_policy.pdf` | `sources/provenance/rights/bi_pbi_12_2024_data_policy.pdf` | `0053dd26eafa80893ef67875b6f1af8702e3fa11d9f99875557d54cd19f263ee` |
