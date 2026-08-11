# Round 5 claim inventory (scoped at round 4's replacement prose and re-rendered images)

Round 1 verdicted the full 90-claim inventory. Rounds 2 to 5 each verdict only what the previous
round changed. Four rounds in, every round's worst findings have lived in the previous round's own
corrections, and round 4's two worst findings were both introduced or left standing by round 3.

Round 4 also ran degraded: two of its four lenses died on API errors and the statistical pass was
run by the adjudicator rather than an independent refuter. **Round 5 must re-run an independent
statistical lens over round 4's arithmetic, not only over its prose.**

## A. Draft sentences round 4 rewrote or introduced

| # | Line | Claim as it now stands |
|---|---|---|
| A1 | 14-15 | "Per person the risk did fall, by about a fifth, but that is the denominator: 28 percent more people alive, no fewer dying." |
| A2 | 20 | "The point is that the dying have no number attached to them like that one." |
| A3 | 22-26 | "**30 percent of road deaths are people inside a car.** Pedestrians are 23 percent, riders of two and three wheelers 21, cyclists 6, and e-scooter users 3 ... Fifty-three percent are what WHO calls vulnerable road users" |
| A4 | 28 | "fifteen years of engineering went into the object seven in ten of the victims were never inside" |
| A5 | 31 | "holding 60 percent of the world's vehicles" (round 4 dropped "around") |
| A6 | 66-68 | "is there a validated biological target, something in the body that an intervention can act on" |
| A7 | 69-71 | "Hold burden constant and the gap narrows to about two and a half times, but it survives" |
| A8 | 86-87 | "**American disease burden accounts for essentially none of the NIH spending these categories capture.**" |
| A9 | 92-93 | "Two caveats, both mine" |
| A10 | 95 | "Among the twelve largest of those rows, in the right-hand panel above" |
| A11 | 112-115 | "Depression has no validated biological target ... No validated biological target is a claim about mechanism" |
| A12 | 118 | "Recoding depression the other way strengthens the result, so the concession costs me nothing." |
| A13 | 133-135 | "That figure flatters it: the NIH category is all of eye disease, a whole field's money over one condition's damage." |
| A14 | 148-154 | The whole rewritten AI paragraph, including the consumer-surplus figures |
| A15 | 156-159 | "It is an agreed series. Thirteen years of money, published every year by everyone, against two observations from one research group in one country, first reported this year." |
| A16 | 193-197 | The three-WHO-totals disclosure |
| A17 | 212-220 | The FC3 note, including "the three-step gradient I say I abandoned is the order the dollars actually produce" |
| A18 | 222-228 | "the promises I broke", both of them |
| A19 | 230-237 | "Categories overlap, and three are broader than the condition" |
| A20 | 239-248 | "What the road user split rests on, and the number I nearly published" |
| A21 | 250-255 | "The last chart's three windows differ" |

## B. Chart strings round 4 re-rendered

| # | Where | Text |
|---|---|---|
| B1 | chart 1 left panel | WHO's published split, the grey 17% residual bar, "70% were not in a car", "53% were pedestrians, riders, cyclists or on e-scooters" |
| B2 | chart 1 x-axis | "Share of the world's road deaths, WHO's published global split" |
| B3 | chart 1 footnote | the residual's composition, and the RS_246 disagreement figures |
| B4 | chart 1 right panel | "25% in 2025" and its new offset |
| B5 | chart 2 | the "Depression" and "Stroke" leader lines added in round 4 |
| B6 | chart 2 footnote | "One exception, and it runs the other way ... That undercounts a low-effort condition and so flatters the pattern." |
| B7 | chart 3 right title | "The twelve largest of these 31 burdens, by US money per US year lost" |
| B8 | chart 3 bar labels | "$11.5" and "Road injury, falls" |
| B9 | chart 3 footnote | the three-broader-categories sentence |
| B10 | chart 4 AI row | "No agreed year-by-year welfare series exists, so no bar is drawn on this row" |
| B11 | chart 4 footnote | "the AI Index itself carries a population-level estimate of US consumer surplus with two dated observations" |

## C. Reference entry round 4 added

C1 Stanford Institute for Human-Centered Artificial Intelligence. (2026). *The 2026 AI index
report: Economy*. Verify the title, the publisher, the URL and whether the AI Index is the right
thing to cite for a figure the underlying study reports differently.

## D. Repository text round 4 wrote

D1 `build_analysis.py` `WHO_PUBLISHED_SPLIT`, `WHO_PUBLISHED_RESIDUAL_LABEL`, the `transport_act`
comment block, `consumer_surplus_*`, the rewritten `benefit_note`, the warning loop that replaced
three assertions, `bool()` on `burden_explains_nih_dollars`, the FC3 note.
D2 `make_charts.py` docstring rewrite, `SHORT` rename, `NUDGE`/`LEADERS` changes.
D3 `conditions.py` new docstring paragraph, including its claim that no condition was coded on the
"identified causal agent" limb alone.
D4 design doc: chart 1 rebuild, section 5.1 item 1 correction, section 5.3, the sources table.
D5 `README.md` round-4 section and the rewritten transport and binary paragraphs.
D6 `data/README.md` trap 5.

## E. Known open, assigned to the adjudicator rather than a lens

E1 "about a fifth" and "28 percent more people alive" are computed from UN world population figures
typed into a scratch script and NOT reproducible from this repository. House rule: every number in
a deliverable is reproduced by a script in the repo. Fix before anything else.
E2 A12's recoding claim came from a refuter's report and was never re-derived here.
