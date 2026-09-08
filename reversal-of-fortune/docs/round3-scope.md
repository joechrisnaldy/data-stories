# Round 3 scope: everything fact-check round 2 changed

Round 3 verdicts ONLY the items below, plus any claim whose evidence these changes touch.
Round 1 verdicted the full claim inventory (`docs/claim-inventory-r1.md`); round 2 verdicted round 1's
changes (`docs/round2-scope.md`). This file is round 3's contract.

**Assume every one of these is wrong until checked. Round 2's own corrections are the least-checked
text in the repository, and on this blog that is reliably where the next round's worst findings are.
Round 2 proved the point: its two HIGH findings were both defects round 1 introduced.**

Body is FROZEN at 1,999 words against a 2,000 ceiling. Any fix that adds words must name what it cuts.

## A. Draft body sentences round 2 wrote or rewrote

- **A1** "What follows disputes what the correlation means." (was "Everything in it disputes")
- **A2** "about a fifth of the variation in **log** income" (was "national income")
- **A3** "On the 159 countries where all three can be measured, temperature manages minus 0.46,
  absolute latitude does better at plus 0.60, and a plain Africa dummy does better still at minus
  0.68." (replaced a three-different-samples comparison)
- **A4** "I left those out of an earlier draft, which was the wrong instinct: they tell you how much
  the thermometer is really carrying."
- **A5** "seventeen **places** above twenty degrees with incomes over forty thousand dollars, ten of
  them sovereign states and the rest territories" (was "seventeen countries")
- **A6** "per unit of land, with uninhabitable desert netted out, reconstructed from historical
  population atlases" (was "per unit of **arable** land, built from Colin McEvedy and Richard
  Jones's population atlas"). NOTE: the McEvedy and Jones names were REMOVED because no verified
  reference entry existed. Check whether "historical population atlases" is now too vague to be
  honest, and whether removing a named source to dodge a citation is the right trade.
- **A7** "Acemoglu, Johnson and Robinson, whose measure this is, concede the theoretical link is
  'more complex' than that and rely on it anyway"
- **A8** "their **other** measure runs through urbanisation, where the claim is that only places
  with high agricultural productivity **and a developed transport network** can support large towns"
- **A9** DELETED: "I come back to what that proxy can and cannot bear." Check nothing now dangles.
- **A10** "on a list that overlaps the first by 94." (replaced "in the same places")
- **A11** DELETED: "Hot places were not the dense places everywhere."
- **A12** "Among the **69 not on that list**" and "That group is AJR's residual rather than a list of
  untouched places; Bermuda and Puerto Rico are in it."
- **A13** "This is the test the argument actually rests on." (deleted the earlier-draft clause)
- **A14** "The gap between them is, with a t of minus 3.6."
- **A15** "I am not going to tell you what caused the reversal." (second sentence deleted)
- **A16 THE FILTER, entirely restated.** "**No explanation of the ranking between countries can have
  an effect that was both constant over the period and the same whether or not Europeans arrived.**
  The test is on the effect, not the cause: the equator has not moved, but what it does to
  prosperity may have. ... it cannot produce a ranking that inverted in one group and **did not** in
  the other. ... Outside that world heat ran the same way in both eras, **minus 0.21** then and
  **minus 0.29** now, which is the other half of the contrast."
  Round 2 refuted the previous version as INVALID (it equivocated between a constant cause and a
  constant effect, and had no domain restriction so it disqualified the Dell et al. result the post
  endorses). This replacement is the fix. **It is the single highest-risk item in the round.**
- **A17** "an earlier draft said something stronger and false: that a climate story cannot see the
  colonial split. Climate sees it extremely well."
- **A18** "It is disqualified only if **its effect** also held steady across the five centuries."
  (deleted "and the interesting geographic stories do not")
- **A19** "anything **whose effect** changed over those five centuries, and anything constant that
  acted differently depending on **whether Europeans arrived**" (was "who arrived")
- **A20** "That is a set, not an answer, and I am leaving it as a set. Less satisfying, and the
  honest shape of what the data supports: ..."
- **A21** "The middle of the distribution." and "The real reversals are brutal."
- **A22 THE DELL ET AL. PARAGRAPH, rewritten.** "Dell et al. (2012) ... a one degree warmer year
  **cut** growth that year by about **1.3** percentage points, with **no effect in rich countries
  they could tell apart from zero**. That is a within-country question rather than a question about
  the ranking between them, **so the filter above does not touch it**, and it is **evidence of** a
  real effect of heat on output." Round 2 found the previous 1.1 figure came from the superseded
  2008 NBER working paper.
- **A23** "Two problems with the comparison itself, on the record rather than buried."
- **A24** "and partly on things like latitude that shape income today, so the thing I am conditioning
  on sits **downstream of one side of the comparison and upstream of the other**. That minus 0.74 is
  the measurement of it."
- **A25** "density measures **production per unit of land**" (was "total production") and "**AJR
  raise that caution themselves.**"
- **A26** "Density is the wider-coverage second of AJR's two proxies rather than their first, and it
  **carries more weight here than any single variable should**."
- **A27** "The urbanisation measure is the **check** on that objection" (was "the answer")
- **A28 THE CLOSE, rewritten.** "because **among former colonies that same thermometer used to point
  the other way: the hot places were the crowded ones**. ... and **an explanation whose effect never
  changed and never depended on whether Europeans arrived** cannot." and "it cannot be **what
  inverted the ranking underneath it**." Round 2 found the previous close asserted an income ranking
  no code computes and reintroduced the Dell et al. contradiction in the most quotable position.

## B. Method notes round 2 rewrote or added

- **B1** "Two transforms, both load-bearing", rewritten: "Logging density is AJR's own specification;
  logging the 2023 income series is **my extension of it**. ... falls from minus 0.49 to minus 0.10
  **while the never-colonised one stays positive at plus 0.17** ... **the interaction that the
  argument actually rests on falls from a t of minus 5.3 to minus 1.4, which is not distinguishable
  from zero. The sign pattern survives the transform. The test does not.** ... everything above is a
  result about log density, and a reader following an unlogged recipe would reproduce the shape and
  not the significance."
- **B2** NEW: "One assumption that is not a measurement." The 1500 correlations use today's
  temperatures and assume rank stability over five centuries.
- **B3** "Two bugs", rewritten: "that row carries latitude but **neither density nor income** ...
  **Urbanisation was unaffected.** ... moved **six published correlations** at the second decimal and
  **changed every sample size in the post by one or two** ... **matches to the precision AJR publish**
  ... **A second round then found I had fixed that filter in the analysis script and left the dead
  copy in the chart script** ... enforced and asserted **in both scripts**."
- **B4** "none of the three **need have** fired, **because the third is a bare test of signs with no
  minimum size**."
- **B5** ADDED to the chart accounting: "Chart two was specified in advance as a global claim, that
  claim turned out false, and the chart was narrowed to former colonies after the data came back,
  which is the least clean of the four."
- **B6** NEW: "Evidence I loaded and did not use." Settler mortality and expropriation risk are in
  the file and were left alone.
- **B7** "Samples", rewritten: "69 **places absent from AJR's ex-colony list**... a residual, not a
  curated set... contains Bermuda, the Cayman Islands, Puerto Rico, Aruba and Cambodia among others.
  **Reclassifying all nine of the awkward cases as colonies leaves the interaction at a t of minus
  4.7**, so the result does not depend on where they sit."

## C. Code round 2 changed

- **C1** `build_analysis.py load()`: blank-string `shortnam` filtered before the merge; `kind="stable"`
  on the sort; `africa` added to the t5 selection; two new asserts; de-duplication comment rewritten
  (DEU/ZWE/YUG, "latitude but no density or income", "Urbanisation was unaffected", Table V not
  Table 6, "matches to the precision" not "reconciles exactly").
- **C2** NEW functions `temp1_sanity()` and `interact()`. The main interaction block was REPLACED by
  a call to `interact()`; verify it computes exactly what the inline code did.
- **C3** NEW results.json keys: `tidy_story_raw_dollars`, `rivals_common_sample`,
  `colonisation_vs_latitude`, `hot_and_rich`, `spread_24_28c`, `interaction_urbanisation`,
  `interaction_raw_density`, `flip_raw_density`, `withdrawn_temp1_sanity_check`, `robustness`,
  `density_ties`.
- **C4** `NON_SOVEREIGN` hardcoded set of 7 codes; `AWKWARD` hardcoded list of 9 codes. Both are
  judgment calls compiled into the analysis. Attack the membership of each.
- **C5** `ranks` tie-break: `sort_values(["slide","inc_pct"], ascending=[False,False], kind="stable")`.
  Round 2 found GUY and URY tie at slide -81.383 exactly and the de-duplication fix had silently
  swapped which one renders. Verify the new tie-break is deterministic AND that it did not change
  any published rank.
- **C6** `json.dump` moved inside a `with` block.
- **C7** `make_charts.py`: imports `WB_AGGREGATES` from `build_analysis` and asserts; chart 1 footnote
  rewritten to name the inversion and to read the raw-dollar r from results.json; chart 2 panel
  titles changed to "went with"/"goes with" and the "(former colonies)" suffix dropped; chart 2
  annotation moved from (0.03, 0.06) to (0.03, 0.93) with `va="top"`; chart 2 footnote gained the
  tied-density clause reading `density_ties` from results.json; chart 4 `set_title(loc="left")`
  replaced by `fig.suptitle(x=0.0)`; the `"BDI2": ""` junk NAME entry removed; the missing-name
  assert moved before the plotting loop.
  **A cross-module import is new. Check it cannot break the chart script's independence.**

## D. Documents round 2 rewrote

- **D1** `docs/2026-09-07-reversal-design.md`: AMENDED markers added to §3.1, §4 and §4.1 for stale
  pre-de-duplication figures; §6.1's "Table 6 Panel A" corrected to Table V Panel A column 1;
  `models.interaction` corrected to `interaction`; Appendix Table A1 relabelled; **NEW §6.2 with 13
  numbered round-2 amendments.** Every one of those 13 is a claim about what was found and fixed.
- **D2** `docs/provenance-audit.md`: the `ex2col` entry now records BOTH labels; the Appendix
  correction relabelled to "Appendix 2" for the QJE; a round-2 provenance note added to the sanity
  check; the stale NOTES bullet marked WITHDRAWN with its full previous text preserved.

## E. Standing checks that must be re-run because the text moved

- Every figure in the draft against `results.json` (round 2 reconciled 20 of them; the list changed).
- Every figure rendered in a PNG against the draft and `results.json`.
- Word count: body must be 1,600 to 2,000, measured as
  `awk 'NR>1 && NR<$(line of "## Method notes")' | grep -v '^!\[' | wc -w`.
- No em dashes, en dashes or Unicode minus in any file or rendered image.
- Every in-text citation has a reference entry and every entry is cited.
- Determinism: `build_analysis.py` then `make_charts.py`, twice, byte-identical.
