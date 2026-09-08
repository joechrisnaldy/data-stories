# Writing conventions for all posts in this series

1. **Punctuation: no long dashes.** Do not use em or en dashes in post text. Use commas, semicolons, colons, or parentheses depending on the sentence.
2. **References: APA 7 for external sources.** Every fact, figure, or quote taken from the internet (anything not derived from the post's own dataset) gets an entry in a "References" section at the end of the post, formatted in APA 7. Dataset-derived numbers are covered by the method notes instead.
3. Apply both at drafting time. Verification agents should check compliance before a draft goes to review.

## Pipeline reminder

Brainstorm question → dataset → Python analysis (he drives POV, Claude codes) →
Word draft for review → MDX on the portfolio blog → notebook + code to GitHub
(data gitignored; download instructions instead).

## The gate: mechanical checks before any draft is shown

Post 25 took four adversarial fact-check rounds. Reviewing what each round actually caught, six of the
seven recurring defect classes were mechanically checkable, and none of them needed a language model:

| Defect class | Times it shipped | Caught by |
|---|---|---|
| Two correlations quoted side by side from different samples | 3 | `checks/samples.py` |
| A number in the draft that no script produces | 9 | `checks/numbers.py` |
| Chart defect visible only in the rendered PNG | ~8 | `checks/surfaces.py` (rendered strings) |
| A process claim ("fixed in both scripts") that was false | 4 | `check.py` loader drift |
| A figure disagreeing across draft, results.json, chart and design doc | 5 | `check.py` cross-surface |
| An assert that could never fire | 1 | `check.py` tautology scan |
| Reading a data file's label instead of the paper | 2 | not mechanical: see below |

`reversal-of-fortune/check.py` is the reference implementation. Copy it into each new post folder and
adapt the paths. **Run it before showing a draft to anyone, not after.** It is cheap, deterministic,
and it catches these classes every time rather than only when a refuter lens happens to look.

`checks/test_gate.py` holds real defective sentences from this repository's history and asserts the
gate still catches them. Add to it whenever a new class of defect gets through; a gate with no test is
a gate that quietly stops working.

**The one class that is not mechanical** is trusting a variable label over the document that defines
it. It shipped twice in Post 25 and the second time was inside the correction for the first. The rule
that follows: **the provenance audit opens the primary document for every VARIABLE the post leans on,
not just for every external figure, and records the defining quote with its page.** A Stata label, a
column header and a codebook entry are not definitions. If no quote from the paper is on file for a
variable, the post may not characterise what that variable measures.

With the gate in place, round 1 should start from a draft where every number is reproducible, every
paired statistic is on a named sample, and every rendered string agrees with the data. The adversarial
rounds are then spent on what they are actually good at: whether the argument is valid, whether the
sources say what the post claims, and what a hostile reader can do with a sentence.
