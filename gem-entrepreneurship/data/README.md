# Data

Three sources, all public, none redistributed here. Everything below reproduces from scratch.

## 1. GEM Adult Population Survey (the survey under examination)

**Global Entrepreneurship Monitor**, the longest-running cross-national survey of entrepreneurial
activity, run since 1999 by a consortium of national teams. Site: [gemconsortium.org](https://www.gemconsortium.org/data).

GEM publishes both national-level aggregates and **individual-level microdata**, on a deliberate
three-year lag, so 2022 is the newest round available. That openness is the reason this analysis was
possible at all: the composition tests in `build_analysis.py` need respondent-level records, and most
survey programmes never release them.

### Download route (undocumented, so recorded here)

The download buttons on the data-sets page carry a `file="NNNNN"` attribute and resolve to:

```bash
curl -sL -A "Mozilla/5.0" -H "Referer: https://www.gemconsortium.org/data/sets?id=aps" \
     -o out.zip "https://www.gemconsortium.org/file/open?fileId=51007"
```

File ids used here, all read off `https://www.gemconsortium.org/data/sets?id=aps`:

| Year | National | Individual |
|---|---|---|
| 2013 | 48743 | 50442 |
| 2014 | 48910 | 49485 |
| 2015 | 49474 | 49815 |
| 2016 | 49619 | 50016 |
| 2017 | 50019 | 50215 |
| 2018 | 50111 | 50444 |
| 2019 | 50304 | 50676 |
| 2020 | 50617 | 50903 |
| 2021 | 50750 | 51144 |
| 2022 | 51007 | 51376 |

Individual-level files used here: 2013, 2016, 2018, 2020 and 2022. The others are national only.

Expected layout: `data/national/<year>/….sav` and `data/individual/`.

### Gotchas

- Some "zip" downloads are **raw `.sav` files** with a `.zip` name (2011 to 2013 national). Check
  with `file` before unzipping.
- The **2013 individual file uses Deflate64**, which neither Python's `zipfile` nor macOS `ditto`
  can read. Install `zipfile-deflate64` and extract with that. It expands to **4.39 GB**.
- Files are SPSS `.sav`; read with `pyreadstat.read_sav`.
- Column names carry the two-digit year (`TEA13` … `TEA22`), so nothing can be hardcoded.
- Pre-2013 national files have a numeric `country` column and no `country_name`. Note also that
  `country` (numeric code) and `country_name` both exist in later files; matching on `country` by
  accident silently yields zero rows.
- **Indonesia's continuous participation runs from 2013, with no round in 2019 or 2021.** There is
  also an isolated earlier Indonesian round in 2006, unused here because 2007 to 2012 are missing.
- The 2018 individual file needs `encoding="latin1"`; pyreadstat's default fails on it.
- **Interview mode is not recorded** in the 2013 or 2022 individual files, so it cannot be tested.

## 2. Indonesia's own labour force survey (the benchmark)

**ILOSTAT** `EMP_TEMP_SEX_STE_NB_A`, employment by sex and status in employment, source `BA:510`,
which is Indonesia's **Sakernas** labour force survey. This is directly collected national data.

```bash
curl -sL "https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_STE_NB_A&ref_area=IDN\
&timefrom=2012&timeto=2023&format=.csv&channel=ilostat" -o ilo_idn.csv
```

ICSE-93 codes: `1` employees, `2` employers, `3` own-account workers, `5` contributing family
workers. GEM's established-ownership question asks about **owning and managing** a business, so the
like-for-like Sakernas cut is **employers plus own-account workers**, excluding contributing family
workers.

**Why not the World Bank headline series.** `SL.EMP.SELF.ZS` is a *modelled* ILO estimate. A flat
modelled series would prove nothing about reality, so the Indonesia claim rests on the direct
Sakernas figures above. The modelled series is used only for the cross-country panel, where a
consistent definition across 100+ economies matters more and no single-country claim is made.

## 3. World Bank

```bash
curl -s "https://api.worldbank.org/v2/country/all/indicator/SL.EMP.SELF.ZS?format=json\
&per_page=20000&date=2013:2022" -o wb_self.json        # cross-country comparison
curl -s "https://api.worldbank.org/v2/country/IDN/indicator/SP.POP.1564.TO?format=json\
&per_page=60&date=2013:2022" -o pop_1564.json          # the shared denominator
```

Save as `data/wb_selfemp.csv` (flattened to `iso3,name,year,self_emp`) and `data/pop_1564.json`
(a plain `{year: value}` map).

## What the vet found

GEM passed every authenticity check: real national teams, plausible values, real country names,
World Bank income groups, no reconstructable outcomes, no frozen columns. It is a serious instrument
and this post is not a claim otherwise.

What it did not pass is external validation for **Indonesia specifically**. Between 2013 and 2022
GEM records Indonesian established business ownership falling 21.2% to 5.7% of the 18 to 64 population,
while Sakernas records employers plus own-account workers **rising** from 43.0 to 53.6 million
people, 25.2% to 28.3% of the same population. The two sources sit 4.0 points apart in 2013 and 22.6
points apart in 2022. Sample size, sample composition and survey weighting were each tested and none
explains it. The cause remains unidentified, which the essay states plainly.

## The variables that matter

| Variable | Meaning |
|---|---|
| `ownmge` | The screening question Q2A: "are you, alone or with others, currently the owner of a business you help manage, self-employed, or selling any goods or services to others?" |
| `ESTBBUSO` | "Manages and owns a business that is older than 42 months". The published established-ownership measure. Its weighted mean reproduces `Estbbu<yy>` exactly. |
| `ESTBBUS1` | "Value ESTBBUSO **before** reclassification". NOT the published measure. An earlier version of this analysis used it and got 3.49% for 2022 instead of 5.69%. |
| `omyr5job` | The year the business first paid the owner. Without it the 42-month rule cannot be applied, so the respondent cannot be classed as established. |

Note also that GEM spells four economies two ways (USA/United States, Korea/South Korea,
Japan/japan, Uruguay/Urguay). Canonicalise before any `groupby`, not just before a merge.
