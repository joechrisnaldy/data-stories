# Post 23, adversarial fact-check round 1

Four independent refuter lenses against the 90-claim inventory in `claim-inventory-r1.md`. Roughly
eighteen HIGH findings survived adjudication. Two were post-blocking and forced a rebuild of two of
the three acts, which voided the Word-review approval and was escalated rather than fixed quietly.

## Post-blocking

**1. The road-death series was stale and the newer WHO figure inverted the argument.**
The draft used Our World in Data's copy of the SDG road-death rate, which stops at 2019, and called
2019 "the most recent year the World Health Organization has published for that indicator". WHO has
published 2021: GHO indicator `RS_198` returns 15.0 per 100,000 for GLOBAL, and the UN SDG database
returns 15.02 sourced to the Global Status Report on Road Safety 2023. Worse, the rate fell about a
sixth over the decade, so the draft's "road deaths barely moved" was beaten by WHO's own newer
number.

Fix: the transport act was rebuilt from WHO directly. It now uses the Global Health Estimates death
COUNT, one consistent series 2000 to 2021 from the same release as every disease-burden figure in
the post, which says something better and true: 1,177,422 killed in 2000, 1,174,078 in 2021. The
rate per person fell because there are more people. New indicators `RS_196`, `RS_198` and `RS_246`
are fetched from WHO's API in `fetch_data.py`. Chart 1 was replaced entirely.

Lesson: *a mirror's last row is not the source's last row.* A claim about what an institution has
published must be checked against that institution, never against a copy of it.

**2. The AI claim was refutable from the post's own reference list.**
The draft said there is no measure of what AI has done for human welfare, "not a weak one, not a
contested one", two paragraphs after citing the Stanford AI Index for its investment figures. The
AI Index's economy chapter carries estimates of AI's economic value, and randomised studies exist:
Noy and Zhang (2023) in Science, Brynjolfsson, Li and Raymond (2025) in the QJE. Both verified
through Crossref.

Fix: the body now claims only what the method note always claimed, that no population-level welfare
series exists to plot against investment year by year, and names the studies that do exist. Chart
4's in-panel text and footnote were rewritten to match.

Lesson: *the strongest universal negative in a piece deserves the same check as its numbers.* This
one was refuted by a document already in the bibliography.

## Findings that changed what the post is allowed to claim

**3. The market refutation does not carry as written.** The proxy is a burden SHARE, not a market
size, and healthy years lost are not revenue. Multiple sclerosis therapies are priced in the tens
of thousands per patient-year; back pain is generics and physiotherapy across millions. The post
now claims only that where the paying patients live does not predict where the research goes, and
says the revenue version was not tested.

**4. The money section is null, not "softer".** The draft said the money showed the same pattern
more faintly. Running the target binary against NIH dollars returns t of minus 1.50. Not attenuated,
absent. New model `money_m4_no_target` added and the paragraph rewritten as a correction.

**5. Road injury cannot be mapped onto the registry, and it is the most influential point.** Every
pre-registered term was crash vocabulary; ClinicalTrials.gov files trauma by pathology (traumatic
brain injury 2,610, fractures 4,815 against road injury's 338). So the "most generous term"
guarantee is false for this one condition. Dropping it: high-income basis t goes minus 3.05 to
minus 2.50 and survives; global basis goes minus 2.26 to minus 1.71 and does not. The point stays
in, because removing an observation after seeing its residual is the move this repository refuses.
New models `drop_road_injury_hi` and `drop_road_injury_global`, and a probe file recording the
alternative terms.

## Factual corrections

| Was | Is |
|---|---|
| Migraine listed among conditions with no target | Migraine is coded `t1=True` (CGRP) and renders blue; removed from that list |
| "Malaria is up in the top left" of chart 2 | Third lowest of 34 by trial count; now "far left and well above the fitted line" |
| "Strip out HIV, tuberculosis and malaria" | Removes two rows; malaria was already out because its US burden rounds to zero. n = 29, now stated |
| "31 conditions" in the money analysis | 31 rows covering 32 conditions, road injury and falls merged |
| "I coded every condition, before running any of this" | The admission that a vetting table was read first now sits at the claim, not 80 lines later |
| MS cited inside "Among the twelve largest burdens" | MS is not in that panel; the sentence now says so |
| "no rich-world market for a malaria drug at all" | Softened; tafenoquine was FDA-approved for prophylaxis in 2018 |
| AI investment attributed to Stanford HAI | Quid via the AI Index, and the figures are constant 2021 dollars |
| "Epoch AI tracks 527 notable models" | Our World in Data's copy of the Epoch series carries compute for 527 systems |
| Back pain "one of the most thoroughly monetised conditions", unsourced | Cited to Dieleman et al. (2020), largest of 154 conditions at $134.5bn |
| COVID-19 burden ranking computed in a throwaway shell command | `burden_ranking()` in `build_analysis.py`, asserted, in `results.json` |
| README: "One of them fired" about the falsification conditions | None fired; what failed was the section 3.2 ordering, a different thing |
| References dated 2026 with wrong producers, no retrieval dates | Producers corrected, retrieval dates added, WHO road safety dated 2023 |

## Chart defects visible only in the rendered images

- Chart 3: the left panel's fitted line was drawn straight through the right panel's "Road injury
  and falls" tick label. Fixed by widening the figure and the gridspec `wspace`.
- Chart 4: the transport outcome bar was clipped flush against the axis spine by `xlim(-3, ...)`,
  so a large fall and a small one rendered nearly the same length, which the design doc explicitly
  forbids for that chart. The lower limit is now derived from the data.
- Chart 1 (old): the annotation printed "0.01% in 2010" against the prose's 0.012 percent, a `.2f`
  format string. Moot after the rebuild, but it is the same class of defect.

Reading the chart code catches none of these. Opening the PNG catches all three.

## Transferable lessons

1. **A mirror's last row is not the source's last row.** Anything asserted about what a body has
   published gets checked against that body.
2. **Check the strongest sentence in the piece as hard as the numbers.** The AI universal negative
   was the single most quotable line and the least verified.
3. **A "most generous option" guarantee is only as good as the vocabulary the candidate list is
   written in.** Road injury's terms were exhaustive within the wrong vocabulary.
4. **Assertions catch broken builds; scorecards catch failed hypotheses.** Keeping the pre-registered
   predictions as printed pass or fail rather than as `assert` statements is what let the ordering
   failure be reported instead of crashing or being quietly recoded.
5. **A shared category must be merged, not deduplicated.** Keeping road injury and dropping falls
   credited one condition with the pair's whole budget against half the harm.
