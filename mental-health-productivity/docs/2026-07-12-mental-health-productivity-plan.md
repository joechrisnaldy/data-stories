# What Actually Moves Your Mental Health: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 07, an essay that ranks the lifestyle levers of mental health (raw vs adjusted so the double-counting is visible), bridges them to a productivity proxy (concentration), and prices the payoff with real external evidence, on a synthetic dataset whose limits are foregrounded.

**Architecture:** Content build. One Kaggle CSV (synthetic, 500 rows). The analysis builds a distress composite, ranks the 7 lifestyle levers by raw correlation and by adjusted (standardized-regression + permutation) importance, computes the distress-to-concentration bridge, and writes results.json. Three charts. The productivity/economic payoff comes from verified external citations, not our numbers. Verification is data sanity, an adjusted-vs-raw ranking gate, citation checks, a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy, scikit-learn, matplotlib) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/mental-health-productivity/docs/2026-07-12-mental-health-productivity-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact; correlational/associational language only; not medical or financial advice. **Live blog domain is `joechrisnaldy.com` (NOT .app).**

**Title (chosen):** "What Actually Moves Your Mental Health (It Isn't the Sleep Tips)"
**Slug / filename base:** `what-actually-moves-your-mental-health`

---

## File map

- Done: `mental-health-productivity/data/mental_health_prediction.csv` (downloaded, 500 rows)
- Done: `mental-health-productivity/profile_data.py` (written + runs; the profiler)
- Create: `mental-health-productivity/build_analysis.py` (distress composite, lever ranking, bridge; writes results.json)
- Create: `mental-health-productivity/results.json`
- Create: `mental-health-productivity/make_charts.py` (3 charts)
- Create: `mental-health-productivity/data/README.md` (Kaggle download note + synthetic warning)
- Create: `mental-health-productivity/README.md` (storytelling README)
- Create: `mental-health-productivity/docs/2026-07-12-mental-health-productivity-references-verified.md`
- Create: `mental-health-productivity/draft/what-actually-moves-your-mental-health.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/mentalhealth-1-levers.png`, `mentalhealth-2-bridge.png`, `mentalhealth-3-payoff.png`
- Create: `site/src/content/blog/what-actually-moves-your-mental-health.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 07 row)

Image prefix `mentalhealth-` is unused on the site (checked against existing prefixes: 4months, gamingaddiction, moscowhousing, speeddating, studenthealth, whatittakes, worldcup2026, educationroi).

---

### Task 1: Analysis (distress composite, lever ranking, bridge)

**Files:** Create `mental-health-productivity/build_analysis.py`; writes `results.json`

- [ ] **Step 1: Write the analysis.** The distress composite is the mean of z-scored stress, anxiety, depression (higher = worse). `rank_levers` returns, per lever: raw pairwise correlation, standardized OLS beta (adjusted for the other levers, listwise-complete), and permutation importance from a NaN-native HistGradientBoosting model. Same method for `concentration_level`. The bridge is the person-level distress-vs-concentration correlation plus a small scatter array for chart 2.

```python
"""Post 07 analysis: rank the lifestyle levers of mental health (raw vs adjusted),
bridge to concentration (a productivity proxy). Writes results.json.
Data is synthetic (500 rows); associational only, no causal claims."""
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "mental_health_prediction.csv")

LEVERS = ["work_life_balance", "social_support", "sleep_quality", "sleep_hours",
          "physical_activity_days", "academic_work_pressure", "social_media_hours"]


def z(s):
    return (s - s.mean()) / s.std()


df["distress"] = (z(df.stress_level) + z(df.anxiety_score) + z(df.depression_score)) / 3.0


def rank_levers(target):
    """raw corr, standardized OLS beta (adjusted), permutation importance for one target."""
    raw = df[LEVERS].corrwith(df[target])  # pairwise-complete correlations
    sub = df[LEVERS + [target]].dropna()   # listwise-complete for the regression
    Xz = (sub[LEVERS] - sub[LEVERS].mean()) / sub[LEVERS].std()
    ols = LinearRegression().fit(Xz, sub[target])
    beta = pd.Series(ols.coef_, index=LEVERS)
    r2 = ols.score(Xz, sub[target])
    m = df[target].notna()                 # HGB handles NaN in X, needs complete y
    hgb = HistGradientBoostingRegressor(random_state=0).fit(df.loc[m, LEVERS], df.loc[m, target])
    pim = permutation_importance(hgb, df.loc[m, LEVERS], df.loc[m, target],
                                 n_repeats=30, random_state=0)
    perm = pd.Series(pim.importances_mean, index=LEVERS)
    rows = [{"lever": L, "raw_corr": round(float(raw[L]), 3),
             "std_beta": round(float(beta[L]), 3),
             "perm_imp": round(float(perm[L]), 4)} for L in LEVERS]
    rows.sort(key=lambda r: abs(r["std_beta"]), reverse=True)
    return {"levers": rows, "ols_r2": round(float(r2), 3),
            "n_listwise": int(len(sub)), "n_perm": int(m.sum())}


distress = rank_levers("distress")
concentration = rank_levers("concentration_level")

b = df[["distress", "concentration_level", "mental_health_condition"]].dropna()
bridge_corr = float(b["distress"].corr(b["concentration_level"]))
scatter = [{"d": round(float(r.distress), 3), "c": float(r.concentration_level),
            "cond": r.mental_health_condition} for r in b.itertuples()]

out = {"n_rows": int(len(df)), "distress": distress, "concentration": concentration,
       "bridge_corr": round(bridge_corr, 3), "bridge_n": int(len(b)), "scatter": scatter}
(BASE / "results.json").write_text(json.dumps(out, indent=2))

print("distress ranking (by |adjusted beta|):")
for r in distress["levers"]:
    print(f"  {r['lever']:24s} raw={r['raw_corr']:+.2f}  adj={r['std_beta']:+.2f}  perm={r['perm_imp']:.3f}")
print(f"OLS R^2={distress['ols_r2']}  n_listwise={distress['n_listwise']}  n_perm={distress['n_perm']}")
print(f"bridge distress~concentration r={bridge_corr:.3f}  n={len(b)}")
```

- [ ] **Step 2: Run and sanity-check.** `cd mental-health-productivity && ../sberbank-housing/.venv/bin/python build_analysis.py`. Expected (matches the brainstorm probe): work_life_balance and social_support are the top two by |adjusted beta| (about -0.29 and -0.18); sleep_quality and physical_activity_days DEFLATE to |beta| < 0.15 despite strong raw correlations (about -0.68 and -0.66); OLS R^2 about 0.79, n_listwise about 319; bridge r about -0.7. **GATE: if work_life_balance and social_support are NOT the top two adjusted levers, or if sleep_quality/exercise do NOT deflate, STOP and reconcile with the design before writing (the whole essay turns on that reshuffle).**

---

### Task 2: Charts

**Files:** Create `mental-health-productivity/make_charts.py`; writes `charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette, reading `results.json`.

```python
"""Charts for 'What Actually Moves Your Mental Health'. Reads results.json.
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

NICE = {"work_life_balance": "work-life balance", "social_support": "social support",
        "sleep_quality": "sleep quality", "sleep_hours": "sleep hours",
        "physical_activity_days": "physical activity", "academic_work_pressure": "work pressure",
        "social_media_hours": "social media hours"}


def save(fig, name):
    fig.savefig(BASE / "charts" / name, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print("charts/" + name)


def chart1_levers():
    rows = R["distress"]["levers"]  # already sorted by |std_beta| desc
    rows = rows[::-1]               # barh plots bottom-up; reverse so strongest on top
    names = [NICE[r["lever"]] for r in rows]
    raw = [abs(r["raw_corr"]) for r in rows]
    adj = [abs(r["std_beta"]) for r in rows]
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    h = 0.38
    ax.barh(y + h / 2, raw, height=h, color=MUTED, label="raw correlation (alone)")
    hi = {"work-life balance", "social support"}
    adjc = [AQUA if n in hi else (RED if n in ("sleep quality", "physical activity") else BLUE)
            for n in names]
    ax.barh(y - h / 2, adj, height=h, color=adjc, label="adjusted for the other levers")
    ax.set_yticks(y, names, fontsize=10)
    ax.set_xlabel("strength of association with distress (|correlation|, |standardized beta|)")
    ax.set_title("What actually moves mental health, once you stop double-counting")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.text(0.12, -0.02, "Distress = stress + anxiety + depression (standardized). Balance and "
             "support (green) stay on top; sleep quality and exercise (red) shrink once you "
             "adjust for the fact the levers travel together. Synthetic data, 500 rows.",
             fontsize=8.5, color=MUTED)
    save(fig, "01_levers.png")


def chart2_bridge():
    pts = R["scatter"]
    cond_color = {"Normal": AQUA, "Anxiety": YELLOW, "Depression": BLUE, "Burnout": RED}
    fig, ax = plt.subplots(figsize=(8.4, 6.4))
    for cond, col in cond_color.items():
        xs = [p["d"] for p in pts if p["cond"] == cond]
        ys = [p["c"] for p in pts if p["cond"] == cond]
        ax.scatter(xs, ys, s=26, color=col, alpha=0.75, edgecolor="white",
                   linewidth=0.4, label=cond, zorder=3)
    xd = np.array([p["d"] for p in pts])
    yd = np.array([p["c"] for p in pts])
    m, c = np.polyfit(xd, yd, 1)
    xs = np.array([xd.min(), xd.max()])
    ax.plot(xs, m * xs + c, color=INK2, lw=1.5, ls=(0, (4, 3)), zorder=4)
    ax.set_xlabel("distress  (worse mental health ->)")
    ax.set_ylabel("concentration level (1-10)  (better focus ->)")
    ax.set_title("Worse mental health tracks worse focus")
    ax.legend(loc="upper right", frameon=False, fontsize=9, title="condition")
    ax.annotate(f"r = {R['bridge_corr']:.2f}", (0.04, 0.06), xycoords="axes fraction",
                fontsize=11, color=INK, fontweight="bold")
    fig.text(0.12, -0.02, "Each point is one person (n=%d). Concentration is the in-data proxy "
             "for 'can you actually work'. The same two levers, balance and support, sit behind "
             "both. Association only; synthetic data." % R["bridge_n"],
             fontsize=8.5, color=MUTED)
    save(fig, "02_bridge.png")


def chart3_payoff():
    """External macro evidence, kept visually separate from the toy data. Numbers are
    verified in the references file, NOT computed from the dataset."""
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.axis("off")
    ax.set_title("What poor mental health costs, and what treating it returns",
                 loc="left", pad=16)
    ax.text(0.02, 0.60, "US$1 trillion", fontsize=34, color=RED, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.02, 0.42, "lost every year to depression and anxiety\nin reduced productivity",
            fontsize=11, color=INK2, transform=ax.transAxes, va="top")
    ax.text(0.56, 0.60, "US$4 back", fontsize=34, color=AQUA, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.56, 0.42, "in health and productivity for every\nUS$1 put into scaled-up treatment",
            fontsize=11, color=INK2, transform=ax.transAxes, va="top")
    ax.axvline(0.52, ymin=0.12, ymax=0.78, color=BASELINE, lw=0.8)
    fig.text(0.02, 0.02, "Source: WHO, Mental health at work (2024); Chisholm et al. (2016), "
             "The Lancet Psychiatry. Global figures, not from this dataset.",
             fontsize=8.5, color=MUTED)
    save(fig, "03_payoff.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_levers()
    chart2_bridge()
    chart3_payoff()
```

- [ ] **Step 2: Run and eyeball.** `cd mental-health-productivity && ../sberbank-housing/.venv/bin/python make_charts.py`. Read each PNG back; fix label collisions or legend overlaps before proceeding. Confirm chart 3's two numbers exactly match the figures pinned in Task 3 (do not ship a number the references file has not verified).

---

### Task 3: Pin the citations (the load-bearing external facts)

**Files:** Create `mental-health-productivity/docs/2026-07-12-mental-health-productivity-references-verified.md`

This post's honesty rests on real external evidence. Verify each figure against its primary source with WebFetch before it goes in a chart or the prose.

- [ ] **Step 1: Verify the WHO productivity cost and the treatment return.** WebFetch the WHO "Mental health at work" fact sheet (who.int) and confirm the wording for the ~US$1 trillion/year lost-productivity figure (commonly stated as "12 billion working days lost each year to depression and anxiety, at a cost of US$1 trillion per year in lost productivity"). Confirm the 4:1 return figure and its origin: Chisholm, D., Sweeny, K., Sheehan, P., Rasmussen, B., Smit, F., Cuijpers, P., & Saxena, S. (2016). Scaling-up treatment of depression and anxiety: A global return on investment analysis. *The Lancet Psychiatry*, 3(5), 415-424. **If the exact figure differs (some sources say a 4:1 return on the US$1 spent), use the primary source's exact number and wording; adjust chart 3 to match.**
- [ ] **Step 2: Verify two or three peer-reviewed anchors that the levers are real** (so the ranking is trustworthy despite synthetic data). Confirm exact citation details for one each of:
  - work-life balance / job strain and depression (candidate: Madsen, I. E. H., et al. (2017). Job strain as a risk factor for clinical depression: Systematic review and meta-analysis. *Psychological Medicine*, 47(8), 1342-1356);
  - social support and mental health (candidate: Harandi, T. F., Taghinasab, M. M., & Nayeri, T. D. (2017). The correlation of social support with mental health: A meta-analysis. *Electronic Physician*, 9(9), 5212-5222);
  - physical activity and depression (candidate: Schuch, F. B., et al. (2018). Physical activity and incident depression: A meta-analysis of prospective cohort studies. *American Journal of Psychiatry*, 175(7), 631-648).
  Use whichever you can verify; swap any that do not check out.
- [ ] **Step 3: Record the Kaggle dataset citation.** Harpartap Singh. (2026). *Mental health prediction dataset* [Data set]. Kaggle. https://www.kaggle.com/datasets/harpartapsingh13/mental-health-prediction-dataset
- [ ] **Step 4: Write each as an APA 7 entry** into the references file, annotated with the claim it supports and the access date, and flag which figures appear in chart 3.

---

### Task 4: Data-download note and storytelling README

**Files:** Create `mental-health-productivity/data/README.md` and `mental-health-productivity/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source (`harpartapsingh13/mental-health-prediction-dataset`), the CLI download command (`kaggle datasets download -d harpartapsingh13/mental-health-prediction-dataset`), the column scales (from the dataset description), and a prominent note: the data is SYNTHETIC ("real-world inspired"), 500 rows, balanced by design, so it illustrates rather than proves; there is NO productivity/economic column.
- [ ] **Step 2: Write `mental-health-productivity/README.md`** as the storytelling README (argument in three charts, how-the-analysis-works table linking `profile_data.py` / `build_analysis.py` / `make_charts.py`, reproduce steps, method and caveats), matching `international-education/README.md` style. Foreground synthetic + cross-sectional + concentration-is-a-proxy. Link the live essay URL once known. No long dashes.

---

### Task 5: Draft the essay for author review

**Files:** Create `mental-health-productivity/draft/what-actually-moves-your-mental-health.md` and `.docx`

Draft ~1,300 to 1,700 words following the six-section spine, using numbers from `results.json`. Match the author's voice from `international-education/draft/the-cheapest-degree-abroad-isnt-the-best-deal.md` (stance-first, plain, honest about limits).

Required content anchors:
- **Open, stance-first:** everyone has a theory about what wrecks their head; a dataset lets us rank the levers; one honest caveat up front, it is synthetic, so read it as a hypothesis made visible, not proof.
- **Rank the levers (chart 1):** raw ranking, then adjusted. Balance and support hold the top. The teachable, slightly counterintuitive moment: sleep quality and exercise LOOK powerful alone but shrink once you adjust, because the levers travel together (people with good balance also sleep and move more). Explain standardized regression plainly.
- **The honest nuance on the deflation:** do NOT say sleep or exercise "do not matter". Real evidence says they do (cite the physical-activity meta-analysis). In this data their apparent effect is mostly shared with balance and support; that is a statement about overlap, not a claim they are useless.
- **The bridge to work (chart 2):** the same levers predict concentration; worse mental health tracks worse focus (r about -0.7). Introduce `concentration_level` honestly as a proxy for output, not output itself.
- **What it is worth (chart 3):** the real external numbers (WHO ~US$1T/yr; ~4:1 return). This is where the "for the economy/company" claim is earned, on real evidence rather than our toy data.
- **The honesty reckoning:** synthetic and self-confirming (label ~86% reconstructable, balanced by design); cross-sectional, so it cannot cut the chicken-and-egg the hypothesis raises (which way does the arrow run?); why we still trust the ranking (real literature finds the same levers).
- **Close, universal:** the biggest levers are relational and structural, not medical or heroic; reframe the chicken-and-egg, stop asking which comes first and invest in the input; mental health is an input to productivity, not a reward for it. Analysis, not medical or financial advice.

Guardrails: no long dashes; associational language only; no personalized medical or financial advice.

- [ ] **Step 1: Write the draft** with figures as `../charts/*.png` refs.
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/md_to_docx.py` (writes `.docx` next to the `.md`).
- [ ] **Step 3: Long-dash scan.** `grep -n $'[–—]' draft/what-actually-moves-your-mental-health.md` expected empty.

---

### Task 6: Adversarial verification (before author handoff)

Run a four-agent Workflow over the draft (per the Post 03-06 lesson, verify BEFORE the author reads it):
(a) **numbers** match `results.json` (raw vs adjusted betas, which levers deflate, the bridge r, n reported honestly);
(b) **logic and honesty** (synthetic + self-confirming stated early; cross-sectional-cannot-resolve-chicken-and-egg is load-bearing, not buried; the deflation is framed as shared-variance NOT "exercise is useless"; concentration is flagged as a proxy; no causal claims);
(c) **facts** (the WHO ~US$1T and 4:1 figures and every peer-reviewed anchor match the pinned references, with correct years and wording);
(d) **voice and no-long-dash**.
Fix confirmed issues; re-run the dash scan; if prose changed materially, re-confirm before handoff.

---

### Task 7: AUTHOR REVIEW GATE

- [ ] Hand the `.docx` to Jonathan. Summarize what it argues and the honesty fixes. **Do not proceed until he approves.**

---

### Task 8: Build the MDX page

**Files:** Create `site/src/content/blog/what-actually-moves-your-mental-health.mdx`

- [ ] **Step 1: Copy charts** to `site/public/images/blog/` as `mentalhealth-1-levers.png`, `mentalhealth-2-bridge.png`, `mentalhealth-3-payoff.png`. Verify non-empty.
- [ ] **Step 2: Frontmatter** (match Post 05-06 shape):

```yaml
---
title: "What Actually Moves Your Mental Health (It Isn't the Sleep Tips)"
slug: "what-actually-moves-your-mental-health"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-12
tags: ["Data", "Health", "Productivity"]
status: published
seoTitle: "What Actually Moves Your Mental Health - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base (`what-actually-moves-your-mental-health`).

- [ ] **Step 3: Paste approved prose; figures as `<figure><img .../><figcaption>...</figcaption></figure>`** with the exact filenames (`/images/blog/mentalhealth-1-levers.png`, etc.). Real alt text and captions.
- [ ] **Step 4: `## References`** block, APA 7 markdown-link format (mirror Post 06), journal/volume italics where applicable, populated from the verified references file. Include a GitHub code link (`github.com/joechrisnaldy/data-stories/tree/main/mental-health-productivity`).
- [ ] **Step 5: Long-dash scan on the MDX.** Expected clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 9: Build the site and verify

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/what-actually-moves-your-mental-health/index.html` generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git restore public/images/blog/` to revert the optimizer's churn on pre-existing images; re-copy the three raw `mentalhealth-*.png` charts so only the new images are added. Stage ONLY this post's files (another session may be editing this repo; do NOT `git add -A`).
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/what-actually-moves-your-mental-health/index.html`: correct title, three `mentalhealth-*.png` refs, section headings, References.

---

### Task 10: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 07 row**, linking `https://joechrisnaldy.com/blog/what-actually-moves-your-mental-health` and `mental-health-productivity/`. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 11: PUBLISH GATE (author-triggered)

Only when Jonathan says go. Publishing pushes two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/`, remote `joechrisnaldy-portfolio`, branch `main`), staging only the new MDX, the three `mentalhealth-*.png`, and `.published-slugs.json`. Triggers Vercel. **Verify live on `https://joechrisnaldy.com/blog/what-actually-moves-your-mental-health` (NOT .app), and that each image resolves 200.**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 07 folder: `profile_data.py`, `build_analysis.py`, `make_charts.py`, `results.json`, `charts/`, `README.md`, `data/README.md`, `docs/`; NOT `draft/` or `data/*.csv`) plus the series-index README update. Before committing, run `git add --dry-run` and confirm every README-referenced script is included and no draft/CSV leaks.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md` + MEMORY.md index): Post 07 shipped, live URL, thesis, gotchas (synthetic self-confirming dataset; no productivity column so concentration proxy + external WHO numbers; raw-vs-adjusted deflation of sleep/exercise; cross-sectional cannot resolve chicken-and-egg).

---

## Self-review

- **Spec coverage:** distress composite + raw-vs-adjusted ranking (Task 1), the deflation gate (Task 1 Step 2), concentration bridge (Task 1, chart 2), external payoff via verified citations (Tasks 2 chart 3, 3), synthetic/cross-sectional honesty (Tasks 4, 5, 6), no Indonesia frame (Task 5 anchors omit it), APA 7 (Tasks 3, 8). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions are filled from the approved draft at Task 8; citation figures are an explicit verify-first task (Task 3) with named candidate sources, not deferred hand-waves. No orphan TODOs.
- **Consistency:** LEVERS list identical in build_analysis and referenced by make_charts via NICE map; chart raw filenames (01_levers/02_bridge/03_payoff) map to site filenames (mentalhealth-1-levers/-2-bridge/-3-payoff) identically in Tasks 2, 8, 9; slug `what-actually-moves-your-mental-health` identical across Tasks 8, 10, 11 and the filename; results.json keys (distress.levers[].std_beta, bridge_corr, scatter) consistent across Tasks 1 and 2.
- **Review gates:** deflation sanity gate (Task 1 Step 2), citation verify-first (Task 3), adversarial verify (Task 6), author Word review (Task 7), publish gate (Task 11).
