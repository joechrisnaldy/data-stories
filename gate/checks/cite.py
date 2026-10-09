"""In-text citations and reference entries match in both directions; the reference list closes the post.

Every 'Name, YEAR' segment of a parenthetical is checked (a multi-citation used to check only its last),
page locators and APA date forms are understood, a narrative citation's surname is read only from its own
clause, and nothing may follow the reference list: an '## Update' appended there was invisible to every
prose check.
"""

import re

from gate.text import body_and_refs

_YEAR = r"(?:1[6-9]\d\d|20\d\d)[a-z]?|n\.d\."
_PAREN = re.compile(r"\(([^()]*)\)")
_SEGMENT = re.compile(r"^(?P<names>[^\d;]*?[A-Z][^\d;]*?),\s*(?P<year>" + _YEAR + r")(?:,\s*(?:p|pp)\.\s*\d+(?:-\d+)?)?$")
_BARE = re.compile(r"^(?P<year>" + _YEAR + r")$")
# 'Author. (Date). Title': the date closes with ')' and a full stop, then the title begins
_ENTRY = re.compile(r"^(?P<author>.+?)\.?\s*\((?P<year>" + _YEAR + r")(?:,\s*[A-Z][a-z]+(?:\s+\d{1,2})?)?\)\.\s+\S")
_NARRATIVE_WORDS = 6


def _entries(refs: str):
    """(entries, failures). An entry is (surname, year, head). A block that parses as none is a failure."""
    out, fails = [], []
    blocks = [" ".join(b.split()) for b in re.split(r"\n\s*\n", refs) if b.strip()]
    for block in blocks:
        if block.startswith("#"):
            fails.append(f"a section follows the reference list ({block[:60]!r}); nothing may come after the "
                         "reference list, because the prose checks stop there")
            continue
        m = _ENTRY.match(block)
        if m:
            out.append((m.group("author").split(",")[0].strip().rstrip("."), m.group("year"), block[:80]))
        else:
            fails.append(f"a block in the reference list is not a reference entry: {block[:90]!r}")
    return out, fails


def _narrative_names(body: str, start: int) -> str:
    """The few words before a bare '(YEAR)', stopping at the previous citation's closing parenthesis."""
    before = body[max(0, start - 200):start]
    before = before.rsplit(")", 1)[-1]
    return " ".join(before.split()[-_NARRATIVE_WORDS:])


def _citations(body: str) -> list:
    out = []
    for m in _PAREN.finditer(body):
        ctx = " ".join(body[max(0, m.start() - 40):m.end()].split())
        for seg in (x.strip() for x in m.group(1).split(";")):
            s = _SEGMENT.match(seg)
            if s:
                out.append((s.group("names"), s.group("year"), ctx))
            elif _BARE.match(seg) and ";" not in m.group(1):
                out.append((_narrative_names(body, m.start()), seg, ctx))
    return out


def check(rendered: str) -> list:
    body, refs = body_and_refs(rendered)
    entries, fails = _entries(refs)
    cited = set()
    for names, year, ctx in _citations(body):
        hits = [e for e in entries if e[1] == year and re.search(r"\b" + re.escape(e[0]) + r"\b", names)]
        if not hits:
            fails.append(f"in-text citation with no reference entry: ...{ctx}")
        cited.update(h[2] for h in hits)
    for surname, year, head in entries:
        if head not in cited:
            fails.append(f"reference entry never cited in the text: {surname} ({year}) {head}")
    return fails
