# Post 17 design: A Third of the World's Labour Laws Still Assume You Work Saturday

> **PARTLY SUPERSEDED.** This doc was written before the analysis and before the adversarial
> fact-check. The four-chart spine, the two coding traps and the stance all survived. Several
> specific figures in it did not, and the check also added a finding the doc never anticipated: the
> paper's own convergence statistic (Table 3) reproduces only when the 96 no-law placeholder is
> included. The authoritative record of what changed is the "What the adversarial fact-check
> changed" table in `../README.md`. In particular, this doc quotes the DECADE dispersion minimum
> (1960s) where the shipped essay quotes the YEARLY minimum (1949), says "all 33" 1890s adopters
> where the true number is four polities across 33 polity-years, and reports an overtime convergence
> of 45.8% that turned out to be a denominator artefact (the honest figure is 29.4%).

Date: 2026-07-29. Status: awaiting approval.
Slug: `labour-laws-still-assume-you-work-saturday`. Chart prefix: `hours-`.

## Where this came from

Jonathan supplied the Data Is Plural edition of 2021-12-22 and asked for a post on working hours.
The entry in that edition is Magnus Bergli Rasmussen's Working Time Regulation Dataset. He also
said he had downloaded the Stata file; it was not on disk, so I pulled it from the Dropbox link in
that edition, which matches the link on the author's own datasets page.

## Brainstorm outcome, his picks

| Dimension | Choice |
|---|---|
| Angle | How the world agreed on a number |
| Hook | We were more standardized in 1950 than we are now |
| Stance | Name the widening, lay out both readings, refuse to crown one |
| Country frame | **Global only, no Indonesia, no personal narrator frame** |
| Fourth chart | The three instruments diverge |
| Close | It measures law, and law is not work |
| Title | A Third of the World's Labour Laws Still Assume You Work Saturday |

He explicitly cut the Indonesia angle even though the data supported a strong one (first law 1925
under Dutch rule, 40 hours in 1948 as the 8th country on earth, still 40 in 2012 while every
mainland neighbour sits at 48). Do not reintroduce it.

## Thesis

The world's statutory working week converged, then stopped converging, then started drifting apart,
and the drift is invisible in the headline average because the average kept falling the whole time.
Among countries that actually had a working-hours law, dispersion bottomed out in the 1960s and has
widened for sixty years since. What replaced the single number is not variety but a standoff between
two numbers, 40 and 48, neither of which has won. And the convergence that did happen was mostly the
spread of one treaty's figure rather than a worked-out answer.

The piece declines to say whether this is decay or progress, because the dataset measures statutes
and cannot measure work.

## The two coding traps, and how the analysis handles them

Both were found in the pre-build vet. Both are silent, and both produce a publishable-looking false
headline. Neither is presented as an error by the author; the second is explicitly outside his stated
coverage.

**Trap 1: `normalhours = 96` is a code for "no law", not a measurement.** It equals `workinglaw == 0`
across all 14,824 such rows with zero exceptions, 55% of the file. A naive
`df.normalhours.mean()` returns 73.4 hours and a naive time series says the world's normal week fell
from 96 hours to 46. **Handling: every hours statistic in this post is computed on
`workinglaw == 1` only.** The naive series is never plotted as if it were real.

**Trap 2: a coverage cliff at 2013.** Holding the same 179 countries and stepping 2012 to 2013, 70
lose their `hours_max` value to missing and 62 drop from a positive overtime premium to exactly zero,
while only 2 change normal hours and 2 change law status. The one-year jump in "has a law but no
overtime premium" is +61 against a largest-ever real-year move of +8 in 1945. The author's datasets
page states coverage to 2014 and the published paper's window ends earlier. **Handling: the entire
analysis is cut at 2012.** Every figure in the post is 2012 or earlier.

## The evidence chain

**1. Agreement peaked and reversed.** Statutory normal hours among law-havers only.

| Decade | n | mean | SD | IQR | CV% | at 40 or 48 |
|---|---|---|---|---|---|---|
| 1880s | 25 | 67.60 | 3.74 | 8.0 | 5.53 | 0.0% |
| 1910s | 124 | 56.77 | 8.24 | 16.5 | 14.52 | 35.5% |
| 1920s | 405 | 50.47 | 5.25 | 2.0 | 10.40 | 67.9% |
| 1940s | 833 | 48.48 | 3.95 | **0.0** | 8.15 | 73.6% |
| 1950s | 1033 | 46.38 | 3.67 | 0.0 | 7.92 | 78.9% |
| 1960s | 1191 | 45.78 | 3.37 | 4.0 | **7.35** | 77.0% |
| 1990s | 1574 | 44.33 | 3.77 | 8.0 | 8.49 | 65.0% |
| 2010s (to 2012) | 503 | 43.72 | 3.99 | 8.0 | 9.12 | 76.3% |

In the 1940s and 1950s the interquartile range was exactly zero: the middle half of every legislating
country sat at precisely 48 hours. Tightest agreement by coefficient of variation is the 1960s at
7.35%. By 2012 it is 9.12% and the IQR is 8 hours.

The mean falls monotonically the entire time. That is why the reversal is invisible in the headline.

**2. Two numbers, not one.** 2012, 168 countries with a law:

| Hours | Countries | Share |
|---|---|---|
| 40 | 73 | 43.5% |
| 48 | 56 | 33.3% |
| everything else (35 to 60, 10 distinct values) | 39 | 23.2% |

76.8% sit on one of two values, split nearly down the middle between them. The median country is at
44, a value in the trough between the two peaks.

**3. How the numbers spread.** First year each country's statutory week equals exactly 48, then
exactly 40:

- **20 countries first hit 48 in the five years 1916 to 1920.** ILO Convention No. 1 was adopted at
  Washington in 1919 and entered into force 13 June 1921, with 52 ratifications.
- **15 French African territories first hit 40 in the single year 1952**, the largest one-year
  adoption event in the file: Benin, Burkina Faso, Central African Republic, Chad, Comoros, Djibouti,
  Gabon, Guinea, Ivory Coast, Madagascar, Mali, Mauritania, Republic of the Congo, Senegal, Togo.
  Niger follows in 1953.
- The 40-hour convention, ILO No. 47 of 1935, took **22 years to enter into force** (23 June 1957)
  and has **15 ratifications**. Its Article 1 only declares approval of "the principle of a
  forty-hour week" and defers all detail to later conventions. The 40-hour wave is unfinished and the
  treaty behind it was never given teeth.

**4. Only one instrument standardized.** Coefficient of variation among law-havers:

| Decade | normal hours | maximum hours | overtime premium |
|---|---|---|---|
| 1880s | 5.53% | 15.97% | 204% |
| 1920s | 10.40% | 19.67% | 116% |
| 1960s | **7.35%** | 19.13% | 86% |
| 2010s | 9.12% | **22.08%** | 70% |

Normal hours converged then re-widened. Overtime premiums converged onto exactly +50%, where 45.2%
of countries sat in 2012. **Maximum permitted hours never converged at all**: CV rose from 16% to
22%, and in 2012 it spans 27 distinct values from 45 to 116 hours across 165 countries. The number
everyone quotes is the one that standardized. The ceiling that actually binds did not.

## Four charts

1. `hours-1-agreement-peaked.png` A fan chart of statutory normal hours among law-havers, 1880 to
   2012: median line with p25 to p75 and p10 to p90 bands. The band pinches shut in the 1940s and
   1950s and reopens after. The whole thesis in one shape.
2. `hours-2-two-numbers.png` The distribution of statutory normal hours across countries, 1950
   against 2012, as two rows of dots. 1950 stacked on 48; 2012 split between 40 and 48.
3. `hours-3-how-it-spread.png` First adoption of exactly 48 and exactly 40 by five-year window,
   1900 to 2012, with 1919 and 1952 marked.
4. `hours-4-three-instruments.png` Three small multiples sharing an x axis, independent y scales:
   CV of normal hours, of maximum hours, and of the overtime premium, 1920 to 2012.

## Honesty requirements

- **Every hours figure excludes `normalhours == 96`.** Say so in the method notes.
- **Nothing after 2012.** Say why.
- **The title's claim must be stated precisely in the body.** 48 hours is the figure ILO Convention
  No. 1 paired with an eight-hour day, and six eight-hour days is where it comes from, but Article
  2(b) of that convention explicitly permits exceeding eight hours on some days when others are
  shorter, capped at one extra hour. The dataset has no days-per-week column. So the defensible
  claim is arithmetic: **a 48-hour statutory week cannot be worked as five eight-hour days**, and 56
  of 168 countries legislated one in 2012. Do NOT assert that all 56 mandate a Saturday.
- **Do not attribute the 1952 cluster to a specific provision of the Code du travail d'outre-mer.**
  Law n° 52-1322 of 15 December 1952 is verified to exist and to have established a labour code
  across those territories; its hours article could not be retrieved (Legifrance 403s, Gallica OCR
  incomplete). The chart shows the cluster; the text names the law's existence and the fact that all
  15 are French territories, and stops there.
- **The 48-hour bloc is not a welfare ranking.** It contains Germany, Ireland and the United Kingdom
  next to Saudi Arabia and Bangladesh, because in the first group 48 is a statutory ceiling and the
  shorter real week comes from collective agreements, which this dataset cannot see. This must appear
  in the body, not just the notes, because a reader will otherwise think the data is broken.
- **Scope.** The regulations coded are for **industrial workers**. Not all employment, not the
  informal sector. State it.
- **Refuse to crown a reading.** Both readings get a fair paragraph: stalled reform versus national
  legislatures choosing for themselves. The essay declines, on the stated ground that statutes are
  not hours worked.
- **Credit the author.** This check is possible only because he published a manually coded 231-year
  panel as a straight download. The ask is a documented no-law code and a stated end-of-coverage
  year, not a correction.

## Citations, resolved

- Rasmussen, M. B. (2024). The great standardisation: working hours around the world. *Labor
  History, 65*(4), 563-591. https://doi.org/10.1080/0023656X.2023.2291512
  Resolved via the Crossref API, since Taylor & Francis returns 403 to WebFetch. Online first
  2023-12-20, print issue 2024-07-03, so the reference year is 2024. Page ranges take a plain hyphen,
  not an en dash, per the house punctuation rule and the Post 16 precedent.
- International Labour Organization. (1919). *Hours of Work (Industry) Convention, 1919 (No. 1)*.
  Verified verbatim from NORMLEX, including Article 2 and Article 2(b), entry into force 13 June
  1921, 52 ratifications.
- International Labour Organization. (1935). *Forty-Hour Week Convention, 1935 (No. 47)*. Verified
  verbatim from NORMLEX, including Article 1, entry into force 23 June 1957, 15 ratifications.
- France. Loi n° 52-1322 du 15 décembre 1952. Existence and scope verified via Legifrance and NATLEX
  metadata; hours provision NOT verified and therefore not asserted.

## Data sources

- Rasmussen Working Time Regulation Dataset, `public_workingtimedata.dta`, from
  `dropbox.com/s/ie1zvkr7iht2i1j/public_workingtimedata.dta`. 27,192 country-years, 202 polities,
  1789 to 2020, built on the V-Dem country-year frame. Four substantive columns: `workinglaw`,
  `normalhours`, `hours_max`, `overtime_remun`. No external join required.
- ILO NORMLEX for the two conventions. Note the site sits behind Cloudflare plus Oracle APEX and
  returns a redirect loop without a cookie jar; the working recipe is recorded in `data/README.md`.
