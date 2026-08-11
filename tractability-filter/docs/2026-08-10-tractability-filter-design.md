# Post 23 design: Greed You Can Regulate. Difficulty You Have to Pay For.

Binding design document. Written 2026-08-10, before any analysis script exists and before any
residual has been examined. Amendments are marked in place (AMENDED / WITHDRAWN / SUPERSEDED)
rather than edited silently, so that a refuted decision cannot quietly return.

Blog slug: `greed-you-can-regulate-difficulty-you-have-to-pay-for`
Repo folder: `Projects/analytics-blog/tractability-filter/`

---

## 1. The question and the answer

The reader's question, in the form it was asked: with all this advanced technology, does it really
benefit human lives, or is it just for money?

The post's answer: neither. Research effort does miss the largest human problems, but the filter
is not profit. It is tractability. Money and effort go where the work is easy, meaning where there
is something to aim at and something to measure. The problems that resist study are not the
unprofitable ones. They are the ones that will not hold still.

This matters because it changes the remedy. A profit filter is regulable. A difficulty filter is
not: it has to be deliberately paid for, by someone willing to fund work that will look
unproductive for a long time.

## 2. Structure

Three acts, escalating, no Indonesia frame, target 1,800 to 2,000 words.

1. **Transport.** We know precisely what kills people on roads, and the number barely moves. The
   money goes to electrification and autonomy, which are tractable engineering problems with clean
   metrics. Sets the pattern.
2. **Medicine.** Carries the proof, because it is the only one of the three where effort and human
   cost are measured on comparable units for the same conditions. Two charts.
3. **AI.** Shortest, and the punchline. The input side is measured to the petaflop; the benefit
   side has no denominator at all. The pattern is not history, it is happening now at maximum speed.

Closing line: greed you can regulate, difficulty you have to choose to pay for. The title is that
line, so the close must be a sharper earned variant, not a repetition. Handled at draft time.

## 3. Pre-registered method

### 3.1 The measurements

- **Research effort** = count of studies registered on ClinicalTrials.gov whose condition field
  matches the query term for that condition. Registry-wide stock, all years, retrieved via API v2
  `countTotal`. ~~A date-windowed count (registered 2015 onward) is computed alongside as a
  robustness check, because registry coverage grew sharply after the FDA Amendments Act of 2007.~~
  **WITHDRAWN 2026-08-10, fact-check round 3: never computed.** Round 4 sharpens the wording,
  which was too loose: no date-windowed count was computed FOR ANY CONDITION. A date-windowed
  query does exist in `fetch_data.py`, but it is registry-wide by calendar year and feeds chart
  4's medicine row, which is a different object and no robustness check on anything.
  Recorded rather than deleted, because a silently dropped robustness check is indistinguishable
  from one that was run and disliked.
- **Research money** = sum of `award_amount` over NIH projects tagged with the corresponding RCDC
  spending category, from RePORTER API v2, most recent complete fiscal year. RCDC categories
  overlap by construction and do not sum to the NIH total; this is NIH's own documented behaviour
  and the post must say so rather than presenting the categories as a partition.
- **Human cost** = DALYs, WHO Global Health Estimates 2021 (July 2024 release), both the
  high-income economies aggregate and the global total. High-income is the primary basis for the
  market test because that is where the paying patients are.

### 3.2 The tractability coding, fixed now

Every condition is coded on two binary axes from clinical reference material, and the coding is
committed to the repository BEFORE any regression is run or any residual is inspected.

- **T1 TARGET.** Is there a validated biological target or identified causal agent that an
  intervention can act on? A pathogen, a receptor, a protein, a tumour, a defined autoimmune
  process. Yes or no.
- **T2 ENDPOINT.** Is the primary outcome objectively instrument-measurable rather than
  patient-reported? Survival, viral load, HbA1c, lesion count on MRI, tumour response count as yes.
  A pain score or a mood scale counts as no.

Class: **tractable** = T1 and T2. **Partly tractable** = exactly one. **Intractable** = neither.

Predicted ordering of research effort per unit of burden: tractable > partly > intractable.

### 3.3 The competing explanation, also fixed now

The profit hypothesis is operationalised without any judgement call, straight from the burden data:

- **Market proxy** = high-income share of global burden for that condition, that is
  `HI DALYs / Global DALYs`. A condition concentrated in rich countries has paying patients; a
  condition concentrated in poor countries does not.

Both explanations are entered against the same outcome. The post reports which survives.

### 3.4 Falsification conditions

The thesis is wrong, and the post says so and becomes a different post, if any of these hold:

1. Controlling for burden, the market proxy predicts research effort and the tractability coding
   does not.
2. The effort gap between tractability classes disappears when the most generous search term is
   used for every low-effort condition.
3. The ordering reverses between the trial-count measure and the NIH dollar measure.

### 3.5 Guardrails against rigging

- **Adversarial term selection.** For every condition, alternate ClinicalTrials.gov query terms are
  tested and the term that returns the MOST trials is used. The test is loaded against the thesis
  by construction. All alternates and their counts are recorded in `results.json`.
- **AMENDED 2026-08-10: the maximise rule applies to trial search terms only, not to NIH
  categories.** A ClinicalTrials.gov condition query cannot reach beyond the condition, so taking
  the largest count is pure generosity. An RCDC category can be strictly broader than the disease:
  "Chronic Pain" covers far more than back and neck pain, and "Arthritis" covers both of the
  arthritis conditions here. Maximising there would not be generosity, it would be crediting a
  condition with other diseases' money, and it would inflate the tractable conditions just as
  readily as the intractable ones. Rule instead: use the most specific RCDC category matching the
  GHE cause, uniformly, with no maximisation. Broader alternates are fetched and reported in
  `results.json` as a robustness check, and where the primary category is known to be broader than
  the cause (liver disease for cirrhosis, eye disease for refractive errors) the post says so.
- **Documented exclusion.** Leukaemia has no general RCDC category, only "Childhood Leukemia", so
  it is excluded from the money analysis and kept in the trials analysis. Road injury and falls
  share one RCDC category, so for the money analysis only they are combined into a single row with
  their DALYs summed. Neither exclusion was chosen after seeing a residual.
- **No post-hoc reclassification.** A condition's tractability class may not be changed after its
  residual is seen. If a coding looks wrong, the change is logged in this document with a reason
  that does not reference the residual.
- **NIH reconstruction is validated.** WITHDRAWN 2026-08-10, fact-check round 3. The comparison
  against NIH's own published RCDC figures was never run. The post uses cautious wording it never
  earned: nobody knows whether the reconstruction would have passed. The post now states this in
  the money section rather than only here, because it is the missing counterweight to the most
  quotable sentence in the piece. **Round 4 adds two things.** First, this bullet's original text
  was replaced rather than struck through, which breaks the rule at the top of this document; the
  original wording is unrecoverable, so the post no longer quotes a specific number of categories
  it was supposed to check. Second, the published RCDC figures were never even downloaded, so the
  check was not merely skipped: nothing in `data/` would have supported it.
- **Two burden bases reported.** Trials are global; high-income DALYs are not. Every effort-per-
  burden figure is computed on both the high-income and the global basis, and the post states
  which one it is quoting.

### 3.6 What the coding is and is not, recorded against myself

**The coding is not blind, and pretending otherwise would be the exact failure this post is about.**
A vetting table of trials per unit of burden was computed and read on 2026-08-10 BEFORE the coding
rule in 3.2 was written down. The rule is theory-driven and mechanically checkable by any reader
from clinical reference, but I had already seen the ordering it would produce. That is a real
limitation and it goes in the post's method notes, not just here.

Three consequences follow, all binding:

1. **The headline evidence does not depend on the coding at all.** Back and neck pain carries
   roughly 36 times the high-income burden of multiple sclerosis and draws fewer than twice the
   trials. Malaria has essentially no high-income burden and still draws over a thousand trials.
   Those are facts about burden and trial counts. The tractability coding is corroboration and the
   post must present it as corroboration, never as the proof.
2. **A stricter single-axis variant is reported alongside.** T1 alone, the presence of a validated
   biological target, involves less judgement than the two-axis class. If the two disagree, both
   are reported.
3. **Borderline cases are named in advance, not discovered later.** Drug use disorders is coded
   tractable under the rule (receptor targets exist, urine toxicology is objective) despite low
   measured effort, and uncorrected refractive errors is coded tractable despite low measured
   effort because its remaining problem is delivery rather than discovery. Both cut against the
   thesis. They stay in. Removing an inconvenient case after seeing it is rigging.

## 4. Chart spine

Exactly four charts, prefix `tf-`. House palette and matplotlib settings as in prior posts
(`axes.unicode_minus: False`, `text.parse_math: False`).

**`tf-1-what-we-fixed-and-what-we-did-not.png`** (transport) **WITHDRAWN 2026-08-10 after
fact-check round 1.** Panel A used Our World in Data's copy of SDG indicator 3.6.1, which stops at
2019, and the draft called that WHO's latest published year. WHO has published 2021, and the rate
fell about a sixth over the decade, which beats the "nearly flat" reading this chart was built to
show. Do not reinstate.

**`tf-1-who-dies-and-what-we-rebuilt.png`** (transport) REPLACEMENT, locked 2026-08-10.
~~Panel A: share of the world's road deaths by road user type, WHO Global Health Observatory
indicator RS_246 (2016 shares) weighted by RS_196 (2021 death counts).~~ **AMENDED 2026-08-10 after
fact-check round 4, and SUPERSEDED 2026-08-11 by round 5: the road-user figures in this round-4 paragraph are wrong, though its 22.8, 139, 66 percent, 82 and 37 percent still stand, and section 5.4 item 1 has the corrected split. Kept because a replaced amendment is indistinguishable from one that was never made.** That recomputation put car
occupants at 22.8 percent. WHO's own Global status report on road safety 2023, the upstream source
of RS_246 and a document this post already cites, publishes 30 percent. The gap is the completeness
filter: requiring all five categories present drops the sample from 139 countries covering 66
percent of the world's road deaths to 82 covering 37 percent, and across all 139 the same
calculation returns 31.3 percent. Publishing a subsample recomputation in bold, seven points below
the cited source and in the direction that flatters the argument, is the failure this post is
about. Panel A now plots WHO's published split, with the 17-point residual drawn in grey and
labelled a residual because WHO does not publish it as a figure. The recomputation survives in
`results.json` under `transport.user_split_disagreement`, on both filters, and the post states the
spread. Do not reinstate the recomputation as the headline.
Panel B: electric car share of new car sales, World, 2010 to 2025.
The caption must state the source of panel A, the residual, the disagreement with the
recomputation, and that the panels share no unit. The claim the chart carries is that the
engineering went into the vehicle a minority of the victims are inside, which survives at 30
percent and does not depend on any trend in the death rate.

**`tf-2-burden-against-effort.png`** (medicine, the core)
Log-log scatter. x = high-income DALYs, y = registered trials. ~~Roughly 30 labelled conditions.~~ The built chart labels 16.
Point colour = pre-registered tractability class. AMENDED 2026-08-10: the built chart colours by
the T1 binary (validated biological target, yes or no), not by the three-class coding, because the
three-class ordering failed and the binary is what survived. Legend and prose use the same words,
which round 4 had to enforce: round 3 unified the PROSE on "causal target" while the legend, the
coding file, the README and section 3.2 all said "biological". Section 3.2 is the pre-registration
and wins; the prose changed back. AMENDED AGAIN 2026-08-10, round 4: "roughly 30 labelled
conditions" above is wrong for the built chart, which labels 16 and would be unreadable with 30,
and the claim sentence below still used three-class vocabulary this document had already dropped.
OLS fit on the logs drawn as a reference line. The claim the chart carries: at any given burden,
conditions with a validated biological target sit above the line and those without sit below.

**`tf-3-two-explanations.png`** (medicine, the money) **WITHDRAWN 2026-08-10.** Never built. The
built chart is `tf-3-money-against-damage.png`: panel A is a log-log scatter of US burden against
NIH dollars with the fitted line, panel B a ranked bar of dollars per US healthy year lost for the
twelve largest high-income burdens, both coloured by the validated-target binary. Round 2 found the
substitution had happened silently, and round 3 found this heading still standing after that. The
original specification below is superseded and must not be reinstated.
Two panels testing the two hypotheses head to head, using NIH dollars per DALY as the outcome so
that money appears explicitly.
Panel A: NIH dollars per DALY against the market proxy (high-income share of global burden).
Panel B: NIH dollars per DALY by tractability class.
If the thesis holds, panel A is flat or noisy and panel B separates cleanly.

**`tf-4-the-input-we-count-the-outcome-we-do-not.png`** (AI, and the synthesis) LOCKED 2026-08-10.
One row per domain, paired bars: change in the input measure against change in the human outcome
measure over a comparable and explicitly stated window. Medicine pairs registered trials against
burden.

AMENDED 2026-08-10 after fact-check round 1, both corrections forced and neither optional:
transport now pairs electric car share of new sales against the COUNT of people killed, not the
death rate, because WHO publishes only a single year for the rate and the count is one consistent
series; and the AI row's reason is that no AGREED POPULATION-LEVEL WELFARE SERIES exists to plot,
not that no measure of AI's human benefit exists. The stronger original wording was refuted from
this post's own reference list and must not return.

Rules for this chart, because a chart with a deliberately empty bar is one bad decision away from
being a rhetorical trick rather than a finding:
- The empty slot must be visibly an absence of data, not a zero. A zero-length bar is forbidden.
- Each row states its own window in the row label. The windows differ and the chart must say so.
- The two bars in a row do not share a unit and the axis is labelled percent change, not level.
- If a reader cannot see from the chart alone that the three rows are measured over different
  windows, the chart is wrong and gets redrawn rather than footnoted.

## 5. Data sources

| Source | Use | Access |
|---|---|---|
| WHO Global Health Estimates 2021, July 2024 release, DALYs by cause and World Bank income group | burden | `cdn.who.int` xlsx, direct download |
| Same release, DALYs by cause and country (2021, 2010) | US burden for the money analysis; world population rows | `cdn.who.int` xlsx |
| Same release, DEATHS by cause, global | the road death totals the post opens on, cause code 1530 | `cdn.who.int` xlsx, added round 6 |
| Brynjolfsson et al. (2026), What is Generative AI Worth? | the consumer-surplus pair | working paper PDF |
| ClinicalTrials.gov API v2 | research effort | public, no key, `countTotal` |
| NIH RePORTER API v2 | research money | public, no key, POST search |
| ~~OWID grapher, WHO SDG 3.6.1, road deaths per 100,000~~ | WITHDRAWN, stops at 2019; downloaded but unused | grapher CSV |
| WHO Global Health Observatory API, indicators RS_196, RS_198 | road deaths, death rate | GHO API, direct |
| ~~WHO GHO indicator RS_246~~ | ~~road user split~~ WITHDRAWN round 4 as the published figure; retained as a disclosed disagreement | GHO API, direct |
| WHO Global status report on road safety 2023 | the road user split the post quotes | WHO publication and launch statement |
| WHO Global Health Estimates, road injury deaths by country and year | the 2000 to 2021 death count series | via OWID's copy, stated as such in the post |
| OWID grapher, IEA | electric car share of new sales | grapher CSV |
| OWID grapher, Epoch AI | training compute of notable AI systems | grapher CSV |
| OWID grapher, Stanford AI Index / Quid | private and corporate AI investment | grapher CSV |

Data files are gitignored. `data/README.md` records exact URLs and download instructions.

### 5.1 Access traps already hit and their fixes

1. This machine's Python has an **empty CA bundle** (`cert_store_stats` returns zero x509).
   ~~Fix: resolve a CA file explicitly (`certifi`, then `/etc/ssl/cert.pem`, then Homebrew's
   openssl bundle).~~ **CORRECTED 2026-08-10, fact-check round 4: that is not what was built.**
   `fetch_data.py` shells out to `curl` for every request and never imports `ssl`, so it uses the
   system trust store. `data/README.md` had this right and this document did not. Verification was
   never disabled either way.
2. **ClinicalTrials.gov rejects urllib** with HTTP 403 regardless of User-Agent, but serves curl.
   Fix: shell out to curl for that host.
3. **OWID returns HTTP 403 for IHME-sourced charts** ("non-redistributable"). All IHME burden
   charts are unavailable this way, which is why burden comes from WHO GHE directly. WHO-sourced
   OWID charts do download.
4. **GHE cause codes are not guessable.** Code 970 is Epilepsy and 980 is Multiple sclerosis, the
   reverse of the obvious guess. All lookups are keyed by exact cause name, not by code, and the
   parsed cause list is asserted non-empty for every name used.

## 5.2 Amendments after fact-check round 1, 2026-08-10

Recorded here rather than applied silently, per the rule at the top of this document. Full detail
in `round1-fixes.md`.

1. **Road deaths are sourced from WHO directly**, not through Our World in Data. Indicators RS_196,
   RS_198 and RS_246 are fetched from the Global Health Observatory, and the death-count series
   comes from the same Global Health Estimates release as every disease-burden figure here.
2. **Chart 3's built form differs from the section 4 specification** and this was not marked at the
   time, which was itself a breach of this document's rule. The specification called for market
   proxy against class; the built chart pairs a burden-versus-dollars scatter with a ranked
   dollars-per-DALY panel. AMENDED to the built form.
3. **The exclusion of HIV, tuberculosis and malaria from the money models is post-hoc.** It is not
   in section 3.5 and it moves the slope from t 0.77 to t 2.23. It is now reported only as a
   secondary reading, with the unrestricted model as primary, and this amendment is the disclosure.
4. **The maximise rule for ClinicalTrials.gov terms has one documented failure**, road injury,
   whose candidate list was exhaustive within crash vocabulary while the registry indexes trauma by
   pathology. The pre-registered terms stay, the failure is disclosed, and models
   `drop_road_injury_hi` and `drop_road_injury_global` report what it is worth.
5. **The market proxy is demoted.** It tests where paying patients live, not market size, and the
   post no longer claims to have refuted the profit explanation in general.
6. **The AI claim is narrowed** from "no measure exists" to "no population-level welfare series
   exists to plot", the only version the evidence supports.

## 5.3 Amendments after fact-check round 4, 2026-08-10

Round 4 ran four refuter lenses against round 3's replacement prose and the re-rendered images.
Full scope in `docs/round4-scope.md`.

1. **The road user split is WHO's published figure, not a recomputation.** See the chart 1 entry in
   section 4. This changed a bolded number in the post from 22.8 to 30 percent.
2. **The AI absence claim is narrowed a second time.** Round 3 dropped the word AGREED, which
   section 4 had made binding, and the result was refutable from the post's own investment source:
   the Stanford AI Index carries a population-level US consumer-surplus estimate, 116 billion
   dollars rising to 172 billion. The post now cites it and claims only that no AGREED year-by-year
   series exists to run alongside the money.
3. **T1 is named "validated biological target" everywhere.** Section 3.2 is the pre-registration
   and the prose was the outlier.
4. **Three NIH categories are wider than the condition they stand for** and the post now says so,
   as section 3.5 always required: refractive errors under all eye disease, cirrhosis under all
   liver disease, drug use disorders under substance misuse. The refractive-errors figure is the
   post's own showpiece of self-criticism and was inflated by this.
5. **Three assertions in `build_analysis.py` encoded post claims rather than structural facts** and
   would have crashed the build if the essay stopped being true. Round 5 finished the job: they are
   scored into `results.json` under `scorecard.post_claims_still_true`, because a warning printed
   during a build nobody watches is not a check either.
6. **The headline "American research spending" is narrowed to NIH spending these categories
   capture**, which is what the analysis measures.
7. **The road-death rate concession is stated.** Per person the risk did fall by about a fifth; the
   count did not move. Omitting the first half was the Post 22 selection error repeating.
8. **Two chart labels were moved after measuring the rendered pixels once, by hand.** The
   "Depression" label sat on the blue lung-cancer marker, which made the chart contradict the prose
   at its most contested point. There is no standing pixel check in the code and this document
   should not have implied one; round 5 measured again and found a third collision.

## 5.4 Amendments after fact-check round 5, 2026-08-11

Round 5 ran four independent lenses, including the statistical lens round 4 had to do without.

1. **The road user split is corrected a THIRD time, and this is the round's post-blocking finding.**
   Round 4 replaced the recomputation with figures taken from WHO's launch NEWS RELEASE of
   13 December 2023 rather than from the report. The release contradicts the report it announces:
   it assigns 30 percent to four-wheeled occupants, which is the report's figure for
   MOTORCYCLISTS, and prints a 3 percent micro-mobility share the report says does not exist
   globally. The report, pages 10, 15 and 17, says riders of powered two and three wheelers 30,
   occupants of four-wheeled vehicles 25, pedestrians 21, cyclists 5, and publishes its own 19
   percent residual. The post now says 25 and "three in four", and the argument is stronger than
   it was at 30 and "seven in ten". A press release is not the report.
2. **The 31.3 percent recomputation is WITHDRAWN as an artefact.** Six of the 139 reporting
   countries returned exactly one category, all four-wheel, and renormalising a lone category to
   its own sum scales it to 100 percent. Those six supply 34.8 percent of the 31.3. Excluding them
   the answer is 22.9, the same as the complete filter. Round 4 published it as the upper end of a
   bracket around WHO's figure; there was no upper end.
3. **The filter is described accurately.** 139 countries report something, 101 report all five
   categories, and a sum tolerance of 12 points drops 19 more including the United States, whose
   five shares sum to 66.7. Every text that said "139 to 82" skipped the middle step.
4. **Class dollar medians were computed on the unmerged condition list**, so road injury and falls
   each carried the whole shared category over their own burden. That put the partly class at $288
   instead of $160 and made the top two classes look 4 percent apart when they are 47.
5. **The road-death rate is computed in the repository**, from the Global Health Estimates' own
   population rows, rather than from figures typed into a scratch script: 29 percent more people,
   a 23 percent fall in the rate, a 0.28 percent fall in the count.
6. **The consumer-surplus figures come from the study, not the Index's arithmetic**: 116 billion
   rising to 172, Brynjolfsson, Collis, Eggers, Kazinnik and Nguyen, two waves eight months apart.
7. **`conditions.py`'s round-4 docstring claim was false.** HIV, tuberculosis and malaria are coded
   on the causal-agent limb. The consequence for road injury is stated rather than smoothed over,
   and the recoding sensitivity is now in the post.

## 5.5 Amendments after fact-check round 6, 2026-08-11, and the decision to stop

Round 6 changed the question. Rounds 2 to 5 each asked what the previous round had broken. Round 6
asked which external figures nobody had opened the primary document for, and answered it for every
one of them. That is the audit that should have run first.

1. **The post's opening two numbers were Our World in Data's aggregation, attributed to WHO.** WHO
   publishes 1,184,514 for 2000 and 1,182,759 for 2021; OWID's copy says 1,177,422 and 1,174,078
   and differs from WHO's published country file in 177 of 183 countries. `fetch_data.py` now
   downloads WHO's deaths workbook. The derived rate, 14.897 per 100,000 for 2021, matches WHO's
   own published crude death rate in the same row exactly. OWID's annual series is retained for
   shape, because WHO publishes six years and not a series, and labelled wherever it appears.
2. **Dieleman, Hartung and the Epoch AI count were rescoped** after the papers were opened rather
   than the abstracts: "low back and neck pain" and 85.2 percent of US health spending; a
   pre-rebate acquisition cost against 41,000 to 53,000 after rebates; a count of a mirror's
   snapshot rather than Epoch's own figure.
3. **The fact sheet names no year.** Round 5's disclosure note took 2025 from a press release,
   inside the paragraph whose purpose is warning that WHO's publications disagree.
4. **Two round-5 defects.** `vuln()` matched a renamed label, so every vulnerable-road-user share
   in `results.json` was 100 minus "other"; and the chart 2 leader line moved to clear the multiple
   sclerosis marker was moved into it.
5. **The recoding sensitivity is computed and published.** `models.recode_injuries_as_target`, t
   minus 1.06 and 10 percent, is in the post's method notes. Two files had asserted it was there
   when it existed nowhere.
6. **Decorative assertions replaced.** One tested a mathematical identity, the other compared two
   hardcoded constants; neither could fail, and neither would have caught round 4's transposition.
   The replacements can.

**Stopping rule, recorded because this document is where decisions go.** Six rounds found real
errors every time, but from round 2 to round 5 roughly half of each round's findings were created
by the previous round's own fixes, at close to a one-for-one rate. That loop does not converge by
running it again; it converges by changing what a round is allowed to do. This round was
verification-only with the body frozen at its word count, and the post ships after it. Residual
defects are expected. The provenance audit that makes shipping defensible is complete: every
external figure in this post has been read in its publisher's own document.

## 6. Out of scope

- Any claim that a named funder, company or agency acted in bad faith. The post's whole point is
  that no villain is required.
- Policy prescription. The close turns toward what to do in one sentence and stops there.
- The other four topic areas the reader supplied (internet, space and satellites, general R&D,
  technological change). Named nowhere in the post as a promise.
- Any claim about AI's benefits or harms. The post's AI claim is strictly about what is and is not
  measured.
