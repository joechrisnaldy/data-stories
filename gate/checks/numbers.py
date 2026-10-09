"""Every quantity in the prose is bound to a result, or exempted by an [allow] phrase with a reason.

Digits are found regardless of what follows them, quantities written as words are found from a fixed
lexicon, and a sign or a percent typed by hand next to a placeholder is reported, because each of those
let a wrong figure through an earlier version (see audit/gate-replay-2026-10-09.txt).
"""

import os
import re

from gate.render import percent_unit
from gate.text import body_and_refs, mask_spans, paragraphs

# A digit preceded by a letter, another digit or a dot belongs to a name or a number already being read
# (ERA5, G20, PM2.5), so a number may only START after anything else, including '=' or '('.
# An underscore may precede a figure ('_0.44_' is italics), and so may a bare dot ('r = .44', APA style,
# or '.5' glued after a placeholder).
_DIGITS = re.compile(r"(?<![A-Za-z\d.])\.?\d+(?:[.,]\d+)*")
_FRACTION_CHARS = re.compile(r"[¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]")
_ORDINALS = ("third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|"
             "fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|thirtieth|fortieth|fiftieth|"
             "sixtieth|seventieth|eightieth|ninetieth|hundredth|thousandth")
_WORDS = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|"
    r"ninety|hundreds?|thousands?|millions?|billions?|trillions?|dozens?|half|halves|quarters?|thirds|fifths|"
    r"sixths|sevenths|eighths|ninths|tenths|" + _ORDINALS + r"|"
    r"halv(?:e|ed|es|ing)|doubl(?:e|ed|es|ing)|tripl(?:e|ed|es|ing)|quadrupl\w*|\w+fold|twice)\b", re.I)
# 'first' and 'second' are left out: they are overwhelmingly enumerators ('First, ...', 'a second round').
_URL = re.compile(r"https?://\S+")
_LINK_TARGET = re.compile(r"\]\([^)]*\)")
_YEAR = r"(?:1[6-9]\d\d|20\d\d)[a-z]?"
# Only the 'Name..., YEAR(, p. N)' segments of a citation are masked, never other text in the same
# parentheses: '(by 1.1 points; Dell et al., 2012)' still exposes '1.1'.
_CITE_SEGMENT = re.compile(r"(?<=[(;])\s*[^()\d;]*?[A-Z][^()\d;]*?,\s*" + _YEAR +
                           r"(?:,\s*(?:p|pp)\.\s*\d+(?:-\d+)?)?\s*(?=[;)])")
_CITE_YEAR = re.compile(r"\(" + _YEAR + r"\)")
_GAP = r"(?:\s|&nbsp;|&#160;|\u00a0)*"
_SIGN_BEFORE = re.compile(r"(?:\b(?:minus|plus|negative|positive)|[-+−])" + _GAP + r"(?:\*{1,2}|_)?" + _GAP + "$",
                          re.I)
_PERCENT_AFTER = re.compile(r"^" + _GAP + r"-?(?:\*{1,2}|_)?" + _GAP + r"(?:per\s*cent|percent|percentage|%)", re.I)
_POINTS_AFTER = re.compile(r"^" + _GAP + r"-?(?:\*{1,2}|_)?" + _GAP + r"percentage\s+points?\b", re.I)


# In READMEs only, code is identifiers, not claims: a fenced block and an inline span that contains a
# letter ('`ex2col == 0`' yes, '`0.44`' no: a bare figure in backticks is still a figure). The post itself
# masks no code. Everywhere, an ordered-list marker is structure, but only in a paragraph that opens as a
# list: a hard-wrapped line can start with '197. The rest'.
_FENCE = re.compile(r"^```.*?^```", re.S | re.M)
_INLINE_CODE = re.compile(r"`[^`\n]*[A-Za-z][^`\n]*`")
_LIST_MARKER = re.compile(r"^[ \t]*(\d+)\.(?=[ \t])", re.M)


def _list_markers(text: str) -> list:
    """Markers of a numbered list: the paragraph opens with one, and each later one is the next number. A
    hard-wrapped '197.' inside item 1 is not item 2, so it stays a figure."""
    spans = []
    for a, b in paragraphs(text):
        start = text.rfind("\n", 0, a) + 1              # back to the line start, so an indented list counts
        markers = list(_LIST_MARKER.finditer(text[start:b]))
        if not markers or markers[0].start() != 0:
            continue
        expected = int(markers[0].group(1))
        for m in markers:
            if int(m.group(1)) == expected:
                spans.append((start + m.start(), start + m.end()))
                expected += 1
    return spans


def _masked(source: str, bindings, readme: bool = False) -> str:
    """The text to scan. The post stops at its reference list (cite checks that); a README is read whole."""
    body = source if readme else body_and_refs(source)[0]
    spans = [(b.start, b.end) for b in bindings if b.end <= len(body)]
    for rx in (_URL, _LINK_TARGET, _CITE_SEGMENT, _CITE_YEAR) + ((_FENCE, _INLINE_CODE) if readme else ()):
        spans += [m.span() for m in rx.finditer(body)]
    return mask_spans(body, spans + _list_markers(body))


def _covered(text: str, allow: dict):
    intervals, used = [], set()
    for phrase in allow:
        words = r"\s+".join(re.escape(w) for w in phrase.split())
        for m in re.finditer(r"(?<!\w)" + words + r"(?!\w)", text):
            intervals.append(m.span())
            used.add(phrase)
    return intervals, used


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _scan(text: str, where, allow: dict, used: set) -> list:
    intervals, hit = _covered(text, allow)
    used.update(hit)
    fails = []
    for rx, kind in ((_DIGITS, "number"), (_WORDS, "number word"), (_FRACTION_CHARS, "fraction")):
        for m in rx.finditer(text):
            if any(a <= m.start() and m.end() <= b for a, b in intervals):
                continue
            ctx = " ".join(text[max(0, m.start() - 50):m.end() + 30].split())
            fails.append(f"unbound {kind} {m.group(0)!r} at {where(m.start())}: ...{ctx}...")
    return fails


def _beside(text: str, bindings, where) -> list:
    """A sign or a percent typed by hand next to a placeholder."""
    fails = []
    for b in bindings:
        before, after = text[max(0, b.start - 24):b.start], text[b.end:b.end + 24]
        if _SIGN_BEFORE.search(before):
            fails.append(f"a sign is typed by hand before {{{{{b.path}:{b.fmt}}}}} at {where(b.start)}: "
                         f"the formatter must carry the sign (use signed{b.fmt[-1] if b.fmt[-1].isdigit() else 2})")
        unit = percent_unit(b.leaf)
        points = unit == "pp" and _POINTS_AFTER.search(after)
        if _PERCENT_AFTER.search(after) and not (b.fmt.startswith("pct") or unit == "pct" or points):
            fails.append(f"{{{{{b.path}:{b.fmt}}}}} is printed as a percent at {where(b.start)} but is neither "
                         f"formatted with pct0/pct1 nor a key ending in _pct (or _pp, for percentage points): "
                         f"off by a factor of 100?")
    return fails


def check(source: str, bindings, allow: dict, extra: dict = None, templates=()) -> list:
    """Prose, plus extra hand-typed text (chart-script literals keyed by file:line), plus further templates
    as (label, text, bindings): published fields, extra templates, unconfigured READMEs."""
    used = set()
    text = _masked(source, bindings)
    body_where = lambda pos: f"line {_line_of(text, pos)}"
    fails = _scan(text, body_where, allow, used)
    fails += _beside(body_and_refs(source)[0], [b for b in bindings if b.end <= len(text)], body_where)
    for label, lit in (extra or {}).items():
        fails += _scan(lit, lambda pos, label=label: label, allow, used)
    for label, tmpl, binds in templates:
        masked = _masked(tmpl, binds, readme=True)
        fails += _scan(masked, lambda pos, label=label: label, allow, used)
        fails += _beside(tmpl, binds, lambda pos, label=label: label)
    for phrase in sorted(set(allow) - used):
        fails.append(f"[allow] entry {phrase!r} matches nothing in the prose: remove it")
    return fails


def unconfigured_readmes(cfg) -> list:
    """README files in the post that are not rendered from a template; their figures are hand-typed."""
    rendered = {p for pair in cfg.extra for p in pair}   # outputs, and the templates checked as templates
    out = []
    for root, dirs, files in os.walk(cfg.root):
        dirs[:] = [d for d in dirs if d not in {"sources", "__pycache__", ".rounds"}]
        out += [os.path.join(root, f) for f in files
                if f.lower().startswith("readme") and f.endswith(".md") and os.path.join(root, f) not in rendered]
    return sorted(out)


def _values(obj, out: list, key: str = ""):
    """Every number in the results, with the key it sits under."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            _values(v, out, str(k))
    elif isinstance(obj, list):
        for v in obj:
            _values(v, out, key)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool) and obj == obj:
        out.append((float(obj), key))
    return out


_SIGNED_NUMBER = re.compile(r"(?<![A-Za-z_\d.])([+-]?)(\d+(?:,\d{3})*(?:\.\d+)?)")
_SIGN_WORD = re.compile(r"\b(minus|negative|plus|positive)\s*$", re.I)
_PCT_AFTER = re.compile(r"^\s*(?:%|per\s*cent\b|percent\b)", re.I)


_R_SHOWN = re.compile(r"\br\s*=\s*(minus\s+|negative\s+|plus\s+|[+-])?(\d*\.\d+|\d+)", re.I)
_N_EQ = re.compile(r"\bn\s*=\s*([\d,]+)", re.I)


def _stat_objects(obj, out: list) -> list:
    """Every result object that carries both an r and an n."""
    if isinstance(obj, dict):
        if isinstance(obj.get("r"), (int, float)) and isinstance(obj.get("n"), (int, float)):
            out.append(obj)
        for v in obj.values():
            _stat_objects(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _stat_objects(v, out)
    return out


def _paired(text: str, stats: list):
    """A text printing one 'r = X' and one 'n = Y' must print them from the same result object: matched
    separately, a sign-flipped r found an unrelated correlation elsewhere in the results."""
    rs, ns = _R_SHOWN.findall(text), _N_EQ.findall(text)
    if len(rs) != 1 or len(ns) != 1:
        return None
    sign, digits = rs[0]
    places = len(digits.split(".")[1]) if "." in digits else 0
    r = float(digits) * (-1 if sign.strip().lower() in ("-", "minus", "negative") else 1)
    n = int(ns[0].replace(",", ""))
    if any(o["n"] == n and round(o["r"], places) == round(r, places) for o in stats):
        return None
    return f"prints r = {r:+.{places}f} with n = {n}, but no single result has both"


def chart_figures(capture: list, results: dict, src: dict, allow: dict) -> list:
    """Every figure a chart prints (tick labels aside) must be a result at its printed precision, read as
    written: a bare number is not negative, 'minus' makes it negative, and a percent is a share times 100
    or a key already in percent.

    Weaker than binding, because chart text is generated by code rather than a template, but it catches
    the hand-typed 'r = +0.81' and figures built in ways the source scan cannot see.
    """
    known = _values(results, []) + _values(src or {}, [])
    stats = _stat_objects(results, [])
    plain = {v for v, _ in known}
    percent = {v * 100 for v, _ in known} | {v for v, k in known if re.search(r"_(?:pct|pp)$", k)}
    fails = []
    for rec in capture:
        for text in rec.get("prose", []):
            intervals, _ = _covered(text, allow)
            pair = _paired(text, stats) if not intervals else None
            if pair:
                fails.append(f"{rec['file']}: {pair}: {' '.join(text.split())[:80]!r}")
            for m in _SIGNED_NUMBER.finditer(text):
                if any(a <= m.start(2) and m.end(2) <= b for a, b in intervals):
                    continue
                digits = m.group(2).replace(",", "")
                places = len(digits.split(".")[1]) if "." in digits else 0
                word = _SIGN_WORD.search(text[:m.start()])
                negative = m.group(1) == "-" or (not m.group(1) and word and word.group(1).lower() in ("minus", "negative"))
                value = float(digits) * (-1 if negative else 1)
                pool = percent if _PCT_AFTER.match(text[m.end():]) else plain
                if not any(round(k, places) == round(value, places) for k in pool):
                    fails.append(f"{rec['file']}: the chart prints {(word.group(0) if word else '') + m.group(0)!r}, "
                                 f"which is no result at that precision and sign: {' '.join(text.split())[:80]!r}")
    return fails
