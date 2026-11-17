"""Replay the percent-unit rule on the real posts: no live sentence breaks it, and every percent figure is reported
once the unit is taken out of the record it sits in.

For every post with a gate.toml under the blog root, each surface the rule reads (the draft body, every rendered
README template, every [published] field) is checked as the numbers check reads it. Three parts:

1. Baseline: no surface reports a 'names no unit' failure.
2. Sentence mutants: for each sentence of the rule's own splitter that prints a percent figure, every unit word in it
   is deleted, and the check must report each of its figures. This tests the unit words and the cut, not the split.
3. Record mutants, the part independent of the rule's splitter (the attack round of 2026-11-17 found the first
   version of this harness blind to joined sentences): an oracle written here, stricter than the rule, cuts each
   markdown block line (list item, table row, quote, heading, image) on its own and ends a record at every stop
   followed by a space, whatever opens the next. For each record that prints a percent figure, its unit words are
   deleted and the check must report each figure in it, unless the figure's table column names the unit in its
   header. A figure the rule does not report is a DISAGREEMENT, printed with both units, unless every record boundary
   inside the rule's sentence opens with a lowercase letter, which the rule does not split: a known limit, listed.
   The oracle knows the block grammar of the live posts (tables with leading pipes, '-', '*', '+' and numbered lists,
   '#' headings, image and quote lines, hard line breaks); a layout neither knows, such as a table without leading
   pipes or a heading underlined with '===', is one unit to both, and gate/README.md lists it as a limit.

Post 31's defect of 2026-11-17 ('76.4 of internet users') is the case on record. A run that mutates nothing fails.

Run from Projects/analytics-blog:  python3 gate/replay/replay_units.py
Fast (no rebuilds). Not part of the self-test: it reads the live posts.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLOG = os.getcwd()
sys.path.insert(0, ROOT)
from gate import config  # noqa: E402  (the harness lives two folders below the package's parent)
from gate.checks import numbers  # noqa: E402
from gate.render import render  # noqa: E402
from gate.text import body_and_refs, mask_spans, sentence_spans  # noqa: E402

ABBREV = ("et al.", "e.g.", "i.e.", "vs.", "St.", "Dr.", "No.", "cf.")      # as the gate protects them
_ORACLE_BLOCK = re.compile(r"[ \t]*(?:[-*+][ \t]|\d+[.)][ \t]|\||>|#|!\[)")
_ORACLE_ONE_LINE = re.compile(r"[ \t]*(?:\||#|!\[)")
_ORACLE_STOP = re.compile(r"[.!?…][*_)\]\"'”’]*(?:\[\^[^\]\s]+\])?\s+")
_ORACLE_BREAK = re.compile(r"(?:<br\s*/?>|[ ]{2,}|\\)$")


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def surfaces(cfg) -> list:
    """(label, template, is_body) for every surface the rule reads."""
    out = [("draft", _read(cfg.source), True)]
    out += [(os.path.relpath(t, cfg.root), _read(t), False) for t, _ in cfg.extra]
    return out + [(f"[published] {k}", v, False) for k, v in cfg.published.items()]


def unit_fails(tmpl: str, results: dict, src, body: bool) -> list:
    _, binds = render(tmpl, results, src)
    fails = numbers.check(tmpl, binds, {}) if body else numbers.check("", [], {}, templates=[("t", tmpl, binds)])
    return [f for f in fails if "names no unit" in f]


def oracle_records(printed: str) -> list:
    """(start, end, boundary_before) of each record, by this harness's own split (see the docstring)."""
    t = printed
    for a in ABBREV:                                   # as words only, so 'devs.' keeps its stop
        t = re.sub(r"(?<![A-Za-z])" + re.escape(a), lambda m: m.group(0).replace(".", "\x00"), t)
    blocks = []
    for para in re.finditer(r"(?:[^\n]|\n(?![ \t]*\n))+", t):
        start, single = para.start(), False
        for line in re.finditer(r"[^\n]*", t[para.start():para.end()]):
            s, e = para.start() + line.start(), para.start() + line.end()
            if s == e and line.start() > 0:
                continue
            if _ORACLE_BLOCK.match(t, s) or single:
                if s > start:
                    blocks.append((start, s - 1))
                start = s
            single = bool(_ORACLE_ONE_LINE.match(t, s) or _ORACLE_BREAK.search(t, s, e))
        blocks.append((start, para.end()))
    out = []
    for s, e in blocks:
        pos, before = s, ""
        for m in _ORACLE_STOP.finditer(t, s, e):
            out.append((pos, m.end(), before))
            pos, before = m.end(), t[m.end()] if m.end() < e else ""
        out.append((pos, e, before))
    return [(a, b, c) for a, b, c in out if t[a:b].strip()]


def figures(tmpl: str, results: dict, src, body: bool):
    """The printed text, a probe with URLs, link targets, code and comments masked, each source offset's origin, and
    every percent figure as (placeholder span, unit, first printed offset)."""
    text = body_and_refs(tmpl)[0] if body else tmpl
    _, binds = render(tmpl, results, src)
    bound = [b for b in binds if b.end <= len(text)]
    printed, origin = numbers._printed(text, bound)
    masks = (numbers._URL, numbers._LINK_TARGET, numbers._NOT_PROSE)
    probe = mask_spans(printed, [m.span() for rx in masks for m in rx.finditer(printed)])
    figs = {}
    for b in bound:
        unit = numbers._printed_unit(b)
        if unit and (b.start, b.end) not in figs:
            figs[(b.start, b.end)] = (unit, origin.index((b.start, b.end)))
    return printed, probe, origin, figs


def cut(tmpl: str, origin: list, probe: str, units: set, a: int, e: int) -> str:
    """tmpl with every unit word of `units` printed in [a, e) deleted (a space before each goes too)."""
    spans = sorted({(origin[m.start()][0], origin[m.end() - 1][1])
                    for u in units for m in numbers._UNIT_NAMED[u].finditer(probe, a, e)
                    if all(origin[i][1] - origin[i][0] == 1 for i in range(m.start(), m.end()))}, reverse=True)
    for s0, s1 in spans:
        s0 -= 1 if s0 and tmpl[s0 - 1] == " " else 0
        tmpl = tmpl[:s0] + tmpl[s1:]
    return tmpl


def reported(fails: list, tmpl: str, span: tuple) -> bool:
    return any(f.startswith(tmpl[span[0]:span[1]] + " prints a percent") for f in fails)


def main() -> int:
    posts = sorted(os.path.dirname(p) for p in glob.glob(os.path.join(BLOG, "*", "gate.toml")))
    tally = {"baseline": 0, "sentences": 0, "sentences caught": 0, "records": 0, "records caught": 0,
             "header": 0, "lowercase": 0, "disagree": 0}
    for post in posts:
        cfg = config.load(post)
        results = json.loads(_read(cfg.results))
        src = json.loads(_read(cfg.sources)) if cfg.sources else None
        name = os.path.basename(post)
        for label, tmpl, body in surfaces(cfg):
            base = unit_fails(tmpl, results, src, body)
            tally["baseline"] += len(base)
            for f in base:
                print(f"BASELINE FAILS  {name} | {label} | {f}")
            printed, probe, origin, figs = figures(tmpl, results, src, body)
            covered = {s for s, (u, at) in figs.items() if (lambda c: c and numbers._UNIT_NAMED[u].search(
                probe[c[0]:c[1]]))(numbers._header_cell(printed, at))}
            records = oracle_records(printed)
            for a, e in sentence_spans(printed):                       # part 2
                inside = {s: u for s, (u, at) in figs.items() if a <= at < e and s not in covered}
                if not inside:
                    continue
                fails = unit_fails(cut(tmpl, origin, probe, set(inside.values()), a, e), results, src, body)
                ok = all(reported(fails, tmpl, s) for s in inside)
                tally["sentences"] += 1
                tally["sentences caught"] += ok
                if not ok:
                    print(f"MISSED  sentence  {name} | {label} | {' '.join(printed[a:e].split())[:110]}")
            for a, e, before in records:                                # part 3
                inside = {s: u for s, (u, at) in figs.items() if a <= at < e}
                if not inside:
                    continue
                fails = unit_fails(cut(tmpl, origin, probe, set(inside.values()), a, e), results, src, body)
                tally["records"] += 1
                missed = []
                for s, u in inside.items():
                    cell = numbers._header_cell(printed, figs[s][1])
                    if cell and numbers._UNIT_NAMED[u].search(probe[cell[0]:cell[1]]):
                        tally["header"] += 1
                    elif not reported(fails, tmpl, s):
                        missed.append(tmpl[s[0]:s[1]])
                if not missed:
                    tally["records caught"] += 1
                    continue
                at = figs[next(s for s in inside if tmpl[s[0]:s[1]] in missed)][1]
                rule = next(((x, y) for x, y in sentence_spans(printed) if x <= at < y), (a, e))
                inner = [printed[s] for s, _, _ in records if rule[0] < s < rule[1]]
                kind = "lowercase" if inner and all(c.islower() for c in inner) else "disagree"
                tally[kind] += 1
                print(f"{'KNOWN LIMIT (record opens lowercase)' if kind == 'lowercase' else 'DISAGREEMENT'}  {name} | "
                      f"{label} | record: {' '.join(printed[a:e].split())[:90]!r} | rule's sentence: "
                      f"{' '.join(printed[rule[0]:rule[1]].split())[:90]!r} | not reported: {', '.join(missed)}")
    print(f"\n{len(posts)} posts; baseline failures {tally['baseline']}; sentence mutants {tally['sentences caught']} of "
          f"{tally['sentences']} caught; record mutants {tally['records caught']} of {tally['records']} caught "
          f"({tally['header']} figure(s) covered by a column header, {tally['lowercase']} known-limit record(s), "
          f"{tally['disagree']} disagreement(s))")
    if not tally["sentences"] or not tally["records"]:
        print("REPLAY FAILED: NO PERCENT SENTENCES FOUND, so nothing was tested")
        return 1
    if tally["baseline"] or tally["sentences caught"] < tally["sentences"] or tally["disagree"]:
        print("REPLAY FAILED")
        return 1
    print("REPLAY OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
