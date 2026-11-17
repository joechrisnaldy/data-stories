"""Splitting prose into the units the checks reason about, with offsets back into the source."""

import re

_ABBREV = ("et al.", "e.g.", "i.e.", "vs.", "St.", "Dr.", "No.", "cf.")
_SENT_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(*\[])")


def body_and_refs(text: str):
    """Split at a '## References' heading; the reference list is checked separately."""
    m = re.search(r"^##\s+References\s*$", text, re.M)
    return (text, "") if not m else (text[:m.start()], text[m.end():])


def paragraphs(text: str):
    """(start, end) offsets of each non-blank paragraph, separated by blank lines, trimmed."""
    out, pos = [], 0
    bounds = [(m.start(), m.end()) for m in re.finditer(r"\n[ \t]*\n", text)] + [(len(text), len(text))]
    for sep_start, sep_end in bounds:
        a, b = pos, sep_start
        while a < b and text[a].isspace():
            a += 1
        while b > a and text[b - 1].isspace():
            b -= 1
        if a < b:
            out.append((a, b))
        pos = sep_end
    return out


def sentences(text: str):
    protected = text
    for i, a in enumerate(_ABBREV):
        protected = protected.replace(a, a.replace(".", f"\x00{i}\x00"))
    parts = _SENT_END.split(" ".join(protected.split()))
    restore = lambda s: re.sub(r"\x00(\d+)\x00", ".", s)
    return [restore(p).strip() for p in parts if p.strip()]


# The units the percent-unit rule reads, finer than paragraph_sentences (which the rounds use, and which stays as it
# is): within a paragraph, a list item, a table row, a heading, an image line and a quote line each start a new one,
# and a heading, an image line, a table row and a line ending in a hard break end with their line; a stop ends a
# sentence even when closing marks follow it ('.**', '._', '."', '.)', '.[^1]'), and the next one may open with
# anything but a lowercase letter. The attack and verification rounds of 2026-11-17 printed Post 31's bare
# '76.4 of internet users' through each of those layouts with the rule's earlier splitters, which joined them.
_BLOCK = re.compile(r"[ \t]*(?:[-*+][ \t]|\d+[.)][ \t]|\||>|#{1,6}(?=\s|$)|!\[)")
_ONE_LINE = re.compile(r"[ \t]*(?:\||#{1,6}(?=\s|$)|!\[)")
_STOP = re.compile(r"[.!?…][*_)\]\"'”’]*(?:\[\^[^\]\s]+\])?(?=\s)")
_HARD_BREAK = re.compile(r"(?:<br\s*/?>|(?<! )[ ]{2,}|\\)$")       # a run starts once, so a long one is linear


def _split(t: str, s: int, e: int) -> list:
    spans, start = [], s
    for m in _STOP.finditer(t, s, e):
        nxt = m.end()
        while nxt < e and t[nxt].isspace():
            nxt += 1
        if nxt < e and not t[nxt].islower():
            spans.append((start, m.end()))
            start = nxt
    spans.append((start, e))
    out = []
    for a, b in spans:
        while a < b and t[a].isspace():
            a += 1
        while b > a and t[b - 1].isspace():
            b -= 1
        if a < b:
            out.append((a, b))
    return out


def sentence_spans(text: str):
    """(start, end) offsets of each unit of the percent-unit rule (see above), in text order."""
    protected = text
    for a in _ABBREV:            # protected only as a word of its own ('devs.' keeps its stop); same length, so offsets hold
        protected = re.sub(r"(?<![^\W\d_])" + re.escape(a), lambda m: m.group(0).replace(".", "\x00"), protected)
    out = []
    for a, b in paragraphs(protected):
        cuts, pos = {a, b}, a
        while pos < b:
            end = protected.find("\n", pos, b)
            end = b if end == -1 else end
            if _BLOCK.match(protected, pos):
                cuts.add(pos)
            if _ONE_LINE.match(protected, pos) or _HARD_BREAK.search(protected, pos, end):
                cuts.add(end)
            pos = end + 1
        bounds = sorted(cuts)
        for s, e in zip(bounds, bounds[1:]):
            out += _split(protected, s, e)
    return out


def mask_spans(text: str, spans) -> str:
    """Replace each (start, end) span with spaces, keeping every other offset unchanged."""
    chars = list(text)
    for a, b in spans:
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def paragraph_sentences(text: str):
    """Sentences split within paragraphs, so a heading or image line never joins the sentence before it."""
    return [s for a, b in paragraphs(text) for s in sentences(text[a:b])]


_FENCE = re.compile(r"^```.*?^```", re.S | re.M)
_INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """A README with its fenced blocks and inline code blanked out: code is identifiers, not prose."""
    return mask_spans(text, [m.span() for rx in (_FENCE, _INLINE_CODE) for m in rx.finditer(text)])
