# Data for Post 25

Nothing in this folder is committed. Everything below is public and free, and none of it needs a
login or an API key.

| File | Source | How |
|---|---|---|
| `wb_gdp_2023.json` | World Bank, GDP per capita, PPP, constant 2021 international dollars | `api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?date=2023&format=json&per_page=400` |
| `cckp_tas.json` | World Bank Climate Change Knowledge Portal, ERA5 near-surface air temperature, annual mean 1991 to 2020 | the exact request is recorded as `CCKP_REQUEST` in `build_analysis.py`; the portal's own download page 403s to curl, so use the API host |
| `ajr_t3/maketable3.dta` | Acemoglu, Johnson and Robinson (2002) replication files, Table 3: urbanisation in 1500 | the first author's MIT data archive, "Reversal of Fortune" section |
| `ajr_t5/maketable5.dta` | Same archive, Table 5: population density in 1500, 1995 income, the ex-colony classification | as above |

The AJR archive serves Dropbox links; substitute `dl.dropboxusercontent.com` for `www.dropbox.com`
to fetch them without a browser. The URL printed inside AJR's own shipped readme is now 410 Gone.

## Traps hit while building this

1. **Read the paper, not the variable label.** `lland15` is labelled "log land area in 1500". The
   paper defines the density denominator as **arable** land three times (p. 1243, the note to
   Table V, and Appendix 2, which names the variable "log arable land in 1500"). A fact-check round
   rewrote "arable" out of the post on the strength of the label and a later round had to put it
   back. The shipped variable is not fully consistent with the paper either: `exp(lland15)` equals
   known total land area to within two percent for the United States, India and Brazil, while
   desert states are cut hard (Egypt 0.040). Definition is the authors', measure is looser.
2. **The same files carry junk rows.** Both `.dta` files hold 120 rows with an empty-string country
   code and 33 more whose code is a US state abbreviation, a bare `.`, or the literal
   `notIndonesia`. None carries an analysis value except `ex2col = 0` on the `.` row, which sat in
   the never-colonised group as a phantom member until an ISO3 filter was added.
3. **Duplicate country rows.** DEU, ZWE and YUG appear twice. For Germany and Zimbabwe the first row
   carries latitude but neither density nor income, so a naive `drop_duplicates()` silently deletes
   them from every correlation that needs either. Keep the most-populated row.
4. **`temp1` through `temp5` are withdrawn.** They are documented (Appendix 2, sourced to Parker
   1997) but they fail a sanity check as country annual means: the United States reads 27 degrees
   and Greenland 26, and they correlate at only 0.58 with ERA5 over 200 matched countries. All
   temperature in this post is ERA5.
5. **`ex2col == 0` does not mean "never colonised".** It means "absent from AJR's list", and the
   residual contains Bermuda, the Cayman Islands, Puerto Rico, Aruba and Cambodia. The post says so.

## Reproducing

```bash
python3 build_analysis.py   # writes results.json
python3 make_charts.py      # writes charts/rf-1..4.png
python3 check.py            # the gate: 10 deterministic checks, must pass before publishing
python3 checks/test_gate.py # asserts the gate still catches real historical defects
```
