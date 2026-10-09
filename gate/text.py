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
