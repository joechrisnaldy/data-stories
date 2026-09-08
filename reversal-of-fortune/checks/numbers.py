"""Every quantity the draft asserts must be reproduced by a script in this repository.

Round 2 shipped seven figures no script emitted; round 3 shipped two more. The rule already existed,
in CLAUDE.md and in build_analysis.py's own docstring. Nothing enforced it, so nothing obeyed it.

Numbers legitimately absent from results.json are the ones taken from a source rather than computed.
Those live in EXTERNAL below, each with its citation, so the list itself is auditable.
"""

import re

# Structural numbers: years, journal volumes, page references, chart counts, prose quantities.
STRUCTURAL = {1000, 1500, 1978, 1991, 1995, 1997, 2002, 2012, 2020, 2021, 2023, 2026,
              1, 2, 3, 4, 5, 28, 117, 1243}

# Figures taken from a source rather than computed here. Each needs a citation in the draft.
EXTERNAL = {
    -0.38: "AJR 2002, Table V Panel A col 1, coefficient",
    0.34: "AJR 2002, Table V Panel A col 1, R-squared",
    1.3: "Dell et al. 2012, p. 67, percentage points of growth per degree",
}

APPROX = re.compile(r"\b(?:about|roughly|around|nearly|almost)\s+$", re.I)


def result_numbers(results: dict) -> set:
    out = set()

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, (int, float)) and o == o:
            for p in (0, 1, 2, 3):
                out.add(round(float(o), p))
    walk(results)
    return out


def _sig(v: float, n: int = 2) -> float:
    """Round to n significant figures, for prose that says 'about 130,000'."""
    if v == 0:
        return 0.0
    from math import floor, log10
    return round(v, -int(floor(log10(abs(v)))) + (n - 1))


def draft_numbers(text: str) -> list:
    """(value, is_approx, context) for every quantity the prose asserts.

    The reference list and every URL are excluded: DOIs and page ranges are not results.
    """
    body = text.split("## References")[0]
    body = re.sub(r"https?://\S+", " ", body)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)

    found, consumed = [], []
    for m in re.finditer(r"\b(minus|plus)\s+(\d+(?:\.\d+)?)", body):
        v = float(m.group(2)) * (-1 if m.group(1) == "minus" else 1)
        found.append((v, False, body[max(0, m.start() - 60):m.end() + 20]))
        consumed.append((m.start(), m.end()))
    for m in re.finditer(r"(?<![\w.,])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?:st|nd|rd|th)?(?![\w,])", body):
        if any(a <= m.start() < b for a, b in consumed):
            continue          # already counted as a signed correlation
        v = float(m.group(1).replace(",", ""))
        pre = body[max(0, m.start() - 30):m.start()]
        found.append((v, bool(APPROX.search(pre)), body[max(0, m.start() - 60):m.end() + 20]))
    return found


def check(draft: str, results: dict) -> list:
    known = result_numbers(results) | {float(x) for x in STRUCTURAL} | set(EXTERNAL)
    approx_known = {_sig(k) for k in known} | {_sig(k, 3) for k in known}
    fails = []
    for v, is_approx, ctx in draft_numbers(draft):
        if any(abs(v - k) < 1e-9 for k in known):
            continue
        if is_approx and any(abs(_sig(v) - k) < 1e-9 or abs(_sig(v, 3) - k) < 1e-9
                             for k in approx_known):
            continue
        fails.append(f"{v:g} has no source in results.json or EXTERNAL: ...{' '.join(ctx.split())}...")
    return fails
