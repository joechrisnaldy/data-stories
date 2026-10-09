# Writing conventions for all posts in this series

1. **Punctuation: no long dashes.** Do not use em or en dashes in post text. Use commas, semicolons, colons, or parentheses depending on the sentence.
2. **References: APA 7 for external sources.** Every fact, figure, or quote taken from the internet (anything not derived from the post's own dataset) gets an entry in a "References" section at the end of the post, formatted in APA 7. Dataset-derived numbers are covered by the method notes instead.
3. Apply both at drafting time. Verification agents should check compliance before a draft goes to review.

## Pipeline reminder

Brainstorm question → dataset → Python analysis (he drives POV, Claude codes) →
Word draft for review → MDX on the portfolio blog → notebook + code to GitHub
(data gitignored; download instructions instead).

## The gate: mechanical checks before any draft is shown

> **WITHDRAWN IN PART, 2026-10-09.** A defect audit across all 25 posts (its ledger is kept private, because it is built from private working notes) found
> this section overclaims. The "Caught by" column below is false: the audit's attack on
> `reversal-of-fortune/check.py` evaded every one of those checks on a scratch copy, and judged the gate
> adequate for none of the 35 defect classes on record. Its number check tests membership in
> `results.json`, not binding to the claim, so swapping the two halves of a finding passes. And copying
> `check.py` into a new post does not work: it imports that post's own modules and hardcodes its draft,
> surfaces and chart functions. Until the gate is rebuilt as one shared, per-post-configured tool, treat
> it as a smoke test only, and do not cite it as evidence that a class is covered.
>
> **SUPERSEDED, 2026-10-09:** the per-post `check.py` was deleted from `reversal-of-fortune/` and replaced
> by the shared `gate/` package described in the next section. Everything from here to the next section
> is kept as history: do not copy `check.py` or add to `checks/test_gate.py`, which no longer exist; new
> defect classes become checks with tests in `gate/`. The paragraph on the one non-mechanical class still
> holds.

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

## The gate (2026-10-09): one shared tool, configured per post

`gate/` is the gate for every post from Post 26 on. Run `python3 -m gate <post>` from this folder; see
`gate/README.md` for commands, what each check guarantees, and what it cannot check. It was built from
a defect audit of all 25 posts (ledger kept private: 404 incidents, 35 classes, 130 introduced by a
previous round's fix, 34 of 35 classes recurring after a lesson about them had been written down), and
proved against every attack that audit used (`audit/gate-replay-2026-10-09.txt`).

Rules that follow from it, all enforced or listed by the gate:

1. **No number is typed.** The build script emits every quantity the prose states, derived ones
   included; the draft is `draft/<slug>.src.md` with `{{key:fmt}}` placeholders, rendered by the gate.
   The same goes for both READMEs (`docs/README.src.md`, `docs/data-README.src.md`, declared in
   `[post] extra`) and every text field of the published MDX (`[published]` templates).
2. **External figures come from a stored, hash-pinned copy of the cited document** (`sources/`,
   gitignored) with a verbatim quote in `docs/sources.json`. Not opened means not cited.
3. **Every universal, superlative or causal word sits inside a `[claims]` phrase naming its licence.**
   A licence covers only the words inside its phrase. A refuted universal is replaced with a bound
   count, never with another universal.
4. **A variable is characterised only from its defining document**, quoted with its page in the
   provenance audit. A data file's label is not a definition.
5. **A fix may only delete text or narrow a claim to a bound key.** Anything added is a new claim and
   enters the next round's scope, which `gate scope --since N` computes.
6. **Nothing publishes until `gate publish-check` passes**: a closed round with nothing refuted,
   unverified or open, and no edit since. No waivers.
