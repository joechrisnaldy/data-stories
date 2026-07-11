# The Cheapest Degree Abroad Isn't the Best Deal: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 06, an education-ROI essay showing that the tuition-sticker-price ranking of study-abroad destinations misleads, and that measuring payback (years of local salary to earn the degree back) plus employment reshuffles which countries are the real value.

**Architecture:** Content build. The Kaggle cost data joins to external OECD average wages and an employment rate by Country; the analysis restricts to the ~30 OECD destinations with clean wage coverage, computes total Master's cost per country and payback = cost / wage, and overlays employment. Verification is coverage checks, data sanity, citation checks, a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/international-education/docs/2026-07-11-education-roi-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact. **Live blog domain is `joechrisnaldy.com` (NOT .app).**

---

## File map

- Create: `international-education/external/oecd_avg_wages_2024.csv` (country, avg_annual_wage_usd_ppp, source) — committed, documented
- Create: `international-education/external/employment_rate.csv` (country, employment_rate, year, source) — committed, documented
- Create: `international-education/external/README.md` (provenance of the two external tables)
- Create: `international-education/profile_data.py`
- Create: `international-education/build_analysis.py` (cost per country, payback, employment overlay; writes results.json)
- Create: `international-education/make_charts.py` (3 charts)
- Create: `international-education/results.json`
- Create: `international-education/data/README.md` (Kaggle cost-data download note)
- Create: `international-education/README.md` (storytelling README)
- Create: `international-education/docs/2026-07-11-education-roi-references-verified.md`
- Create: `international-education/draft/the-cheapest-degree-abroad-isnt-the-best-deal.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/educationroi-1-cost.png`, `-2-payback.png`, `-3-employment.png`
- Create: `site/src/content/blog/the-cheapest-degree-abroad-isnt-the-best-deal.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 06 row)

Cost data already at `international-education/data/International_Education_Costs.csv` (907 rows, 71 countries).

---

### Task 1: Obtain external wage + employment data (DE-RISK, gate)

**Files:** Create `external/oecd_avg_wages_2024.csv`, `external/employment_rate.csv`, `external/README.md`

- [ ] **Step 1: Get OECD average annual wages (2024, PPP-USD).** WebFetch the OECD-sourced average-annual-wages table (OECD Data Explorer dataset AV_AN_WAGE, or the Wikipedia "List of countries by average wage" table which reproduces OECD 2024 PPP-USD figures). Extract the value for each OECD country. Cross-check 2 to 3 values (USA, Germany, Japan) against the OECD indicator page (oecd.org average-annual-wages). Write `external/oecd_avg_wages_2024.csv` with columns `country,avg_annual_wage_usd_ppp` plus a header comment noting the source and access date. Use country names that will reconcile to the cost data (see Step 4).

- [ ] **Step 2: Get employment rate.** Fetch the World Bank employment-to-population ratio (indicator SL.EMP.TOTL.SP.ZS, 15+, modeled ILO), latest available year:

```bash
curl -s "https://api.worldbank.org/v2/country/all/indicator/SL.EMP.TOTL.SP.ZS?format=json&date=2023:2024&per_page=600" -o /tmp/wb_emp.json
```
Parse the JSON to the latest non-null value per country; write `external/employment_rate.csv` with `country,employment_rate,year`. (If a cleaner OECD 15-64 employment rate is easy to obtain, prefer it and document the definition; otherwise use the World Bank ratio and label it precisely.)

- [ ] **Step 3: Write `external/README.md`** documenting both tables: exact source, indicator, year, definition (employment-to-population ratio is economy-wide, 15+, not new-graduate), and access date.

- [ ] **Step 4: Reconcile country names and CHECK COVERAGE (the gate).**

```bash
cd international-education && ../sberbank-housing/.venv/bin/python - <<'EOF'
import pandas as pd
cost = pd.read_csv("data/International_Education_Costs.csv")
wage = pd.read_csv("external/oecd_avg_wages_2024.csv", comment="#")
emp = pd.read_csv("external/employment_rate.csv", comment="#")
# reconcile: cost uses USA, UK, South Korea; sources may use United States, United Kingdom, Korea
ALIAS = {"United States":"USA","United Kingdom":"UK","Korea":"South Korea",
         "Korea, Rep.":"South Korea","Czechia":"Czech Republic","Turkiye":"Turkey","Türkiye":"Turkey",
         "Slovak Republic":"Slovakia"}
wage["country"] = wage.country.replace(ALIAS)
emp["country"] = emp.country.replace(ALIAS)
cc = set(cost.Country.unique())
both = cc & set(wage.country) & set(emp.country)
print("cost countries:", len(cc))
print("with wage+employment (the analysis set):", len(both))
print(sorted(both))
print("cost countries with NO wage:", sorted(cc - set(wage.country))[:40])
EOF
```
Expected: the analysis set is about 30 countries. **If it is under 20, STOP and report to the user before proceeding** (the scope decision assumed ~30). Add any missing ALIAS reconciliations and rerun.

- [ ] **Step 5: Commit the external tables.**

```bash
cd /Users/jonathanchrisnaldy/Claude-Workspace/Projects/analytics-blog
git add international-education/external/
git commit -m "data: external OECD wages + employment rate for education ROI (post 06)"
```

---

### Task 2: Profile the cost data

**Files:** Create `international-education/profile_data.py`

- [ ] **Step 1: Write the profiler**

```python
"""Profile the international education cost dataset: shape, levels, per-country
Master's program counts, cost columns."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "International_Education_Costs.csv")
print("shape:", df.shape, "| countries:", df.Country.nunique())
print("levels:", df.Level.value_counts().to_dict())
m = df[df.Level == "Master"]
print("Master rows:", len(m), "| countries with Masters:", m.Country.nunique())
print("Master programs per country (top 15):")
print(m.Country.value_counts().head(15).to_string())
print("cost columns nulls:", df[["Tuition_USD","Rent_USD","Visa_Fee_USD","Insurance_USD","Duration_Years"]].isna().sum().to_dict())
```

- [ ] **Step 2: Run it.** `cd international-education && ../sberbank-housing/.venv/bin/python profile_data.py`. Confirm the `Level` value for Master's (exact string, likely "Master"), and that cost columns are non-null.

---

### Task 3: Analysis (cost, payback, employment)

**Files:** Create `international-education/build_analysis.py`; writes `results.json`

- [ ] **Step 1: Write the analysis**

```python
"""Education ROI: total Master's cost per country, payback = cost / local average wage,
employment overlay. Restricted to countries with OECD wage + employment coverage."""
import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
cost = pd.read_csv(BASE / "data" / "International_Education_Costs.csv")
wage = pd.read_csv(BASE / "external" / "oecd_avg_wages_2024.csv", comment="#")
emp = pd.read_csv(BASE / "external" / "employment_rate.csv", comment="#")

ALIAS = {"United States": "USA", "United Kingdom": "UK", "Korea": "South Korea",
         "Korea, Rep.": "South Korea", "Czechia": "Czech Republic", "Turkiye": "Turkey",
         "Türkiye": "Turkey", "Slovak Republic": "Slovakia"}
wage["country"] = wage.country.replace(ALIAS)
emp["country"] = emp.country.replace(ALIAS)

m = cost[cost.Level == "Master"].copy()
# total cost of the degree in USD
m["total_cost"] = (m.Tuition_USD * m.Duration_Years
                   + m.Rent_USD * 12 * m.Duration_Years
                   + m.Visa_Fee_USD + m.Insurance_USD)

# median per country (robust to a few elite universities), with program count
agg = (m.groupby("Country")
       .agg(total_cost=("total_cost", "median"),
            tuition=("Tuition_USD", "median"),
            n_programs=("total_cost", "size"),
            avg_duration=("Duration_Years", "median")))
agg = agg[agg.n_programs >= 3]  # drop countries with too few programs to be stable

w = wage.set_index("country").avg_annual_wage_usd_ppp
e = emp.set_index("country").employment_rate
agg = agg.join(w, how="inner").join(e, how="inner")
agg["payback_years"] = (agg.total_cost / agg.avg_annual_wage_usd_ppp).round(2)
agg = agg.rename(columns={"avg_annual_wage_usd_ppp": "avg_wage", "employment_rate": "employment"})

cost_rank = agg.total_cost.rank(ascending=False).astype(int)
payback_rank = agg.payback_years.rank(ascending=False).astype(int)
agg["cost_rank"] = cost_rank
agg["payback_rank"] = payback_rank

out = {
    "n_countries": int(len(agg)),
    "by_country": agg.reset_index().round(2).to_dict(orient="records"),
    "cheapest": agg.total_cost.idxmin(),
    "most_expensive": agg.total_cost.idxmax(),
    "best_payback": agg.payback_years.idxmin(),
    "worst_payback": agg.payback_years.idxmax(),
}
(BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
print("countries in analysis:", out["n_countries"])
print("cheapest total cost:", out["cheapest"], "| most expensive:", out["most_expensive"])
print("best payback:", out["best_payback"], "| worst payback:", out["worst_payback"])
print(agg.sort_values("payback_years")[["total_cost", "avg_wage", "payback_years", "employment"]].to_string())
```

- [ ] **Step 2: Run and sanity-check.** `cd international-education && ../sberbank-housing/.venv/bin/python build_analysis.py`. Expected: about 30 countries; the cost ranking and payback ranking differ (the reshuffle is the thesis); Germany-type countries (low cost, decent wage) show short payback, high-tuition countries (USA, UK, Australia) longer payback unless offset by high wages. **If the reshuffle is trivial (cost and payback rankings nearly identical), STOP and reconsider the framing before writing.** Confirm payback values are plausible (roughly 0.3 to 3 years of average salary).

---

### Task 4: Charts

**Files:** Create `international-education/make_charts.py`; writes `charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette (BLUE #2a78d6, AQUA #1baf7a, YELLOW #eda100, RED #e34948, INK #0b0b0b, INK2 #52514e, MUTED #898781, GRID #e1e0d9, BASELINE #c3c2b7, SURFACE #fcfcfb), reading `results.json`. Produce:
  1. `01_cost.png`: total Master's cost by country, ranked bars. The familiar expensive-West ranking.
  2. `02_payback.png`: payback (years of local salary) by country, ranked bars, showing the reshuffle; annotate a couple of movers (e.g., a country that was expensive but pays back fast, and one that was cheap but pays back slow).
  3. `03_employment.png`: a scatter of payback (x) versus employment rate (y), or a value view, so the reader sees payback and the odds of a job together; label the standout value countries.
  Write real titles, labels, footnotes (source: OECD wages 2024, employment source, 2026 snapshot). No long dashes.

- [ ] **Step 2: Run and eyeball.** Read each PNG back; fix label collisions before proceeding.

---

### Task 5: Pin the citations

**Files:** Create `international-education/docs/2026-07-11-education-roi-references-verified.md`

- [ ] **Step 1: Confirm the OECD average annual wages citation** (OECD, average annual wages, 2024, PPP-USD, dataset AV_AN_WAGE) with the exact source URL and access date; note it is economy-wide.
- [ ] **Step 2: Confirm the employment source** (World Bank, employment-to-population ratio 15+, modeled ILO estimate, indicator SL.EMP.TOTL.SP.ZS, with year), or the OECD employment rate if used instead.
- [ ] **Step 3: Record the Kaggle cost dataset citation** (adilshamim8, 2025).
- [ ] **Step 4: Write each as an APA 7 entry** into the references file, annotated with the claim it supports.

---

### Task 6: Data-download note and storytelling README

**Files:** Create `international-education/data/README.md` and `international-education/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source (`adilshamim8/cost-of-international-education`), the CLI download command, and a note that salary/employment are NOT in this dataset and come from `external/` (OECD, World Bank).
- [ ] **Step 2: Write `international-education/README.md`** as the storytelling README (argument in three charts, how-the-analysis-works table, reproduce steps, method and caveats), matching `speed-dating/README.md` style. Foreground the "assumes you stay and work there" caveat. Link the live essay URL once known.

---

### Task 7: Draft the essay for author review

**Files:** Create `international-education/draft/the-cheapest-degree-abroad-isnt-the-best-deal.md` and `.docx`

Draft ~1,300 to 1,700 words following the five-section spine, using numbers from `results.json`. Match the author's voice from `a-model-can-be-86-percent-right-and-useless.mdx`.

Required content anchors:
- Open stance-first: people shop for a degree abroad by tuition sticker price, the wrong ruler.
- The cost ranking (chart 1): the familiar expensive-West order.
- The payback reshuffle (chart 2): years of local salary to earn it back; who the real bargains are; name the biggest movers with actual numbers.
- The employment reality check (chart 3): value is payback and the odds of a job together.
- The load-bearing caveat, early and plain: the wage is the DESTINATION country's, so payback assumes you stay and work there, which many international students cannot; average wage is not a new-grad wage (payback reads optimistic); economy-wide, not by field; cost data is a sample.
- Light Indonesia close (the gengsi of an expensive Western degree vs payback) and the universal lesson (price is not value). Frame as analysis, not financial advice.

Guardrails: no long dashes; correlation/associational only; do not give personalized financial advice.

- [ ] **Step 1: Write the draft** with figures as `../charts/*.png` refs.
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/md_to_docx.py`.
- [ ] **Step 3: Long-dash scan.** Expected clean.
- [ ] **Step 4: AUTHOR REVIEW GATE.** Hand the `.docx` to Jonathan; do not proceed until he approves.

---

### Task 8: Adversarial verification (before handoff)

Run a four-agent Workflow over the draft: (a) numbers match `results.json` (costs, payback years, ranks, employment); (b) logic and honesty (the "assumes you stay and work there" caveat is early and load-bearing; average-wage-not-new-grad stated; no causal overreach; the reshuffle claim is real, not cherry-picked); (c) facts (OECD wage and employment citations match the pinned sources; year and definition correct); (d) voice and no-long-dash. Fix confirmed issues; re-run the dash scan; if prose changed, re-confirm with the author. (Do this BEFORE the author reads it, per the Post 03-05 lesson.)

---

### Task 9: Build the MDX page

**Files:** Create `site/src/content/blog/the-cheapest-degree-abroad-isnt-the-best-deal.mdx`

- [ ] **Step 1: Copy charts** to `site/public/images/blog/` as `educationroi-1-cost.png`, `educationroi-2-payback.png`, `educationroi-3-employment.png`. Verify non-empty.
- [ ] **Step 2: Frontmatter** (match Post 02-05 shape):

```yaml
---
title: "The Cheapest Degree Abroad Isn't the Best Deal"
slug: "the-cheapest-degree-abroad-isnt-the-best-deal"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-11
tags: ["Data", "Education", "Economics"]
status: published
seoTitle: "The Cheapest Degree Abroad Isn't the Best Deal - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base.

- [ ] **Step 3: Paste approved prose; figures as `<figure><img .../><figcaption>...</figcaption></figure>`** with the exact filenames. Real alt text and captions.
- [ ] **Step 4: `## References`** block, APA 7 markdown-link format (mirror the prior post), with journal/volume italics where applicable, populated from the verified references file.
- [ ] **Step 5: Long-dash scan on the MDX.** Expected clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 10: Build the site and verify

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git restore public/images/blog/` to revert the optimizer's churn on pre-existing images; re-copy the raw Post 06 charts so only the new `educationroi-*.png` are added. Stage ONLY my post's files (another session may be editing this repo, do NOT `git add -A`).
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/the-cheapest-degree-abroad-isnt-the-best-deal/index.html`: correct title, three `educationroi-*.png` refs, section headings, References. (Dev server port 4321 may be taken; the built HTML check is sufficient.)

---

### Task 11: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 06 row**, linking `https://joechrisnaldy.com/blog/the-cheapest-degree-abroad-isnt-the-best-deal` and `international-education/`. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 12: PUBLISH GATE (author-triggered)

Only when Jonathan says go. Publishing pushes two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/`, remote `joechrisnaldy-portfolio`, branch `main`), staging only the new MDX, `educationroi-*.png`, and `.published-slugs.json`. Triggers Vercel. **Verify live on `https://joechrisnaldy.com/...` (NOT .app).**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 06 folder: code, external/, results.json, README, docs, data/README.md; NOT draft/ or data/*.csv) plus the series-index README update.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md`): Post 06 shipped, live URL, thesis, gotchas (external OECD+WB join, country-name reconciliation, the stay-and-work assumption).

---

## Self-review

- **Spec coverage:** external data acquisition + coverage gate (Task 1), scope OECD ~30 (Tasks 1, 3), payback metric (Task 3), cost/payback/employment charts (Task 4), the load-bearing caveats (Tasks 6, 7, 8), light Indonesia close (Task 7), APA 7 (Tasks 5, 9). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions filled from the approved draft at Task 9; the wage/employment sources and exact numbers are explicit acquisition tasks with a coverage gate, not deferred hand-waves. No orphan TODOs.
- **Consistency:** country-name ALIAS map identical in Task 1 Step 4 and Task 3; chart filenames identical across Task 9 Step 1 and Step 3; slug identical across Task 9 and the filename; column names (total_cost, avg_wage, payback_years, employment) consistent across Tasks 3 and 4; domain `.com` throughout.
- **Review gates:** external-data coverage gate (Task 1 Step 4), reshuffle sanity gate (Task 3 Step 2), author Word review (Task 7 / reordered with Task 8), adversarial verify (Task 8), publish gate (Task 12).
