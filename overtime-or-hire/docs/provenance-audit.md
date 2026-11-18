# Provenance audit: Post 32 (overtime-or-hire)

Every variable the post leans on and every external figure it states, with the defining document, its page and
the verbatim quote. The documents are stored under `sources/` (gitignored), each in its own folder; `store_text.py`
writes the text copies, and `docs/sources.json` pins each copy's sha256 and holds the quotes the gate checks. A page
is the page of the stored PDF unless a printed page is named. A data file's label is not a definition: each
variable below is defined by its codebook or lexicon entry.

## 1. The survey: American Time Use Survey, 2003-24 activity summary file (U.S. Bureau of Labor Statistics)

The data file is `atussum_0324.dat` inside `atussum-0324.zip`; `docs/data-README.src.md` says where it comes from.

| Variable | Document, page | Verbatim quote |
|---|---|---|
| one row per respondent | `Sum0324_info.txt` (in the zip) | "Each record corresponds to a unique respondent, as indicated by a unique value of the variable TUCASEID." |
| activity columns | `Sum0324_info.txt` | "contains data for the total number of minutes that each respondent spent doing each 6-digit activity" |
| TELFS | data dictionary (`atusintcodebk0324.pdf`), page 19 | "TELFS Edited: labor force status"; value "1 Employed - at work" |
| TEHRUSLT | data dictionary, page 17 | "Edited: total hours usually worked per week (sum of TEHRUSL1 and TEHRUSL2)"; universe "TELFS = 1 or 2"; "-4 (Hours vary) is also valid for TEHRUSLT" |
| TEAGE | data dictionary, page 12 | "TEAGE Edited: age" |
| TUFNWGTP | data dictionary, page 44 | "ATUS final weight"; "Cases with [TUYEAR = 2020] will have missing values for TUFNWGTP." |
| TU20FWGT | data dictionary, page 39 | "ATUS final weight for 2020 data"; "researchers need to use the weighting variable TU20FWGT instead of TUFNWGTP" |
| TUDIARYDAY | data dictionary, page 42 | "Day of the week of diary day"; values "1 Sunday" to "7 Saturday" |
| TRHOLIDAY | data dictionary, page 26 | "Flag to indicate if diary day was a holiday"; "1 Diary day was a holiday" |
| sleep | coding lexicon (`lexiconnoex0324.pdf`), page 2 | "0101 Sleeping": "010101 Sleeping", "010102 Sleeplessness", "010199 Sleeping, n.e.c.*" |
| sports, exercise and recreation | coding lexicon, page 8 | "1301 Participating in Sports, Exercise, and Recreation" (codes 130101 to 130136 and 130199) |

What the lexicon's category 1301 holds matters for the wording: it includes "130112 Fishing" and "130118 Hunting"
(page 8), and golfing, billiards, bowling and boating. It counts taking part, not watching: attending events is
code 1302, which the post does not count. The post calls it taking part in sports, exercise and recreation, or sports,
exercise and recreation for short, and never calls it exercise alone.

The sleep codes are the survey's own category 0101, so sleep time includes time recorded as sleeplessness (010102). The
published figure the build script reproduces before any band is built: `atus2024_sleep` in `docs/sources.json`
(the 2024 release, page 9, Table 1, row Sleeping, average hours per day, civilian population, total).

## 2. Employer costs: Employer Costs for Employee Compensation, June 2026 (U.S. Bureau of Labor Statistics)

- Unit (technical note, web page): "provides the average employer cost for wages and salaries as well as benefits per
  hour worked".
- Group: full-time private industry workers. Figures: `ecec_ft_total`, `ecec_ft_wages`, `ecec_ft_benefits`.
- The release does not say which costs scale with hours worked and which come per person. That split is a model
  assumption, named in `build_analysis.py`.

## 3. The US overtime rule: Fair Labor Standards Act (U.S. Department of Labor, Wage and Hour Division)

- `fs23_overtime` (Fact Sheet #23): overtime pay is due for hours over 40 in a workweek "at a rate not less than time
  and one-half their regular rates of pay". The rate is written in words, so the gate cannot bind it as a number:
  `build_analysis.py` holds the overtime rate beside these words and stops if they leave the `fs23_overtime` quote in
  `docs/sources.json`; the gate checks that quote against the stored copy.
- `fs23_no_limit` (Fact Sheet #23): the Act sets no limit on weekly hours for employees aged 16 and older.
- Exempt employees: `fs17a_salary` (Fact Sheet #17A) and, on the same page, "Job titles do not determine exempt
  status". The regulation behind it is stored as `sources/ecfr-29-541/` (29 CFR part 541; section 541.600 sets the
  salary level, "not less than $684 per week").

## 4. Output and weekly hours: Pencavel (2014), IZA Discussion Paper 8129

- Data: page 3, "Observations on munition workers, most of them women"; page 6, "the First World War, the Great War";
  page 40, Table 4 is "Fitted to All 122 Weekly Observations".
- Findings bound in `docs/sources.json`: `pencavel_knot` (output proportional to hours below 49 weekly hours),
  `pencavel_peak` (output peaks at about 63 hours) and `pencavel_56_70`, all on page 18 (printed page 15).
- Page 40, Table 4: column (ii), linear below 49 hours and quadratic above, has "b2 113.617 126.089 144.192" and
  "c2 -3.920 -4.533 -3.709" (columns i, ii, iii) and "H xmax 63 63 68". Column (iii) adds a Sunday variable and
  peaks at 68 hours.
- How the post uses it: in column (ii) the slopes below and above the knot are equal, so the output from one more
  hour stays constant up to 49 hours and then falls in a straight line, reaching zero at the peak. Column (ii)
  puts that peak at 49 plus 126.089 divided by twice 4.533, or 62.9 hours, which the paper rounds to about 63;
  `build_analysis.py` uses the two quoted values, 49 and 63. The curve describes British munition workers a century
  ago: the post uses it as a stated assumption, never as a measurement of office work.

## 5. Team productivity in a modern firm: Shangguan, DeVaro and Owan (2021), RIETI Discussion Paper 21-E-040

- Setting (abstract, page 2): "using single-firm Japanese data on construction design projects".
- Finding (abstract, page 2): larger teams have lower average productivity because "weaker workers join teams when
  more hours are needed than the top performers can handle". This bears on the merit assumption of the cost test.
- Figure: `rieti_productivity`, page 5.

## 6. What insufficient sleep costs: Hafner et al. (2016), RAND

- Data (page 28): "Our empirical analysis is based on data acquired from the 'Britain's Healthiest Workplace' (BHW)
  competition". The productivity losses per worker are estimated on employees in Britain; the U.S. figures come from
  RAND's model, which applies them to the U.S. working population. The post says so.
- Sleep measure (page 29): "Information on self-reported sleep duration is derived from the survey question".
- Figures: `rand_loss`, `rand_es2_us` (Table ES.2: scenarios 1 to 3; scenario 2 is the lowest) and `rand_worker`.
  The report's count of working days lost in the U.S. (page 12) is not used: by the method in the note to its
  Table ES.1, its own inputs give a figure about 225 times larger.
- The report gives a figure per worker (`rand_worker`), but by band of usual sleep from a survey question. The time-use
  diary measures sleep differently, so the post cannot place its hours bands in those sleep bands: the figure stays in
  the sleep section and out of the cost test.

## 7. What replacing an employee costs: Boushey and Glynn (2012), Center for American Progress

- `cap_cases`, `cap_turnover`: the typical (median) cost of turnover across 27 case studies, as a share of annual
  salary. It is a cost of replacing an employee, not of adding one. `build_analysis.py` uses it as a benchmark: a
  hiring cost of that size (`costs.hiring_cost`) and the weeks the third hire takes to repay it (`nonexempt`), and the
  post calls it the cost of replacing an employee.

## 8. Indonesia: Undang-Undang Nomor 27 Tahun 2026 tentang Pelindungan Ketenagakerjaan

- In force (page 127, Pasal 313): "Undang-Undang ini mulai berlaku pada tanggal diundangkan"; page 128, "Diundangkan di
  Jakarta pada tanggal 28 Oktober 2O26" (the text layer reads the year's zero as a letter O; the page image reads 2026).
- Older implementing regulations (page 127, Pasal 310) remain in force where they do not conflict: "dinyatakan masih
  tetap berlaku sepanjang tidak bertentangan dengan ketentuan dalam Undang-Undang ini".
- Figures: `uu27_hours` (Pasal 115 ayat (2) huruf b, page 50), `uu27_overtime_cap` (Pasal 116 ayat (1) huruf c,
  page 51), `uu27_overtime_pay` (Pasal 116 ayat (2), page 51).
- The first overtime hour is counted once per workday: the elucidation of Pasal 116 ayat (1) huruf c (page 153) defines
  overtime for a five-day week as work beyond "8 (delapan) jam dalam 1 (satu) Hari", and Pasal 116 ayat (2) prices
  the first overtime hour and each later one.
- The design named Government Regulation 35 of 2021. The law has the same caps and rates: the regulation's Pasal 26
  (page 17), "Waktu Kerja Lembur hanya dapat dilakukan paling lama 4 (empat)jam dalam 1 (satu) hari dan 18 (delapan
  belas) jam dalam 1 (satu) minggu", and Pasal 31 (page 19), "1,5 (satu koma lima) kali Upah sejam" for the first
  hour. The post cites the law in force.
