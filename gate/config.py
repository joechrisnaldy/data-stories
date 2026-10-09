"""Load and validate a post's gate.toml. Every path is made absolute against the post folder.

Strict on purpose: a misspelt optional key used to be ignored, which silently switched whole checks off.
"""

import os
import tomllib
from dataclasses import dataclass, field


class ConfigError(ValueError):
    pass


_REQUIRED = ("slug", "source", "rendered", "results", "build")
_OPTIONAL_PATHS = ("sources", "charts", "docx", "mdx")
_POST_KEYS = set(_REQUIRED) | set(_OPTIONAL_PATHS) | {"chart_dir", "extra", "site_public"}
_SECTIONS = {"post", "allow", "claims", "pairs", "published"}


@dataclass(frozen=True)
class Config:
    root: str
    slug: str
    source: str
    rendered: str
    results: str
    build: tuple
    chart_dir: str
    sources: str = None
    charts: str = None
    docx: str = None
    mdx: str = None
    site_public: str = None     # the site's public folder: each published image src resolves inside it
    extra: tuple = ()           # further (source, rendered) template pairs, e.g. the post README
    allow: dict = field(default_factory=dict)
    claims: dict = field(default_factory=dict)
    pairs: dict = field(default_factory=dict)       # phrase -> {"reason": str, "paths": [result paths]}
    published: dict = field(default_factory=dict)   # MDX field -> template, e.g. "alt:rf-1.png", "excerpt"


def _reasons(table: dict, name: str) -> dict:
    for phrase, reason in table.items():
        if not isinstance(reason, str) or not reason.strip():
            raise ConfigError(f"[{name}] entry {phrase!r} has no reason; every exemption must say why")
        if not phrase.strip():
            raise ConfigError(f"[{name}] has an empty phrase")
    return dict(table)


def _pairs(table: dict) -> dict:
    for phrase, entry in table.items():
        ok = (isinstance(entry, dict) and isinstance(entry.get("reason"), str) and entry["reason"].strip()
              and isinstance(entry.get("paths"), list) and entry["paths"]
              and all(isinstance(x, str) for x in entry["paths"]))
        if not ok:
            raise ConfigError(f"[pairs] entry {phrase!r} must be {{reason = \"...\", paths = [\"result.path\", ...]}}: "
                              "an exemption names exactly which figures it excuses")
    return dict(table)


def load(post_dir: str) -> Config:
    post_dir = os.path.abspath(post_dir)
    path = os.path.join(post_dir, "gate.toml")
    if not os.path.exists(path):
        raise ConfigError(f"no gate.toml in {post_dir}")
    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"gate.toml is not valid TOML: {e}") from e
    unknown = set(raw) - _SECTIONS
    if unknown:
        raise ConfigError(f"unknown section(s) {sorted(unknown)}; allowed: {sorted(_SECTIONS)}")
    post = raw.get("post", {})
    missing = [k for k in _REQUIRED if k not in post]
    if missing:
        raise ConfigError(f"[post] is missing {missing}")
    stray = set(post) - _POST_KEYS
    if stray:
        raise ConfigError(f"[post] has unknown key(s) {sorted(stray)}; allowed: {sorted(_POST_KEYS)}")
    if not (isinstance(post["build"], list) and post["build"] and all(isinstance(b, str) for b in post["build"])):
        raise ConfigError("[post] build must be a non-empty list of script paths")
    extra = post.get("extra", [])
    if not (isinstance(extra, list) and all(isinstance(e, list) and len(e) == 2
                                            and all(isinstance(x, str) and x.strip() for x in e) for e in extra)):
        raise ConfigError("[post] extra must be a list of [source, rendered] pairs")
    p = lambda rel: os.path.normpath(os.path.join(post_dir, rel))
    published = raw.get("published", {})
    if not all(isinstance(v, str) and v.strip() for v in published.values()):
        raise ConfigError("[published] values must be non-empty template strings")
    return Config(
        root=post_dir, slug=post["slug"], source=p(post["source"]), rendered=p(post["rendered"]),
        results=p(post["results"]), build=tuple(p(b) for b in post["build"]),
        chart_dir=p(post.get("chart_dir", "charts")),
        **{k: (p(post[k]) if k in post else None) for k in _OPTIONAL_PATHS + ("site_public",)},
        extra=tuple((p(a), p(b)) for a, b in extra),
        allow=_reasons(raw.get("allow", {}), "allow"), claims=_reasons(raw.get("claims", {}), "claims"),
        pairs=_pairs(raw.get("pairs", {})), published=dict(published))
