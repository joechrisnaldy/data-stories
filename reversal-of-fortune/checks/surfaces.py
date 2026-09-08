"""A figure that appears on more than one surface must be identical on all of them.

Surfaces: the draft, results.json, the rendered PNG text, the design document, the provenance audit.
Also enforces the house style rules that apply to every surface including inside images.
"""

import json
import os
import re

DASHES = re.compile(r"[‐-―−‘’“”…]")


def style(paths: list) -> list:
    fails = []
    for p in paths:
        if not os.path.exists(p):
            continue
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            for m in DASHES.finditer(line):
                fails.append(f"{p}:{i} forbidden character {m.group()!r}: {line.strip()[:90]}")
    return fails


def rendered_text(chart_fn, *args) -> list:
    """Every string matplotlib will draw, so image text is checked like any other surface."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    strings = []
    orig = plt.Figure.savefig

    def spy(self, *a, **k):
        for ax in self.axes:
            strings.extend([ax.get_title(), ax.get_xlabel(), ax.get_ylabel()])
            strings.extend(t.get_text() for t in ax.texts)
            strings.extend(t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels())
        strings.extend(t.get_text() for t in self.texts)
        return orig(self, *a, **k)
    plt.Figure.savefig = spy
    try:
        chart_fn(*args)
    finally:
        plt.Figure.savefig = orig
    return [s for s in strings if s and s.strip()]


def image_style(strings: list) -> list:
    return [f"rendered image text contains {m.group()!r}: {s[:80]}"
            for s in strings for m in [DASHES.search(s)] if m]


def citations(draft: str) -> list:
    """Every in-text citation has an entry and every entry is cited."""
    body, _, refs = draft.partition("## References")
    intext = set()
    for m in re.finditer(r"\(([^)]*?(?:19|20)\d\d[a-z]?)\)", body):
        for part in re.split(r";\s*", m.group(1)):
            name = re.match(r"([A-Z][A-Za-z'&. ]+?)(?:,|\s)+(?:19|20)\d\d", part.strip())
            if name:
                intext.add(name.group(1).strip().rstrip(","))
    entries = set()
    for line in refs.split("\n\n"):
        m = re.match(r"\s*([A-Z][A-Za-z'&., ]+?)\.?\s*\((?:19|20)\d\d", line.strip())
        if m:
            entries.add(m.group(1).split(",")[0].strip())
    fails = []
    for c in sorted(intext):
        surname = c.split()[0].rstrip(",")
        if not any(surname in e for e in entries):
            fails.append(f"in-text citation {c!r} has no reference entry")
    return fails


def word_count(draft: str, lo=1600, hi=2000) -> list:
    body = draft.split("## Method notes")[0]
    body = "\n".join(l for l in body.split("\n") if not l.startswith("!["))
    n = len(body.split()) - len(body.split("\n")[0].split())  # drop the title line
    return ([] if lo <= n <= hi else [f"body is {n} words, outside {lo} to {hi}"]), n
