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
python3 -m gate snapshot <post> <N>        # store the post at the start of fact-check round N, before its panel runs
python3 -m gate scope <post> --since <N>   # what changed since round N started: sentences added, changed, moved or
                                           # deleted, and chart files; --json FILE writes the next round's inventory
python3 -m gate close-round <post> <N>     # record round N; refuses on a red gate or open findings
python3 -m gate changed <post>             # after the last round: each difference as a row, and what settles it
                                           # (--json FILE writes the rows for the final read)
python3 -m gate accept <post> --index <I> --starts "<opening words>" --owner "<the owner's words>"   # one row
python3 -m gate publish-check <post>       # hard precondition of publishing
python3 -m unittest discover -s gate/tests -t .   # the gate's own tests (also run by every check)
python3 gate/replay/replay_audit.py <post>        # replay known attacks on a copy of a post (slow)
python3 gate/replay/replay_rounds.py <post> ... --old <rounds.py from before 2026-11-16>   # both publish rules
```

Every check first runs the gate's own tests and refuses to judge anything if one fails or is skipped;
with the self-test switched off (`GATE_SKIP_SELFTEST`) the verdict is GATE INCOMPLETE, never a pass. A
check that raises is reported as CRASHED, never as a pass, and the other checks still run.

## Configuring a post

`gate.toml` is strict: an unknown key, a missing reason or a malformed entry stops the gate.

- `[post]`: `slug`, `source` (the `.src.md` draft), `rendered`, `results`, `build` (scripts, in order),
  and optionally `sources`, `charts`, `chart_dir`, `docx`, `mdx`, `site_public` (the site's public
  folder, found from the MDX path when omitted), `restricted_inputs` (a list naming each input whose
  terms bar redistribution; `publish-check` then requires the results file to be git-ignored), and
  `extra`, a list of `[template, output]` pairs rendered like the draft. Both READMEs belong in `extra`;
  a README that is not rendered from a template is scanned as hand-typed text.
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
| numbers | no digit (including `.44` and `_0.44_`), number word (ordinals, "doubled", "-fold", "twice", "trillion", italic `_three_`) or Unicode fraction in the prose, headings, alt text, published fields, READMEs or chart-script strings is unbound, except `[allow]` phrases with a reason; no sign or percent (any spelling) is typed beside a placeholder; every figure a chart prints is a result at its printed precision, sign and percent read as written, and
an `r = X` printed with an `n = Y` must come from one result object; every sentence that prints a percent (a `pct0`/`pct1` placeholder, or a key named for a percent printed as a number; an ordinal, a fraction or a year is not one) names its unit at least once, 'percent', 'per cent' or '%', or 'point' or 'points' for a key in percentage points, outside URLs, link targets, code and HTML comments, where a list item, a table row (which may take the unit from its column's header), a heading, an image line and a quote line are sentences of their own, a line ending in a hard break ends one, and a stop ends one even
before a closing mark. Citation dates and their page locators in the forms `numbers.py` masks, URLs and the sequential markers of a numbered list are not quantities (a citation's names part is read); in READMEs only, neither are fenced code and inline code containing a letter | digits only; a number before a comma was invisible; a percent printed as a bare number passed (Post 31, 2026-11-17) |
| pairs | like-for-like figures from different samples in one paragraph each show their n (`sample` ids decide), in the draft, the README templates and the published fields | a phrase such as "on each side" silenced it |
| claims | every universal, superlative (any -est word) or causal word, however it is quoted or italicised, in the prose, the reference list, the READMEs (code aside), on a chart or in a published field, sits inside a `[claims]` phrase naming its licence | not attempted |
| cite | every segment of every in-text citation matches a reference entry and every entry is cited; page locators and APA dates are understood; nothing follows the reference list | one direction, parenthetical only, last segment only |
| sources | each external figure, wherever it is used, comes from a hash-pinned stored copy of the cited document whose title (the reference entry's, whole or up to its colon) opens its first page; the quote occurs exactly once and starts and ends on whole tokens; each value appears in it as an exact signed number, one number per value, read in the entry's `number_format` (`en`, the default: comma thousands, dot decimals; `id`: dot thousands, comma decimals; a grouped number is one number and an attached ½ is a half); the paragraph cites that author and year (`Surname YEAR` or `Surname n.d.`) | an allowlist anyone could add to |
| fresh | the post rebuilds twice in temp copies with every output removed (an output folder reached through a link outside the post is refused, never emptied); every template prints identically from the committed and the rebuilt results; committed results and charts match by meaning (results within 1e-12 relative, charts within 4/255 per pixel); a chart no script produces fails; the two builds match byte for byte | rebuilt in place, overwriting what it checked |
| panels | each chart panel plots exactly the n it prints in its annotations, title, axis labels or legend; on a one-panel chart, the footnote's n too | recomputed n instead of reading the chart |
| style | no em dash, en dash or Unicode minus in any text file (the README inside `data/` included), the .docx, the MDX, or any rendered chart string; no `--` or dash entity in Markdown outside code | six hardcoded files |
| links | every image the draft links to exists | not attempted |
| published | the whole live page, references included, equals the rendered draft; title equals the H1; captions are the charts' own footnotes; every front-matter text field and alt text equals its template; each image, at the path the page links, matches its chart | not attempted |
| rounds | rounds are consecutive and closed once; a round cannot close on a red gate, with an errored lens, or with an UNVERIFIED, OPEN or unevidenced finding; a snapshot is taken before its round's verdicts exist and holds the rendered text of every surface, a manifest of every input and the hash of every file in the chart folder; round 2 onward must account for exactly the rendered sentences changed since the previous snapshot (figures changed by code included), and a missing snapshot is an error; a clean round means no input moved during it; publishing follows the rule of the next section, with both the charts script and the MDX configured | a dead verifier's finding could be filed as refuted |

## Publishing: two rounds, then cuts only

The owner's rule of 2026-11-16. `publish-check` compares the post with the snapshot the last closed round
started from: its sentences, surface by surface and in order (a reference entry counts as one sentence),
and the files of its chart folder.

- **After round 1**, any such difference needs round 2. Round 2's inventory is the file
  `scope <post> --since 1 --json FILE` writes from round 2's own snapshot: the changed sentences, the
  `[moved]` and `[deleted]` ones, and each `[chart]` file that differs. An item's id is its place followed
  by a check of its text, so a verdict given for another list is joined to nothing and the round cannot
  close on it.
- **After round 2**, `changed` lists each difference as a row. A cut (a sentence with words removed,
  where it stood) or a deleted sentence is settled by one CONFIRMED read of that row. New words, a
  moved sentence and a changed chart are settled only by the owner's acceptance of that row (`accept`,
  in the owner's words; a chart is accepted at one version). A read or an acceptance counts only for
  the row it was made for, and a row the read REFUTED stays open until it is undone or the owner
  accepts it afterwards. Reads and acceptances live in `docs/after-round<N>.json`.
- A surface that did not exist at the snapshot (a new `[published]` field, the alt text of a new chart)
  is covered by no read and no acceptance: it needs a round.
- A third round is possible and never required by the gate except for that case.

What this rule no longer blocks, on purpose: a change to a build script, a `[claims]`, `[allow]` or
`[pairs]` reason, `docs/sources.json` or untemplated MDX front matter that moves no rendered sentence
and no chart, and a round's `fixed` count taken alone. The `fresh`, `published` and `sources` checks
still guard those. On a post whose last snapshot predates per-file hashes (the six closed before
2026-11-16) the gate cannot tell which input moved: any input change shows as one marker row, which the
owner accepts as a whole, and the first round opened on such a post lists every chart.

## Changing the gate

A change to the gate starts from a stated invariant and a test that can find violations by itself (a
model test, a replay on real posts, mutants). It gets ONE attack round and ONE verification round, and
fixes only what breaks a real post, what the previous gate caught, or what lets through a defect on
record. Everything else becomes a line in the next section or its own task.

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
- Chart text is not read sentence by sentence: a changed chart file is one `[chart]` item of the next
  round's inventory and one row of `changed`, through its own hash.
- A cut that changes the meaning by what it removes (a qualifier, a unit word, a sign word such as
  "minus", part of a number written in words). The one read exists for that.
- A cut is recognised only where the sentence stood. A sentence that was cut and also moved, or cut
  between repeated sentences that the comparison lines up elsewhere, shows as new words plus a deletion:
  more for the owner, never less. Inside one changed stretch, new words that all occur in order in a
  neighbouring deleted sentence are called a cut of it; the row still points the read at that stretch.
- A read or an acceptance is of a text and of the change it is, not of a place: identical sentences on
  one surface share it, and a later change nearby is a row only if a sentence changes. An edit made
  after the read that leaves no row of its own (new words taken out again before anyone accepted them)
  does not void the reads of the sentences around it: after any edit, run the read again.
- Paragraph breaks, line breaks and spacing are not compared. A paragraph regrouped, or a star list run
  into its paragraph, is no row when no sentence and no order changes. The reference list is the
  exception: each paragraph after `## References` is one entry, so entries joined or split by a blank
  line are rows, and a list written without blank lines between its entries is one row.
- A body sentence is split at `U.S.` before a capital; each half is its own row.
- `scope`'s list of moved or deleted sentences holds a deleted one only from a stretch that lost more
  than it gained; a sentence rewritten in place appears as its new text.
- When the panel read the post. A snapshot taken after the panel ran but before `make_verdicts.py` wrote
  the verdicts holds whatever was edited in between. A record written or edited by hand is trusted.
- Two record commands at the same moment (`accept`, `make_final_read.py`) can lose an entry or leave
  `docs/after-round<N>.json` unreadable: run one at a time; if the record is not valid JSON, remove it
  and record again.
- `--starts` that is only a surface label such as `[README.md] ` does not guard a wrong `--index`: type
  the row's own opening words after the label.
- A final read is recorded whole or not at all (a row without a verdict, or evidence under 12 characters,
  voids the run), and recording the same read a second time makes it newer than an acceptance given in
  between.
- `restricted_inputs` is read at `publish-check` only, and checks only that the results file is
  git-ignored.
- `cite` reads only the draft: a README citing a work with no reference entry passes.
- `style` reads READMEs directly inside `data/` and `sources/`, not in folders below them.
- A one-word hyphenated `[claims]` entry licenses every later use of that term.
- A value already in percent whose key name does not say so is multiplied by 100 by `pct0`/`pct1`.
- The percent-unit rule reads a unit named once as covering every percent figure in its sentence, so a second figure printed
  bare beside a stated one passes ('76.4 percent of users, against 54.9 for WhatsApp' is the convention it allows). A sentence
  that opens with a lowercase letter, or that follows a stop inside a link's text or a protected abbreviation ('et al.'), is
  read as part of the one before it; a unit word in a citation's title, a link's text or an address written without
  `https://` counts; for a key in percentage points any 'point' counts ('at that point'); in a joined placeholder only the
  first key's unit is asked for. A table without leading pipes, a heading underlined with '===' or '---', and a
  sentence that ends in a closing mark outside the splitter's set (an HTML tag, '~~', '»') join the next sentence;
  a unit word in a reference-style link label, a double-backtick span or a '~~~' or indented code block counts.
  Chart text is not read for units: a chart names its unit on the axis, and its figures are bound by value.
- A quote whose number uses a mid-dot decimal or space-separated thousands (`11·38`, `1 234`) is not
  read as one number.
- Setting `GATE_IN_SELFTEST` by hand skips the self-test and can still print GATE PASSED; it exists only
  for the self-test's own runs.

Known false positives, each with `[allow]` or rewording as the way out: a README reference list is
scanned for numbers; a `'%.1f'` format string in a chart script reads as `.1`; a name in a citation that holds a
number word or ends in "fold" (`Group of Twenty`, `Penfold`) is reported, and its `[allow]` phrase is the name
without the date; a citation that lists a year or a span and then a date of another kind (`n.d.`, a span, or a year
after a span), such as `(Smith, 2007, n.d., 2012)`, is reported although cite reads it, and giving each date its own
segment, `(Smith, 2007; Smith, n.d.; Smith, 2012)`, clears it; in a README or a published field, a citation inside
parentheses that also hold another pair, such as `(by the consumer price index (CPI); BPS, 2024)`, is reported, and
moving the inner pair out, `(BPS, 2024; the consumer price index, CPI)`, clears it. The percent-unit rule's are cleared by
rewording, never by `[allow]`: it asks for 'percent',
'per cent' or '%' as written, so 'percentage', 'per-cent', 'per&nbsp;cent', '&#37;' and a full-width percent sign are reported,
and so is a gap between two shares printed with `pct0`/`pct1` and named in points (emit it as a `_pp` key); a key whose name says
`pc` (per capita) or `pp` (per person) is read as a percent or as points (rename the key); an abbreviation the splitter does not
protect, such as `U.S.` or `p. 12`, or a quoted question, cuts a sentence in two; a '%' written directly after a link is masked
with the link; a list item takes no unit from the line that introduces the list, and a table row none from a unit named
once in the first column's header or in a caption above the table (name it in each column's header or in the cells); a
hard-wrapped line that opens with a number and '.' or ')', the second '>' line of one quoted sentence and a wrapped image
alt text are cut as sentences of their own; a percent figure inside a URL, a link target or code is still asked for a unit.
- Analysis-code correctness beyond reproducibility, construction alternatives, variable definitions, and
  chart geometry. These are the next phase of the private defect ledger.

Proof of the above: `audit/gate-replay-2026-10-09.txt`, the replay of every attack on the previous
gate and on this gate's first version, against copies of Post 25. The publish rule of 2026-11-16 is
replayed against the rule before it on six real posts in `audit/rounds-replay-2026-11-16.txt`. The percent-unit
rule of 2026-11-17 is replayed on every post with a gate.toml by `gate/replay/replay_units.py`, and the pre-fix Post 31
against the gate before it, in `audit/gate-pct-unit-2026-11-17.txt`.
