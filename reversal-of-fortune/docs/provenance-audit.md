# Provenance audit, Post 25, run before any design

Rule carried from Posts 23 and 24: open the primary source, or report that you could not. This
audit runs FIRST, which is the decision logged on 2026-09-07.

## VERIFIED AND OPEN

**Acemoglu, Johnson and Robinson's own replication files.** From Acemoglu's MIT data archive, the
"Reversal of Fortune" tables. Dropbox serves an interstitial page to `?dl=1`; substituting
`dl.dropboxusercontent.com` for `www.dropbox.com` returns the real zip. Tables 3 and 5 downloaded,
unpacked and read: 376 rows, Stata format, with the authors' own variable labels.

Documented variables I can use:
- `lpd1500s` "log population density, 1500"
- `lpa1500` "log population in 1500", `lland15` "log land area in 1500". ROUND 3 NOTE: the
  label is misleading and round 2 was misled by it. AJR's paper defines the density denominator as
  ARABLE land three times (p. 1243, the note to Table V, and Appendix 2, which names the variable
  "log arable land in 1500"), excluding "primarily desert, inland water, and tundra". The shipped
  variable is not fully consistent with that: exp(lland15) equals known TOTAL land area to within
  one percent for the United States (1.001), India (1.000) and Brazil (1.012), while desert states
  are cut hard (Egypt 0.040, Libya 0.020). So the definition is the authors' and the measure is
  looser than the definition. The post uses the authors' wording and records this caveat.
- `sjb1500` "Bairoch-equiv urbaniz Feb 2001", the urbanisation rate in 1500
- `logpgp95` "log PPP GDP pc in 1995, World Bank" in `maketable5.dta`. As with `ex2col`, the two
  files do not carry identical labels; quote the file alongside the label.
- `lat_abst` "Abs(latitude of capital)/90"
- `ex2col` "dummy=1 for ex-colonies" in `maketable3.dta`, "excolonies new list" in
  `maketable5.dta`. CORRECTED round 2: this audit originally quoted one label as if it were the
  only one, which is the same error it catches for `temp1` below. The two files agree on the
  values (all 42 apparent disagreements are missing-versus-missing), so nothing downstream moves.
  Note also what the variable does NOT mean: 0 is "absent from AJR's list", and that residual
  includes Bermuda, the Cayman Islands, Puerto Rico, Aruba and Cambodia.

**The reversal replicates, and the split is the finding.** Correlation between 1500 prosperity and
1995 income:

| basis | all countries | former colonies | never colonised |
|---|---|---|---|
| log population density 1500 | +0.05 (n=156) | **-0.58 (n=91)** | **+0.50 (n=65)** |
| urbanisation 1500 | +0.05 (n=84) | **-0.44 (n=41)** | **+0.43 (n=43)** |

Pooled, there is no relationship at all. The sign flips depending on whether Europeans colonised
the place. Indonesia is present, flagged `ex2col=1`, with above-average 1500 density.

**Modern income.** World Bank API, `NY.GDP.PCAP.PP.KD`, 265 rows for 2023, 244 with values, no key
required. Indonesia 13,890.

**Modern temperature.** World Bank Climate Change Knowledge Portal API, ERA5 reanalysis, near-surface air
temperature, annual climatology, 1991 to 2020 mean, by ISO3. Returns 200 with a documented metadata
block. This is the properly labelled temperature source the post will use.

## THE TRAP I NEARLY WALKED INTO, AND WHAT I GOT WRONG ABOUT IT

AJR's data contains `temp1` through `temp5`, in degrees Celsius, and an early run of mine reported
"corr(temp1, log GDP 1995) = -0.33" as though temp1 were average temperature.

**CORRECTED 2026-09-07, fact-check round 1. The reason given below was wrong.** This section said
the variables were undocumented, quoting the Stata label "first of 5 temperature indicators" and
concluding that nothing defined them. They ARE documented. CORRECTED AGAIN, round 2: the label is
**"Appendix 2: Variable Definitions and Sources"** in the published QJE, which is the work this post
cites; "Appendix Table A1" is the name it carries in NBER working paper 8460. Verified against both.
The text defines them: "Temperature variables are average temperature, minimum monthly high, maximum monthly
high, minimum monthly low, and maximum monthly low, all in centigrade", sourced to Parker (1997).
I had read the replication data files without reading the paper's appendix, which is the same class
of error this audit exists to prevent.

Two further corrections to what stood here:
- The label is not single. `maketable5.dta` says "first of 5 temperature indicators";
  `maketable3.dta` says "first of five temperature **categories**". The audit quoted one and called
  it "in full".
- This section said "They are not [dummies], they are continuous." `temp1` takes 33 distinct
  integer values over 323 rows with 89 rows at the single value 7. Calling it continuous overstates.

**The withdrawal still stands, on a better reason.** The values fail a sanity check as country
average temperatures: the United States reads 27 degrees, Greenland 26, Cambodia 7. Against the
ERA5 series this post uses, temp1 correlates at 0.58 with a mean absolute error of 4.7 degrees over
200 matched countries. Round 3 correction: the "33 distinct integer values over 323 rows with 89 rows at the single value 7" figures below describe the RAW column; on the de-duplicated matched frame the function reports 33 distinct values over 209 rows with 29 at 7. Both are now emitted separately. Round 2 note: those figures were hand computations that no script in this
repository produced, against the rule that every shipped number is reproducible. They are now
emitted by `temp1_sanity()` in `build_analysis.py` and land in
`results.json` under `withdrawn_temp1_sanity_check`. Whatever they are, they are not the country annual means the withdrawn
correlation treated them as. The number is withdrawn and appears nowhere in the post.

## STALE FIGURES IN AN EARLIER VERSION OF THIS FILE, CORRECTED

The table above originally reported the 1995 former-colony correlation as -0.58 (n=91) while
`results.json` carried -0.59 (n=90), and I described that as the audit being wrong. It was the
other way round. This audit was computed before `build_analysis.py` existed, without the
de-duplication step that script later introduced, and that step was silently deleting Germany and
Zimbabwe. The audit's -0.58 on 91 countries was correct, matches AJR's own published table, and the
pipeline has been fixed to agree with it.

## NOTES

- WITHDRAWN, round 2. This bullet said: "`testparm temp1-temp5` in the do-file initially suggested
  these were dummies. They are not, they are continuous. Both the dummy worry and the 'it must be
  mean temperature' assumption were wrong; the label settles it and the label says almost nothing."
  Two of its three claims are refuted by the correction above: 33 distinct integers over 323 rows
  is not continuous, and the label does NOT settle it, the paper's appendix does. Left visible
  rather than deleted, because round 1 corrected the section above and left this one standing,
  which is exactly the failure mode this file is supposed to catch.
- Income in AJR's file is 1995. Modern charts use World Bank 2023 separately rather than splicing.
