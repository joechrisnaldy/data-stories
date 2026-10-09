"""The claims register: every universal, superlative or causal word needs a [claims] entry in gate.toml
naming what licenses it.

This is a register, not a judge. It cannot tell whether the licence is sound; it guarantees that every
such word is listed, with a stated licence, where round 1's logic lens can review it. Universals were the
class most often introduced by fixes (14 of 14 late records), because a refuted universal was usually
replaced with another one.

A licence covers the flagged words INSIDE its phrase, not the whole sentence: otherwise a causal clause
added to a registered sentence by a later fix inherited that sentence's licence. For the same reason a
phrase shorter than three words licenses only a sentence that consists of exactly that phrase, unless it is
a single hyphenated term such as a group name ('never-colonised').
"""

import re

from gate.text import body_and_refs, paragraph_sentences, strip_code

# "cannot" is here because the close of Post 25 asserted an unconditional "cannot be what inverted
# the ranking" that round 4 had to narrow; modal impossibility is a universal claim.
UNIVERSAL = ("every", "everything", "everyone", "all", "none", "never", "always", "only", "nobody",
             "nothing", "cannot", "can't", "can’t", "can not", "impossible", "everywhere", "entirely",
             "uniquely", "solely", "invariably", "throughout", "most", "least", "best", "worst", "unprecedented",
             "not a single", "no other", "no country", "no countries", "no one", "not one")
CAUSAL = ("because", "cause", "causes", "caused", "causing", "drive", "drives", "driven", "drove", "driver",
          "drivers", "driving", "explain", "explains", "explained", "due to", "lead to", "leads to", "led to",
          "leading to", "results in", "resulted in", "responsible for", "determines", "determined",
          "determined by", "produce", "produces", "produced", "prove", "proves", "proved", "proven", "proof",
          "account for", "accounts for", "accounted for", "accounting for", "therefore", "thus", "hence")
# Any superlative: a word ending in -est, except the common words that only look like one. The review of
# v2 found 'hottest', 'poorest' and 'clearest' unflagged, and the live Post 25 draft had two of them.
_NOT_SUPERLATIVE = {
    "honest", "dishonest", "interest", "modest", "immodest", "invest", "divest", "suggest", "protest",
    "test", "pretest", "retest", "contest", "attest", "detest", "rest", "unrest", "arrest", "west",
    "midwest", "northwest", "southwest", "east", "northeast", "southeast", "forest", "request", "bequest",
    "conquest", "inquest", "quest", "harvest", "digest", "ingest", "congest", "manifest", "infest", "chest",
    "nest", "guest", "pest", "vest", "zest", "jest", "crest", "behest", "earnest", "lest", "priest",
    "wrest", "breast", "beast", "feast", "yeast", "tempest", "everest", "budapest"}
# Not listed, deliberately: "first", "any", "each", "whole", "make". They are mostly enumeration or
# idiom, and flagging them would bury the register in noise. Round 1 reads the prose for those.
# Bounded by letters and digits only: an apostrophe, a quote or '_' italics around a word never hides it
_TOKEN = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(t) for t in sorted(UNIVERSAL + CAUSAL, key=len, reverse=True))
                    + r"|[A-Za-z]{2,}est)(?![A-Za-z0-9])", re.I)
_MIN_WORDS = 3


def _norm(s: str) -> str:
    return " ".join(s.split())


def _flags(sentence: str) -> list:
    """Flagged token matches. 'at all' is exempt only as the idiom that ends a clause ('here at all.')."""
    out = []
    for m in _TOKEN.finditer(sentence):
        word = m.group(1).lower()
        if word.endswith("est") and word not in UNIVERSAL + CAUSAL and word in _NOT_SUPERLATIVE:
            continue
        if word == "all" and re.search(r"\bat\s+$", sentence[:m.start()], re.I) \
                and re.match(r"\s*(?:[.,;:!?)\]]|$)", sentence[m.end():]):
            continue
        out.append(m)
    return out


def _short(phrase: str) -> bool:
    """A phrase under three words licenses only a whole sentence, unless it is one hyphenated term."""
    words = phrase.split()
    return len(words) < _MIN_WORDS and not (len(words) == 1 and "-" in words[0].strip(".,;:"))


def _phrase_spans(sentence: str, phrase: str) -> list:
    words = r"\s+".join(re.escape(w) for w in phrase.split())
    spans = [m.span() for m in re.finditer(r"(?<!\w)" + words + r"(?!\w)", sentence)]
    if _short(phrase):
        whole = sentence.strip().strip("*_")
        spans = [sp for sp in spans if sentence[sp[0]:sp[1]].strip("*_") == whole]
    return spans


def check(rendered: str, register: dict, extra=(), readmes=()) -> list:
    """extra: whole strings such as chart text and published fields; readmes: rendered READMEs, read
    sentence by sentence without their code."""
    body, refs = body_and_refs(rendered)
    # the reference list too: a sentence appended to an entry was otherwise read by no check at all
    units = paragraph_sentences(body) + paragraph_sentences(refs) + [_norm(s) for s in extra]
    units += [s for r in readmes for s in paragraph_sentences(strip_code(r))]
    used, fails = set(), []
    for s in units:
        spans = {p: _phrase_spans(s, _norm(p)) for p in register}
        for m in _flags(s):
            lic = [p for p, sp in spans.items() if any(a <= m.start() and m.end() <= b for a, b in sp)]
            if lic:
                used.update(lic)
            else:
                fails.append(f"'{m.group(1)}' needs a [claims] entry whose phrase contains it, naming its licence: "
                             f"{s[:160]}")
    for p in sorted(set(register) - used):
        fails.append(f"[claims] entry {p!r} licenses nothing: remove it or fix the sentence it was for")
    return fails
