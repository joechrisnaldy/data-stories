# What the Bank Sees When It Looks at You: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Post 10, an essay that reads a synthetic loan dataset's leaked generator (its "rulebook") to show that an automated credit decision is a stack of human choices, income and debt dominate over the credit score people fret over, some factors are not about risk at all, and the whole apparatus can only judge people it can already see.

**Architecture:** Content build on a synthetic loan dataset that ships its own generator. The analysis computes what drives approval (correlations + permutation importance), how credit acts through the interest rate, the age gradient in approval, and the fully-banked nature of the sample; then writes results.json. FOUR charts. The real-world anchors (debt-to-income in underwriting, ECOA age protection, the World Bank Findex unbanked count) are external, verified, carried in prose and the fourth chart. Verification is data sanity, citation checks (verified-or-omit), a long-dash scan, a slug match, and a clean Astro build.

**Tech Stack:** Python (pandas, numpy, scikit-learn, matplotlib) in the reused venv at `sberbank-housing/.venv`; Astro MDX site; series dataviz palette.

**Design doc:** `Projects/analytics-blog/loan/docs/2026-07-14-loan-rulebook-design.md`

**Rules (repo CONVENTIONS.md):** no long dashes; APA 7 references for every external fact; verified or omit; descriptive only; NOT financial advice; keep the synthetic caveat loud; do not claim real banks discriminate (only that this rulebook makes these choices). **FOUR charts (new series standard). Live blog domain is `joechrisnaldy.com` (NOT .app).**

**Title (chosen):** "What the Bank Sees When It Looks at You"
**Slug / filename base:** `what-the-bank-sees`

---

## File map

- Done: `loan/data/Loan.csv` (20,000 rows) and `loan/data/CSV_Generation.py` (the generator/rulebook)
- Done: `loan/profile_data.py` (written + runs; the profiler)
- Create: `loan/build_analysis.py` (drivers, credit-to-rate, age gradient, legibility; writes results.json)
- Create: `loan/results.json`
- Create: `loan/make_charts.py` (4 charts)
- Create: `loan/data/README.md` (Kaggle download note + synthetic/generator explanation)
- Create: `loan/README.md` (storytelling README)
- Create: `loan/docs/2026-07-14-loan-rulebook-references-verified.md`
- Create: `loan/draft/what-the-bank-sees.md` and `.docx` (gitignored)
- Create: `site/public/images/blog/loan-1-what-weighs.png`, `loan-2-credit-prices.png`, `loan-3-not-risk.png`, `loan-4-no-score.png`
- Create: `site/src/content/blog/what-the-bank-sees.mdx`
- Modify: `Projects/analytics-blog/README.md` (Post 10 row)

Image prefix `loan-` is unused on the site (existing: 4months, gamingaddiction, moscowhousing, speeddating, studenthealth, whatittakes, worldcup2026, educationroi, mentalhealth, nutritionscore, happiness).

---

### Task 1: Analysis (drivers, credit-to-rate, age gradient, legibility)

**Files:** Create `loan/build_analysis.py`; writes `results.json`

- [ ] **Step 1: Write the analysis.**

```python
"""Post 10 analysis: read the bank's rulebook. What actually drives loan approval (income and
debt, not credit score), how credit acts through the interest rate, the not-about-risk factors
(age), and the fact that everyone here is already banked. Writes results.json. Synthetic data."""
import json
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "Loan.csv")

NICE = {"AnnualIncome": "annual income", "TotalDebtToIncomeRatio": "debt-to-income",
        "InterestRate": "loan interest rate", "LoanAmount": "loan amount", "NetWorth": "net worth",
        "CreditScore": "credit score", "Age": "age",
        "LengthOfCreditHistory": "credit-history length", "PreviousLoanDefaults": "past defaults"}
FEATS = list(NICE.keys())

# chart 1: correlation with approval for a curated, non-redundant feature set
corr_approval = sorted(
    [{"feature": f, "nice": NICE[f], "corr": round(float(df[f].corr(df.LoanApproved)), 3)}
     for f in FEATS], key=lambda r: abs(r["corr"]), reverse=True)

# permutation importance (concurs; routes through derived features like InterestRate)
num = df.select_dtypes("number").drop(columns=["LoanApproved", "RiskScore"], errors="ignore")
clf = HistGradientBoostingClassifier(random_state=0).fit(num, df.LoanApproved)
pim = permutation_importance(clf, num, df.LoanApproved, n_repeats=5, random_state=0)
importance = sorted([{"feature": c, "imp": round(float(v), 4)}
                     for c, v in zip(num.columns, pim.importances_mean)],
                    key=lambda r: r["imp"], reverse=True)[:8]

# chart 2: credit score prices you (credit -> interest rate)
credit_rate_corr = float(df.CreditScore.corr(df.InterestRate))
credit_approval_corr = float(df.CreditScore.corr(df.LoanApproved))
samp = df.sample(2500, random_state=0)
credit_rate_scatter = [{"credit": int(r.CreditScore), "rate": round(float(r.InterestRate), 4)}
                       for r in samp.itertuples()]

# chart 3: approval by age band (not-about-risk); plus education + season secondary
df["age_band"] = pd.cut(df.Age, [17, 25, 35, 45, 55, 65, 80],
                        labels=["under 25", "25-35", "35-45", "45-55", "55-65", "65+"])
approval_by_age = [{"band": str(b), "rate": round(float(g.LoanApproved.mean()), 3), "n": int(len(g))}
                   for b, g in df.groupby("age_band", observed=True)]
approval_by_edu = [{"edu": e, "rate": round(float(g.LoanApproved.mean()), 3), "n": int(len(g))}
                   for e, g in df.groupby("EducationLevel")]
month = pd.to_datetime(df.ApplicationDate).dt.month
ss = month.between(3, 8)
season = {"spring_summer_rate": round(float(df.LoanApproved[ss].mean()), 3),
          "rest_rate": round(float(df.LoanApproved[~ss].mean()), 3)}

# chart 4: everyone here is already legible to the bank
legible = {"n": int(len(df)),
           "with_credit_score": int((df.CreditScore > 0).sum()),
           "with_accounts": int(((df.SavingsAccountBalance > 0) | (df.CheckingAccountBalance > 0)).sum())}

out = {"n": int(len(df)), "approval_rate": round(float(df.LoanApproved.mean()), 3),
       "corr_approval": corr_approval, "importance": importance,
       "credit_rate_corr": round(credit_rate_corr, 3),
       "credit_approval_corr": round(credit_approval_corr, 3),
       "credit_rate_scatter": credit_rate_scatter,
       "approval_by_age": approval_by_age, "approval_by_edu": approval_by_edu,
       "season": season, "legible": legible,
       "findex_unbanked_millions": 1400}  # EXTERNAL; verify exact figure/year in Task 3
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("approval rate:", out["approval_rate"])
print("corr with approval:", [(r["nice"], r["corr"]) for r in corr_approval])
print("top importance:", [(r["feature"], r["imp"]) for r in importance[:6]])
print("credit->rate corr:", out["credit_rate_corr"], "| credit->approval corr:", out["credit_approval_corr"])
print("approval by age:", [(r["band"], r["rate"]) for r in approval_by_age])
print("season:", season, "| legible:", legible)
```

- [ ] **Step 2: Run and sanity-check.** `cd loan && ../sberbank-housing/.venv/bin/python build_analysis.py`. Expected (matches profiling): approval rate ~0.24; annual income has the strongest approval correlation (~+0.60), far above credit score (~+0.14); permutation importance top is debt-to-income / interest rate / income with CreditScore small (~6th); credit-to-interest-rate correlation strongly NEGATIVE (rate is mostly a function of credit); approval rate rises monotonically with age (~0.12 under 25 to ~0.32 for 65+). **GATE: if income does NOT clearly outrank credit score for approval, or the age gradient is flat, STOP and reconcile (both are load-bearing).**

---

### Task 2: Charts (4)

**Files:** Create `loan/make_charts.py`; writes `charts/*.png`

- [ ] **Step 1: Write the chart script** using the series palette, reading `results.json`.

```python
"""Charts for 'What the Bank Sees When It Looks at You'. Reads results.json.
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


def chart1_what_weighs():
    rows = R["corr_approval"][::-1]               # barh bottom-up: strongest on top
    names = [r["nice"] for r in rows]
    mags = [abs(r["corr"]) for r in rows]
    signs = [r["corr"] for r in rows]
    colors = [RED if r["feature"] == "CreditScore"
              else (AQUA if r["feature"] == "AnnualIncome" else BLUE) for r in rows]
    fig, ax = plt.subplots(figsize=(8.8, 6.2))
    y = np.arange(len(names))
    ax.barh(y, mags, color=colors, height=0.72)
    ax.set_yticks(y, names, fontsize=10.5)
    for yi, m, s in zip(y, mags, signs):
        tag = "more likely" if s > 0 else "less likely"
        ax.annotate(f"{m:.2f}  ({tag})", (m, yi), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=INK2)
    ax.set_xlim(0, max(mags) * 1.28)
    ax.set_xlabel("strength of link to getting approved (|correlation|)")
    ax.set_title("What the decision actually weighs: income and debt, not your credit score")
    ax.grid(axis="y", visible=False)
    fig.text(0.12, -0.02, "Curated features, correlation with approval on 20,000 synthetic "
             "applicants. Annual income (green) dominates; the credit score people guard (red) "
             "is near the\nbottom. A gradient-boosting model agrees.", fontsize=8.5, color=MUTED)
    save(fig, "01_what_weighs.png")


def chart2_credit_prices():
    s = R["credit_rate_scatter"]
    x = np.array([p["credit"] for p in s])
    yv = np.array([p["rate"] * 100 for p in s])   # percent
    fig, ax = plt.subplots(figsize=(8.4, 6.2))
    ax.scatter(x, yv, s=10, color=BLUE, alpha=0.25, edgecolor="none", zorder=3)
    ax.set_xlabel("credit score")
    ax.set_ylabel("loan interest rate offered (%)")
    ax.set_title("Your credit score prices you, it does not judge you")
    ax.annotate(f"correlation = {R['credit_rate_corr']:.2f}", (0.05, 0.90),
                xycoords="axes fraction", fontsize=11, color=INK, fontweight="bold")
    fig.text(0.12, 0.005, "Each dot is an applicant. A better credit score buys a lower interest "
             "rate, almost mechanically. And it is the interest rate, not the score itself, that\n"
             "the approval decision leans on. Synthetic data.", fontsize=8.5, color=MUTED)
    save(fig, "02_credit_prices.png")


def chart3_not_risk():
    a = R["approval_by_age"]
    names = [r["band"] for r in a]
    rates = [r["rate"] * 100 for r in a]
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    x = np.arange(len(names))
    ax.bar(x, rates, color=YELLOW, width=0.66)
    ax.set_xticks(x, names, fontsize=10)
    for xi, r in zip(x, rates):
        ax.annotate(f"{r:.0f}%", (xi, r), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=9, color=INK2)
    ax.set_ylabel("share of applicants approved")
    ax.set_xlabel("applicant age")
    ax.set_title("Factors that are not about risk: older applicants get approved more")
    ax.grid(axis="x", visible=False)
    ss = R["season"]["spring_summer_rate"] * 100
    rest = R["season"]["rest_rate"] * 100
    fig.text(0.12, -0.04, "Approval rate by age on the synthetic data. The rulebook also rewards "
             "more education and penalizes applying in spring or summer (%.0f%% vs %.0f%%). These "
             "are\nchoices dressed as objective risk." % (ss, rest), fontsize=8.5, color=MUTED)
    save(fig, "03_not_risk.png")


def chart4_no_score():
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    ax.axis("off")
    ax.set_title("The rulebook can only judge people it can already see", loc="left", pad=16)
    ax.text(0.01, 0.60, "20,000 of 20,000", fontsize=30, color=BLUE, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.01, 0.44, "applicants in this dataset already have\nincome, accounts and a credit "
            "history:\nfully legible to any scorecard", fontsize=11, color=INK2,
            transform=ax.transAxes, va="top")
    ax.text(0.55, 0.60, "~1.4 billion", fontsize=30, color=RED, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.55, 0.44, "adults worldwide have no bank account,\ncast no financial shadow, and are"
            "\ninvisible to any credit rulebook", fontsize=11, color=INK2,
            transform=ax.transAxes, va="top")
    ax.axvline(0.51, ymin=0.12, ymax=0.80, color=BASELINE, lw=0.8)
    fig.text(0.01, 0.0, "Left: this dataset (synthetic). Right: World Bank Global Findex 2021. A "
             "credit score is a stack of choices, and also a fence.", fontsize=8.5, color=MUTED)
    save(fig, "04_no_score.png")


if __name__ == "__main__":
    import os
    os.makedirs(BASE / "charts", exist_ok=True)
    chart1_what_weighs()
    chart2_credit_prices()
    chart3_not_risk()
    chart4_no_score()
```

- [ ] **Step 2: Run and eyeball.** `cd loan && ../sberbank-housing/.venv/bin/python make_charts.py`. Read each PNG back; fix label collisions. Confirm chart 1 has income on top and credit score (red) near the bottom; chart 2 is a tight downward cloud; chart 3 rises with age; chart 4's two numbers read cleanly. Chart files: `01_what_weighs.png`, `02_credit_prices.png`, `03_not_risk.png`, `04_no_score.png`.

---

### Task 3: Pin + verify the citations (verified-or-omit)

**Files:** Create `loan/docs/2026-07-14-loan-rulebook-references-verified.md`

Verify each external fact against a primary source with WebFetch/WebSearch. Drop anything not confirmable. Keep the synthetic caveat loud.

- [ ] **Step 1: The dataset.** Zoppelletto, L. (2024). *Financial risk for loan approval* [Data set]. Kaggle. https://www.kaggle.com/datasets/lorenzozoppelletto/financial-risk-for-loan-approval . Confirm it is synthetic and that it ships a generator script.
- [ ] **Step 2: Debt-to-income in real underwriting.** Confirm from an authoritative primary source that lenders use the debt-to-income ratio as a core factor in loan/mortgage decisions (candidate: the US Consumer Financial Protection Bureau, CFPB, on debt-to-income and ability-to-repay). Record the exact citation and URL. **If not confirmable, soften to what is.**
- [ ] **Step 3: Age is protected in credit decisions.** Confirm the US Equal Credit Opportunity Act (ECOA) prohibits discrimination in credit on the basis of age (with narrow exceptions). Cite a primary/authoritative source (CFPB/FTC or the statute). Record exact wording. **Frame carefully: the ECOA governs REAL lenders; our dataset is synthetic and its age preference is illustrative, not evidence about any real bank.**
- [ ] **Step 4: The unbanked count.** Confirm the World Bank Global Findex 2021 figure that about 1.4 billion adults remain unbanked (no account). Record exact figure, year, and wording; adjust the `findex_unbanked_millions` value and chart 4 text if the verified figure differs.
- [ ] **Step 5: Write each as an APA 7 entry** into the references file, annotated with the claim it supports and access date, and flag any wording that must stay hedged (especially: synthetic, no real-bank claims).

---

### Task 4: Data-download note and storytelling README

**Files:** Create `loan/data/README.md` and `loan/README.md`

- [ ] **Step 1: Write `data/README.md`** with the Kaggle source, the CLI download command, and a clear note: the data is SYNTHETIC (20,000 rows) and, unusually, ships its own generator (`CSV Generation.py`) that encodes the exact approval and risk rules; everyone in it is already a banked applicant. The essay reads the rulebook and the data; it makes no claims about real banks.
- [ ] **Step 2: Write `loan/README.md`** as the storytelling README (argument in four charts, how-the-analysis-works table linking `profile_data.py` / `build_analysis.py` / `make_charts.py`, reproduce steps, method and caveats), matching `happiness/README.md` style. Foreground: synthetic rulebook, income-over-credit, the not-about-risk factors, the unbanked close. No long dashes.

---

### Task 5: Draft the essay for author review

**Files:** Create `loan/draft/what-the-bank-sees.md` and `.docx`

Draft ~1,400 to 1,700 words following the eight-part spine in the design doc, using numbers from `results.json`. Match the author's voice from `happiness/draft/the-most-generous-country-isnt-the-happiest.md` (stance-first, plain, honest).

Required content anchors:
- **Open, a person becomes a number:** you fill in thirty boxes about your life and the lender compresses you into one yes/no; and this dataset lets us read the formula.
- **What actually moves it (chart 1):** annual income dominates approval (corr ~0.60), debt-to-income and the interest rate next; the credit score people guard is a minor, indirect lever (~0.14).
- **Credit prices you, does not judge you (chart 2):** credit score mostly sets the interest rate (near-mechanical), and the rate is what the decision weighs.
- **The factors that are not risk (chart 3):** approval rises with age (~12% to ~32%); the rule also rewards education and penalizes spring/summer applications. A risk score is a stack of choices. Note it is synthetic; where real scorecards use age, US fair-lending law (ECOA) restricts it.
- **The honesty layer:** synthetic, relationships are designed, which is the point; real underwriting really does hinge on income and debt-to-income (verified anchor).
- **Who it can not see (chart 4):** everyone here is already banked; ~1.4 billion adults worldwide are unbanked and invisible to any rulebook (Findex). A score is a stack of choices and also a fence.
- **Close, universal:** you are scored by rulebooks you can not read; the people with no score at all are the ones it should worry us most about. Not financial advice.
- **Method notes.**

Guardrails: no long dashes; descriptive only; NO claim that real banks discriminate (synthetic rulebook only); not financial advice; distinguish generator-rule facts from data correlations.

- [ ] **Step 1: Write the draft** with figures as `../charts/*.png` refs.
- [ ] **Step 2: Convert to Word** via `../sberbank-housing/.venv/bin/python ../sberbank-housing/md_to_docx.py draft/what-the-bank-sees.md draft/what-the-bank-sees.docx`.
- [ ] **Step 3: Long-dash scan.** `grep -n $'[–—]' draft/what-the-bank-sees.md` expected empty.

---

### Task 6: Adversarial verification (before author handoff)

Run a four-agent Workflow over the draft (verify BEFORE the author reads it):
(a) **numbers** match `results.json` (income vs credit correlations; the age gradient; credit-to-rate correlation; approval rate; permutation-importance ordering; the two-file/generator provenance);
(b) **logic and honesty** (income-dominates and credit-is-indirect are stated correctly; "credit prices you" is accurate to the generator; the age/education/season factors are framed as THIS synthetic rulebook's choices, NOT proof real banks discriminate; the synthetic caveat is loud and early; correlations not causes; no financial advice);
(c) **facts** (the DTI-in-underwriting, ECOA-age, and Findex ~1.4B claims match the pinned references with correct wording; verified-or-omit respected; the dataset credited as synthetic + self-documenting);
(d) **voice and no-long-dash** (series voice; no em/en dashes; the opening leads with the human "person becomes a number" scene; neutral-explanatory, not an exposé).
Fix confirmed issues; re-run the dash scan; if prose changed materially, re-confirm before handoff.

---

### Task 7: AUTHOR REVIEW GATE

- [ ] Hand the `.docx` to Jonathan. Summarize what it argues and the honesty fixes. **Do not proceed until he approves.**

---

### Task 8: Build the MDX page

**Files:** Create `site/src/content/blog/what-the-bank-sees.mdx`

- [ ] **Step 1: Copy charts** to `site/public/images/blog/` as `loan-1-what-weighs.png` (from `01_what_weighs.png`), `loan-2-credit-prices.png` (from `02_credit_prices.png`), `loan-3-not-risk.png` (from `03_not_risk.png`), `loan-4-no-score.png` (from `04_no_score.png`). Verify non-empty.
- [ ] **Step 2: Frontmatter** (match Post 08-09 shape):

```yaml
---
title: "What the Bank Sees When It Looks at You"
slug: "what-the-bank-sees"
excerpt: "<one to two sentences from the approved draft; single quotes only, no long dashes>"
publishedAt: 2026-07-14
tags: ["Data", "Finance", "Society"]
status: published
seoTitle: "What the Bank Sees When It Looks at You - Jonathan Chrisnaldy"
metaDescription: "<about 150 chars, no long dashes, no internal double quotes>"
---
```
Slug MUST equal the filename base (`what-the-bank-sees`).

- [ ] **Step 3: Paste approved prose; FOUR figures as `<figure><img .../><figcaption>...</figcaption></figure>`** with the exact filenames (`/images/blog/loan-1-what-weighs.png`, etc.). Real alt text and captions.
- [ ] **Step 4: `## References`** block, APA 7 markdown-link format (mirror Post 09), populated from the verified references file. Include a GitHub code link (`github.com/joechrisnaldy/data-stories/tree/main/loan`).
- [ ] **Step 5: Long-dash scan on the MDX.** Expected clean.
- [ ] **Step 6: Confirm slug equals filename.**

---

### Task 9: Build the site and verify

- [ ] **Step 1: Build.** `cd site && npm run build`. Expected EXIT 0 and the route `/blog/what-the-bank-sees/index.html` generated.
- [ ] **Step 2: Guard the image-optimizer side effect.** After the build, `git restore public/images/blog/` to revert the optimizer's churn on pre-existing images; re-copy the four raw `loan-*.png` charts so only the new images are added. Stage ONLY this post's files (another session may be editing this repo; do NOT `git add -A`).
- [ ] **Step 3: Verify the built HTML** at `dist/client/blog/what-the-bank-sees/index.html`: correct title, FOUR `loan-*.png` refs, section headings, References.

---

### Task 10: Update the series index

**Files:** Modify `Projects/analytics-blog/README.md`

- [ ] **Step 1: Add the Post 10 row**, linking `https://joechrisnaldy.com/blog/what-the-bank-sees` and `loan/`. Use `.com`.
- [ ] **Step 2: Dash-scan the README.**

---

### Task 11: PUBLISH GATE (author-triggered)

Only when Jonathan says go. Publishing pushes two repos.

- [ ] **Step 1: Commit and push the portfolio site** (`site/`, remote `joechrisnaldy-portfolio`, branch `main`), staging only the new MDX, the four `loan-*.png`, and `.published-slugs.json`. Triggers Vercel. **Verify live on `https://joechrisnaldy.com/blog/what-the-bank-sees` (NOT .app), and that each image resolves 200.**
- [ ] **Step 2: Commit and push the analytics-blog repo** (Post 10 folder: `profile_data.py`, `build_analysis.py`, `make_charts.py`, `results.json`, `charts/`, `README.md`, `data/README.md`, `docs/`; NOT `draft/` or `data/Loan.csv` or `data/CSV_Generation.py`) plus the series-index README update. Before committing, run `git add --dry-run` and confirm every README-referenced script is included and no draft/CSV/generator leaks.
- [ ] **Step 3: Update memory** (`analytics-blog-workflow.md` + MEMORY.md index): Post 10 shipped, live URL, thesis, gotchas (dataset ships its own generator = readable rulebook; income dominates over credit; credit acts through interest rate; age gradient baked in; synthetic so no real-bank claims; 4 charts now standard).

---

## Self-review

- **Spec coverage:** what-weighs (Task 1 + chart 1), credit-prices (Task 1 + chart 2), not-about-risk age gradient (Task 1 + chart 3), the unbanked close (Task 1 legibility + chart 4 + Task 3 Findex), synthetic/honesty layer (Tasks 4, 5, 6), verified anchors DTI/ECOA/Findex (Task 3), universal close (Task 5), FOUR charts (Task 2). All present.
- **Placeholder scan:** excerpt/metaDescription/alt/captions filled from the approved draft at Task 8; citations are an explicit verify-first task (Task 3) with named candidate sources and drop-if-unconfirmable instructions; the `findex_unbanked_millions` value is flagged for verification. No orphan TODOs.
- **Consistency:** results.json keys (corr_approval[].nice/corr/feature, importance, credit_rate_corr, credit_rate_scatter, approval_by_age[].band/rate, season, legible, findex_unbanked_millions) defined in build_analysis and consumed by make_charts identically; chart raw filenames (01_what_weighs/02_credit_prices/03_not_risk/04_no_score) map to site filenames (loan-1-what-weighs/-2-credit-prices/-3-not-risk/-4-no-score) identically across Tasks 2, 8, 9; slug `what-the-bank-sees` identical across Tasks 8, 10, 11 and the filename.
- **Review gates:** income-over-credit + age-gradient sanity gate (Task 1 Step 2), citation verify-first with drop-if-unconfirmable (Task 3), adversarial verify (Task 6), author Word review (Task 7), publish gate (Task 11).
