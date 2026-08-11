# Round 6 claim inventory

Two scopes this round, because round 5 taught a lesson that is not about prose.

**Scope one, the usual:** every sentence, chart string and repository text round 5 changed.

**Scope two, new and the more important:** every external figure in this post that nobody working
on it has personally opened the primary document for. Round 5's own worst finding was that round 4
had sourced a "published" WHO figure from a press release, written "from the Global status report
on road safety 2023" into four files and a PNG, and never opened the report. The report answered a
plain curl on the first attempt. Every remaining external number gets the same treatment or it does
not ship.

## A. External figures and their provenance status

| # | Figure | Where it came from | Opened the primary document? |
|---|---|---|---|
| A1 | Road deaths 1,177,422 (2000) and 1,174,078 (2021) | `deaths-from-road-injuries.csv`, **Our World in Data's copy** of WHO GHE | **NO.** This is a mirror, and a mirror is what round 1 caught. WHO publishes GHE itself. |
| A2 | WHO's road user split 30 / 25 / 21 / 5, residual 19, "half of all deaths" | Global status report on road safety 2023, pp. 10, 15, 17 | YES, round 5, PDF from IRIS |
| A3 | "around 60 percent of the world's vehicles and 92 percent of its road deaths" | WHO road traffic injuries fact sheet | YES |
| A4 | "leading cause of death for children and young adults aged 5 to 29" | same fact sheet | YES |
| A5 | 1.19 million (road safety report) and ~1.16 million (fact sheet, 2025) | report p. 3 and fact sheet | PARTIAL. Confirm the 1.19 is 2021 and the 1.16 is 2025, from the documents. |
| A6 | Back and neck pain the largest US health spending category, 134.5 billion dollars, 154 conditions | Dieleman et al. (2020), *JAMA* | **NO.** Abstract and Crossref only. Open the paper. |
| A7 | First-generation MS drugs about 60,000 dollars a patient-year as of 2013 | Hartung et al. (2015), *Neurology* | **NO.** Abstract only. Open the paper and check the scope and the year. |
| A8 | "Brynjolfsson et al. (2025) tracked five thousand support agents" | *QJE* abstract via Crossref | **NO.** The abstract says 5,172. Confirm from the paper. |
| A9 | Consumer surplus 116 billion to 172 billion, two waves July 2025 and March 2026 | Brynjolfsson et al. (2026) working paper | YES, round 5, PDF |
| A10 | EV share 0.012 percent (2010) to 25 percent (2025) | OWID's copy of IEA Global EV Outlook 2026 | PARTIAL. IEA's own text was quoted; confirm both endpoints from IEA. |
| A11 | 527 systems, AI investment 6.01bn to 290.1bn | OWID CSVs in `data/` | Reproducible in repo, but the OWID series is itself a mirror of Epoch AI and Quid. |

## B. Draft sentences round 5 rewrote

B1 lines 14-15, "by 23 percent … 29 percent more people alive". B2 line 20, "The dying have a
number too". B3 lines 23-29, the whole corrected road-user paragraph. B4 line 31, "three in four".
B5 line 34, "around 60 percent". B6 line 78, migraine added to the bottom list. B7 line 98, "the
twelve rows carrying the largest high-income burden". B8 the road-injury paragraph's new "The
two-and-a-half-times gap becomes twice." B9 lines 148-158, the AI paragraph and its close. B10 the
"same story, with the gap at its widest" framing. B11 "for us, or for the paying patients".
B12 the closing inference disclaimer. B13 the FC3 method note with its 300 / 160 / 135 medians.
B14 the rewritten road-user method note. B15 the three-WHO-totals note. B16 every word trimmed in
the two passes that took the body from 2,064 to 1,997, since trimming is where round 4 broke a
sentence.

## C. Chart strings round 5 changed

C1 chart 1 rebuilt entirely: five bars, WHO's residual, "75% were not in a four-wheeled vehicle",
the WHO "half of all deaths" line, the new footnote with the recomputation variants. C2 chart 2's
Rheumatoid arthritis leader moved to 3050. C3 chart 3's suptitle "NIH money does not follow the
damage either", its wrapped annotation, its two-line right-panel title, and the HIV/TB clause that
replaced the unevidenced "explicit global health mandate". C4 chart 4 unchanged this round, so it
is only a consistency target.

## D. Repository text round 5 wrote

D1 `build_analysis.py`: `WHO_PUBLISHED_SPLIT` and its comment block, `WHO_PUBLISHED_RESIDUAL*`,
`WHO_VULNERABLE_WORDING`, the four-variant `disagreement` block, `filter_steps`, the merged-basis
fix to `by_class` and `by_target` dollar medians, the new structural asserts, `post_claims_still_true`,
the world-population block. D2 `conditions.py`'s corrected docstring, including its claim that only
Road injury and Falls refuse in the word "biological" and its statement of the recoding
sensitivity. D3 design doc 5.4 and the superseded marker on the round-4 chart 1 amendment.
D4 `README.md`'s round-5 section and superseded marker. D5 `data/README.md` trap 10.

**Round 5's descriptions of round 5 are the least-checked text in the repository.** Round 5 found
that round 4's descriptions of its own work were wrong in eight separate places while round 4's
arithmetic was almost entirely right. Assume the same shape here.
