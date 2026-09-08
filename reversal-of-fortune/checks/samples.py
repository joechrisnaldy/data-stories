"""Two correlations in one sentence must share a sample, or must name a sample size for each.

This defect shipped three times in one post: the rival-variable comparison (n=196 beside n=159),
chart 2's two panels (97 beside 98), and the never-colonised pair (76 beside 85). Each read as a
single comparison and was not one. corr() drops NA pairwise, so every correlation silently gets its
own sample, and the prose is the only place the mismatch becomes visible.
"""

import re

SIGNED = re.compile(r"(?:minus|plus)\s+\d+\.\d+")
# "across 163 countries", "on the 159 countries ... for", "43 countries on each side", "n = 97"
SHARED = re.compile(
    r"\b(?:across|among|on|of)\s+(?:the\s+|all\s+)?\d{2,3}\s+(?:countries|places|entities|of them)"
    r"|\bon\s+each\s+side\b|\beach\s+side\b|\bn\s*=\s*\d{2,3}\s*(?:each|per)\b",
    re.I)
COUNTED = re.compile(r"\b(?:across|among|on|of)\s+(?:the\s+)?(\d{2,3})\b|\bn\s*=\s*(\d{2,3})\b", re.I)


def sentences(text: str) -> list:
    body = text.split("## Method notes")[0]
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    return [" ".join(s.split()) for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


def check(draft: str) -> list:
    fails = []
    for s in sentences(draft):
        vals = SIGNED.findall(s)
        if len(vals) < 2:
            continue
        if SHARED.search(s):
            continue
        ns = [g for pair in COUNTED.findall(s) for g in pair if g]
        if len(ns) >= len(vals):
            continue
        fails.append(f"{len(vals)} correlations, {len(ns)} sample size(s), no shared-sample phrase: {s[:150]}")
    return fails
