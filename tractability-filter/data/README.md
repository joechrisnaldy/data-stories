# Data for Post 23

Nothing in this folder is committed. Run `python3 fetch_data.py` from the post directory and it
rebuilds everything below. All five sources are public, free, and need no key or registration:
WHO Global Health Estimates, the WHO Global Health Observatory API, Our World in Data grapher
CSVs, the ClinicalTrials.gov API, and the NIH RePORTER API.

## Sources

| File | Source | How |
|---|---|---|
| `ghe2021_daly_wbincome_new.xlsx` | WHO Global Health Estimates 2021, July 2024 release, DALYs by cause and World Bank income group | direct download from `cdn.who.int` |
| `ghe2021_daly_bycountry_2021.xlsx`, `..._2010.xlsx` | Same release, DALYs by cause and country | direct download; the United States column is what the money analysis needs |
| `ghe2021_deaths_global_new2.xlsx` | WHO Global Health Estimates 2021, DEATHS by cause, global. Cause code 1530 Road injury. **The post's opening two numbers come from here, not from the OWID copy below**, which differs by 7,000 to 9,000 deaths a year | direct download from `cdn.who.int` |
| `who_road_deaths_count.json` | WHO Global Health Observatory `RS_196`, estimated number of road traffic deaths, 2021 | GHO API, direct |
| `who_road_death_rate.json` | WHO GHO `RS_198`, estimated road traffic death rate per 100,000, 2021 | GHO API, direct |
| `who_road_user_type.json` | WHO GHO `RS_246`, distribution of road deaths by road user type, 2013 and 2016. NOT the source of the split the post quotes: see trap 10 | GHO API, direct |
| `ct_road_injury_probe.json` | Alternative ClinicalTrials.gov terms for road injury, kept as a DISCLOSURE of a mapping failure and never fed to the analysis | API v2 |
| `death-rate-road-traffic-injuries.csv` | WHO SDG indicator 3.6.1, via Our World in Data. Retained for context only: it stops at 2019 and the post does NOT use it, because WHO has published 2021 | grapher CSV |
| `deaths-from-road-injuries.csv` | WHO Global Health Estimates, via Our World in Data | grapher CSV |
| `electric-car-sales-share.csv` | International Energy Agency, via Our World in Data | grapher CSV |
| `private-investment-in-artificial-intelligence.csv`, `corporate-investment-...csv` | Stanford AI Index, via Our World in Data | grapher CSV |
| `computation-used-to-train-notable-artificial-intelligence-systems.csv` | Epoch AI, via Our World in Data | grapher CSV |
| `ct_counts.json` | ClinicalTrials.gov API v2, study counts per condition query | `countTotal=true` |
| `ct_by_year.json` | ClinicalTrials.gov API v2, studies first posted per calendar year | `filter.advanced=AREA[StudyFirstPostDate]RANGE[...]` |
| `nih_categories.json`, `nih_spend.json` | NIH RePORTER API v2, FY2024 awards by RCDC spending category | POST search, paged |

## Traps hit while building this, and what they cost

1. **This machine's Python has an empty CA bundle.** `ssl.create_default_context().cert_store_stats()`
   returns zero certificates, so every `urllib` HTTPS request fails with CERTIFICATE_VERIFY_FAILED.
   Fixed by shelling out to curl throughout. Verification was never disabled.
2. **ClinicalTrials.gov returns HTTP 403 to `urllib` regardless of User-Agent**, but answers curl
   normally. Only visible after the TLS problem above was fixed, because it presented as the same
   failure.
3. **Our World in Data returns HTTP 403 for IHME-sourced charts**, with a body explaining the data
   is non-redistributable. That rules out every IHME burden chart, including
   `burden-of-disease-by-cause` and `road-deaths-by-type`. Burden here comes from WHO directly.
   OWID charts sourced from WHO, IEA, Epoch and Stanford do download.
4. **GHE cause codes are not guessable.** Code 970 is Epilepsy and 980 is Multiple sclerosis, which
   is the reverse of the obvious guess. Every lookup in this post is keyed by exact cause name and
   asserts the name was found.
5. **The GHE by-country workbook is wide, not long.** Countries are columns in row 7, ISO-3 codes
   in row 8, values in thousands. The cause name is the last non-empty cell across the indent
   columns, and only `Persons` rows are read.
6. **NIH has no general Leukemia category**, only "Childhood Leukemia", so leukaemia is excluded
   from the money analysis. Road injury and falls share "Physical Injury - Accidents and Adverse
   Effects", so they are merged with burden summed rather than one being dropped.
7. **Malaria's US burden rounds to zero**, so dollars per US healthy year lost is undefined for it
   and it drops out of the money models. That is recorded rather than imputed, and the fact that
   the NIH funds it anyway is itself part of the argument.
8. **RCDC categories overlap and do not partition the NIH budget.** This is NIH's documented
   behaviour, not an artefact of the reconstruction.
9. **ClinicalTrials.gov counts are a registry-wide stock, not an annual flow.** Registry coverage
   grew sharply after the FDA Amendments Act of 2007, so the by-year series is reported separately
   rather than used to make stock counts comparable across eras.

10. **Country-level `RS_246` does not reproduce WHO's own published global split, and neither did
    WHO's press release.** Two separate errors, three rounds apart, both flattering the argument.

    First: requiring all five road-user categories, which you must do or you are renormalising
    partial returns, leaves 101 countries; adding the sum tolerance leaves 82, and 37 percent of
    the world's road deaths. The
    filter has three steps, not two: 139 countries report something, 101 report all five
    categories, and a tolerance requiring the five to sum within 12 points of 100 drops 19 more,
    the United States among them at 66.7. On that sample four-wheeled occupants come to 22.8
    percent; on all 101 reporting five categories, 26.2.

    Second: WHO's *Global status report on road safety 2023* publishes 25 percent for four-wheeled
    occupants, on pages 10, 15 and 17. WHO's launch **news release** for that report publishes 30
    percent, and that 30 is the report's figure for motorcyclists. An earlier draft of this post
    took the release's numbers. The report is the source. The IRIS full text answers a plain curl
    with a browser User-Agent.

    **Withdrawn:** the "all 139 reporting countries" variant, which returned 31.3 percent and was
    published as an upper bound. Six of those countries reported exactly one category, all
    four-wheel, and renormalising a single category to its own sum scales it to 100 percent. Those
    six supply 34.8 percent of the 31.3. Excluding them the figure is 22.9. `build_analysis.py`
    still computes all four variants into `transport.user_split_disagreement`, with that one
    labelled an artefact, so the mistake stays visible rather than being deleted.

    The old code asserted that the computed vulnerable-road-user share exceeded 50 percent, which
    passed only on the filtered sample (56.3) and fails on the full one (49.2). An assertion that
    can only be satisfied by the sample you chose validates the sample instead of testing it. It is
    gone, and structural guards that test the build rather than the finding replaced it.
