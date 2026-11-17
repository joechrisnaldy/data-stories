"""Replay attacks on the gate against throwaway copies of a real post, and record what it catches.

The 2026-10-09 audit defeated the previous gate with these attacks on a scratch copy of Post 25. This
harness applies each to a fresh temp copy, runs `python3 -m gate`, and compares the problems reported
with the baseline run. An attack is CAUGHT when the expected check reports a problem the baseline did
not. Attacks expected NOT to be caught are the gate's honest limit, and are recorded as such.

An attack that tampers with a figure asks the gate's own renderer what the post prints for it (`figure`),
so it keeps finding its target after the post's data changes. On 2026-11-16 eleven attacks had gone stale
because they hard-coded figures (minus 0.44, n = 196) and sentences that later rounds of Post 25 changed.
An attack whose anchor is gone is reported as ERROR and fails the run: it is never counted as caught, and
an honest-limit attack passes only as NOT CAUGHT. A gate run that prints no verdict line, or hangs, is an
error, never zero problems. Some attacks still hang on a sentence of the post ('The sign flipped.' among
them): when one is reworded they ERROR, which is the signal to point them at the new wording.

Run from Projects/analytics-blog:  python3 gate/replay/replay_audit.py reversal-of-fortune
Slow by design (each run rebuilds the post twice). Not part of the self-test.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

GATE_TIMEOUT = 900   # seconds per gate run; a hang is an error, never waited on silently or read as no problems

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from gate.render import render, resolve  # noqa: E402  (the harness lives two folders below the package's parent)


def run_gate(post: str) -> dict:
    try:
        r = subprocess.run([sys.executable, "-m", "gate", post], cwd=ROOT, capture_output=True, text=True,
                           timeout=GATE_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"gate run exceeded {GATE_TIMEOUT}s on {post}") from None
    if not re.search(r"^(GATE PASSED|GATE FAILED|GATE INCOMPLETE|setup +FAILED)", r.stdout, re.M):
        last = ((r.stdout + r.stderr).strip().splitlines() or ["no output"])[-1]
        raise RuntimeError(f"the gate gave no verdict (exit {r.returncode}): {last[:140]}")
    problems, current = {}, None
    for line in r.stdout.splitlines():
        m = re.match(r"^(\w+)\s+(\d+) problem", line)
        if m:
            current = m.group(1)
            problems.setdefault(current, [])
        elif line.startswith("            - ") and current:
            problems[current].append(line.strip()[2:])
        elif re.match(r"^\w+\s+ok", line):
            current = None
        if line.startswith(("config ", "setup ", "render    FAILED")):
            problems.setdefault("config", []).append(line)
    return problems


def copy_post(post: str) -> str:
    d = tempfile.mkdtemp(prefix="replay-")
    dst = os.path.join(d, os.path.basename(post))
    shutil.copytree(os.path.join(ROOT, post), dst, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    cfg = os.path.join(dst, "gate.toml")
    text = open(cfg).read()
    mdx = re.search(r'^mdx = "([^"]+)"', text, re.M)
    if mdx:                        # the MDX lives outside the post folder; point the copy at it absolutely
        absolute = os.path.normpath(os.path.join(ROOT, post, mdx.group(1)))
        local = os.path.join(dst, "published.mdx")
        shutil.copy(absolute, local)
        # and tell it where the site's public folder is, so the copy still compares images with the charts
        public = os.path.join(absolute.split(os.sep + "src" + os.sep)[0], "public")
        text = text.replace(mdx.group(0), f'mdx = "published.mdx"\nsite_public = "{public}"')
    open(cfg, "w").write(text)
    return dst


def edit(path, old, new, count=1):
    s = open(path).read()
    if old not in s:
        raise LookupError(f"attack anchor not found in {os.path.basename(path)}: {old[:60]!r}")
    open(path, "w").write(s.replace(old, new, count))


def figure(d, path, fmt, by=0):
    """What the post prints for results[path] in format `fmt`; with `by`, the same figure wrong by that much."""
    value = resolve(path, json.load(open(f"{d}/results.json")))[3]
    return render("{{x:" + fmt + "}}", {"x": value + by}, None)[0]


def retype(d, rel, path, fmt, by, within=None):
    """Hand-edit one printed figure in a file, as an attacker with an editor would: the first place the post
    prints results[path], or the first such place inside a stretch matching the pattern `within`."""
    file = f"{d}/{rel}"
    text = open(file).read()
    shown = figure(d, path, fmt)
    printed = re.compile(r"(?<![\w.])(?<!\d[,-])" + re.escape(shown) + r"(?![\w])(?![.,-]\d)")   # never inside a longer number
    stretches = re.finditer(within, text, re.S | re.M) if within else [re.match(r".*", text, re.S)]
    hit = next((m for m in stretches if printed.search(m.group(0))), None)
    if not hit:
        raise LookupError(f"attack anchor not found in {os.path.basename(file)}: {shown!r}" + (f" inside {within!r}" if within else ""))
    wrong = figure(d, path, fmt, by)
    if wrong == shown:
        raise ValueError(f"attack changes nothing: {path} still prints {wrong!r} when off by {by}")
    changed = printed.sub(wrong, hit.group(0), count=1)
    open(file, "w").write(text[:hit.start()] + changed + text[hit.end():])


def rerender(d):
    subprocess.run([sys.executable, "-m", "gate", "render", d], cwd=ROOT, capture_output=True, check=True)


def regenerate(d):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    for script in ("build_analysis.py", "make_charts.py"):
        subprocess.run([sys.executable, script], cwd=d, env=env, capture_output=True, check=True)


def _swap_document(d, head, keep_quote=False):
    """Replace the stored Dell et al. text and update its recorded hash, as a careful attacker would."""
    import hashlib
    src = json.load(open(f"{d}/docs/sources.json"))
    body = src["dell2012"]["quote"] if keep_quote else open(f"{d}/sources/dell2012.txt").read().split("\n", 8)[-1]
    text = head + body + "\n"
    open(f"{d}/sources/dell2012.txt", "w").write(text)
    src["dell2012"]["sha256"] = hashlib.sha256(text.encode()).hexdigest()
    json.dump(src, open(f"{d}/docs/sources.json", "w"), indent=1, ensure_ascii=False)


def _stale_chart(d):
    """Regenerate the charts from an edited script, then put the script back: the committed chart is stale."""
    path = f"{d}/make_charts.py"
    original = open(path).read()
    title = re.search(r'ax\.set_title\(\s*"([^"\\]*[a-z][^"\\]*)"\s*[,)]', original)    # the first title typed as plain text
    if not title:
        raise LookupError("attack anchor not found in make_charts.py: ax.set_title(\"...\") with a plain lower-case string")
    open(path, "w").write(original[:title.start(1)] + title.group(1).upper() + original[title.end(1):])
    regenerate(d)
    open(path, "w").write(original)


def _stale_results(d):
    """Bump one n in the committed results, so they no longer match a clean rebuild."""
    n = json.load(open(f"{d}/results.json"))["tidy_story"]["n"]
    edit(f"{d}/results.json", f'"n": {n}', f'"n": {n + 1}')


def _requote_meta_description(d):
    """Rewrite the page's metaDescription in single quotes with one figure changed, as a hand edit would."""
    path = f"{d}/published.mdx"
    text = open(path).read()
    field = re.search(r'^metaDescription: "([^"\\]*)"$', text, re.M)
    if not field:
        raise LookupError("attack anchor not found in published.mdx: a double-quoted metaDescription with no escapes")
    open(path, "w").write(text[:field.start()] + "metaDescription: '" + field.group(1).replace("'", "''") + "'" + text[field.end():])
    retype(d, "published.mdx", "tidy_story.r", "signed2", -0.05, within=r"^metaDescription: '[^\n]*'$")


def _swap_two_keys(d):
    """Swap the two flip figures' keys in the draft, re-render, and republish on the page each line the re-render
    changed (found by line, never by searching the page for a printed figure, which can match another sentence)."""
    before = open(f"{d}/{RENDERED}").read().splitlines()
    f, n = (f"{{{{{key}.r:signed2}}}}" for key in (F, N))
    edit(f"{d}/{SRC}", f, "@@F@@")
    edit(f"{d}/{SRC}", n, f)
    edit(f"{d}/{SRC}", "@@F@@", n)
    rerender(d)
    changed = [(a, b) for a, b in zip(before, open(f"{d}/{RENDERED}").read().splitlines()) if a != b]
    if not changed:
        raise ValueError("attack changes nothing: the two figures print alike")
    for a, b in changed:
        edit(f"{d}/published.mdx", a, b)


def _point_images_at_copy(d):
    """Copy this post's live images into a copy of the public folder and point the config at it."""
    cfg = f"{d}/gate.toml"
    text = open(cfg).read()
    live = re.search(r'^site_public = "([^"]+)"', text, re.M)
    srcs = re.findall(r'<img src="/([^"]+)"', open(f"{d}/published.mdx").read())
    for rel in srcs:
        os.makedirs(os.path.dirname(f"{d}/site-public/{rel}"), exist_ok=True)
        shutil.copy(os.path.join(live.group(1), rel), f"{d}/site-public/{rel}")
    open(cfg, "w").write(text.replace(live.group(0), f'site_public = "{d}/site-public"'))
    return srcs


def _set_source_value(d, key, name, value, quote=None):
    src = json.load(open(f"{d}/docs/sources.json"))
    src[key]["values"][name] = value
    if quote is not None:
        src[key]["quote"] = quote
    json.dump(src, open(f"{d}/docs/sources.json", "w"), indent=1, ensure_ascii=False)
    rerender(d)


SRC = "draft/the-map-used-to-run-the-other-way.src.md"
RENDERED = "draft/the-map-used-to-run-the-other-way.md"
F, N = "flip.density_1500|income_2023|former_colonies", "flip.density_1500|income_2023|never_colonised"
# two eras' figures for one group, computed on different samples (77 and 87 places on 2026-11-16), printed beside
# the n of a third sample, the places measurable in both eras, which belongs to neither: the round-3 defect
THEN, NOW = ("{{heat_reversal.never_colonised.vs_density_1500.r:signed2}}",
             "{{heat_reversal.never_colonised.vs_income_2023.r:signed2}}")
ELSEWHERE = "Elsewhere, across the {{never_colonised_common_sample.n:int}} places measurable in both eras, it ran"

# (name, expected check or None if it should NOT be caught, mutation)
ATTACKS = [
    ("word quantity rewritten ('a fifth' to 'nine tenths')", "numbers",
     lambda d: edit(f"{d}/{SRC}", "{{tidy_story.r2_share:fraction}}", "nine tenths")),
    ("fabricated number followed by a comma", "numbers",
     lambda d: edit(f"{d}/{SRC}", "Nothing. A flat cloud.", "Nothing across 941, a flat cloud.")),
    ("figure hand-typed in place of its placeholder", "numbers",
     lambda d: edit(f"{d}/{SRC}", "the correlation is **{{tidy_story.r:signed2}}**",
                        f"the correlation is **{figure(d, 'tidy_story.r', 'signed2')}**")),
    ("figure in 'r = -0.49' notation", "numbers",
     lambda d: edit(f"{d}/{SRC}", "This is the test the argument actually rests on.", "This is the test (r = -0.49) the argument rests on.")),
    ("hand-typed figure hidden in the method notes", "numbers",
     lambda d: edit(f"{d}/{SRC}", "Income is logged in every correlation", "Income is logged in 97 correlations")),
    ("external figure laundered with an invented citation", "sources",
     lambda d: (edit(f"{d}/{SRC}", "I nearly wrote it as one.", "I nearly wrote it as one. Nunn (2008) puts it at {{src:nunn2008.values.fe:signed2}}."),
                edit(f"{d}/{SRC}", "McEvedy, C., & Jones, R. (1978).", "Nunn, N. (2008). The long-term effects of Africa's slave trades. *QJE*.\n\nMcEvedy, C., & Jones, R. (1978)."),
                edit(f"{d}/docs/sources.json", '"dell2012": {', '"nunn2008": {"ref": "Nunn 2008", "title": "The long-term effects", "doc": "sources/nunn2008.txt", "sha256": "0", "quote": "fixed effect -0.9137", "values": {"fe": -0.9137}},\n "dell2012": {'),
                rerender(d))),
    ("cited figure from the superseded working paper (1.1 for 1.3)", "sources",
     lambda d: (edit(f"{d}/docs/sources.json", '"growth_pp": 1.3', '"growth_pp": 1.1'), rerender(d))),
    ("working paper stored in place of the cited article, hash updated to match", "sources",
     lambda d: _swap_document(d, "Climate Change and Economic Growth\nNBER Working Paper 14132\n")),
    ("round-3 defect: two eras' figures from different samples, no n", "pairs",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", f"The sign flipped. {ELSEWHERE} {THEN} then and {NOW} now."), rerender(d))),
    ("the same defect split across two sentences", "pairs",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", f"The sign flipped. {ELSEWHERE} {THEN} then. Now it is {NOW}."), rerender(d))),
    ("universal introduced by a fix", "claims",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped in every former colony."), rerender(d))),
    ("causal claim introduced by a fix", "claims",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "Colonisation caused the sign to flip."), rerender(d))),
    ("narrative citation with no reference entry", "cite",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped, as Nunn (2020) argues."), rerender(d))),
    ("reference entry never cited", "cite",
     lambda d: (edit(f"{d}/{SRC}", "McEvedy, C., & Jones, R. (1978).", "Nunn, N. (2008). The long-term effects. *QJE*.\n\nMcEvedy, C., & Jones, R. (1978)."), rerender(d))),
    ("rendered draft hand-edited after rendering", "rendered",
     lambda d: retype(d, RENDERED, "tidy_story.r", "signed2", -0.05)),
    ("stale committed results.json", "fresh", _stale_results),
    ("hardcoded wrong annotation on a chart, regenerated", "panels",
     lambda d: (edit(f"{d}/make_charts.py", "f\"r = {r['r']:+.2f}   n = {r['n']}\"", "\"r = +0.81   n = 250\""), regenerate(d))),
    ("en dash in a chart legend, regenerated", "style",
     lambda d: (edit(f"{d}/make_charts.py", 'label="Income today"', 'label="Income \\u2013 today"'), regenerate(d))),
    ("em dash in the post README", "style",
     lambda d: open(f"{d}/README.md", "a").write("\nAn aside — here.\n")),
    ("broken image link", "links",
     lambda d: (edit(f"{d}/{SRC}", "../charts/rf-4-who-actually-reversed.png", "../charts/missing.png"), rerender(d))),
    ("hand-edited figure in a published alt text", "published",
     lambda d: retype(d, "published.mdx", "tidy_story.r", "signed2", -0.05, within=r'alt="[^"]*"')),
    ("published body drifts from the draft", "published",
     lambda d: edit(f"{d}/published.mdx", "The sign flipped.", "The sign flipped, decisively.")),
    ("exemption added without a reason", "config",
     lambda d: edit(f"{d}/gate.toml", "[allow]\n", '[allow]\n"97" = ""\n')),
    # ---- attacks on the first version of this gate (v1), each fixed in v2
    ("sign word typed by hand beside a placeholder", "numbers",
     lambda d: (edit(f"{d}/{SRC}", "{{tidy_story.r2_share:fraction}}", "minus {{tidy_story.r2_share:dec2}}"), rerender(d))),
    ("quantity written as a verb ('doubled')", "numbers",
     lambda d: (edit(f"{d}/{SRC}", "Nothing. A flat cloud.", "Nothing. The cloud doubled."), rerender(d))),
    ("figure hand-typed in a README nobody renders", "numbers",
     lambda d: (os.makedirs(f"{d}/docs/notes", exist_ok=True),
                open(f"{d}/docs/notes/README.md", "w").write("The flip is minus 0.81 among colonies.\n"))),
    ("figure hand-typed into a chart label, regenerated", "numbers",
     lambda d: (edit(f"{d}/make_charts.py", 'label="Income today"', 'label="Income today (r = 0.81)"'), regenerate(d))),
    ("section appended after the reference list", "cite",
     lambda d: (open(f"{d}/{SRC}", "a").write("\n## Update\n\nThe flip held at minus 0.49 in 2026.\n"), rerender(d))),
    ("second citation of a multi-citation points at no entry", "cite",
     lambda d: (edit(f"{d}/{SRC}", "(Acemoglu et al., 2002), and", "(Acemoglu et al., 2002; Dell et al., 2013), and"), rerender(d))),
    ("causal clause appended to a registered sentence", "claims",
     lambda d: (edit(f"{d}/{SRC}", "unless its effect changed.", "unless its effect changed, because colonisation caused it."), rerender(d))),
    ("new figure from a third sample inside an exempted paragraph", "pairs",
     lambda d: (edit(f"{d}/{SRC}", "somewhere else.", "somewhere else. Colonisation tracks latitude at {{colonisation_vs_latitude.r:signed2}}."), rerender(d))),
    ("'--' in the draft, which the site renders as a dash", "style",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped -- decisively."), rerender(d))),
    ("cited value with its sign flipped against a signed quote", "sources",
     lambda d: _set_source_value(d, "ajr2002_coef", "coef", 0.38)),
    ("cited value matching only part of a number in the quote (3 inside 1.3)", "sources",
     lambda d: _set_source_value(d, "dell2012", "growth_pp", 3)),
    ("quote widened to a whole table row with several numbers", "sources",
     lambda d: _set_source_value(d, "ajr2002_r2", "r2", 0.34, quote="R2 0.34 0.55 0.27")),
    ("committed chart no script produces", "fresh",
     lambda d: shutil.copy(f"{d}/charts/rf-1-the-tidy-story.png", f"{d}/charts/rf-5-orphan.png")),
    ("committed chart stale against its script", "fresh", _stale_chart),
    ("single-quoted front matter field edited by hand", "published", _requote_meta_description),
    ("published caption edited away from the chart's footnote", "published",
     lambda d: retype(d, "published.mdx", "tidy_story.n", "int", 1, within=r"<figcaption>.*?</figcaption>")),
    ("published image is not the chart the scripts produce", "published",
     lambda d: shutil.copy(f"{d}/charts/rf-2-the-same-heat-in-1500.png",
                           f"{d}/site-public/" + next(r for r in _point_images_at_copy(d) if r.endswith("rf-1-the-tidy-story.png")))),
    ("rendered README hand-edited after rendering", "rendered",
     lambda d: retype(d, "README.md", "tidy_story.r", "signed2", -0.05, within=r"^\|[^\n]*\|$")),
    # ---- attacks from the review of v2, each fixed in v3
    ("quote shortened to a bare number found elsewhere in the paper (sign dropped)", "sources",
     lambda d: _set_source_value(d, "ajr2002_coef", "coef", 0.38, quote="0.38")),
    ("quote cut inside a number ('by about 1' from 'by about 1.3')", "sources",
     lambda d: _set_source_value(d, "dell2012", "degrees", 1,
                                 quote="reduced economic growth in that year by about 1")),
    ("source figure read from outside 'values'", "config",
     lambda d: (edit(f"{d}/docs/sources.json", '"growth_pp": 1.3', '"growth_pp": 1.3\n  },\n  "extra": {\n   "growth_pp": 1.1'),
                edit(f"{d}/{SRC}", "{{src:dell2012.values.growth_pp:dec1}}", "{{src:dell2012.extra.growth_pp:dec1}}"))),
    ("paragraph cites the working-paper year for the article's figure", "sources",
     lambda d: (edit(f"{d}/{SRC}", "Dell et al. (2012) use", "Dell et al. (2008) use"), rerender(d))),
    ("stored title loosened to a generic phrase", "sources",
     lambda d: edit(f"{d}/docs/sources.json", '"title": "Temperature shocks and economic growth"', '"title": "economic growth"')),
    ("claim appended inside the reference list", "claims",
     lambda d: (open(f"{d}/{SRC}", "a").write("Heat explains all of the gap.\n"), rerender(d))),
    ("mixed-sample pair added to a README template", "pairs",
     lambda d: (open(f"{d}/docs/README.src.md", "a").write(
         "\nIt ran {{heat_reversal.former_colonies.vs_density_1500.r:signed2}} then and "
         "{{flip.density_1500|income_2023|former_colonies.r:signed2}} now.\n"), rerender(d))),
    ("external figure in a README paragraph that cites nobody", "sources",
     lambda d: (open(f"{d}/docs/README.src.md", "a").write(
         "\nGrowth fell by {{src:dell2012.values.growth_pp:dec1}} points a year.\n"), rerender(d))),
    ("sign word typed into a chart annotation, regenerated", "numbers",
     lambda d: (edit(f"{d}/make_charts.py", "f\"r = {r['r']:+.2f}   n = {r['n']}\", transform=ax.transAxes,\n",
                     "f\"r = minus {abs(r['r']):.2f}   n = {r['n']}\", transform=ax.transAxes,\n"), regenerate(d))),
    ("single-panel footnote prints the wrong n, regenerated", "panels",
     lambda d: (edit(f"{d}/make_charts.py", "Every entity with both, {t['n']} of them", "Every entity with both, {t['n'] - 1} of them"),
                regenerate(d))),
    ("APA-style figure with a leading dot", "numbers",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped (r = .44)."), rerender(d))),
    ("hard-wrapped line that starts with a figure", "numbers",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped across\n197. countries."), rerender(d))),
    ("superlative outside the old word list", "claims",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped in the hottest places."), rerender(d))),
    ("one-word licence covering a new causal clause", "claims",
     lambda d: (edit(f"{d}/gate.toml", "[claims]\n", '[claims]\n"because" = "too short to locate anything"\n'),
                edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped because of colonisers."), rerender(d))),
    ("pairs exemption keyed on a placeholder name", "pairs",
     lambda d: edit(f"{d}/gate.toml", '"Two things worth saying" = {', '"tidy_story" = {')),
    ("em dash in the data README template", "style",
     lambda d: (open(f"{d}/docs/data-README.src.md", "a").write("\nAn aside \u2014 here.\n"), rerender(d))),
    ("published image linked from a stale copy at another path", "published",
     lambda d: (_point_images_at_copy(d),
                os.makedirs(f"{d}/site-public/images/blog/old", exist_ok=True),
                shutil.copy(f"{d}/charts/rf-2-the-same-heat-in-1500.png", f"{d}/site-public/images/blog/old/rf-1-the-tidy-story.png"),
                edit(f"{d}/published.mdx", 'src="/images/blog/rf-1-the-tidy-story.png"', 'src="/images/blog/old/rf-1-the-tidy-story.png"'))),
    ("percent formatter on a key already in percent", "config",
     lambda d: (edit(f"{d}/{SRC}", "{{indonesia.density_pct:ordinal0}}", "{{indonesia.density_pct:pct0}}"))),
    ("config extra entry that is not a pair of paths", "config",
     lambda d: edit(f"{d}/gate.toml", 'extra = [["docs/README.src.md", "README.md"]', 'extra = [[1, 2], ["docs/README.src.md", "README.md"]')),
    # ---- attacks from the diff-scoped review of v3, each fixed before this replay
    ("universal beside an apostrophe ('Everyone's')", "claims",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "Everyone's ranking flipped."), rerender(d))),
    ("universal in underscore italics", "claims",
     lambda d: (edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped in _every_ colony."), rerender(d))),
    ("hard-wrapped figure inside a numbered list in a README", "numbers",
     lambda d: (open(f"{d}/docs/data-README.src.md", "a").write(
         "\n1. Of the colonies, the count fell to\n   197. The rest were dropped.\n"), rerender(d))),
    ("percent formatter on a key named as a percentage", "config",
     lambda d: (edit(f"{d}/results.json", '"indonesia": {', '"indonesia": {"pct_density": 78.72340425531915, '),
                edit(f"{d}/{SRC}", "{{indonesia.density_pct:ordinal0}}", "{{indonesia.pct_density:pct0}}"))),
    # Round bookkeeping (re-closing a round, a manifest change after the last clean round) is exercised
    # in gate/tests/test_rounds.py rather than here.
    # ---- the honest limit: these are expected to pass
    ("two figures' keys swapped, re-rendered and republished consistently", None, _swap_two_keys),
    ("forged source document carrying the cited title and the quote", None,
     lambda d: _swap_document(d, "Temperature Shocks and Economic Growth\n(forged)\n", keep_quote=True)),
    ("figure laundered through an [allow] entry with a plausible reason", None,
     lambda d: (edit(f"{d}/gate.toml", "[allow]\n", '[allow]\n"0.81" = "a figure from the literature"\n'),
                edit(f"{d}/{SRC}", "The sign flipped.", "The sign flipped, at 0.81."), rerender(d),
                edit(f"{d}/published.mdx", "The sign flipped.", "The sign flipped, at 0.81."))),
]


def replay(post, baseline, attack):
    name, expected, mutate = attack
    d = copy_post(post)
    try:
        mutate(d)
        got = run_gate(d)
    except Exception as e:                       # a mutation that cannot be applied is reported, not hidden
        return name, expected, "ERROR", str(e)[:200]
    finally:
        shutil.rmtree(os.path.dirname(d), ignore_errors=True)
    new = {k: [p for p in v if p not in baseline.get(k, [])] for k, v in got.items()}
    new = {k: v for k, v in new.items() if v}
    if expected is None:
        return name, expected, "NOT CAUGHT (expected)" if not new else "CAUGHT", "; ".join(f"{k}" for k in new)
    if any("CRASHED" in p for v in new.values() for p in v):
        return name, expected, "CRASHED", "; ".join(p for v in new.values() for p in v if "CRASHED" in p)[:170]
    hit = expected in new
    return name, expected, "CAUGHT" if hit else "MISSED", (new.get(expected, [""])[0] if hit else f"new problems only in: {sorted(new)}")[:170]


def main(post):
    base_copy = copy_post(post)
    baseline = run_gate(base_copy)
    shutil.rmtree(os.path.dirname(base_copy), ignore_errors=True)
    print(f"baseline: {sum(len(v) for v in baseline.values())} problem(s) in {sorted(baseline)}\n", flush=True)
    rows = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(replay, post, baseline, a) for a in ATTACKS]
        for fut in as_completed(futures):
            name, expected, verdict, detail = fut.result()
            rows.append((name, expected, verdict, detail))
            print(f"{verdict:22s} {('[' + expected + ']') if expected else '[limit]':12s} {name}\n{'':35s}{detail}", flush=True)
    caught = sum(1 for r in rows if r[1] and r[2] == "CAUGHT")
    should = sum(1 for r in rows if r[1])
    limits = sum(1 for r in rows if r[1] is None and r[2].startswith("NOT CAUGHT"))
    errors = sum(1 for r in rows if r[2] == "ERROR")
    print(f"\n{caught} of {should} attacks caught by the expected check; {limits} of "
          f"{len(rows) - should} honest-limit attacks pass, as documented; {errors} attack(s) in ERROR")
    return 0 if caught == should and limits == len(rows) - should and not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
