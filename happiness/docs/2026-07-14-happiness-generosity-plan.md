# The Most Generous Country on Earth Isn't the Happiest: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 09, an Indonesia-forward essay using the generosity paradox (Indonesia gives the most and feels the most daily joy, yet ranks ~80th on the happiness ladder) to open up the gap between evaluated happiness (the ladder) and experienced happiness (daily affect).

**Architecture:** Content build on the World Happiness Report data (2024 cross-section + 2005-2024 panel). The analysis computes Indonesia's world ranks, the near-zero generosity-to-ladder correlation, and the loose ladder-to-affect link, then writes results.json. Three charts. The cultural corroboration (World Giving Index) and the evaluated-vs-experienced distinction (Kahneman & Deaton 2010) are external, verified, and carried in prose. Verification is data sanity, citation checks (verified-or-omit), a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy, scikit-learn, matplotlib) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/happiness/docs/2026-07-14-happiness-generosity-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact; verified or omit; descriptive/associational only; not medical/life advice; neutral honest tone (credit the ranking as one real measure, no flag-waving or ranking-bashing). **Live blog domain is `joechrisnaldy.com` (NOT .app).**

**Title (chosen):** "The Most Generous Country on Earth Isn't the Happiest"
**Slug / filename base:** `the-most-generous-country-isnt-the-happiest`

---

## File map

- Done: `happiness/data/world-happiness-2024.csv` and `world-happiness-panel-2005-2024.csv` (downloaded)
- Done: `happiness/profile_data.py` (written + runs; the profiler)
- Create: `happiness/build_analysis.py` (Indonesia ranks, correlations, chart data; writes results.json)
- Create: `happiness/results.json`
- Create: `happiness/make_charts.py` (3 charts)
- Create: `happiness/data/README.md` (Kaggle download note + two-file explanation)
- Create: `happiness/README.md` (storytelling README)
- Create: `happiness/docs/2026-07-14-happiness-generosity-references-verified.md`
- Create: `happiness/draft/the-most-generous-country-isnt-the-happiest.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/happiness-1-two-happinesses.png`, `happiness-2-generosity.png`, `happiness-3-feeling-judging.png`
- Create: `site/src/content/blog/the-most-generous-country-isnt-the-happiest.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 09 row)

Image prefix `happiness-` is unused on the site (existing: 4months, gamingaddiction, moscowhousing, speeddating, studenthealth, whatittakes, worldcup2026, educationroi, mentalhealth, nutritionscore).

---

### Task 1: Analysis (ranks, correlations, chart data)

**Files:** Create `happiness/build_analysis.py`; writes `results.json`

- [ ] **Step 1: Write the analysis.** Read both CSVs with `encoding="latin-1"`. Use the 2024 cross-section for the official ladder ranking and its regional labels; use the panel's latest year per country for raw values, affect, generosity, and all correlations.

```python
"""Post 09 analysis: Indonesia's generosity paradox and the gap between evaluated (ladder) and
experienced (affect) happiness. World Happiness Report 2024 + 2005-2024 panel. Writes
results.json. Descriptive/associational only."""
import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
cross = pd.read_csv(BASE / "data" / "world-happiness-2024.csv", encoding="latin-1")
panel = pd.read_csv(BASE / "data" / "world-happiness-panel-2005-2024.csv", encoding="latin-1")

region = dict(zip(cross["Country name"], cross["Regional indicator"]))
latest = panel.sort_values("year").groupby("Country name").tail(1).copy()
L = latest.dropna(subset=["Life Ladder", "Positive affect", "Negative affect",
                          "Generosity", "Social support", "Log GDP per capita"]).copy()
L["region"] = L["Country name"].map(region).fillna("Other")
L["ladder_rank"] = L["Life Ladder"].rank(ascending=False).astype(int)
L["posaff_rank"] = L["Positive affect"].rank(ascending=False).astype(int)


def rank_desc(series, country):
    v = series[L["Country name"] == country].iloc[0]
    return int((series > v).sum()) + 1


ic = cross[cross["Country name"] == "Indonesia"].iloc[0]
ladder_rank_2024 = int((cross["Ladder score"] > ic["Ladder score"]).sum()) + 1
il = L[L["Country name"] == "Indonesia"].iloc[0]
indonesia = {
    "ladder_2024": round(float(ic["Ladder score"]), 2), "n_2024": int(len(cross)),
    "ladder_rank_2024": ladder_rank_2024,
    "generosity": round(float(il["Generosity"]), 3),
    "generosity_rank": rank_desc(L["Generosity"], "Indonesia"),
    "positive_affect": round(float(il["Positive affect"]), 3),
    "positive_affect_rank": rank_desc(L["Positive affect"], "Indonesia"),
    "ladder_panel": round(float(il["Life Ladder"]), 2),
    "ladder_rank_panel": rank_desc(L["Life Ladder"], "Indonesia"), "n_panel": int(len(L)),
}
corr = {
    "generosity_ladder": round(float(L["Generosity"].corr(L["Life Ladder"])), 3),
    "posaff_ladder": round(float(L["Positive affect"].corr(L["Life Ladder"])), 3),
    "negaff_ladder": round(float(L["Negative affect"].corr(L["Life Ladder"])), 3),
    "social_ladder": round(float(L["Social support"].corr(L["Life Ladder"])), 3),
}
lin = LinearRegression().fit(L[["Log GDP per capita"]], L["Life Ladder"])
corr["loggdp_ladder_r2"] = round(float(lin.score(L[["Log GDP per capita"]], L["Life Ladder"])), 3)

scatter = [{"country": r["Country name"], "ladder": round(float(r["Life Ladder"]), 2),
            "posaff": round(float(r["Positive affect"]), 3), "region": r["region"]}
           for _, r in L.iterrows()]
generosity_top = [{"country": r["Country name"], "generosity": round(float(r["Generosity"]), 3),
                   "ladder": round(float(r["Life Ladder"]), 2)}
                  for _, r in L.nlargest(10, "Generosity").iterrows()]
curated = []
for cty in ["Indonesia", "Finland", "Costa Rica", "Poland"]:
    row = L[L["Country name"] == cty]
    if len(row):
        r = row.iloc[0]
        curated.append({"country": cty, "ladder_rank": int(r["ladder_rank"]),
                        "posaff_rank": int(r["posaff_rank"]),
                        "ladder": round(float(r["Life Ladder"]), 2),
                        "posaff": round(float(r["Positive affect"]), 3)})
L["gap"] = L["ladder_rank"] - L["posaff_rank"]  # positive => feel more than they rate
feel_more = [r["Country name"] for _, r in L.nlargest(6, "gap").iterrows()]
rate_more = [r["Country name"] for _, r in L.nsmallest(6, "gap").iterrows()]

out = {"indonesia": indonesia, "corr": corr, "n_panel": int(len(L)), "scatter": scatter,
       "generosity_top": generosity_top, "curated": curated,
       "feel_more": feel_more, "rate_more": rate_more}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("Indonesia:", indonesia)
print("corr:", corr)
print("feel_more:", feel_more)
print("rate_more:", rate_more)
print("curated:", [(c["country"], "ladder#" + str(c["ladder_rank"]), "feel#" + str(c["posaff_rank"])) for c in curated])
```

- [ ] **Step 2: Run and sanity-check.** `cd happiness && ../sberbank-housing/.venv/bin/python build_analysis.py`. Expected (matches profiling): Indonesia generosity_rank 1, positive_affect_rank 5, ladder_rank_2024 about 80 (n_2024 143); corr generosity_ladder about 0.06 (near zero), posaff_ladder about 0.46, social_ladder about 0.79; feel_more dominated by Latin America / Africa, rate_more by Eastern Europe. **GATE: if Indonesia is not #1 in generosity or generosity_ladder is not near zero, STOP and reconcile (the paradox is the whole essay).**

---

### Task 2: Charts

**Files:** Create `happiness/make_charts.py`; writes `charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette, reading `results.json`.

```python
"""Charts for 'The Most Generous Country on Earth Isn't the Happiest'. Reads results.json.
Output: charts/*.png on a light surface (series dataviz palette)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

BLUE, AQUA, YELLOW, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"

plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK2,
    "text.color": INK, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
})

FEEL_REGIONS = {"Latin America and Caribbean", "Southeast Asia"}
RATE_REGIONS = {"Central and Eastern Europe", "Commonwealth of Independent States"}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_two_happinesses():
    pts = R["scatter"]
    fig, ax = plt.subplots(figsize=(8.8, 6.8))
    for p in pts:
        if p["country"] == "Indonesia":
            continue
        reg = p["region"]
        col = AQUA if reg in FEEL_REGIONS else (BLUE if reg in RATE_REGIONS else "#c9c8c0")
        ax.scatter(p["ladder"], p["posaff"], s=34, color=col, alpha=0.8,
                   edgecolor="white", linewidth=0.4, zorder=3)
    ind = next(p for p in pts if p["country"] == "Indonesia")
    ax.scatter(ind["ladder"], ind["posaff"], s=150, color=RED, edgecolor="white",
               linewidth=1.0, zorder=5, marker="*")
    ax.annotate("Indonesia", (ind["ladder"], ind["posaff"]), xytext=(8, 6),
                textcoords="offset points", fontsize=10, color=RED, fontweight="bold")
    ax.set_xlabel("how they RATE their life  (ladder score, 0-10)  ->")
    ax.set_ylabel("how they FEEL day to day  (positive affect)  ->")
    ax.set_title("Two kinds of happiness, and they only loosely agree")
    ax.annotate("Latin America and SE Asia:\nfeel more than they rate", (0.02, 0.90),
                xycoords="axes fraction", fontsize=9, color="#0e7a54", fontweight="bold", va="top")
    ax.annotate("Eastern Europe:\nrate more than they feel", (0.62, 0.12),
                xycoords="axes fraction", fontsize=9, color="#1c5fb0", fontweight="bold")
    fig.text(0.12, -0.02, "Each dot is a country (latest survey year). The ladder tracks daily "
             "feeling only loosely (r = %.2f). Indonesia feels a lot and rates itself middling."
             % R["corr"]["posaff_ladder"], fontsize=8.5, color=MUTED)
    save(fig, "01_two_happinesses.png")


def chart2_generosity_crown():
    g = R["generosity_top"][::-1]                 # barh bottom-up, so #1 ends on top
    names = [x["country"] for x in g]
    vals = [x["generosity"] for x in g]
    colors = [RED if n == "Indonesia" else BLUE for n in names]
    fig, ax = plt.subplots(figsize=(8.6, 5.8))
    y = np.arange(len(names))
    ax.barh(y, vals, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10)
    for yi, v in zip(y, vals):
        ax.annotate(f"{v:.2f}", (v, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlabel("generosity (giving, after accounting for income)")
    ax.set_title("Indonesia gives more than any country on earth")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.03, "World Happiness Report generosity measure, latest year. And it buys "
             "nothing on the ranking: generosity's correlation with the happiness ladder is %.2f,\n"
             "so these givers sit all across it." % R["corr"]["generosity_ladder"],
             fontsize=8.5, color=MUTED)
    save(fig, "02_generosity.png")


def chart3_feeling_vs_judging():
    cur = R["curated"]
    n = len(cur)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    y = np.arange(n)[::-1]
    for yi, c in zip(y, cur):
        ax.plot([c["posaff_rank"], c["ladder_rank"]], [yi, yi], color=BASELINE, lw=2.2, zorder=1)
        ax.scatter(c["posaff_rank"], yi, s=90, color=AQUA, zorder=3, edgecolor="white")
        ax.scatter(c["ladder_rank"], yi, s=90, color=BLUE, zorder=3, edgecolor="white")
    ax.set_yticks(y, [c["country"] for c in cur], fontsize=11)
    ax.set_xlabel("world rank (1 = best)  <- better")
    ax.set_title("Where a country ranks on feeling vs on judging its life")
    ax.scatter([], [], color=AQUA, label="rank on daily feeling (positive affect)")
    ax.scatter([], [], color=BLUE, label="rank on rating life (the ladder)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.04, "Indonesia is near the top of the world for daily feeling but "
             "middling on the ladder; Poland is the opposite. Latest survey year, ~%d countries."
             % R["n_panel"], fontsize=8.5, color=MUTED)
    save(fig, "03_feeling_judging.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_two_happinesses()
    chart2_generosity_crown()
    chart3_feeling_vs_judging()
```

- [ ] **Step 2: Run and eyeball.** `cd happiness && ../sberbank-housing/.venv/bin/python make_charts.py`. Read each PNG back; fix label collisions. Confirm chart 1 shows Indonesia as a red star high on affect / mid on ladder; chart 2 has Indonesia #1; chart 3 dumbbells show Indonesia's wide feel-vs-judge gap. Note the chart files are `01_two_happinesses.png`, `02_generosity.png`, `03_feeling_judging.png`.

---

### Task 3: Pin + verify the citations (verified-or-omit)

**Files:** Create `happiness/docs/2026-07-14-happiness-generosity-references-verified.md`

Verify each external fact against a primary source with WebFetch/WebSearch. Drop anything not confirmable.

- [ ] **Step 1: Verify the World Happiness Report 2024.** Confirm the editors (Helliwell, J. F., Layard, R., Sachs, J. D., De Neve, J.-E., Aknin, L. B., & Wang, S., eds.), publisher (Sustainable Development Solutions Network / Wellbeing Research Centre, Oxford), the Cantril ladder question (0-10 worst-to-best life), and that "generosity" is the residual of charity-donation responses regressed on GDP. Record the exact citation and URL.
- [ ] **Step 2: Verify the World Giving Index.** Confirm the Charities Aid Foundation (CAF) World Giving Index ranked Indonesia the most generous country, and the exact edition years (Indonesia topped the 2021, 2022, and 2023 editions). Record the exact citation and URL. **If the specific years cannot be confirmed, state only what is confirmable (e.g., "topped the most recent editions") or drop the claim.**
- [ ] **Step 3: Verify Kahneman & Deaton (2010).** Confirm Kahneman, D., & Deaton, A. (2010), "High income improves evaluation of life but not emotional well-being", PNAS, 107(38), 16489-16493, and that it supports the distinction between evaluated and experienced well-being. Do NOT overclaim the specific income-threshold finding; cite it only for the evaluated-vs-experienced distinction.
- [ ] **Step 4: Record the Kaggle dataset.** jaina. (2024). *World happiness report 2024 (yearly updated)* [Data set]. Kaggle. https://www.kaggle.com/datasets/jainaru/world-happiness-report-2024-yearly-updated
- [ ] **Step 5: Write each as an APA 7 entry** into the references file, annotated with the claim it supports and access date, flagging any wording that must stay hedged.

---

### Task 4: Data-download note and storytelling README

**Files:** Create `happiness/data/README.md` and `happiness/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source, the CLI download command, and a clear explanation of the two files: the 2024 cross-section (ladder + factor CONTRIBUTIONS that sum to the ladder + Dystopia+residual; used for the official ranking) and the 2005-2024 panel (RAW factor values + positive/negative affect; used for all correlations and the affect analysis). Note the `latin-1` encoding.
- [ ] **Step 2: Write `happiness/README.md`** as the storytelling README (argument in three charts, how-the-analysis-works table linking `profile_data.py` / `build_analysis.py` / `make_charts.py`, reproduce steps, method and caveats), matching `nutrition/README.md` style. Foreground: evaluated vs experienced happiness, generosity does not track the ladder (r 0.06), associational only. Link the live essay URL once known. No long dashes.

---

### Task 5: Draft the essay for author review

**Files:** Create `happiness/draft/the-most-generous-country-isnt-the-happiest.md` and `.docx`

Draft ~1,300 to 1,700 words following the seven-part spine in the design doc, using numbers from `results.json`. Match the author's voice from `nutrition/draft/the-score-you-didnt-build.md` (stance-first, plain, honest).

Required content anchors:
- **Open, two people / one country:** an Indonesian can laugh with friends all afternoon and still, asked to rate their life 0 to 10, say six. Both honest. Two different questions.
- **The two happinesses (chart 1):** the ladder (how you rate life) and daily affect (how you feel) agree only loosely (r 0.46). Latin America and SE Asia feel the most; Eastern Europe rates high but feels low. Indonesia: high feeling, middling rating.
- **The generosity crown (chart 2):** Indonesia is 1st of ~150 in the report's generosity measure (give far more than income predicts), corroborated by the World Giving Index. Giving does not move the ladder at all (r 0.06); the most generous countries are scattered across it.
- **Light cultural corroboration:** World Giving Index; a careful, sourced nod to communal and religious giving (zakat, gotong royong) as context, NOT a proven cause of the ladder gap.
- **Where Indonesia stands (chart 3):** high on feeling, middling on judging. What the ladder rewards (money, social support r 0.79) versus what Indonesia has (daily joy, giving). Neither is the whole truth.
- **Turn it on the reader:** rating your life and feeling your life are two questions for you too; no single number holds both; which are you optimizing? Reference Kahneman & Deaton (2010) for the evaluated-vs-experienced distinction. Analysis, not life advice.
- **Close + method notes.**

Guardrails: no long dashes; associational only (no causal/policy claims; culture is context); neutral honest tone (no ranking-bashing or flag-waving); be precise which number comes from the cross-section vs the panel.

- [ ] **Step 1: Write the draft** with figures as `../charts/*.png` refs.
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/.venv/bin/python ../sberbank-housing/md_to_docx.py draft/the-most-generous-country-isnt-the-happiest.md draft/the-most-generous-country-isnt-the-happiest.docx`.
- [ ] **Step 3: Long-dash scan.** `grep -n $'[–—]' draft/the-most-generous-country-isnt-the-happiest.md` expected empty.

---

### Task 6: Adversarial verification (before author handoff)

Run a four-agent Workflow over the draft (verify BEFORE the author reads it):
(a) **numbers** match `results.json` (Indonesia generosity #1, affect #5, ladder ~80/143; generosity-ladder r 0.06; posaff-ladder r 0.46; social-ladder r 0.79; the two-file provenance of each number);
(b) **logic and honesty** (the generosity-ladder r 0.06 is "essentially none", not "negative"; correlations not causal; culture is context not proven cause; "hold both truths" is maintained, no ranking-bashing; the felt-vs-judged framing is stated correctly; generosity is the income-adjusted residual, not raw dollars);
(c) **facts** (WHR 2024 editors/definition, World Giving Index year(s), Kahneman & Deaton 2010 all match the pinned references with correct details; verified-or-omit respected);
(d) **voice and no-long-dash** (series voice; no em/en dashes; neutral honest tone; the opening leads with the human two-people scene).
Fix confirmed issues; re-run the dash scan; if prose changed materially, re-confirm before handoff.

---

### Task 7: AUTHOR REVIEW GATE

- [ ] Hand the `.docx` to Jonathan. Summarize what it argues and the honesty fixes. **Do not proceed until he approves.**

---

### Task 8: Build the MDX page

**Files:** Create `site/src/content/blog/the-most-generous-country-isnt-the-happiest.mdx`

- [ ] **Step 1: Copy charts** to `site/public/images/blog/` as `happiness-1-two-happinesses.png` (from `01_two_happinesses.png`), `happiness-2-generosity.png` (from `02_generosity.png`), `happiness-3-feeling-judging.png` (from `03_feeling_judging.png`). Verify non-empty.
- [ ] **Step 2: Frontmatter** (match Post 07-08 shape):

```yaml
---
title: "The Most Generous Country on Earth Isn't the Happiest"
slug: "the-most-generous-country-isnt-the-happiest"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-14
tags: ["Data", "Indonesia", "Happiness"]
status: published
seoTitle: "The Most Generous Country on Earth Isn't the Happiest - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base (`the-most-generous-country-isnt-the-happiest`).

- [ ] **Step 3: Paste approved prose; figures as `<figure><img .../><figcaption>...</figcaption></figure>`** with the exact filenames (`/images/blog/happiness-1-two-happinesses.png`, etc.). Real alt text and captions.
- [ ] **Step 4: `## References`** block, APA 7 markdown-link format (mirror Post 08), journal/volume italics where applicable, populated from the verified references file. Include a GitHub code link (`github.com/joechrisnaldy/data-stories/tree/main/happiness`).
- [ ] **Step 5: Long-dash scan on the MDX.** Expected clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 9: Build the site and verify

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/the-most-generous-country-isnt-the-happiest/index.html` generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git restore public/images/blog/` to revert the optimizer's churn on pre-existing images; re-copy the three raw `happiness-*.png` charts so only the new images are added. Stage ONLY this post's files (another session may be editing this repo; do NOT `git add -A`).
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/the-most-generous-country-isnt-the-happiest/index.html`: correct title, three `happiness-*.png` refs, section headings, References.

---

### Task 10: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 09 row**, linking `https://joechrisnaldy.com/blog/the-most-generous-country-isnt-the-happiest` and `happiness/`. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 11: PUBLISH GATE (author-triggered)

Only when Jonathan says go. Publishing pushes two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/`, remote `joechrisnaldy-portfolio`, branch `main`), staging only the new MDX, the three `happiness-*.png`, and `.published-slugs.json`. Triggers Vercel. **Verify live on `https://joechrisnaldy.com/blog/the-most-generous-country-isnt-the-happiest` (NOT .app), and that each image resolves 200.**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 09 folder: `profile_data.py`, `build_analysis.py`, `make_charts.py`, `results.json`, `charts/`, `README.md`, `data/README.md`, `docs/`; NOT `draft/` or `data/*.csv`) plus the series-index README update. Before committing, run `git add --dry-run` and confirm every README-referenced script is included and no draft/CSV leaks.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md` + MEMORY.md index): Post 09 shipped, live URL, thesis, gotchas (WHR two-file structure = cross-section contributions vs panel raw+affect; Indonesia generosity #1 / affect #5 / ladder ~80; generosity-ladder r 0.06; evaluated-vs-experienced framing; latin-1 encoding).

---

## Self-review

- **Spec coverage:** Indonesia ranks + generosity-ladder near-zero correlation (Task 1 + charts 1-2), evaluated-vs-experienced (Task 1 + chart 1/3), World Giving Index + Kahneman-Deaton (Tasks 3, 5), light cultural corroboration + no causal overclaim (Tasks 5, 6), reader-turn close (Task 5), two-file precision (Tasks 1, 4), APA 7 verified-or-omit (Tasks 3, 8). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions filled from the approved draft at Task 8; citations are an explicit verify-first task (Task 3) with named candidate sources and drop-if-unconfirmable instructions. No orphan TODOs.
- **Consistency:** results.json keys (indonesia.*, corr.generosity_ladder/posaff_ladder/social_ladder, scatter[].region, generosity_top, curated[].ladder_rank/posaff_rank) defined in build_analysis and consumed by make_charts identically; chart raw filenames (01_two_happinesses/02_generosity/03_feeling_judging) map to site filenames (happiness-1-two-happinesses/-2-generosity/-3-feeling-judging) identically across Tasks 2, 8, 9; slug `the-most-generous-country-isnt-the-happiest` identical across Tasks 8, 10, 11 and the filename.
- **Review gates:** paradox sanity gate (Task 1 Step 2), citation verify-first with drop-if-unconfirmable (Task 3), adversarial verify (Task 6), author Word review (Task 7), publish gate (Task 11).
