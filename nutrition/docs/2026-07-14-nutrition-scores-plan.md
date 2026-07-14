# The Score You Didn't Build: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 08, an essay that reverse-engineers a popular dataset's "Nutrition Density" score (an exact, dimensionally nonsensical sum of 8 nutrients), contrasts it with calories (honest Atwater 4/4/9 arithmetic) and Nutri-Score (a disclosed, validated bundled score), and teaches readers to interrogate any score they did not build.

**Architecture:** Content build. One nutrition dataset (5 group CSVs, 2,395 foods). The analysis recovers the score's formula by linear regression (R^2 = 1.0), decomposes its contribution shares to expose the unit-mixing, and confirms calories are Atwater arithmetic. Three charts. Nutri-Score is the constructive foil, carried in prose from verified citations. No food-ranking analysis (the dataset's absolute values are unreliable). Verification is data sanity, citation checks, a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy, scikit-learn, matplotlib) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/nutrition/docs/2026-07-14-nutrition-scores-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact; descriptive/associational only; not medical or financial advice; neutral tone (credit the dataset, critique the metric and the practice, not the person). **Live blog domain is `joechrisnaldy.com` (NOT .app).**

**Title (chosen):** "The Score You Didn't Build (and Shouldn't Trust)"
**Slug / filename base:** `the-score-you-didnt-build`

---

## File map

- Done: `nutrition/data/FOOD-DATA-GROUP1..5.csv` (downloaded, 2,395 foods)
- Done: `nutrition/profile_data.py` (written + runs; the profiler)
- Create: `nutrition/build_analysis.py` (recover formula, decompose, Atwater; writes results.json)
- Create: `nutrition/results.json`
- Create: `nutrition/make_charts.py` (3 charts)
- Create: `nutrition/data/README.md` (Kaggle download note + data-quality warning)
- Create: `nutrition/README.md` (storytelling README)
- Create: `nutrition/docs/2026-07-14-nutrition-scores-references-verified.md`
- Create: `nutrition/draft/the-score-you-didnt-build.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/nutritionscore-1-recipe.png`, `nutritionscore-2-madeof.png`, `nutritionscore-3-calories.png`
- Create: `site/src/content/blog/the-score-you-didnt-build.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 08 row)

Image prefix `nutritionscore-` is unused on the site (existing: 4months, gamingaddiction, moscowhousing, speeddating, studenthealth, whatittakes, worldcup2026, educationroi, mentalhealth).

---

### Task 1: Analysis (recover the formula, decompose, Atwater)

**Files:** Create `nutrition/build_analysis.py`; writes `results.json`

- [ ] **Step 1: Write the analysis.**

```python
"""Post 08 analysis: reverse-engineer the 'Nutrition Density' score (an exact sum of 8
nutrients), decompose its contribution shares to expose unit-mixing, and confirm calories
are Atwater 4/4/9 arithmetic. Writes results.json. Descriptive/associational only."""
import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
frames = [pd.read_csv(p) for p in sorted((BASE / "data").glob("FOOD-DATA-GROUP*.csv"))]
df = pd.concat(frames, ignore_index=True)
df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed") or c == ""],
             errors="ignore")

NUTRIENTS = [c for c in df.select_dtypes("number").columns if c != "Nutrition Density"]
UNIT = {"Fat": "g", "Carbohydrates": "g", "Protein": "g", "Dietary Fiber": "g",
        "Vitamin A": "ug", "Vitamin C": "mg", "Calcium": "mg", "Iron": "mg"}

# (1) recover the formula: regress the score on the 33 nutrient columns
lin = LinearRegression().fit(df[NUTRIENTS], df["Nutrition Density"])
w = pd.Series(lin.coef_, index=NUTRIENTS)
ingredients = [c for c in NUTRIENTS if w[c] >= 0.5]
raw_sum = df[ingredients].sum(axis=1)
max_abs_diff = float((df["Nutrition Density"] - raw_sum).abs().max())
r2 = float(lin.score(df[NUTRIENTS], df["Nutrition Density"]))

# (2) decompose contribution shares (mean value of each ingredient / total)
mean_contrib = df[ingredients].mean()
share = mean_contrib / mean_contrib.sum() * 100
contribution = sorted(
    [{"term": t, "unit": UNIT.get(t, "?"), "mean": round(float(mean_contrib[t]), 2),
      "share_pct": round(float(share[t]), 1)} for t in ingredients],
    key=lambda r: r["share_pct"], reverse=True)

density_calorie_corr = float(df["Nutrition Density"].corr(df["Caloric Value"]))
density_calcium_corr = float(df["Nutrition Density"].corr(df["Calcium"]))

# (3) calories = Atwater 4/4/9
pred = 4 * df.Carbohydrates + 4 * df.Protein + 9 * df.Fat
resid = df["Caloric Value"] - pred
macro_sum = df.Fat + df.Carbohydrates + df.Protein + df.Water
clean = df["Caloric Value"].between(1, 900) & (macro_sum <= 105)  # physically plausible
corr_all = float(df["Caloric Value"].corr(pred))
corr_clean = float(df.loc[clean, "Caloric Value"].corr(pred[clean]))
scatter = [{"pred": round(float(pred[i]), 1), "actual": round(float(df["Caloric Value"][i]), 1)}
           for i in df.index[clean]]
mdf = df.assign(pred=pred, resid=resid)
mdf = mdf.reindex(resid.abs().sort_values(ascending=False).index).head(6)
misses = [{"food": r["food"], "actual": round(float(r["Caloric Value"]), 1),
           "pred": round(float(r["pred"]), 1), "resid": round(float(r["resid"]), 1)}
          for _, r in mdf.iterrows()]

out = {
    "n_foods": int(len(df)),
    "recipe": {"r2": round(r2, 4), "ingredients": ingredients,
               "max_abs_diff": round(max_abs_diff, 3),
               "weights_all": [{"nutrient": c, "weight": round(float(w[c]), 3)}
                               for c in w.sort_values(ascending=False).index]},
    "contribution": contribution,
    "density_calorie_corr": round(density_calorie_corr, 3),
    "density_calcium_corr": round(density_calcium_corr, 3),
    "atwater": {"corr_all": round(corr_all, 4), "corr_clean": round(corr_clean, 4),
                "median_abs_err_clean": round(float(resid[clean].abs().median()), 2),
                "within20_clean_pct": round(float((resid[clean].abs() <= 20).mean() * 100), 1),
                "n_clean": int(clean.sum()), "n_all": int(len(df))},
    "atwater_scatter": scatter,
    "atwater_misses": misses,
}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("recipe R^2:", out["recipe"]["r2"], "| ingredients:", ingredients)
print("max abs diff (density - raw sum):", out["recipe"]["max_abs_diff"])
for c in contribution:
    print(f"  {c['term']:16s} ({c['unit']}) {c['share_pct']:5.1f}%")
print("density~calories r:", out["density_calorie_corr"], "density~calcium r:", out["density_calcium_corr"])
print("Atwater corr_clean:", out["atwater"]["corr_clean"],
      "median_abs_err:", out["atwater"]["median_abs_err_clean"],
      "within20%:", out["atwater"]["within20_clean_pct"], "n_clean:", out["atwater"]["n_clean"])
```

- [ ] **Step 2: Run and sanity-check.** `cd nutrition && ../sberbank-housing/.venv/bin/python build_analysis.py`. Expected (matches profiling): recipe R^2 = 1.0; ingredients = Fat, Carbohydrates, Protein, Dietary Fiber, Vitamin A, Vitamin C, Calcium, Iron; max_abs_diff < 0.5; Calcium top contribution share ~49%, Vitamin A ~0.7%; density~calories r ~0.54, density~calcium r ~0.80; Atwater corr_clean ~0.98, median_abs_err ~3 kcal, within20 ~90%. **GATE: if R^2 is not ~1.0 or the 8 ingredients differ, STOP and reconcile (the reveal is the whole essay).**

---

### Task 2: Charts

**Files:** Create `nutrition/make_charts.py`; writes `charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette, reading `results.json`.

```python
"""Charts for 'The Score You Didn't Build'. Reads results.json.
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


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_recipe():
    rows = R["recipe"]["weights_all"]          # 33 nutrients, sorted by weight desc
    rows = rows[::-1]                           # barh bottom-up
    names = [r["nutrient"] for r in rows]
    wts = [r["weight"] for r in rows]
    ingredients = set(R["recipe"]["ingredients"])
    colors = [AQUA if n in ingredients else "#d7d6cf" for n in names]
    fig, ax = plt.subplots(figsize=(8.6, 9.2))
    y = np.arange(len(names))
    ax.barh(y, wts, color=colors, height=0.78)
    ax.set_yticks(y, names, fontsize=8.5)
    ax.set_xlabel("weight recovered by regressing the score on every nutrient")
    ax.set_title("We fed the 'Nutrition Density' score to a regression.\nIt handed back the recipe.")
    ax.grid(axis="y", visible=False)
    ax.axvline(1.0, color=BASELINE, lw=0.8, ls=(0, (4, 3)))
    fig.text(0.12, 0.02, "Eight nutrients (green) each enter with weight 1; the other 25 (grey) "
             "are ignored. R-squared = 1.00: the score is exactly their sum.",
             fontsize=8.5, color=MUTED)
    save(fig, "01_recipe.png")


def chart2_madeof():
    c = R["contribution"]                       # sorted by share desc
    names = [f"{r['term']} ({r['unit']})" for r in c][::-1]
    shares = [r["share_pct"] for r in c][::-1]
    top = c[0]["term"]
    colors = [RED if r["term"] == top else (BLUE if r["unit"] == "g" else "#9bbcea")
              for r in c][::-1]
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    y = np.arange(len(names))
    ax.barh(y, shares, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10)
    for yi, s in zip(y, shares):
        ax.annotate(f"{s:.0f}%", (s, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=9, color=INK2)
    ax.set_xlabel("share of the total 'Nutrition Density' score")
    ax.set_title("Half the 'nutrition' score is calcium,\nonly because calcium is counted in milligrams")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.02, "The score adds grams (macros), milligrams (calcium, vitamin C, iron) "
             "and micrograms (vitamin A) as if equal. Big-number units win; the vitamins it is\n"
             "named for barely count. It correlates %.2f with calories." % R["density_calorie_corr"],
             fontsize=8.5, color=MUTED)
    save(fig, "02_madeof.png")


def chart3_calories():
    s = R["atwater_scatter"]
    xp = np.array([p["pred"] for p in s])
    ya = np.array([p["actual"] for p in s])
    fig, ax = plt.subplots(figsize=(7.8, 7.4))
    ax.scatter(xp, ya, s=10, color=BLUE, alpha=0.25, edgecolor="none", zorder=3)
    lim = 900
    ax.plot([0, lim], [0, lim], color=INK2, lw=1.4, ls=(0, (4, 3)), zorder=4)
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("calories predicted from macros  (4*carb + 4*protein + 9*fat)")
    ax.set_ylabel("calories listed in the dataset")
    ax.set_title("Calories are also a formula, but an honest one")
    at = R["atwater"]
    ax.annotate(f"r = {at['corr_clean']:.2f}\nmedian miss = {at['median_abs_err_clean']:.1f} kcal",
                (0.05, 0.90), xycoords="axes fraction", fontsize=11, color=INK, fontweight="bold")
    fig.text(0.12, 0.01, "Each dot is one food (n=%d plausible foods). The dashed line is a "
             "perfect match. Atwater's 1900s 4/4/9 factors reproduce the calorie column\n"
             "to within a few kcal. The honest misses are alcohol (not a macro column here); "
             "a few impossible rows are excluded." % at["n_clean"], fontsize=8.5, color=MUTED)
    save(fig, "03_calories.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_recipe()
    chart2_madeof()
    chart3_calories()
```

- [ ] **Step 2: Run and eyeball.** `cd nutrition && ../sberbank-housing/.venv/bin/python make_charts.py`. Read each PNG back; fix label collisions before proceeding. Confirm chart 1's 8 green bars sit at 1.0, chart 2's calcium bar is on top near 49%, chart 3 is a tight diagonal.

---

### Task 3: Pin + verify the citations

**Files:** Create `nutrition/docs/2026-07-14-nutrition-scores-references-verified.md`

Verify each external fact against a primary source with WebFetch/WebSearch before it enters the prose.

- [ ] **Step 1: Verify the Atwater factors.** Confirm the general (rounded) Atwater factors are 4 kcal/g for carbohydrate, 4 kcal/g for protein, 9 kcal/g for fat (and 7 kcal/g for alcohol, 2 kcal/g for fiber), and pin a primary source, e.g. FAO (2003), *Food energy: Methods of analysis and conversion factors* (FAO Food and Nutrition Paper 77), Chapter 3. Record the exact citation and URL.
- [ ] **Step 2: Verify the Nutri-Score claim.** Confirm that Nutri-Score is a front-of-pack label derived from a nutrient-profiling model with a PUBLISHED point system (negatives: energy, sugars, saturated fat, sodium; positives: fibre, protein, fruit/vegetables/legumes) and that it has been VALIDATED against health outcomes. Pin two citations: (a) the underlying nutrient profiling model, e.g. the UK FSA/Ofcom model, and (b) a validation study, e.g. a cohort study linking the FSAm-NPS/Nutri-Score to health outcomes (Julia/Hercberg et al.). Record exact citations, journal, year, DOI. **If a specific study does not check out, swap it for one that does; keep the "published + validated" claim only as strongly as the verified sources support.**
- [ ] **Step 3: Record the Kaggle dataset citation.** Dey, U. (2024). *Food nutrition dataset* [Data set]. Kaggle. https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset
- [ ] **Step 4: Write each as an APA 7 entry** into the references file, annotated with the claim it supports and the access date.

---

### Task 4: Data-download note and storytelling README

**Files:** Create `nutrition/data/README.md` and `nutrition/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source (`utsavdey1410/food-nutrition-dataset`), the CLI download command, the note that the data is 5 group CSVs (2,395 foods, per-100g nutrient columns), and a prominent data-quality warning: the values are not reliably per-100g (821 foods list water > 100 g/100g; ~48% of rows have fat+carb+protein+water > 105 g), so the essay uses the derived-column formulas and relationships, not absolute values or food rankings.
- [ ] **Step 2: Write `nutrition/README.md`** as the storytelling README (argument in three charts, how-the-analysis-works table linking `profile_data.py` / `build_analysis.py` / `make_charts.py`, reproduce steps, method and caveats), matching `mental-health-productivity/README.md` style. Foreground: derived columns, unit-mixing, no food rankings, Nutri-Score as the good foil. Link the live essay URL once known. No long dashes.

---

### Task 5: Draft the essay for author review

**Files:** Create `nutrition/draft/the-score-you-didnt-build.md` and `.docx`

Draft ~1,300 to 1,700 words following the seven-part spine in the design doc, using numbers from `results.json`. Match the author's voice from `mental-health-productivity/draft/what-actually-moves-your-mental-health.md` (stance-first, plain, honest).

Required content anchors:
- **Open, villain first:** a "Nutrition Density" score in a dataset 25,000+ people downloaded that adds grams of fat to milligrams of calcium to micrograms of vitamin A.
- **The reveal (chart 1):** regress the score on every nutrient; it returns an exact sum of 8, weight 1 each (R^2 = 1.0). Explain reverse-engineering plainly.
- **Why it is nonsense (chart 2):** unit-mixing means big-number columns dominate; calcium is ~49%, macros ~40%, the vitamins ~8% (vitamin A ~0.7% because micrograms); it correlates ~0.54 with calories, so it rewards heavy caloric foods. Not a health score.
- **The honest counterexample (chart 3):** calories look like the same kind of derived number but are Atwater 4/4/9, a disclosed, century-old, physically grounded formula accurate to ~3 kcal. A formula is not the problem; a hidden, arbitrary one is. Note the honest miss (alcohol at 7 kcal/g, not in the macro columns) and that a few rows are simply broken (state the dataset is imperfect).
- **What good looks like (Nutri-Score, prose):** also one number from many nutrients, but with published weights, a stated purpose (diet quality), and validation against health outcomes. The difference is disclosure, purpose, and validation, not bundling.
- **The general lesson (broad):** any score you did not build (health-app ratings, sleep scores, wellness indices, credit scores) is a bundle of someone's choices; ask what goes in, how it is weighted, and whether anyone checked it; you can often reverse-engineer it in an afternoon.
- **Close + method notes.** Analysis, not medical or financial advice.

Guardrails: no long dashes; descriptive language only; neutral tone (credit the dataset, critique the metric/practice, not the person); no food rankings.

- [ ] **Step 1: Write the draft** with figures as `../charts/*.png` refs.
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/md_to_docx.py` with an explicit output path: `../sberbank-housing/.venv/bin/python ../sberbank-housing/md_to_docx.py draft/the-score-you-didnt-build.md draft/the-score-you-didnt-build.docx`.
- [ ] **Step 3: Long-dash scan.** `grep -n $'[–—]' draft/the-score-you-didnt-build.md` expected empty.

---

### Task 6: Adversarial verification (before author handoff)

Run a four-agent Workflow over the draft (verify BEFORE the author reads it):
(a) **numbers** match `results.json` (recipe R^2 = 1.0 and the 8 ingredients; contribution shares, especially calcium ~49% and vitamin A ~0.7%; density~calories ~0.54; Atwater corr ~0.98 and median miss ~3 kcal; n reported honestly);
(b) **logic and honesty** (the unit-mixing critique is stated correctly; "it tracks calories" is not overstated at r 0.54; calories framed as a disclosed/validated formula, not "fake"; the alcohol miss and the broken rows are acknowledged; no food-ranking claims from the unreliable absolute values; no causal or medical claims);
(c) **facts** (Atwater factors 4/4/9 and the Nutri-Score "published + validated" claim match the pinned references with correct years/DOIs; the dataset is credited neutrally);
(d) **voice and no-long-dash** (series voice; no em/en dashes; neutral tone, critiques the practice not the person; opening leads with the concrete reveal).
Fix confirmed issues; re-run the dash scan; if prose changed materially, re-confirm before handoff.

---

### Task 7: AUTHOR REVIEW GATE

- [ ] Hand the `.docx` to Jonathan. Summarize what it argues and the honesty fixes. **Do not proceed until he approves.**

---

### Task 8: Build the MDX page

**Files:** Create `site/src/content/blog/the-score-you-didnt-build.mdx`

- [ ] **Step 1: Copy charts** to `site/public/images/blog/` as `nutritionscore-1-recipe.png`, `nutritionscore-2-madeof.png`, `nutritionscore-3-calories.png`. Verify non-empty.
- [ ] **Step 2: Frontmatter** (match Post 06-07 shape):

```yaml
---
title: "The Score You Didn't Build (and Shouldn't Trust)"
slug: "the-score-you-didnt-build"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-14
tags: ["Data", "Nutrition", "Metrics"]
status: published
seoTitle: "The Score You Didn't Build (and Shouldn't Trust) - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base (`the-score-you-didnt-build`).

- [ ] **Step 3: Paste approved prose; figures as `<figure><img .../><figcaption>...</figcaption></figure>`** with the exact filenames (`/images/blog/nutritionscore-1-recipe.png`, etc.). Real alt text and captions.
- [ ] **Step 4: `## References`** block, APA 7 markdown-link format (mirror Post 07), journal/volume italics where applicable, populated from the verified references file. Include a GitHub code link (`github.com/joechrisnaldy/data-stories/tree/main/nutrition`).
- [ ] **Step 5: Long-dash scan on the MDX.** Expected clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 9: Build the site and verify

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/the-score-you-didnt-build/index.html` generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git restore public/images/blog/` to revert the optimizer's churn on pre-existing images; re-copy the three raw `nutritionscore-*.png` charts so only the new images are added. Stage ONLY this post's files (another session may be editing this repo; do NOT `git add -A`).
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/the-score-you-didnt-build/index.html`: correct title, three `nutritionscore-*.png` refs, section headings, References.

---

### Task 10: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 08 row**, linking `https://joechrisnaldy.com/blog/the-score-you-didnt-build` and `nutrition/`. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 11: PUBLISH GATE (author-triggered)

Only when Jonathan says go. Publishing pushes two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/`, remote `joechrisnaldy-portfolio`, branch `main`), staging only the new MDX, the three `nutritionscore-*.png`, and `.published-slugs.json`. Triggers Vercel. **Verify live on `https://joechrisnaldy.com/blog/the-score-you-didnt-build` (NOT .app), and that each image resolves 200.**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 08 folder: `profile_data.py`, `build_analysis.py`, `make_charts.py`, `results.json`, `charts/`, `README.md`, `data/README.md`, `docs/`; NOT `draft/` or `data/*.csv`) plus the series-index README update. Before committing, run `git add --dry-run` and confirm every README-referenced script is included and no draft/CSV leaks.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md` + MEMORY.md index): Post 08 shipped, live URL, thesis, gotchas (reverse-engineered a published score to an exact 8-nutrient sum; unit-mixing so calcium dominates; calories = Atwater; dataset per-100g quality issues so no food rankings; Nutri-Score as the good-score foil; neutral tone honoring the Post-08-cancel ethics lesson).

---

## Self-review

- **Spec coverage:** recover-the-formula (Task 1 + chart 1), decompose/unit-mixing (Task 1 + chart 2), calories-as-Atwater (Task 1 + chart 3), Nutri-Score foil (Tasks 3, 5), broad "any score" lesson (Task 5), neutral tone + data-quality honesty (Tasks 4, 5, 6), APA 7 (Tasks 3, 8). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions filled from the approved draft at Task 8; citations are an explicit verify-first task (Task 3) with named candidate sources. No orphan TODOs.
- **Consistency:** NUTRIENTS/ingredients/UNIT defined in build_analysis and consumed by make_charts via results.json keys (recipe.weights_all, recipe.ingredients, contribution[].share_pct/unit, atwater_scatter, atwater.corr_clean); chart raw filenames (01_recipe/02_madeof/03_calories) map to site filenames (nutritionscore-1-recipe/-2-madeof/-3-calories) identically across Tasks 2, 8, 9; slug `the-score-you-didnt-build` identical across Tasks 8, 10, 11 and the filename.
- **Review gates:** formula-recovery sanity gate (Task 1 Step 2), citation verify-first (Task 3), adversarial verify (Task 6), author Word review (Task 7), publish gate (Task 11).
