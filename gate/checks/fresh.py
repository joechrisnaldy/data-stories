"""Rebuild the post twice in temporary copies and compare with what is committed.

Committed vs fresh is compared by MEANING, not bytes: results.json numerically (relative tolerance
1e-12, ten times the measured drift and far below any change that alters a printed figure) and charts
by the largest per-pixel change. Measured on Post 25 after the macOS 27 upgrade
(2026-09-16), unchanged code and data drifted by at most 1 part in 1e13 in regression outputs and by
at most 2/255 in 117 to 271 anti-aliased pixels, while changing one annotation digit moved 863 pixels
by up to 255/255. Two back-to-back fresh builds must still match byte for byte (determinism).

Never writes into the post folder. The previous gate re-ran the build scripts in place halfway through
its own run, overwriting the results.json it had just checked against; a stale artifact was silently
refreshed instead of reported.
"""

import filecmp
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

# gate/checks/fresh.py -> the directory that CONTAINS the gate package, so "-m gate.chart_capture" imports
BUILD_TIMEOUT = 900
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf")
GATE_PARENT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SKIP = shutil.ignore_patterns("__pycache__", ".rounds", "*.docx", "~$*")


class _Outside(Exception):
    pass


def _isolate(cfg, where: str) -> None:
    """Re-point absolute links that lead back into the post at the copy, so a build reads and writes only
    the copy; then remove the outputs, so whatever no script regenerates shows up as missing."""
    for root, dirs, files in os.walk(where):
        for name in dirs + files:
            p = os.path.join(root, name)
            if os.path.islink(p):
                target = os.readlink(p)
                if os.path.isabs(target) and (target == cfg.root or target.startswith(cfg.root + os.sep)):
                    os.unlink(p)
                    os.symlink(os.path.join(where, os.path.relpath(target, cfg.root)), p)
    copy_root = os.path.realpath(where)
    for out in (cfg.results, cfg.chart_dir):
        resolved = os.path.realpath(os.path.join(where, os.path.relpath(out, cfg.root)))
        if not (resolved == copy_root or resolved.startswith(copy_root + os.sep)):
            raise _Outside(f"{os.path.relpath(out, cfg.root)} resolves outside the post through a link; the gate "
                           "will not empty or rebuild it, so it cannot be checked. Keep outputs inside the post")
    results = os.path.join(where, os.path.relpath(cfg.results, cfg.root))
    if os.path.exists(results):
        os.remove(results)
    # empty the chart folder but keep it: a fresh clone has the folder, and a script may rely on that.
    # A folder that is a link is replaced, never emptied: emptying it deleted the files it points at.
    charts_copy = os.path.join(where, os.path.relpath(cfg.chart_dir, cfg.root))
    if os.path.islink(charts_copy):
        os.unlink(charts_copy)
        os.makedirs(charts_copy)
    elif os.path.isdir(charts_copy):
        for name in os.listdir(charts_copy):
            p = os.path.join(charts_copy, name)
            shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)


def _run(cmd, where, env, label):
    try:
        r = subprocess.run(cmd, cwd=where, env=env, capture_output=True, text=True, timeout=BUILD_TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"{label} exceeded {BUILD_TIMEOUT}s in a clean copy"
    return f"{label} failed in a clean copy: {r.stderr.strip()[-400:]}" if r.returncode else None


def _build(cfg, where: str):
    # symlinks are copied as links, never followed: a post folder may hold a link back into itself
    shutil.copytree(cfg.root, where, ignore=_SKIP, symlinks=True)
    try:
        _isolate(cfg, where)
    except _Outside as e:
        return None, str(e)
    env = {**os.environ, "PYTHONPATH": GATE_PARENT, "MPLBACKEND": "Agg"}
    for script in cfg.build:
        rel = os.path.relpath(script, cfg.root)
        err = _run([sys.executable, rel], where, env, rel)
        if err:
            return None, err
    capture = []
    if cfg.charts:
        rel, out = os.path.relpath(cfg.charts, cfg.root), os.path.join(where, ".gate-capture.json")
        err = _run([sys.executable, "-m", "gate.chart_capture", rel, out], where, env, rel)
        if err:
            return None, err
        with open(out) as f:
            capture = json.load(f)
    return capture, None


RESULTS_RTOL = 1e-12   # drift measured at 1e-13; a printed figure can change at 1e-10
PNG_MAX_DELTA = 4 / 255


def _json_diff(a, b, path="") -> list:
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return [f"{path or 'root'}: keys differ ({sorted(set(a) ^ set(b))[:6]})"]
        return [d for k in a for d in _json_diff(a[k], b[k], f"{path}.{k}")]
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: length {len(a)} vs {len(b)}"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in _json_diff(x, y, f"{path}[{i}]")]
    if isinstance(a, float) and isinstance(b, float):
        return [] if math.isclose(a, b, rel_tol=RESULTS_RTOL, abs_tol=1e-15) else [f"{path}: {a!r} vs {b!r}"]
    return [] if a == b else [f"{path}: {a!r} vs {b!r}"]


def _png_diff(a: str, b: str):
    import matplotlib.image as mi
    import numpy as np
    x, y = mi.imread(a), mi.imread(b)
    if x.shape != y.shape:
        return f"size {x.shape[1]}x{x.shape[0]} vs {y.shape[1]}x{y.shape[0]}"
    d = np.abs(x - y).max(axis=-1)
    if d.max() <= PNG_MAX_DELTA:
        return None
    return f"{int((d > PNG_MAX_DELTA).sum())} pixels changed by up to {d.max() * 255:.0f}/255"


def _same(fresh_path: str, committed_path: str):
    """None if equivalent beyond environment noise, else a description of the difference."""
    if filecmp.cmp(fresh_path, committed_path, shallow=False):
        return None
    if fresh_path.endswith(".json"):
        with open(fresh_path) as a, open(committed_path) as b:
            diffs = _json_diff(json.load(a), json.load(b))
        return None if not diffs else f"{len(diffs)} value(s) differ, e.g. {diffs[0]}"
    if fresh_path.endswith(".png"):
        return _png_diff(fresh_path, committed_path)
    return "bytes differ"


def _outputs(cfg, base: str) -> list:
    rel = [os.path.relpath(cfg.results, cfg.root)]
    chart_dir = os.path.join(base, os.path.relpath(cfg.chart_dir, cfg.root))
    if os.path.isdir(chart_dir):
        rel += [os.path.join(os.path.relpath(cfg.chart_dir, cfg.root), f)
                for f in sorted(os.listdir(chart_dir)) if f.lower().endswith(IMAGE_EXT)]
    return rel


def _printed_diffs(cfg, fresh_results: str, templates) -> list:
    """Render each template with the committed and the rebuilt results: the text must be identical. A value
    on a rounding boundary can flip a printed digit by less than any tolerance."""
    from gate.render import RenderError, render
    with open(cfg.results) as f:
        committed = json.load(f)
    with open(fresh_results) as f:
        rebuilt = json.load(f)
    src = None
    if cfg.sources:
        with open(cfg.sources) as f:
            src = json.load(f)
    fails = []
    for label, text in templates:
        try:
            if render(text, committed, src)[0] != render(text, rebuilt, src)[0]:
                fails.append(f"{label} prints differently from a clean rebuild's results")
        except RenderError as e:
            fails.append(f"{label} does not render from a clean rebuild's results: {e}")
    return fails


def check(cfg, templates=()):
    """Return (failures, chart_capture_records). templates: (label, text) rendered from both results."""
    tmp = tempfile.mkdtemp(prefix="gate-fresh-")
    try:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        cap, err = _build(cfg, a)
        if err:
            return [err], []
        _, err = _build(cfg, b)
        if err:
            return [err], cap
        fails = []
        rebuilt = os.path.join(a, os.path.relpath(cfg.results, cfg.root))
        if templates and os.path.exists(rebuilt) and os.path.exists(cfg.results):
            fails += _printed_diffs(cfg, rebuilt, templates)
        expected = set(_outputs(cfg, a))
        committed = set(_outputs(cfg, cfg.root))
        for rel in sorted(expected | committed):
            fa, fc, fb = (os.path.join(x, rel) for x in (a, cfg.root, b))
            if not os.path.exists(fc):
                fails.append(f"{rel}: produced by the scripts but not committed")
            elif not os.path.exists(fa):
                fails.append(f"{rel}: committed but no script produces it")
            else:
                diff = _same(fa, fc)
                if diff:
                    fails.append(f"{rel}: committed file differs from a fresh build (stale or hand-edited): {diff}")
            if os.path.exists(fa) and os.path.exists(fb) and not filecmp.cmp(fa, fb, shallow=False):
                fails.append(f"{rel}: two fresh builds differ (not deterministic)")
        return fails, cap
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
