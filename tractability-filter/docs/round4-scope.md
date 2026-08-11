# Round 4 claim inventory (scoped at round 3's replacement prose and re-rendered images)

Round 1 verdicted the full 90-claim inventory (`claim-inventory-r1.md`). Rounds 2, 3 and now 4 each
verdict only what the previous round changed, plus any claim whose evidence those changes touch.

On this post the pattern has held every round: four of round 2's five HIGH findings were created by
round 1's own fixes, and round 3 found two never-run pre-registered checks plus three more
prose-versus-PNG desyncs. Round 3's own fixes are therefore the least-checked text in the repository.

## A. Draft sentences round 3 rewrote

| # | File:line | Claim as it now stands |
|---|---|---|
| A1 | draft:8 | Section heading "The car got rebuilt. Most of the people it kills were never inside it." |
| A2 | draft:18 | "Electrification was aimed at tailpipe emissions, not at crashes, and I am not judging it against a goal it never had." |
| A3 | draft:19 | "The point is that nothing of comparable force was aimed at the dying" |
| A4 | draft:37 | Section heading "Where the effort should be, if effort followed the damage" |
| A5 | draft:66-68 | "first-generation multiple sclerosis drugs cost about 60,000 dollars a patient-year as of 2013 (Hartung et al., 2015)" |
| A6 | draft:71-74 | "is there a validated causal target" and "The 24 conditions with a target ... The 10 without one draw 300." |
| A7 | draft:80 | "Malaria is far left, tiny, and above the fitted line" |
| A8 | draft:94 | "across the remaining 29 rows it improves to a t of 2.23 and 12.5 percent" |
| A9 | draft:95-96 | "One caveat: these 31 rows are disease categories, not the NIH budget, and I never ran the validation I promised myself." |
| A10 | draft:98 | "Among the twelve largest high-income burdens in the right-hand panel above" |
| A11 | draft:107-108 | "the interval runs from a large gap down through zero to a small one pointing the other way" |
| A12 | draft:113 | "First, I predicted a clean three-step gradient" (enumerator added) |
| A13 | draft:116-121 | "Depression has no validated causal target ... my coding may simply be wrong for it." |
| A14 | draft:128-129 | "no longer significant at the 5 percent level" |
| A15 | draft:150-153 | "What does not exist is a population-level welfare series to set against the investment line year by year. That is the only version I can defend." |
| A16 | draft:206-213 | The whole FC3 method note |
| A17 | draft:215-220 | "What the money analysis cannot see, and one promise I broke." |

## B. Chart captions and labels re-rendered in round 3

| # | Where | Text |
|---|---|---|
| B1 | chart 1 x-axis | "Share of road deaths in the 82 reporting countries (37% of the world's)" |
| B2 | chart 1 footnote | "It reproduces WHO's own published statement that more than half of road deaths are among vulnerable road users, including pedestrians, cyclists and motorcyclists." |
| B3 | chart 2 footnote | "That term rule provably failed for road injury, labelled here: its candidate terms were all crash vocabulary while the registry files trauma by pathology." |
| B4 | chart 2 legend | "Has a validated biological target" / "No validated biological target" |
| B5 | chart 3 panel A note | "Slope t = 0.77, adjusted R squared = -0.014, 31 rows." |
| B6 | chart 3 right title | "The twelve largest high-income burdens, by US money per US year of life lost" |
| B7 | chart 3 footnote | "excludes leukaemia ... and malaria, whose American burden rounds to zero; road injury and falls share a category and are merged, so 31 rows cover 32 conditions" |
| B8 | chart 4 AI row | "No agreed population-level welfare series exists, so no bar is drawn on this row" |
| B9 | chart 4 footnote | "Randomised task-level studies of AI's effect on people do exist and are cited in the post" |

## C. Reference entries round 3 rewrote

C1 IEA "Global EV outlook 2026". C2 Quid title and dropped corporate URL. C3 Hartung subtitle.
C4 WHO 2026b July 20 date. C5 year anchors for Epoch AI, NIH, NLM. C6 WHO 2026a in-text anchor.

## D. Documents round 3 amended

D1 design doc 3.1 WITHDRAWN (date-windowed trial count never computed) and its claim that the only
by-year series in the repository is a different object, given that chart 4's medicine row uses one.
D2 design doc 3.5 WITHDRAWN (NIH validation never run). D3 chart 3 heading WITHDRAWN. D4 chart 2
spec AMENDED, including its promise that "Legend and prose use the same words". D5 README's
falsification-condition paragraph. D6 `data/README.md`.

## E. Carried over from round 3, unresolved

E1 design doc 5.1 item 1 describes a certifi/`/etc/ssl/cert.pem` fallback; `fetch_data.py` uses curl
throughout. E2 dead `SHORT["Falls and road injury"]`; the merged row is named "Road injury and
falls". E3 the 11.5 / $12 / 12 rounding drift across draft, chart 3 and README. E4 chart 1's
"25.0% in 2025" annotation sitting almost on the series line.

## F. Evidence the round-3 changes touch, therefore back in scope

F1 The full transport opening paragraph (draft:12-20), because A1, A2 and A3 all sit in it: check
the 2000-to-2021 endpoints against the whole series, including the 2012 peak and the 2020 pandemic
trough. F2 The whole target-binary passage, because A6 renamed the binary. F3 The AI section,
because A15 rewrote its only claim.
