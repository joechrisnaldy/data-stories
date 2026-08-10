# Data

Four extracts, two from The DHS Program's public API and two from Our World in Data. All primary.
Nothing is redistributed here. Run `python3 fetch_data.py` from the post folder and they reproduce.
The whole download is under 1.5 MB; there is no large file in this post.

## The files

| File | What it is | Producer | Coverage |
|---|---|---|---|
| `dhs_literacy.json` | The eight columns of the published literacy table: never tested, read a whole sentence, read part of one, cannot read, no card in language, blind, missing, and the headline literate rate | The DHS Program | 226 surveys, 64 countries, women 15 to 49 |
| `dhs_education.json` | Share of women with secondary-or-higher and with more-than-secondary education | The DHS Program | same surveys |
| `mode_of_reporting.csv` | How each country's literacy rate was obtained: self-reported by the individual, self-reported by the head of household, a literacy test, or an indirect estimate | UNESCO Institute for Statistics, via Our World in Data | 169 countries, 1975 to 2016 |
| `dhs_vs_unesco.csv` | DHS and UNESCO adult literacy side by side | Both, via Our World in Data | 33 country-years with both, 28 countries |

The DHS API needs no key and no registration. It publishes the full percent distribution behind
every literacy rate, which is the whole reason this post is possible without microdata access.

## Traps in these files

Recorded while building. Each one is a way to publish a wrong number while running correct code.

**TRAP 1. The never-tested column is not a test result, and the API mislabels it.**
`ED_LITR_W_SCH` is served with the label "Women with secondary or higher education". Under the
current rule its numerator is `v106 = 3`, which is *higher than* secondary. The Guide to DHS
Statistics is explicit: "The question on the ability of the respondent to read a sentence are not
asked to women and men with higher than secondary education." Trusting the label would misdescribe
the column in every chart. Use the definition, not the label.

**TRAP 2. Reading part of a sentence counts as literate.**
The published indicator is `v106 = 3 or v155 in 1,2`, where `v155 = 1` is "able to read only parts
of a sentence". This is not an inference from the data; it is in the numerator definition and in
the label of the published Stata recode, which reads "Literate - higher than secondary or can read
part or whole sentence". Across the 46 countries on the current rule, the median country counts
9.6 points of partial reading as literacy. Cambodia has the largest band in points, 28.0 of 80.5. The extreme as a share of the literate
population is Sierra Leone at 43.0 percent; the two metrics pick different countries and must not
be quoted in one sentence.

**TRAP 3. The rule changed, and neither survey type nor fieldwork year identifies the change.**
DHS's own note: "In DHS-VI and earlier surveys the question on the ability of the respondent to
read a sentence was not asked to women and men with secondary education or higher than secondary.
Thus estimates from earlier surveys may overestimate literacy relative to DHS-7 and DHS-8 surveys.
Care should be taken in interpreting trends."

Ghana 2014 DHS and Ghana 2022 DHS sit on opposite sides of it, so `SurveyType` is useless. The two
regimes overlap in time, old-rule surveys running 2000 to 2016 and new-rule 2015 to 2025, so a
fieldwork-year cutoff misclassifies surveys. The API exposes no phase field anywhere, including the
`surveycharacteristics` endpoint.

Classify empirically instead: under the old rule the never-tested column equals the published share
with secondary-or-higher, and under the new rule it equals the share with more-than-secondary. Both
are separately published. Surveys match their assigned rule to a mean of **0.005 points** and miss
the other by **32.9**, so the separation is not a judgement call. 221 of 226 surveys classify; the
five that do not are listed in `results.json` under `method.surveys_unclassified`.

**TRAP 4. A missing column means zero, not unknown.**
DHS omits a category when it rounds to zero. `missing` is absent from 98 surveys, `blind` from 44
and `no card` from 31. An earlier version of `build_analysis.py` required all eight columns and
silently dropped 65 percent of the data, taking all four of the countries the post names with it.
The five load-bearing columns are always present; treat the other three as zero when absent.

**TRAP 5. The instrument errs downward as well as upward, and the post owes the reader both.**
`v155 = 3`, "no card with required language", is counted as NOT literate. Someone who reads
fluently in a language the interviewer had no card for is recorded as illiterate. It is small,
under a tenth of a percent at the median and above one percent in only two of the 46 countries, with Mali highest
at 1.5, but it is real and it is the honest counterweight to the exemption.

**TRAP 6. Three different constructions, never to be merged.**
DHS's published table is women 15 to 49. UNESCO's adult rate is everyone 15 and over. The
DHS-versus-UNESCO comparison file uses a THIRD series, Our World in Data's compilation of DHS
survey estimates across all respondents (DHS Program, 2018), which is not the women 15 to 49 table. Where both cover a country they disagree by up to
+15.9 points (Pakistan 2005) and 11.7 lower (East Timor 2015), around a mean gap of only +1.8. The average
conceals the disagreement completely. Never present the two as one measure.

**TRAP 7. The reporting-mode file counts country-years, not people or countries.**
A country that reported ten times weighs ten times as much as one that reported once. The 333, 283,
52 and 18 are country-years. The country-level counts are separate: 40 countries have ever been
recorded using a literacy test and 129 have not.

**TRAP 8. Method against literacy level has two readings and the data cannot separate them.**
Countries whose rate came from a test sit at a median literacy of 73.2 against 94.1 for individual
self-report. That is consistent with testing being applied where literacy is already doubted, and
equally consistent with testing returning lower numbers than asking. The post must state both and
assert neither.

**TRAP 9. The reporting-mode data ends in 2016.**
Any sentence about "this era" has to be written against that vintage. The DHS side runs to 2025.

## Two gotchas that cost time

`dhsprogram.com` returns HTTP 403 to automated fetches. The Guide to DHS Statistics is reachable
through the Wayback Machine with `curl` (WebFetch cannot reach web.archive.org from here), and the
indicator code is on GitHub at `DHSProgram/DHS-Indicators-Stata`.

The OECD SDMX API does not carry PIAAC. All 1,544 dataflows were checked before the rich-world
section was redesigned around UNESCO's reporting-mode data instead.

## Reproducing

```bash
python3 fetch_data.py
```

Under 1.5 MB. If `urllib` fails with CERTIFICATE_VERIFY_FAILED, that is a Python install with an
empty certificate bundle rather than a network problem; `fetch_data.py` resolves a working bundle
rather than disabling verification.
