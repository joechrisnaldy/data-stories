# Verified references: "What the Bank Sees When It Looks at You"

**Verified:** 2026-07-14 (access date for all web sources). Rule: verified or omit. Every external
fact below was checked against a primary or authoritative source. Anything not confirmable was
dropped or softened.

---

## 1. The dataset (synthetic, self-documenting)

**Claim supported:** The analysis runs on a synthetic dataset of 20,000 loan applicants that also
ships the generator script encoding its own approval and risk rules.

**Verification:** Kaggle dataset metadata (retrieved via API 2026-07-14). Creator: LORENZO
ZOPPELLETTO. Last updated: 2024-09-07. License: CC0 (public domain). Description opens: "Synthetic
Dataset for Risk Assessment and Loan Approval Modeling ... This synthetic dataset comprises 20,000
records." The generator script `CSV_Generation.py` is present in the dataset's own files (downloaded
and read directly), which is how we can read the rulebook. **Hedge: the generator is observed in the
dataset files; treat every rule as this synthetic dataset's design, not evidence about any real bank.**

**APA 7:**
Zoppelletto, L. (2024). *Financial risk for loan approval* [Data set]. Kaggle. https://www.kaggle.com/datasets/lorenzozoppelletto/financial-risk-for-loan-approval

---

## 2. Debt-to-income ratio in real underwriting

**Claim supported:** Real lenders use the debt-to-income ratio as a core measure of ability to repay
(the essay's honesty-layer anchor that this synthetic emphasis on income and debt mirrors reality).

**Verification:** CFPB, "What is a debt-to-income ratio?" Exact wording: "This number is one way
lenders measure your ability to manage the monthly payments to repay the money you plan to borrow."
The page also notes "Different loan products and lenders will have different DTI limits."

**APA 7:**
Consumer Financial Protection Bureau. (n.d.). *What is a debt-to-income ratio?* Retrieved July 14, 2026, from https://www.consumerfinance.gov/ask-cfpb/what-is-a-debt-to-income-ratio-en-1791/

---

## 3. Age is a protected basis in real credit decisions (ECOA)

**Claim supported:** In real lending, U.S. fair-lending law restricts using age; the Equal Credit
Opportunity Act lists age among prohibited bases of discrimination.

**Verification:** CFPB explainer on the ECOA lists the protected bases, including "Age (as long as
the applicant is old enough to enter into a contract)." Corroborated by the U.S. Department of
Justice and the FTC (ECOA, 15 U.S.C. 1691; age added by 1976 amendment). **Hedge: the ECOA governs
REAL lenders. Our dataset is synthetic; its age preference is illustrative of what a rulebook can
encode, NOT evidence that any real bank discriminates. Frame the ECOA as the contrast, not the verdict.**

**APA 7:**
Consumer Financial Protection Bureau. (n.d.). *What you need to know about the Equal Credit
Opportunity Act and how it can help you: Why it was passed and what it is.* Retrieved July 14, 2026,
from https://www.consumerfinance.gov/about-us/blog/what-you-need-know-about-equal-credit-opportunity-act-and-how-it-can-help-you-why-it-was-passed-and-what-it/

---

## 4. The unbanked count (the close)

**Claim supported:** About 1.3 billion adults worldwide have no financial account and are invisible
to any credit rulebook.

**Verification:** World Bank Global Findex 2025. Press release (2025-07-16): "1.3 billion adults
still lack access to financial services," and "Nearly 80% of adults worldwide now have a financial
account, up from 50% in 2011." (Note: this supersedes the widely cited 1.4 billion figure from
Global Findex 2021; the essay and chart 4 use the current 2025 figure.)

**APA 7:**
World Bank. (2025, July 16). *Mobile-phone technology powers saving surge in developing economies*
[Press release]. https://www.worldbank.org/en/news/press-release/2025/07/16/mobile-phone-technology-powers-saving-surge-in-developing-economies

World Bank. (2025). *The Global Findex Database 2025.* https://www.worldbank.org/en/publication/globalfindex

---

## Dropped / not used

- The "1.4 billion / Global Findex 2021" figure: superseded by the verified 2025 figure of ~1.3
  billion; not used.
- No claim is made that any real lender weights age, education, or application season the way this
  synthetic rulebook does. Those are facts about the generator only.
