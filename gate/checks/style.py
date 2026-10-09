"""House rule: no em dash, en dash or Unicode minus on any surface, including inside images, the Word
draft and the published MDX.

Markdown surfaces are also checked for the spellings that become dashes on the live page: the site's
typography step turns '--' into a dash, and '&mdash;' and friends are dashes in all but name.
"""

import os
import re
import zipfile

FORBIDDEN = re.compile(r"[‐-―−]")
_MD_DASH = re.compile(r"(?<![-|])--(?![-|])|&(?:mdash|ndash|minus);|&#(?:8211|8212|8722);|&#x(?:2013|2014|2212);", re.I)
_CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
_SKIP_DIRS = {"data", "sources", "__pycache__", ".rounds"}
_BINARY = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".dta", ".pyc", ".xlsx")


def check_strings(named: dict) -> list:
    return [f"{name}: forbidden character {m.group()!r} in {text[:80]!r}"
            for name, text in named.items() for m in [FORBIDDEN.search(text)] if m]


def _docx_text(path: str) -> str:
    with zipfile.ZipFile(path) as z:
        return "\n".join(z.read(n).decode("utf-8", "replace") for n in z.namelist()
                         if n.startswith("word/") and n.endswith(".xml"))


def _read_text(path: str):
    """Decoded text, or None for a binary file."""
    if path.endswith(".docx"):
        return _docx_text(path)
    with open(path, "rb") as f:
        raw = f.read()
    if b"\x00" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def text_files(cfg) -> list:
    """Every non-binary file in the post (data and stored sources aside), plus the .docx and MDX."""
    out = []
    for root, dirs, files in os.walk(cfg.root):
        for d in dirs:
            # a skipped folder's committed README is still prose (data/README.md)
            if d in _SKIP_DIRS and d != "__pycache__" and os.path.isdir(os.path.join(root, d)):
                out += [os.path.join(root, d, f) for f in os.listdir(os.path.join(root, d))
                        if f.lower().startswith("readme") and f.lower().endswith((".md", ".txt"))]
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
        out += [os.path.join(root, f) for f in files if not f.lower().endswith(_BINARY) and not f.startswith("~$")]
    for extra in (cfg.docx, cfg.mdx):
        if extra and os.path.exists(extra) and extra not in out:
            out.append(extra)
    return sorted(p for p in out if os.path.isfile(p))


def check_files(paths) -> list:
    fails = []
    for p in paths:
        text = _read_text(p)
        if text is None:
            continue
        markdown = p.endswith((".md", ".mdx"))
        scan = _CODE.sub(lambda m: " " * len(m.group(0)), text) if markdown else text
        for i, line in enumerate(scan.split("\n"), 1):
            for m in FORBIDDEN.finditer(line):
                fails.append(f"{p}:{i}: forbidden character {m.group()!r}: {line.strip()[:90]}")
            if markdown and not re.fullmatch(r"\s*-{3,}\s*", line):
                for m in _MD_DASH.finditer(line):
                    fails.append(f"{p}:{i}: {m.group()!r} renders as a dash on the live page: {line.strip()[:90]}")
    return fails
