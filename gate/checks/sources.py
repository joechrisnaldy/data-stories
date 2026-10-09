"""External figures are bound to a stored, hash-pinned copy of the cited document.

For every {{src:...}} placeholder: the document is on disk with the recorded sha256; the verbatim quote
occurs in it exactly once, starting and ending on whole tokens; the quote contains the value; the reference list has the entry; the entry's title opens
the stored document (so a press release or working paper cannot stand in for the cited article); and the
paragraph using the figure cites that reference. This replaces an allowlist that accepted any figure an
author typed in with an invented citation.
"""

import hashlib
import os
import re

from gate.text import body_and_refs, mask_spans, paragraphs

# The title must open the document: the first-page header, not anywhere on page two, where a running
# header repeats it. Measured: both stored Post 25 sources carry their title within 200 characters.
_TITLE_WINDOW = 600


def normalise(text: str) -> str:
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"-\s*\n\s*", "", text)          # rejoin words hyphenated across a line break
    return " ".join(text.split())


_QUOTE_NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")


def _quote_numbers(quote: str) -> list:
    """Every number in the (normalised) quote as a signed float, in order."""
    return [float(m.group(0)) for m in _QUOTE_NUMBER.finditer(quote)]


def _values_fail(key: str, values: dict, quote: str) -> list:
    """Each value must equal a distinct number in the quote exactly, sign included, and the quote may hold
    no more numbers than values: a whole table row would let a figure from the wrong column pass."""
    nums, fails = _quote_numbers(quote), []
    if len(nums) > len(values):
        fails.append(f"src:{key}: the quote holds {len(nums)} numbers for {len(values)} value(s); quote only the "
                     "cell or phrase each value comes from")
    pool = list(nums)
    for name, v in values.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            fails.append(f"src:{key}.values.{name} is not a number: {v!r}")
        elif float(v) in pool:
            pool.remove(float(v))
        else:
            fails.append(f"src:{key}.values.{name} = {v} is not a number in its quote, sign included: {quote[:90]!r}")
    return fails


def _clean_occurrence(text: str, quote: str) -> bool:
    """The quote occurs where it neither starts nor ends inside a number or a word: '0.38' cut from
    '-0.38' drops a sign, '11.3' cut from '11.38' drops a digit."""
    start = text.find(quote)
    while start != -1:
        before, after = text[start - 1:start], text[start + len(quote):start + len(quote) + 2]
        head_ok = not before or not (before.isalnum() or (quote[0] in "0123456789." and before in ".,-+"))
        tail_ok = not after or not (after[0].isalnum() or (quote[-1].isdigit() and re.match(r"[.,]\d", after)))
        if head_ok and tail_ok:
            return True
        start = text.find(quote, start + 1)
    return False


def _entry_titles(entry: str) -> set:
    """The title of an APA entry, whole and up to its colon: '(Year). Title: Subtitle. *Journal*'."""
    m = re.search(r"\)\.\s+(.+)", entry)
    if not m:
        return set()
    rest = m.group(1)
    if rest[0] in "*_":                                 # an italic title: a book, a report, a data set
        end = rest.find(rest[0], 1)
        title = rest[1:end] if end > 0 else ""
    else:                                               # up to the full stop that ends it
        t = re.match(r"(.+?)[.?!](?:\s|$)", rest)
        title = t.group(1) if t else rest
    full = normalise(re.sub(r"[*_]", "", title)).strip(" .?!").lower()
    return {full, full.split(":")[0].strip()} if full else set()


def _cites(para: str, surname: str, year: str) -> bool:
    """A real citation of Surname (Year) or (Surname ..., Year), not the year inside some other word."""
    y = re.escape(year) + r"[a-z]?"
    narrative = r"\b" + re.escape(surname) + r"\b[^()\n]{0,80}?\(\s*" + y + r"\s*(?:,[^()]*)?\)"
    paren = r"\([^()]*\b" + re.escape(surname) + r"\b[^()]*?,\s*" + y + r"\b[^()]*\)"
    flat = " ".join(para.split())
    return bool(re.search(narrative, flat) or re.search(paren, flat))


def _split_ref(ref) -> tuple:
    parts = str(ref or "").rsplit(" ", 1)
    if len(parts) != 2 or not parts[1][:4].isdigit():
        raise ValueError(f"ref must be 'Surname YEAR', got {ref!r}")
    return parts[0], parts[1]


def _ref_entry(refs: str, ref: str):
    surname, year = _split_ref(ref)
    for block in re.split(r"\n\s*\n", refs):
        flat = " ".join(block.split())
        if flat.startswith(surname) and f"({year})" in flat:
            return flat
    return None


def _check_entry(key: str, e: dict, refs: str, root: str) -> list:
    fails = []
    doc = os.path.join(root, e.get("doc", ""))
    if not os.path.isfile(doc):
        return [f"src:{key}: stored document {e.get('doc')!r} not found; fetch the cited document itself"]
    with open(doc, "rb") as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != e.get("sha256"):
        fails.append(f"src:{key}: sha256 of {e['doc']} does not match sources.json; the stored copy changed")
    text = normalise(raw.decode("utf-8", "replace"))
    quote = normalise(e.get("quote", ""))
    if not quote or quote not in text:
        fails.append(f"src:{key}: the quote does not occur verbatim in {e['doc']}: {quote[:90]!r}")
    elif text.count(quote) > 1:
        fails.append(f"src:{key}: the quote occurs {text.count(quote)} times in {e['doc']}; quote enough of its "
                     f"row or sentence to locate one place: {quote[:90]!r}")
    elif not _clean_occurrence(text, quote):
        fails.append(f"src:{key}: the quote starts or ends inside a number or a word in {e['doc']}, which can "
                     f"drop a sign or a digit; quote whole tokens: {quote[:90]!r}")
    fails += _values_fail(key, e.get("values", {}), quote)
    try:
        entry = _ref_entry(refs, e.get("ref"))
    except ValueError as err:
        return fails + [f"src:{key}: {err}"]
    title = normalise(e.get("title", "")).lower()
    if entry is None:
        fails.append(f"src:{key}: no reference entry for {e.get('ref')!r}")
    elif not title or re.sub(r"[*_]", "", title).strip(" .?!") not in _entry_titles(entry):
        fails.append(f"src:{key}: title {e.get('title')!r} is not the title of the reference entry, whole or up "
                     "to its colon")
    if title and title not in text[:_TITLE_WINDOW].lower():
        fails.append(f"src:{key}: title {e.get('title')!r} does not open {e['doc']}; "
                     "is this the cited document or a summary, mirror or earlier version of it?")
    return fails


def check(source: str, rendered: str, bindings, src: dict, root: str) -> list:
    if not src:
        return []
    _, refs = body_and_refs(rendered)
    used = sorted({b.path.split(".")[0] for b in bindings if b.origin == "src"})
    fails = []
    for key in used:
        fails += _check_entry(key, src[key], refs, root)
    body, _ = body_and_refs(source)
    for a, b in paragraphs(body):
        for x in bindings:
            if x.origin != "src" or not (a <= x.start and x.end <= b):
                continue
            entry = src[x.path.split(".")[0]]
            try:
                surname, year = _split_ref(entry.get("ref"))
            except ValueError:
                continue                      # already reported by _check_entry
            # placeholders are masked: the year inside a key such as 'dell2012' is not a citation
            para = mask_spans(body, [(y.start, y.end) for y in bindings if a <= y.start and y.end <= b])[a:b]
            cited = _cites(para, surname, year)
            aliased = any(re.search(r"\b" + re.escape(al) + r"\b", para) for al in entry.get("aliases", []))
            if not (cited or aliased):
                fails.append(f"src:{x.path} is used in a paragraph that does not cite {surname} ({year})")
    return fails
