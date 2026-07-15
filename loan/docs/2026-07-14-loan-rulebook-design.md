# Post 10 design: the bank's leaked rulebook (what the eyes of the bank weigh)

**Date:** 2026-07-14
**Series:** data-stories (Post 10)
**Folder:** `Projects/analytics-blog/loan/`
**Dataset:** Kaggle `lorenzozoppelletto/financial-risk-for-loan-approval` (synthetic; 20,000 loan applicants, 36 columns, ships its own generator `CSV Generation.py`, CC0)

## The idea

You fill in thirty boxes about your life and a lender compresses you into one number that says
yes or no. This synthetic dataset accidentally ships the generator that built its labels, so
for once we can READ the rulebook: exactly what the "eyes of the bank" weigh, what they ignore,
and (by construction) who they can never see. It is a lab specimen of an automated credit score.

## Thesis (chosen)

> An automated loan decision looks like objective math, but it is a stack of human choices about
> what counts. Read this bank's rulebook and income and debt decide far more than the credit
> score you fret over; some factors (age, the season you apply) are not about risk at all; and
> the whole apparatus can only judge people it can already see.

Neutral-explanatory reveal: a "risk score" is a bundle of decisions. Report the choices plainly;
where real scorecards make similar ones, note that is the concern. No exposé overclaim from a
single synthetic dataset.

## Brainstorm decisions (locked)

- **Angle:** the bank's leaked rulebook (what it weighs, ignores, cannot see).
- **Hook:** a person becomes a number, you fill in thirty boxes and become one yes/no number;
  this dataset lets us read how it is built.
- **Stance:** a score is a stack of choices (neutral-explanatory; not an exposé).
- **Reach:** toy as lab specimen, analyze the rulebook thoroughly; reach into real lending only
  with verified anchors; keep the synthetic caveat loud.
- **Close:** the unbanked, universal, ~1.4 billion adults worldwide invisible to any rulebook
  (World Bank Findex). No Indonesia focus this time.

## What the data shows (verified in profiling; 20,000 rows, approval rate 23.9%)

- **The generator IS the rulebook.** `CSV Generation.py` computes `LoanApproved` from a
  transparent weighted scorecard (income, DTI, interest rate, loan amount, credit score,
  bankruptcy, defaults, employment, home ownership, payment history, credit-history length,
  net worth, age, experience, education, application month, plus random noise) and computes a
  separate `RiskScore` from correctly-signed risk buckets. The two targets are built by
  different logic and only partly agree.
- **Income dominates approval, not credit score.** Correlation with LoanApproved: AnnualIncome
  +0.60, TotalDebtToIncomeRatio -0.41, InterestRate -0.30, LoanAmount -0.24, NetWorth +0.19,
  Age +0.14, CreditScore only +0.14. Permutation importance (HistGB, in-sample acc 0.98): top
  are TotalDebtToIncomeRatio (0.145), InterestRate (0.114), MonthlyIncome (0.086); CreditScore
  is 6th (0.025).
- **Credit prices you; it does not directly judge you.** In the generator, the interest rate is
  mostly a function of credit score (`BaseInterestRate = 0.03 + (850-CreditScore)/2000 + ...`),
  and it is the interest rate that carries weight in the decision. So credit acts mostly
  INDIRECTLY, through the price it sets. (Also: `corr(CreditScore, RiskScore) = -0.24`, the
  correct direction, higher credit = lower risk.)
- **Baked-in factors that are not about risk.** Approval rate climbs monotonically with age:
  11.6% (under 25) to 32% (65+); the code adds `abs(Age-40)/100` plus an experience term.
  Education and application season (lower approval in spring/summer) are also in the rule. These
  are choices dressed as objective risk.
- **An unrealistic credit world.** Credit scores cluster low by construction (only 6 of 20,000
  above 700, none above 750), so this synthetic bank almost never sees a high-credit applicant.
  (Use as a caveat, not a headline.)
- **Everyone here is already legible.** Every applicant has income, accounts, and a credit
  history. The unbanked do not appear and cannot; the rulebook can only judge the already-seen.

## Analytical backbone

Reused venv `sberbank-housing/.venv` (pandas, numpy, scikit-learn, matplotlib).

1. Factor influence on approval: correlations + permutation importance from a gradient-boosting
   classifier (report both; note importance can route through derived features like InterestRate).
2. Credit -> interest rate -> decision: correlation of CreditScore with InterestRate (tight,
   mechanical), and CreditScore's small direct correlation with approval.
3. Approval rate by age band (and by education / season as secondary), the not-about-risk factors.
4. Everyone-is-legible note (share with accounts/credit history = 100% by construction).
5. External Findex figure for chart 4 (verified in citations).
6. Write `results.json`.

## Charts (4, series palette)

1. **`01_what_weighs.png`** — factor influence on approval (ranked): income, debt-to-income, and
   the loan's interest rate on top; credit score small. The "it is not your credit score" reveal.
2. **`02_credit_prices.png`** — credit score vs the interest rate it sets (tight negative,
   near-mechanical), annotated that the decision leans on the price, so credit acts through the
   rate rather than judging you directly.
3. **`03_not_risk.png`** — approval rate by age band (11.6% -> 32%), the clearest baked-in
   non-risk factor; caption notes education and season are in the rule too. Choices dressed as risk.
4. **`04_no_score.png`** — external World Bank Findex: about 1.4 billion adults are unbanked and
   invisible to any credit rulebook. Clearly separated from the toy data; the closing chart.

## Section spine (~1,400-1,700 words, no long dashes)

1. **Open, a person becomes a number.** Thirty boxes about your life, compressed to one yes/no.
   And this dataset lets us read the formula behind the number.
2. **The rulebook, and what actually moves it (chart 1).** Income and debt-to-income dominate;
   the credit score you guard is a minor, indirect lever.
3. **Credit prices you, it does not judge you (chart 2).** Your credit score mostly sets your
   interest rate; the rate is what the decision weighs.
4. **The factors that are not about risk (chart 3).** Age, education, the season you apply. A
   "risk score" is a stack of choices, and here you can read them. Note this is a synthetic
   rulebook; where real scorecards use factors like age, fair-lending law restricts it.
5. **The honesty layer.** It is synthetic, the relationships are designed, that is exactly why it
   is useful: we are reading a designed rulebook, not discovering a law of banking. Real
   underwriting really does hinge on income and debt-to-income (verified anchor).
6. **Who the rulebook can not see (chart 4).** The unbanked, ~1.4 billion adults, invisible to
   any scorecard. A score is a stack of choices and also a fence: you must be legible to be judged.
7. **Close, universal.** You are being scored right now by rulebooks you can not read, built from
   someone's choices; the people with no score at all are the ones it should worry us most about.
   Analysis, not financial advice.
8. **Method notes + References.**

## Citations to verify (pin in the plan; verified-or-omit)

- The Kaggle dataset: Zoppelletto, L. (2024). *Financial risk for loan approval* [Data set]. Kaggle.
  Note it is synthetic and ships its own generator script.
- Real underwriting hinges on income and debt-to-income: a primary source on the debt-to-income
  ratio in lending / ability-to-repay (e.g., US CFPB). VERIFY exact source and wording.
- Age is a protected characteristic in credit decisions: the US Equal Credit Opportunity Act
  (ECOA) prohibits credit discrimination on the basis of age (with narrow exceptions). VERIFY.
- The unbanked count: World Bank Global Findex 2021, "about 1.4 billion adults remain unbanked".
  VERIFY exact figure, year, and wording.

## Guardrails

- No long dashes; APA 7 references for every external fact; verified or omit.
- Descriptive only; this is a synthetic rulebook, not evidence about any real bank; do not claim
  real lenders discriminate, only that this rulebook makes these choices and that where real
  scorecards do, law and fairness apply.
- Not financial advice.
- Keep the synthetic caveat prominent and early; distinguish generator-rule facts from data
  correlations.

## Title (CHOSEN)

**"What the Bank Sees When It Looks at You"**

Other candidates considered: "A Loan Is a Number, and the Number Is a Stack of Choices"; "Your
Credit Score Prices You. It Doesn't Judge You."; "The People With No Score".

## Verification (for the plan)

Data sanity (income vs credit importance, the age gradient, credit-to-rate correlation),
citation checks (DTI in underwriting, ECOA age, Findex 1.4 billion), long-dash scan, slug match,
Astro build.
