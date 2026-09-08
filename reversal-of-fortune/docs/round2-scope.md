# Post 25, round 2 scope

Round 1 verdicted the full 54-claim inventory and rewrote roughly half the post. Round 2 verdicts
ONLY what round 1 changed, plus any claim whose evidence those changes touch.

On this blog, replacement prose is where the next round's worst findings live. Round 1 itself found
that the provenance audit written before the design document contained a wrong reason, and that the
draft's central logical claim was refuted by the repository's own data.

## A. Draft sentences round 1 wrote

A1 The r-squared and latitude comparison paragraph ("about a fifth", "plus 0.60", "an Africa dummy
does better still", the 1,100-to-130,000 spread between 24 and 28 degrees).
A2 "there are seventeen countries above twenty degrees with incomes over forty thousand dollars".
A3 "Nothing in this post disputes that the correlation is real. Everything in it disputes what the
correlation means."
A4 The arable-land and McEvedy and Jones paragraph, including the quoted phrase "more complex".
A5 The new n figures throughout: 97, 98, 173, 163, 94, 69, 91, 43.
A6 "minus 0.18" for the global heat-versus-1500-density figure.
A7 The interaction sentence: slopes +0.15 and -0.33, t of -5.3, 163 countries.
A8 The AJR attribution paragraph: "AJR do not publish a correlation. They publish a regression
coefficient of minus 0.38 with an R-squared of 0.34 on those same 91 countries."
A9 "The second of those is not significant on its own. The gap between them is."
A10 The ENTIRE rewritten filter section, especially the conjunction, the -0.74 admission, and the
"a cause can be older than the reversal and still produce it" claim.
A11 Indonesia's revised figures: 79th, 65th, 47th of 94.
A12 The Dell, Jones and Olken paragraph with the 1.1 percentage point figure.
A13 The collider paragraph and the Malthusian paragraph.
A14 The revised close: "cannot be the whole of it, and it cannot be the part that changed".
A15 Every word of the rewritten method notes, including the two-bugs paragraph and the
falsification-gap disclosure.

## B. Code round 1 changed

B1 `build_analysis.py`: the de-duplication fix, `WB_AGGREGATES` and its assert, `CCKP_REQUEST`, the
interaction block.
B2 `make_charts.py`: `frame()` now unions the AJR and income universes; chart 1's annotation moved;
chart 2's panel titles; chart 4's legend, NAME dict and the new assert.
B3 Whether both scripts still regenerate their outputs deterministically after all of it.

## C. Charts re-rendered

C1 All four PNGs. Specifically: does chart 1's new bottom-left annotation collide with anything;
does chart 4's legend now collide with the title; does every panel plot the n it prints; did the
frame change alter any point set unintentionally.

## D. Documents round 1 rewrote

D1 `docs/provenance-audit.md`, corrected in place, including its new claim that the values "fail a
sanity check" with specific figures.
D2 `docs/2026-09-07-reversal-design.md` section 6.1, eight numbered amendments, all written after
the fact about work done earlier.

**Assume every one of these is wrong until checked. Round 1's own corrections are the least-checked
text in the repository.**
