# Post 25 design: the map used to run the other way

Binding design document. Written 2026-09-07, BEFORE any chart exists and before the modern
temperature and 1500 density variables have been put in the same table. Amendments are marked in
place (AMENDED / WITHDRAWN / SUPERSEDED), never edited silently.

Repo folder: `Projects/analytics-blog/reversal-of-fortune/`

---

## 1. The question and the answer

His question, from an article he read: warmer countries are poorer. Why, and how did it happen?

His posture, chosen in the brainstorm: **it felt too neat.** A single clean variable explaining the
wealth of nations is the shape of an answer that is usually wrong.

The answer this post reaches: the correlation is real, and it cannot mean what it looks like,
because five centuries ago the ranking ran the other way. The post does NOT adjudicate what caused
the reversal. It establishes that the reversal happened and uses it as a filter: any explanation of
today's map has to also explain why the map used to be inverted, and a large class of popular
explanations cannot.

**What the post explicitly refuses to do.** It does not claim institutions caused it, does not
adjudicate Acemoglu, Johnson and Robinson against their critics, and does not forecast anything
about climate change. Those are all real debates and all outside what a weekend post can settle.

## 2. Structure

Four acts, target 1,600 to 2,000 words, four charts, light Indonesia touch in one section.

1. **The tidy story.** Temperature against income today. It is real and it is strong.
2. **The same heat, five centuries earlier.** Temperature against population density in 1500.
3. **The flip.** 1500 prosperity against income today, split by whether Europeans colonised.
4. **The filter.** What that rules out, what it leaves standing, and one Indonesia section.

## 3. Pre-registered method

### 3.1 Data, all open and downloadable without registration

- **Modern income.** World Bank API, `NY.GDP.PCAP.PP.KD`, GDP per capita, PPP, constant 2021
  international dollars, most recent year with wide coverage. Logged for all analysis.
- **Modern temperature.** World Bank Climate Change Knowledge Portal API, ERA5 reanalysis, near-surface
  air temperature (`tas`), annual climatology, 1991 to 2020 mean, by ISO3.
- **Historical prosperity and the colonisation split.** Acemoglu, Johnson and Robinson's own
  replication files for "Reversal of Fortune", tables 3 and 5. Variables used, all carrying the
  authors' own labels: `lpd1500s` log population density 1500, `sjb1500` urbanisation 1500,
  `lat_abst` absolute latitude of capital over 90, `ex2col` ex-colony dummy, `logpgp95` log PPP
  GDP per capita 1995.

**WITHDRAWN before use: AJR's `temp1` to `temp5`.** Labelled only "first of 5 temperature
indicators", with temp2 to temp5 unlabelled. An early exploratory correlation of -0.33 between
temp1 and 1995 income is withdrawn and must not appear. All temperature in this post comes from
the climate portal, where the variable has a definition. See `docs/provenance-audit.md`.

### 3.2 Fixed choices

- **"Warm" is annual mean temperature**, from ERA5. Absolute latitude is reported alongside as a
  robustness check because the older literature uses it, never as the headline.
- **The split variable is `ex2col`**, AJR's own ex-colony dummy. It is not re-derived here.
- **Every income measure is logged.** Raw GDP per capita is not used in any correlation.
- **1500 prosperity is population density**, with urbanisation reported as the second basis. Both
  are AJR's; both are proxies for prosperity in a period with no income statistics, and the post
  says so rather than treating density as wealth.

### 3.3 Falsification conditions

The post is wrong, and becomes a different post, if any of these hold:

1. **The premise fails.** Temperature and income are not meaningfully related on current data.
   Then there is nothing to explain and the article he read was wrong.
2. **The reversal is a vintage artefact.** It appears with AJR's 1995 income but disappears when
   the same 1500 measures are matched to 2023 income. AJR published on 1995 data; nobody in this
   repository has checked whether it survives 28 more years, and it is the first thing to test.
3. **The sign does not flip.** The colonised and never-colonised samples do not point in opposite
   directions, meaning the split is not doing the work the argument needs.

### 3.4 Guardrails

- **No mechanism claims.** The post may say what the reversal rules OUT. It may not say what caused
  it. Any sentence asserting institutions, or disease, or extraction as the cause is out of scope,
  however tempting.
- **The filter must be stated precisely.** What the reversal disqualifies is any explanation that
  is BOTH constant over the period AND independent of colonisation: heat acting directly on
  productivity, latitude itself, tropical soils as destiny. What it leaves standing includes
  anything that changed over the period or that interacted with who arrived. The post states both
  halves; disqualifying without saying what survives would be a rhetorical trick.
- **Density is not wealth.** A dense place in 1500 was probably a productive one, but the inference
  is an assumption of AJR's method and the post carries it as an assumption.
- **No climate forecasting.** Out of scope entirely.
- **Indonesia earns its section from the data or it is cut.** Its position in the 1500 and modern
  distributions is checked before the section is written, not asserted.

## 4. Chart spine

Exactly four, prefix `rf-`.

1. `rf-1-the-tidy-story.png` Annual mean temperature against log GDP per capita today, all
   countries with both. The claim, drawn honestly and at full strength.
2. ~~`rf-2-the-same-heat-in-1500.png` Annual mean temperature against log population density in
   1500. If hot places were the dense ones, the heat that predicts poverty now predicted prosperity
   then.~~ **AMENDED 2026-09-07 after computing it: the premise was wrong.** Globally, temperature
   against 1500 density is **-0.17**, slightly NEGATIVE. Hot places were not the dense ones
   worldwide. The relationship is positive only inside the colonised world, at **+0.29** (n=96).
   AMENDED (round 2): -0.17/n=171 and n=96 are PRE-de-duplication values. Post-fix they read
   **-0.18 (n=173)** and **+0.29 (n=97)**. Amendment 6.1-1 said the fix moved three published
   figures; it moved six correlations at two decimals and every sample size in the post, these
   included.
   The chart narrows to former colonies and makes a smaller claim: among the places Europeans
   colonised, heat went with density in 1500 (+0.29) and goes with poverty now (-0.25). That is a
   sign flip on the temperature variable itself, more directly on the post's subject than the
   density-versus-income version, but it is sample-specific and the post says so. The original
   global claim must not be reinstated.
3. `rf-3-the-flip.png` Log population density 1500 against income today, two panels, former
   colonies and never colonised. The sign flip. Unchanged, and fixed before the data was seen.
4. `rf-4-who-actually-reversed.png` **AMENDED 2026-09-07, chosen AFTER seeing the data**, unlike
   charts 1 and 3. Rank change among former colonies: percentile by 1500 population density against
   percentile by income today. Burundi 98th to 1st, Sudan 91st to 10th, Afghanistan 87th to 9th;
   Singapore 4th to 100th, Australia 2nd to 97th, the United States 5th to 99th. A chart chosen
   after seeing the data is a weaker object than one chosen before and the method notes say which.

~~Chart 2 is the one this post lives or dies on and it has not been computed yet.~~ It was computed
and did not survive in the form specified. Recorded rather than quietly rewritten.

### 4.1 Indonesia, resolved against the plan

Section 3.4 required Indonesia to earn its section from the data or be cut. **It did not earn the
section as pitched.** Indonesia sits at the 78th percentile of former colonies by 1500 population
density and the 64th by income today: a 14-point slide, ranking 47th of 93. AMENDED (round 2):
   these are pre-de-duplication values; post-fix Indonesia reads 79th, 65th, 47th of 94, and the
   post quotes those. Middle of the
distribution, not a case study.

RESOLVED: the section stays and its ordinariness is the point. The post says plainly that the
author went looking for his own country in the reversal and found it unremarkable, and that the
large reversals are in East Africa and South Asia. Writing Indonesia as a dramatic instance would
have meant ignoring its rank, which is the failure this document exists to prevent.

## 5. Out of scope

- Any claim about what caused the reversal.
- Any forecast about warming and future growth.
- Any claim about the capabilities, culture or character of people in any region. The post is about
  what a correlation can and cannot license, and the determinism reading is the thing it exists to
  disarm.

## 6.1 Amendments after fact-check round 1, 2026-09-07

Four refuter lenses against a 54-claim inventory. The thesis survived; almost nothing else did
untouched. Recorded here rather than applied silently.

1. **Two analysis bugs.** `drop_duplicates("shortnam")` kept the FIRST row per country and the first
   row for Germany and Zimbabwe is blank, so both were deleted from every historical correlation.
   Fixed to keep the most-populated row. Three published figures moved: +0.27 to +0.28, +0.02 to
   +0.04, -0.59 to -0.58. The corrected 1995 figure, -0.5842 on n=91, reconciles exactly with AJR's
   published table (coefficient -0.38, R-squared 0.34, n=91). AMENDED (round 2): the table is
   **Table V, Panel A, column 1** of the QJE, p. 1251, verified against the paper; "Table 6" was
   wrong and the specification is bivariate, so R-squared equals r-squared and the reconciliation
   is not a coincidence. It matches to the precision AJR publish, not exactly: sqrt(0.34)=0.5831
   against a recomputed r of 0.5842. Separately, the World Bank
   aggregate filter tested a `region` field the indicator endpoint does not return and removed
   nothing; aggregates never reached the output only because the temperature series has no codes
   for them. Both now enforced and asserted.
2. **Section 3.4's filter was stated wrongly in the draft.** This document pre-registered the
   disqualified class as a CONJUNCTION, "BOTH constant over the period AND independent of
   colonisation". The draft split it into two independent sufficient bans, which is strictly
   stronger and which the draft then contradicted three paragraphs later by stating the correct
   survivor set. Worse, the second ban was false on this post's own data: absolute latitude
   correlates with `ex2col` at **-0.74**, so a climate story sees the colonial split perfectly well.
   The draft now states the conjunction, and explicitly notes that a constant tropical disease
   environment acting through European settlement survives it.
3. **The post asserted a Simpson's paradox without testing it.** Two subgroup correlations do not
   establish an interaction. `interaction` in results.json (there is no `models` key) reports
   coefficient -0.4825, t -5.33, n=163,
   slopes +0.148 never-colonised against -0.335 colonised.
4. **The log transform on 1500 density was undisclosed.** AJR's `lpd1500s` is already logged and the
   draft called it "population density in 1500" throughout. On untransformed density the
   former-colony correlation falls from -0.49 to -0.10 and the flip disappears. Now disclosed as
   load-bearing.
5. **The provenance audit's own reasoning was wrong** and is corrected in place. AJR's temperature
   variables ARE documented, in the QJE's "Appendix 2: Variable Definitions and Sources" (the
   same table is Appendix Table A1 in NBER working paper 8460). The withdrawal stands on a sanity
   check instead.
6. **A gap in the falsification set, found in review and not closed.** If the reversal had been
   absent in BOTH income vintages, none of the three conditions would have fired: fc2 requires the
   1995 correlation to be strong, and fc3 is a bare sign test with no magnitude floor. That is the
   most likely way this post could have been wrong and no condition covered it. Disclosed in the
   method notes rather than retro-fitted, because adding a condition after seeing the data is not a
   pre-registration.
7. **Chart defects visible only in the rendered images.** Chart 1's annotation overlapped the
   Singapore and Qatar labels; chart 4's legend lay across the Uruguay row with swatches the same
   size as data markers; chart 2's left panel drew 93 points under an n=96 annotation because the
   frame demanded 2023 GDP for a panel that needs only temperature and 1500 density. All three
   fixed, and chart 4 now asserts on unmapped country codes rather than rendering a bare ISO3.
8. **Source corrections.** Density is per ARABLE land, from McEvedy and Jones. Urbanisation is AJR's
   FIRST proxy and density their wider-coverage second; the post had inverted the emphasis.
   "Twenty-five years" was 24 and started in the wrong place. Dell, Jones and Olken (2012) is now
   cited for the within-country weather work the post previously asserted without a reference. The
   portal is the Climate CHANGE Knowledge Portal. "196 countries" is countries and territories.


## 6.2 Amendments from fact-check round 2

Round 2 was scoped only at what round 1 changed. Its findings, in the order they change the post:

1. **The filter was invalid as stated, not just imprecise.** "An explanation cannot be both constant
   over the period and indifferent to who arrived" equivocates between a constant CAUSE and a
   constant EFFECT. Counterexample: heat's effect on output can be constant in 1500 and today as a
   *cause* while the world's production function changes around it. The bolded claim is now about
   the constancy of the EFFECT, and is restricted to explanations of the ranking BETWEEN countries.
2. **That restriction also removes a self-contradiction.** Without a domain, the filter disqualified
   the Dell et al. within-country result that the post endorses three paragraphs later, and the
   close repeated the unrestricted version in the post's most quotable position.
3. **The Dell et al. figure came from the wrong paper.** "About 1.1 percentage points, with little
   effect in rich ones" is NBER working paper 14132 (2008), a different title. The published 2012
   article says **1.3** and "do not have a robust, discernable effect". Corrected, and the citation
   now matches the sentence.
4. **The log transform costs more than round 1 disclosed.** On raw density the two subgroup signs
   stay opposite (-0.10 against +0.17), so "the flip disappears" was wrong, but the interaction the
   argument rests on falls from t -5.33 to **t -1.37**. Now stated in the method notes.
5. **The rival-variable comparison was across three different samples.** Latitude at +0.60 (n=159)
   was being compared with temperature at -0.44 (n=196). On one common sample of 159: temperature
   **-0.46**, latitude **+0.60**, Africa **-0.68**. Ordering survives, the claim did not.
6. **Seven figures in the post had no script behind them.** The Africa dummy, the -0.74, the
   17 hot-and-rich places, the 24-to-28-degree spread, the raw-dollar r, the urbanisation gap test
   and the temp1 sanity check were all hand computations. All seven are now in build_analysis.py.
7. **The de-duplication comment was wrong on three counts** (the first rows are not blank, YUG is a
   third duplicate, and urbanisation barely moved rather than being unaffected: round 4 found
   its two 1995 pairings did shift, though none of the urbanisation figures the post prints did), and the aggregate filter fix had been applied
   to build_analysis.py only, leaving the dead copy in make_charts.py where 43 aggregates still
   entered the frame. Both corrected.
8. **WITHDRAWN, round 3. This amendment was wrong.** It read: "`lpd1500s` is not density per ARABLE acre." Its denominator `lland15` is total land area with
   desert netted out; checked against known land areas (USA 1.001, India 1.000, Brazil 1.012, Egypt
   0.040). The post said arable and now does not, and "density measures total production" is also
   corrected to production per unit of land."
   **Why it is withdrawn:** the amendment rests on the Stata label "log land area in 1500" plus a
   ratio check, and never opened the paper. AJR define the denominator as arable land three times:
   p. 1243 ("We calculate population density by dividing total population by arable land (also
   estimated by McEvedy and Jones). This excludes primarily desert, inland water, and tundra"), the
   note to Table V ("Population density in 1500 is total population divided by arable land area"),
   and Appendix 2, which names the variable "log arable land in 1500". Verified in round 3 against a
   freshly downloaded PDF, sha256 0385c46c9732235f8c9a37efa4611048c3f38a3154d0ebe291486cc425842f4e.
   This is the same error round 2 corrected round 1 for: trusting a data file's label over the
   document that defines it. The ratio check stands as a caveat on the shipped variable, not as a
   redefinition of it, and is recorded in the provenance audit. The draft is restored to "per unit
   of arable land" and re-credits McEvedy and Jones. The separate correction of "density measures
   total production" stands, but now reads "per unit of arable land".
9. **`ex2col == 0` means "not on AJR's list", not "never colonised".** It contains Bermuda, the
   Cayman Islands, Puerto Rico, Aruba and Cambodia. Recoding all nine awkward cases as colonies
   leaves the interaction at t -4.70, so the result holds; the wording did not and is fixed.
10. **The AJR quote's context was inverted.** "More complex" is their concessive clause ("Although
    the theoretical relationship ... is more complex, it seems clear that ..."), not their
    conclusion, and their urbanisation claim requires a transport network as well as agricultural
    productivity. Both corrected. The Malthusian caution the post offered as its own is theirs,
    from p. 1243, and is now attributed.
11. **Chart defects found only in the rendered PNGs.** Chart 2's left annotation sat 5 px from
    Canada (sub-pixel at blog width) and its "(former colonies)" suffix overflowed its own panel;
    chart 4's title aligned to the axes while charts 2 and 3 align to the figure, indenting it
    286 px from its own footnote; chart 4's bottom row was selected by an arbitrary tiebreak
    between Guyana and Uruguay, which the de-duplication fix had silently swapped. All fixed.
12. **Chart 1 was a determinist poster if shared standalone.** Its footnote's only editorial
    sentence pointed the wrong way. It now names the inversion in the frame that carries the claim.
13. **fc3 fires on a coin flip, not never.** "If the reversal had been absent, none of the three
    would have fired" is false: fc3 is a bare sign test, so with r_col near zero its sign decides.
    Softened to "need have fired" with the reason given.

## 6.3 Amendments from fact-check round 3

Round 3 ran seven refuter lenses over section 6.2's changes, then attacked every finding with three
independent skeptics before it counted. The skeptics killed 14 findings, four of them HIGH. That is
the first time this project has measured its own refuters' false-positive rate, and it is high.

1. **Amendment 6.2-8 was wrong and is withdrawn in place above.** Round 2's own correction
   reintroduced the failure mode that correction existed to fix.
2. **The never-colonised pair was on two different samples.** "minus 0.21 then and minus 0.29 now"
   is n=76 and n=85. On the 69 with both, the figures are -0.153 (t -1.27) and -0.041 (t -0.34), so
   the "now" figure collapses and neither is clear of chance. Corrected in the body;
   `never_colonised_common_sample` now ships in results.json. This is the A10 defect, reintroduced
   two paragraphs later by the very round-2 text that fixed A10.
3. **The close made a rank claim the rank statistics do not support.** On the 97 former colonies
   Spearman is +0.161 (p=0.115) and Kendall +0.106 (p=0.129); only Pearson clears, and it is carried
   by the eleven-country tied block the post's own chart footnote flags. "the hot places were the
   crowded ones" is now "hotter went with more crowded", matching chart 2's panel title.
4. **Three bivariate correlations cannot decompose anything.** "they tell you how much the
   thermometer is really carrying" invited a partial-variance reading; the actual partial reverses
   sign (+0.217 controlling for latitude and Africa, t +2.76, VIF 4.18, so not a collinearity
   artefact). The clause is replaced, and the replacement also supplies the gloss the Africa dummy
   had been shipping without.
5. **The tie-break added in round 2 never fired.** Guyana and Uruguay differ by one unit in the last
   place rather than tying exactly, so row order rested on float residue. The slide is now rounded
   to nine decimals and ties break on income then alphabetically. Five such pairs existed, not one.
   No correlation, no sample size and no Indonesia rank moved.
6. **The new assert found junk rows the old one could not.** Round 2's
   `assert (shortnam.str.len() > 0).all()` could never fail. Replaced with an ISO3 pattern check,
   which immediately surfaced 33 rows per file whose shortnam is a US state code, a bare ".", or the
   literal "notIndonesia". None carried an analysis value except `ex2col=0` on the "." row, which had
   been sitting in the never-colonised group as a phantom member. Filtered explicitly; no published
   figure moved.
7. **`temp1_sanity()` mixed frames.** Two fields were computed on the raw column while the rest used
   the matched frame, so the provenance audit quoted "323 rows, 89 at 7" for a 209-row object. Raw
   and matched counts are now reported separately.
8. **Smaller corrections.** "every sample size" to "most" (two did not change); "six published
   correlations" to "six published figures" (two are slopes); "stays positive at plus 0.17" to
   "falls to" (it fell from +0.28); "three orders of magnitude" to four (4.11); the 159-country
   sample described as AJR's file rather than as a subset of the modern 196; chart 1's footnote now
   names the yardstick the 1500 comparison uses; the de-duplication comment no longer claims YUG has
   the same shape as DEU and ZWE; the two loaders were made identical again.

**What the skeptic panel killed.** Four HIGH findings did not survive: that the atlas attribution was
unverifiable, that "concede ... and rely on it anyway" misreads AJR's concessive clause, that the
Malthusian caution is not AJR's, and one attack on the filter's validity. Also killed: an attack on
chart 2's panel titles and one on the tied-block footnote. This is recorded because the round's
findings are not themselves free of error, and a process that only logs what it caught is flattering
itself.

**Not finished.** 37 of the round's 67 findings never reached a skeptic, because the run hit a usage
limit. Five are HIGH. They are open, not refuted, and are listed in `docs/round4-scope.md`.
