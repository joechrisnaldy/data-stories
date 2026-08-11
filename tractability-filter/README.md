# Greed You Can Regulate. Difficulty You Have to Pay For.

Post 23 in the data-stories series. Not yet published; the live URL will be
https://joechrisnaldy.com/blog/greed-you-can-regulate-difficulty-you-have-to-pay-for

## The question

Does advanced technology actually make human life better, or is it just about money?

The answer this post reaches is neither. Research effort tracks the size of a human problem only
weakly, and it does not track where the paying patients live. What it tracks best, of the things
that can be measured here, is whether the problem has a handle on it: something to aim at and
something to measure.

## What the analysis found

**Transport.** The World Health Organization's own Global Health Estimates deaths tables put road
deaths at 1,184,514 in 2000 and 1,182,759 in 2021. Two decades and the number is almost unchanged. The per-person rate did fall, by 23
percent, and that is the denominator: 29 percent more people alive, no fewer dying. By WHO's own
published global split, occupants of four-wheeled vehicles are 25 percent of road deaths, riders of
powered two and three wheelers 30, pedestrians 21, cyclists 5, and the remaining 19 percent are
buses, heavy goods vehicles and users WHO records as other or unknown. Separately, between 2010 and 2025,
electric vehicles went from 0.012 percent of new car sales to 25 percent. The engineering went into
the object three in four of the victims were never inside.

**Effort does not track damage.** Across 34 conditions, high-income disease burden accounts for
about 9 percent of the variation in registered clinical trials, by adjusted R squared on the logs.
Back and neck pain is the third largest single cause of lost healthy life in rich countries, behind
COVID-19 and ischaemic heart disease. It carries 36 times the high-income burden of multiple
sclerosis and draws 1.6 times the trials, and it is not an unprofitable condition: it was the
largest single category of US health spending of 154 conditions studied, 134.5 billion dollars in
2016 (Dieleman et al., 2020).

**The market proxy predicts nothing, but proves less than it looks.** High-income share of global
burden returns a t of 0.71. Malaria, with 2,541 high-income healthy years lost out of 52.1 million
worldwide, still has 1,472 trials and drew 239.8 million NIH dollars in one year. But a burden
share is not a market size and healthy years lost are not revenue, so the claim the repository
supports is narrower: **where the paying patients live does not predict where the research goes.**

**What works is one binary.** Conditions with a validated biological target draw a median 1,448
trials per million high-income healthy years lost; those without draw 300. That raw ratio flatters
the effect, because the no-target group carries twice the median burden: holding burden constant
the gap is about two and a half times. It survives, at a t of minus 3.05, and adding that yes or no
lifts the variation accounted for from 9 percent to 28.

**Money is the least explained thing here.** American disease burden accounts for essentially none
of American research spending: t of 0.77 and a negative adjusted R squared across 31 rows covering
32 conditions. Dementias draw 895 dollars per healthy year lost in the United States, back and neck
pain 11.5. The target binary that works on trials is inconclusive on dollars: the coefficient points
the same way at about three-quarters the size, but at t of minus 1.50 the interval runs from a large
gap through zero to a small one the other way. The money cannot settle it.

## What failed, and is reported rather than buried

- **The pre-registered three-step gradient does not hold.** Conditions coded least tractable sit
  above the middle group, 642 trials per million against 362, because psychiatry runs enormous
  trial programmes with nothing to aim at. Depression has 12,693 trials, anxiety 10,400, both more
  than back and neck pain.
- **One condition is not measurable and it is the most influential point.** Road injury is a cause
  of injury, not a condition a registry indexes. Every pre-registered term was crash vocabulary
  while ClinicalTrials.gov files trauma by pathology. Drop it and the finding holds on the
  high-income basis at t of minus 2.50 and weakens on the global basis to minus 1.71, p of 0.098. It is left in
  rather than removed after seeing its residual.
- **Two borderline cases declared in advance still cut against the thesis** and are named in the
  post: drug use disorders and uncorrected refractive errors.
- **One of the three pre-registered falsification conditions fired.** All three are now scored in
  `results.json` under `scorecard`, because round 2 found that only the first had ever been
  computed while this README asserted all three had been checked. FC1 (a market measure beats
  tractability) did not fire. FC2 (the gap vanishes under the most generous terms) did not fire,
  with the road injury caveat. **FC3 fired**: the class ordering is tractable, intractable, partly
  by trials and tractable, partly, intractable by dollars. Round 4 added the half of that which
  cuts against the post's own narrative: the three-step gradient the post says it abandoned is the
  order the DOLLARS produce. It is abandoned because it fails on trials, the measure the argument
  rests on. On dollars the gradient is real, at a median 300, 160 and 135 dollars per American
  healthy year lost. Round 5 found those medians had been computed on the unmerged condition list,
  which double-counted the shared road injury and falls category and made the top two look 4
  percent apart when they are 47.

## Round 1 of the fact-check rebuilt two of three acts

Four independent refuter lenses returned roughly eighteen HIGH findings against a 90-claim
inventory. Two were post-blocking and are recorded in `docs/round1-fixes.md`:

1. The road-death series came from a mirror that stops at 2019 and the draft called that "the most
   recent year WHO has published". WHO has published 2021. The transport act was rebuilt from WHO's
   own API and Global Health Estimates.
2. The AI section asserted no measure of AI's effect on people existed, "not a weak one, not a
   contested one", which is refutable from the post's own reference list. It now claims only that
   no population-level welfare series exists to plot, and cites the randomised studies that do.

The tractability coding survived the attack: a refuter re-ran the regression with every clinically
disputable condition flipped and reported that each flip strengthened the result. That check was
run inside the refuter's own scratch workspace and is not reproducible from this repository, so it
is recorded here as testimony rather than as a result.

## Round 4 changed a bolded number and the AI punchline

**Round 5 superseded the road-user half of this section, and round 6 superseded round 5's opening numbers. The 30 percent below is wrong, so is the 70 percent derived from it, and so is the 31.3. See "Round 5 corrected the road user split for the third time" at the end. This account is kept because a deleted mistake teaches nobody anything.**

Four rounds ran. Every round's worst findings lived in the previous round's own corrections, and
round 4 was no exception; it also found two things older than round 3.

1. **The road user split was a subsample recomputation that disagreed with its own source.** The
   post led with "about 22.8 percent of road deaths are people inside a car", computed here from
   WHO's country-level indicator RS_246. WHO's Global status report on road safety 2023, the
   upstream source of that indicator and already in this post's reference list, publishes **30
   percent**. The completeness filter is the difference: it cuts the sample from 139 countries
   covering 66 percent of the world's road deaths to 82 covering 37, and across all 139 the same
   calculation gives 31.3 percent. WHO's figure is now the one the post quotes, the recomputation
   is in `results.json` under `transport.user_split_disagreement` on both filters, and the post
   reports the spread. The argument survives unchanged: 70 percent of road deaths are people who
   were never in a car.
2. **The AI claim was refuted from the post's own source for the second time.** Round 1 killed "no
   measure exists". Round 3 replaced it with "no population-level welfare series exists" by
   dropping the word *agreed*, and the Stanford AI Index, the publication this post's investment
   line comes from, carries a population-level US consumer-surplus estimate of 116 billion dollars
   rising to 172 billion. The post now cites it and claims only that no agreed year-by-year series
   exists to run alongside the money, which is a sharper point than the one it replaces.
3. **Three NIH categories are wider than the condition they stand for**, which section 3.5 of the
   design document always required the post to disclose and the post never did. The worst case is
   the post's own showpiece of self-criticism: refractive errors at 2,812 dollars per American
   healthy year lost is all of eye disease over one condition's damage.
4. Two assertions in `build_analysis.py` encoded claims the essay makes rather than structural
   facts, so the build would have crashed rather than the essay changing. They are warnings now.
5. A chart 2 label sat on the wrong marker, making the picture appear to code depression as having
   a validated target. Two labels were moved after measuring the render; round 5 found a third.

## Files

| File | What it does |
|---|---|
| `conditions.py` | The 34 conditions, search terms, NIH categories, and the pre-registered tractability coding |
| `fetch_data.py` | Downloads all sources into `data/`; `nih` and `roads` arguments re-run single stages |
| `build_analysis.py` | Every number in the post, into `results.json` |
| `make_charts.py` | The four charts in `charts/` |
| `results.json` | Committed output; the post quotes nothing that is not in here |
| `docs/2026-08-10-tractability-filter-design.md` | Binding design document, amendments marked in place |
| `docs/round1-fixes.md` | What round 1 of the fact-check found and what changed |
| `docs/claim-inventory-r1.md`, `docs/round4-scope.md`, `docs/round5-scope.md`, `docs/round6-scope.md` | The claim inventories each round was checked against |
| `data/README.md` | Sources, download instructions, and the traps hit while building this |

## Reproducing

```bash
pip install -r ../requirements.txt
python3 fetch_data.py
python3 build_analysis.py
python3 make_charts.py
```

Data files are gitignored. `fetch_data.py` rebuilds them from public APIs and direct downloads.

## Round 5 corrected the road user split for the third time

Round 4 replaced a subsample recomputation with what it believed was WHO's published figure. It had
taken that figure from WHO's launch **news release**, not from the report, and the release
contradicts the report it announces: it puts four-wheeled occupants at 30 percent, which is the
report's share for **motorcyclists**, and prints a 3 percent micro-mobility share the report says
does not exist globally. The report itself, stating it three times on pages 10, 15 and 17, gives
riders of powered two and three wheelers 30 percent, occupants of four-wheeled vehicles 25,
pedestrians 21, cyclists 5, and its own 19 percent residual. The post says 25 percent and "three in
four", and the argument came out stronger than it was at 30 and "seven in ten".

Round 5 also withdrew the 31.3 percent figure round 4 had published as the upper end of a bracket
around WHO. Six of the 139 reporting countries returned exactly one category, all of them
four-wheel, and renormalising a lone category to its own sum scales it to 100 percent; those six
supply 34.8 percent of the 31.3. Excluding them the recomputation returns 22.9, against the complete
filter's 22.8. There was no upper end.

Three more from that round. The class dollar medians were computed on the unmerged condition list,
so road injury and falls each carried the whole shared category and the top two classes looked 4
percent apart when they are 47. The road-death rate sentence rested on population figures that
existed in no script, and now comes from the Global Health Estimates' own population rows. And
`conditions.py` had acquired a round-4 claim that no condition was coded on the causal-agent limb
of the rule, which three of them are.

## Round 6 went after provenance rather than prose

Rounds 2 to 5 each asked what the previous round had broken, and each found that it had broken
something. Round 6 asked a different question: which external figure in this post has nobody opened
the primary document for? That found the oldest error in the piece.

**The opening sentence was quoting a mirror.** The post said "By the World Health Organization's
Global Health Estimates, 1,177,422 people were killed" and cited WHO. Those figures are Our World
in Data's aggregation. WHO's own deaths tables, cause code 1530, say 1,184,514 and 1,182,759, and
OWID's country values differ from WHO's published country file in 177 of 183 countries. `fetch_data.py`
now downloads WHO's deaths workbook and the headline figures come from it. The check that settles it:
the 2021 rate this derives, 14.897 per 100,000, is exactly the crude death rate WHO prints in the
same row. OWID's annual series is kept for the shape of the curve, because WHO publishes six years
rather than an annual series, and it is labelled as such wherever it appears.

**Three figures had only ever been read in an abstract.** Dieleman is "low back and neck pain" and
the study covers 85.2 percent of US health spending; Hartung's 60,000 dollars is a pre-rebate
acquisition cost against 41,000 to 53,000 after rebates; the 527 AI systems are this repository's
count of OWID's snapshot rather than Epoch AI's own number.

**And the method note written in round 5 to warn about WHO's inconsistent totals had itself taken a
year from a press release.** The fact sheet says "approximately 1.16 million people die each year"
and names no year at all.

Round 6 also found two defects round 5 introduced: `vuln()` still matched a label that had been
renamed, so every vulnerable-road-user share in `results.json` was computed as 100 minus "other";
and the chart 2 leader line round 5 moved to clear the multiple sclerosis marker was moved into it.
