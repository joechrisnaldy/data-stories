# Data

One source, public, not redistributed here. Two ILO conventions read for context. Everything below
reproduces from scratch.

## 1. Working Time Regulation Dataset (the whole analysis)

**Magnus Bergli Rasmussen**, Associate Professor at the University of South-Eastern Norway. Manually
coded working-time regulation for industrial workers across 197 polities from 1789 (the public file
carries 202 country identifiers and his datasets page says 203). Published in
*Labor History*, so this is peer-reviewed academic data rather than an anonymous upload. Entry point:
the Data Is Plural edition of 2021-12-22.

```bash
curl -sL -A "Mozilla/5.0" -o public_workingtimedata.dta \
  "https://www.dropbox.com/s/ie1zvkr7iht2i1j/public_workingtimedata.dta?dl=1"
```

9.9 MB, Stata release 118, stamped 30 Nov 2021. The same link appears on the author's own datasets
page, so the file is his. Expected layout: `data/public_workingtimedata.dta`.

Read with `pyreadstat.read_dta`. 27,192 country-years, 26 columns, zero duplicate country-years.

### The variables that matter

Twenty-two of the 26 columns are the V-Dem country-year skeleton the file was built on, which is why
the Stata label reads `V-Dem CY-Full+Others`. Only four columns are the data:

| Variable | Meaning |
|---|---|
| `workinglaw` | Whether a law regulating total hours of work existed that year. |
| `normalhours` | The "normal" contractually obligated weekly hours. **See the trap below.** |
| `hours_max` | The maximum weekly hours allowed. Missing for 58% of the file. |
| `overtime_remun` | The percentage uplift in pay for overtime. |

### TRAP 1: `normalhours = 96` is a code for "no law", not a measurement

It equals `workinglaw == 0` across all **14,824** such rows with **zero exceptions**, which is **55%** of the rows where it is populated, or 54.5% of all rows. So the innocent `df.normalhours.mean()` returns **73.4 hours**, a figure that
is neither a legal ceiling nor a placeholder but a blend of both. A naive time series says the
world's normal working week fell from 96 hours to 46.

Read on the countries that actually had a law, the statutory week falls from **72.0 hours in 1850 to
43.7 in 2012**, not from 96 to 46. Anchoring a decomposition at 1920, where the naive mean is 86.8,
**90.6%** of the fall to 46.4 is the spread of regulation and only 9.4% is regulated hours falling. That split holds from 84.5% to 96.7% across both orderings, so it does not depend on which
factor you move first.

Do not anchor that decomposition at 1850. In 1850 exactly **one** polity of 86 had a law, so the
split swings from 45.6% to 99.3% by ordering and means nothing.

**Every hours figure in this post is computed on `workinglaw == 1` only.**

### TRAP 2: a coverage cliff at 2013

Holding the same 179 countries and stepping 2012 to 2013:

| What changed | Count |
|---|---|
| lost `hours_max` to missing | 70 |
| dropped from a positive overtime premium to exactly zero | 62 |
| changed `normalhours` | **0** |
| changed `workinglaw` | **0** |

Counting WITHIN-COUNTRY transitions rather than differencing the stock, **61** countries go from a
positive premium to exactly zero in 2013, against a maximum of **one** in any earlier year. (An
earlier version of this note differenced the stock and reported a "largest real move of 8 in 1945";
that counted panel entries and exits as law changes.) Read naively, the file says a third of the world abolished overtime
pay in a single year.

It did not. The author's datasets page states coverage to 2014, while the paper's online appendix says
the public dataset "ends in 2010". Either way 2013 onward sits outside the documented data. **The
analysis is cut at 2012**, because the file is continuous through it and the 2013 break is unambiguous.

### Other gotchas

- Float32 storage turns 41.3 into `41.299999` and 67.3 into `67.300003`, so raw `value_counts`
  fragments. Round the hours columns to 1 decimal first. 40.0 and 48.0 are exactly representable in
  binary floating point, so the "exactly 40" and "exactly 48" tests are unaffected either way.
- The 30 polities that never legislate are mostly pre-unification German and Italian states (Baden,
  Bavaria, Two Sicilies, Papal States, Piedmont-Sardinia), which is a sign the historical coding is
  real rather than backfilled.
- Percentiles are meaningless on a handful of polities. The fan chart starts at 1918, the first year
  at least 20 countries had a law.
- Dispersion claims must state their coverage, and the condition is load-bearing. Among decades with
  at least 20 polity-years the 1890s have the lowest spread, but the 1840s, 1850s and 1860s are lower
  still at exactly zero, because France is the only polity with a law and sits at 72 hours every year.
  Even the 1890s figure rests on **four** polities, all European: Austria, France, Russia and
  Switzerland, across 33 polity-years. The essay quotes the YEARLY series, which is what chart 1
  plots: tightest 1949 and 1950 (identical to the row), tied at 6.22%, never matched after 1951, on
  the condition that at least 20 countries had a law. The decade-pooled minimum is the 1960s, later
  because decade pooling absorbs the 1952 adoption wave.
- The regulations coded are for **industrial workers**, not all employment and not the informal
  sector.
- Statutory is not actual, and 48 does not mean one thing. Germany, Ireland and the United Kingdom
  sit in the 2012 48-hour bloc, but German law fixes eight hours per *Werktag* (Monday to Saturday),
  so its 48 is six eight-hour days, while Britain's is a 48-hour average across a reference period
  that a worker may individually opt out of. The same file records their MAXIMUM week as 60, 60 and
  72, so 48 is not their ceiling. The spread is not a ranking of how hard people work.

## 2. ILO conventions (context only, no data joined)

Read for the two adoption waves. NORMLEX sits behind Cloudflare plus Oracle APEX and returns an
infinite redirect to itself without a session cookie, so a plain `curl` or WebFetch fails. Working
recipe:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
curl -s  -A "$UA" -c cj.txt -o /dev/null "https://normlex.ilo.org/dyn/normlex/en/f?p=NORMLEXPUB:1:0::NO:::"
curl -sL -A "$UA" -b cj.txt -c cj.txt -e "https://normlex.ilo.org/" \
  "https://normlex.ilo.org/dyn/nrmlx_en/f?p=NORMLEXPUB:12100:0::NO::P12100_ILO_CODE:C001"
```

Swap `C001` for `C047`. Ratification counts live at `P11300_INSTRUMENT_ID:312146` (C001) and
`312192` (C047) under the `11300` page.

- **C001, Hours of Work (Industry) Convention, 1919.** Article 2: working hours "shall not exceed
  eight in the day and forty-eight in the week". Entry into force 13 June 1921, 52 ratifications.
  Article 2(b) lets the eight-hour daily limit be exceeded when other days are shorter, but by no
  more than one hour, capping the day at nine. Five nine-hour days reach 45, so even under 2(b) a
  48-hour week still needs a sixth day.
- **C047, Forty-Hour Week Convention, 1935.** Article 1 declares approval only of "the principle of a
  forty-hour week applied in such a manner that the standard of living is not reduced in consequence"
  and defers every detail to later conventions. Entry into force 23 June 1957, 22 years after
  adoption, 15 ratifications.

## 3. What could not be verified, and is therefore not claimed

Fifteen French African territories first reach 40 statutory hours in 1952, the largest single-year
adoption in the file. 1952 is the year France enacted **Law n° 52-1322 of 15 December 1952**
establishing a labour code across its overseas territories, which is verified from Legifrance and
NATLEX metadata. Its **working-hours provision could not be retrieved**: Legifrance returns 403 and
the Gallica scan of the original text is incompletely transcribed. The post therefore names the law
and the fact that all 15 are French territories, and stops there. It does not assert what the code
said about hours.

Similarly, the dataset has no days-per-week column, so the post argues the 48-hour claim as
arithmetic (48 is six eight-hour days, and 48 over five days would need 9.6 hours a day) rather than
asserting that all 56 countries at 48 require a Saturday.

## What the vet found

The dataset passes every authenticity check. Real historical polities including ones that no longer
exist, plausible values, no reconstructable outcome, no frozen columns, no sequential identifiers,
and coverage that grows the way real archival coding grows rather than appearing all at once. The two
traps above are coding conventions and an end-of-coverage boundary, not errors. What the post asks
for is a documented no-law code and a stated last year of coverage.
