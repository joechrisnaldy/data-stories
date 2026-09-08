"""The gate. Run before any draft is shown to anyone: python3 check.py

Every check here exists because the defect it catches actually shipped in this repository and was
found later by an expensive adversarial round. The point of the file is that these classes should
never need a language model to find them again.

  numbers   every quantity in the draft is reproduced by results.json      (round 2: 7 misses)
  samples   two correlations in one sentence share a sample or name both  (rounds 1-3: 3 misses)
  drift     the two loaders agree about every country they both carry     (rounds 2-3: 2 misses)
  asserts   no assert can be shown to be tautological                     (round 3: 1 miss)
  style     no em dash, en dash or Unicode minus on ANY surface           (recurring)
  images    the same, inside the strings matplotlib actually renders      (rounds 1-3: ~8 misses)
  panels    every chart panel plots exactly the n it annotates            (round 1: 1 miss)
  cite      every citation has an entry and every entry is cited          (round 3: 1 miss)
  words     the body is inside its budget
  repeat    both scripts are deterministic across reruns
"""

import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from checks import numbers, samples, surfaces  # noqa: E402

DRAFT = os.path.join(HERE, "draft", "the-map-used-to-run-the-other-way.md")
SURFACES = [DRAFT] + [os.path.join(HERE, p) for p in
                      ("build_analysis.py", "make_charts.py", "results.json",
                       "docs/provenance-audit.md", "docs/2026-09-07-reversal-design.md")]
for _p in SURFACES:
    assert os.path.exists(_p), f"gate surface missing: {_p}"  # never check 1 of 6 and pass


def loader_drift() -> list:
    """build_analysis and make_charts each build a frame. They must not disagree about a country."""
    import build_analysis as B
    import make_charts as M
    _, _, ajr = B.load()
    d = M.frame()
    a = ajr.set_index("shortnam")
    b = d.dropna(subset=["shortnam"]).set_index("shortnam")
    both = a.index.intersection(b.index)
    fails = []
    for col in ("lpd1500s", "ex2col"):
        x, y = a.loc[both, col], b.loc[both, col]
        bad = both[~((x.isna() & y.isna()) | np.isclose(x.fillna(-9e9), y.fillna(-9e9)))]
        if len(bad):
            fails.append(f"loaders disagree on {col} for {sorted(bad)[:8]}")
    only_a, only_b = sorted(set(a.index) - set(b.index)), sorted(set(b.index) - set(a.index))
    if only_a:
        fails.append(f"{len(only_a)} countries in the analysis frame only: {only_a[:8]}")
    return fails


def tautological_asserts() -> list:
    """An assert whose condition is guaranteed by a filter above it can never fire."""
    fails = []
    for f in ("build_analysis.py", "make_charts.py"):
        src = open(os.path.join(HERE, f)).read().split("\n")
        for i, line in enumerate(src, 1):
            m = re.search(r"assert\s+(?:not\s+)?\(?([A-Za-z_][\w.]*)", line)
            if not m or "assert" not in line:
                continue
            # the pattern that bit us: assert re-states a filter applied in the preceding 4 lines
            window = "\n".join(src[max(0, i - 5):i - 1])
            cond = line.split("assert", 1)[1].split(",")[0].strip()
            key = re.sub(r"[^\w]", "", cond)[:24]
            if key and key in re.sub(r"[^\w]", "", window):
                fails.append(f"{f}:{i} assert may be tautological, its condition is applied above: {cond[:70]}")
    return fails


def panel_counts() -> list:
    import make_charts as M
    R = json.load(open(os.path.join(HERE, "results.json")))
    d = M.frame()
    col = d[d.ex2col == 1]
    want = [("chart1", len(d.dropna(subset=["tas", "lgdp"])), R["tidy_story"]["n"]),
            ("chart2L", len(col.dropna(subset=["tas", "lpd1500s"])),
             R["heat_reversal"]["former_colonies"]["vs_density_1500"]["n"]),
            ("chart2R", len(col.dropna(subset=["tas", "lgdp"])),
             R["heat_reversal"]["former_colonies"]["vs_income_2023"]["n"]),
            ("chart3L", len(d[d.ex2col == 1].dropna(subset=["lpd1500s", "lgdp"])),
             R["flip"]["density_1500|income_2023|former_colonies"]["n"]),
            ("chart3R", len(d[d.ex2col == 0].dropna(subset=["lpd1500s", "lgdp"])),
             R["flip"]["density_1500|income_2023|never_colonised"]["n"])]
    return [f"{n}: plots {got} points under an n={ann} annotation" for n, got, ann in want if got != ann]


def determinism() -> list:
    def stamp():
        subprocess.run([sys.executable, "build_analysis.py"], cwd=HERE, capture_output=True, check=True)
        subprocess.run([sys.executable, "make_charts.py"], cwd=HERE, capture_output=True, check=True)
        h = hashlib.sha256()
        for f in sorted(os.listdir(os.path.join(HERE, "charts"))) + ["../results.json"]:
            h.update(open(os.path.join(HERE, "charts", f), "rb").read())
        return h.hexdigest()
    return [] if stamp() == stamp() else ["scripts are not deterministic across reruns"]


def main() -> int:
    draft = open(DRAFT, encoding="utf-8").read()
    results = json.load(open(os.path.join(HERE, "results.json")))
    import make_charts as M

    words_fail, n_words = surfaces.word_count(draft)
    strings = (surfaces.rendered_text(M.chart1, M.frame())
               + surfaces.rendered_text(M.chart2, M.frame())
               + surfaces.rendered_text(M.chart3, M.frame())
               + surfaces.rendered_text(M.chart4))

    groups = [
        ("numbers", numbers.check(draft, results)),
        ("samples", samples.check(draft)),
        ("drift", loader_drift()),
        ("asserts", tautological_asserts()),
        ("style", surfaces.style(SURFACES)),
        ("images", surfaces.image_style(strings)),
        ("panels", panel_counts()),
        ("cite", surfaces.citations(draft)),
        ("words", words_fail),
        ("repeat", determinism()),
    ]
    bad = 0
    for name, fails in groups:
        if fails:
            bad += len(fails)
            print(f"\n{name.upper()}  {len(fails)} problem(s)")
            for f in fails:
                print(f"  - {f}")
        else:
            print(f"{name:9s} ok")
    print(f"\nbody {n_words} words, {len(strings)} rendered strings checked")
    print("GATE FAILED" if bad else "\nGATE PASSED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
