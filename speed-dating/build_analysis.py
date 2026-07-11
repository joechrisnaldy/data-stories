"""Stated vs revealed partner preferences by gender.

STATED: mean of the 100-point 'what I look for' allocation (attr1_1..shar1_1), computed on
the 100-point-allocation waves only (exclude waves 6-9, which used a 1-10 importance scale).
REVEALED: correlation of each 1-10 partner-rating with the yes decision (dec), by gender.
Both are also normalized to a share of importance so they can be compared on one axis, and
ranked 1..6."""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Speed Dating Data.csv", encoding="latin-1")

ATTRS = ["attr", "sinc", "intel", "fun", "amb", "shar"]
STATED = [a + "1_1" for a in ATTRS]
GENDER = {0: "Female", 1: "Male"}

pt = df[~df.wave.isin([6, 7, 8, 9])]  # 100-point-allocation waves only

stated, revealed, stated_share, revealed_share, ranks = {}, {}, {}, {}, {}
for gv, gl in GENDER.items():
    s = pt[pt.gender == gv][STATED].mean()
    s.index = ATTRS
    stated[gl] = {a: round(float(s[a]), 1) for a in ATTRS}
    ssum = float(s.sum())
    stated_share[gl] = {a: round(float(s[a]) / ssum, 3) for a in ATTRS}

    sub = df[df.gender == gv]
    corr = {a: round(float(sub[[a, "dec"]].dropna().corr().iloc[0, 1]), 3) for a in ATTRS}
    revealed[gl] = corr
    csum = sum(corr.values())
    revealed_share[gl] = {a: round(corr[a] / csum, 3) for a in ATTRS}

    stated_rank = {a: r for r, a in enumerate(sorted(ATTRS, key=lambda x: -s[x]), 1)}
    revealed_rank = {a: r for r, a in enumerate(sorted(ATTRS, key=lambda x: -corr[x]), 1)}
    ranks[gl] = {a: {"stated": stated_rank[a], "revealed": revealed_rank[a]} for a in ATTRS}

results = {
    "n_rows": int(len(df)),
    "n_subjects": int(df.iid.nunique()),
    "n_waves": int(df.wave.nunique()),
    "n_stated_rows": int(pt[STATED].dropna(how="all").shape[0]),
    "attrs": ATTRS,
    "stated_by_gender": stated,
    "revealed_corr_by_gender": revealed,
    "stated_share_by_gender": stated_share,
    "revealed_share_by_gender": revealed_share,
    "ranks_by_gender": ranks,
    "yes_rate_by_gender": {GENDER[gv]: round(float(df[df.gender == gv].dec.mean()), 3)
                            for gv in GENDER},
}
(BASE / "results.json").write_text(json.dumps(results, indent=2))
print("stated women:", stated["Female"])
print("stated men:  ", stated["Male"])
print("revealed women:", revealed["Female"])
print("revealed men:  ", revealed["Male"])
print("yes-rate:", results["yes_rate_by_gender"])
print("women intelligence rank stated -> revealed:",
      ranks["Female"]["intel"]["stated"], "->", ranks["Female"]["intel"]["revealed"])
print("women ambition rank stated -> revealed:",
      ranks["Female"]["amb"]["stated"], "->", ranks["Female"]["amb"]["revealed"])
