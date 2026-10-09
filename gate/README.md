# gate

The pre-draft gate for the data-stories series. One shared package, configured per post by
`<post>/gate.toml`. It replaces the per-post `check.py` copied from Post 25, which a 2026-10-09 audit of
404 recorded defects (the ledger is kept private: it is built from private working notes) found adequate for none of 35 defect classes. Its own
first version was then attacked the same day and hardened twice (v2 against the attack round, v3 against
an independent review of v2, finished against one diff-scoped review of v3, which was the declared
stopping point); every attack from all of them is replayed in `gate/replay/replay_audit.py`.

Run everything from `Projects/analytics-blog`, with Python 3.11 or later (the config reader is `tomllib`).

```bash
python3 -m gate <post>                     # check; GATE PASSED or a list of problems, exit 0 or 1
python3 -m gate render <post>              # write the rendered draft and every [post] extra output
python3 -m gate snapshot <post> <N>        # store the draft at the start of fact-check round N
python3 -m gate scope <post> --since <N>   # every sentence added or changed since round N started
python3 -m gate close-round <post> <N>     # record round N; refuses on a red gate or open findings
python3 -m gate publish-check <post>       # hard precondition of publishing
python3 -m unittest discover -s gate/tests -t .   # the gate's own tests (also run by every check)
python3 gate/replay/replay_audit.py <post>        # replay known attacks on a copy of a post (slow)
```

Every check first runs the gate's own tests and refuses to judge anything if one fails or is skipped;
with the self-test switched off (`GATE_SKIP_SELFTEST`) the verdict is GATE INCOMPLETE, never a pass. A
check that raises is reported as CRASHED, never as a pass, and the other checks still run.

## Configuring a post

`gate.toml` is strict: an unknown key, a missing reason or a malformed entry stops the gate.

- `[post]`: `slug`, `source` (the `.src.md` draft), `rendered`, `results`, `build` (scripts, in order),
  and optionally `sources`, `charts`, `chart_dir`, `docx`, `mdx`, `site_public` (the site's public
  folder, found from the MDX path when omitted), and `extra`, a list of `[template, output]` pairs
  rendered like the draft. Both READMEs belong in `extra`; a README that is
  not rendered from a template is scanned as hand-typed text.
- `[allow]`: `"phrase" = "reason"` for words and digits that are not results.
- `[claims]`: `"phrase" = "licence"`. A phrase licenses only the flagged words inside it; under three
  words it licenses only a sentence that is exactly that phrase, unless it is one hyphenated term (a
  group name such as `"never-colonised"`).
- `[pairs]`: `"opening words of one paragraph" = {reason = "...", paths = ["result.path", ...]}`. The key
  must open exactly one paragraph, and the entry excuses only the named figures in it.
- `[published]`: a template for every text field of the live MDX front matter except slug, dates,
  tags, status, cover and draft (`title` is compared with the draft's H1 instead), plus
  `"alt:<chart file>"` for each image.

Every entry is counted on each run, and an entry that matches nothing fails as stale.

## What it checks

| Check | Guarantees | Previously |
|---|---|---|
| render, rendered | every figure in the draft and the `extra` templates is `{{key:fmt}}` resolved from `results.json` or `{{src:id.values.name:fmt}}` from a stored source, through a strict formatter that refuses values it cannot print honestly (no unsigned negative; no percent formatter on a key whose name says it is already in percent, such as
`density_pct`, `pct_growth` or `growth_percent`); each rendered file is exactly a fresh render | numbers were typed and compared to `results.json` by membership |
| numbers | no digit (including `.44` and `_0.44_`), number word (ordinals, "doubled", "-fold", "twice", "trillion") or Unicode fraction in the prose, headings, alt text, published fields, READMEs or chart-script strings is unbound, except `[allow]` phrases with a reason; no sign or percent (any spelling) is typed beside a placeholder; every figure a chart prints is a result at its printed precision, sign and percent read as written, and
an `r = X` printed with an `n = Y` must come from one result object. Citations, URLs and the sequential markers of a numbered list are not quantities; in READMEs only, neither are fenced code and inline code containing a letter | digits only; a number before a comma was invisible |
| pairs | like-for-like figures from different samples in one paragraph each show their n (`sample` ids decide), in the draft, the README templates and the published fields | a phrase such as "on each side" silenced it |
| claims | every universal, superlative (any -est word) or causal word, however it is quoted or italicised, in the prose, the reference list, the READMEs (code aside), on a chart or in a published field, sits inside a `[claims]` phrase naming its licence | not attempted |
| cite | every segment of every in-text citation matches a reference entry and every entry is cited; page locators and APA dates are understood; nothing follows the reference list | one direction, parenthetical only, last segment only |
| sources | each external figure, wherever it is used, comes from a hash-pinned stored copy of the cited document whose title (the reference entry's, whole or up to its colon) opens its first page; the quote occurs exactly once and starts and ends on whole tokens; each value appears in it as an exact signed token, one number per value; the paragraph cites that author and year | an allowlist anyone could add to |
| fresh | the post rebuilds twice in temp copies with every output removed (an output folder reached through a link outside the post is refused, never emptied); every template prints identically from the committed and the rebuilt results; committed results and charts match by meaning (results within 1e-12 relative, charts within 4/255 per pixel); a chart no script produces fails; the two builds match byte for byte | rebuilt in place, overwriting what it checked |
| panels | each chart panel plots exactly the n it prints in its annotations, title, axis labels or legend; on a one-panel chart, the footnote's n too | recomputed n instead of reading the chart |
| style | no em dash, en dash or Unicode minus in any text file (the README inside `data/` included), the .docx, the MDX, or any rendered chart string; no `--` or dash entity in Markdown outside code | six hardcoded files |
| links | every image the draft links to exists | not attempted |
| published | the whole live page, references included, equals the rendered draft; title equals the H1; captions are the charts' own footnotes; every front-matter text field and alt text equals its template; each image, at the path the page links, matches its chart | not attempted |
| rounds | rounds are consecutive and closed once; a round cannot close on a red gate, with an errored lens, or with an UNVERIFIED, OPEN or unevidenced finding; snapshots hold the rendered text of every surface and a manifest of every input; round 2 onward must account for exactly the rendered sentences changed since the previous snapshot (figures changed by code included), and a missing snapshot is an error; a clean round means no input moved during it; publishing requires the last round clean, no change since to anything that determines the post, and both the charts script and the MDX configured | a dead verifier's finding could be filed as refuted |

## What it cannot check (round 1 exists for these)

- A figure bound to the **wrong** key, applied consistently. Keys are visible in the source, which makes
  this reviewable, not impossible.
- An `[allow]`, `[claims]` or `[pairs]` entry whose reason is false. Every entry is listed, counted on
  each run, and fails when stale; its truth is a reviewer's job.
- A stored source document that is itself forged or is the wrong edition with the right title, and a
  quote that is unique but taken from the wrong column of the right table.
- Whether a quote supports the paraphrase built on it, whether the argument is valid, and what a hostile
  reader can do with a sentence.
- In a README, a figure written inside inline code with letters around it (`t = 5.3` in backticks):
  README code is masked.
- A sentence without any flagged word appended inside a reference entry.
- The n printed in the footnote of a multi-panel chart (a footnote may report a statistic it does not
  draw); its figures are still checked as results.
- A cache committed inside `data/` that a build script reads instead of recomputing.
- A mixed-sample comparison split across two paragraphs.
- Chart text is not part of a round's snapshot, so a caption changed by chart code alone does not enter
  the next round's `scope` (it does block a clean close and `publish-check`, through the manifest).
- `cite` reads only the draft: a README citing a work with no reference entry passes.
- `style` reads READMEs directly inside `data/` and `sources/`, not in folders below them.
- A one-word hyphenated `[claims]` entry licenses every later use of that term.
- A value already in percent whose key name does not say so is multiplied by 100 by `pct0`/`pct1`.
- A quote whose number uses a mid-dot decimal or space-separated thousands (`11·38`, `1 234`) is not
  read as one number.
- Setting `GATE_IN_SELFTEST` by hand skips the self-test and can still print GATE PASSED; it exists only
  for the self-test's own runs.

Known false positives, each with `[allow]` or rewording as the way out: a README reference list is
scanned for numbers; a `'%.1f'` format string in a chart script reads as `.1`.
- Analysis-code correctness beyond reproducibility, construction alternatives, variable definitions, and
  chart geometry. These are the next phase of the private defect ledger.

Proof of the above: `audit/gate-replay-2026-10-09.txt`, the replay of every attack on the previous
gate and on this gate's first version, against copies of Post 25.
