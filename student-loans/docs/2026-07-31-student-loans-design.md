# Post 19 design: The Payback Period Assumes You Are Paying It Back

| | |
|---|---|
| Slug | `the-payback-period-assumes-you-are-paying-it-back` |
| Folder | `Projects/analytics-blog/student-loans/` |
| Angle | The payback period is a fiction |
| Hook | Run the sum honestly, let it reassure, then break it |
| Stance | Right sum, wrong question |
| Policy scope | Mechanism only, with the tradeoff named once, neutrally |
| Framing | US federal data only. No Indonesia, no personal angle. Widen at the close to any loan written against income you do not have yet |
| Close | A price is not a deadline |
| Sources | Federal Student Aid data center (via Data Is Plural, 2020-12-02) and College Scorecard field of study |

## The argument

Debt divided by earnings is a real, correct, useful number. It tells you the **price** of a degree
in years of gross salary, and by that measure the median American programme is cheap: about seven
months. People read it as a **deadline**, as in how long until this is over. That is a different
question, and the repayment data answers it differently.

The break is not that borrowers are irresponsible. It is that the ten-year schedule the calculation
silently assumes is a minority arrangement and has been for a decade.

## The two sources, and why both are needed

| | Federal Student Aid data center | College Scorecard, field of study |
|---|---|---|
| Unit | Direct Loan portfolio, quarterly, by status and by repayment plan | One row per programme per institution per credential |
| Covers | FY2013 Q3 to FY2026 Q2 | Most recent pooled cohorts |
| Gives | What borrowers actually do | What the degree cost and what it earned |
| Missing | Any earnings figure at all | Any repayment behaviour at all |

Neither source can make the argument alone. That is the point of the post and it is stated in the
piece rather than hidden.

## Traps found in the vet, all handled

1. **Recipient counts are loan-level.** The file's own note: "recipients may be counted multiple
   times across varying loan statuses." Recipient counts therefore cannot be summed across statuses.
   **Every share in this post is a share of dollars outstanding.**
2. **The pandemic pause makes any single recent quarter a policy artifact.** Repayment share of
   dollars ran 56.9% in 2019 Q3, fell to 0.7% in 2023 Q3 under the CARES suspension, and is 39.2% in
   2026 Q2. Handling: plot the whole series, quote the pre-pandemic baseline for any structural
   claim, and treat the suspension as a second and separate argument rather than as evidence of a
   trend.
3. **The repayment-plan table has a different denominator from the loan-status table.** Its notes
   say it covers borrowers "in Repayment, Deferment and Forbearance" and **excludes** default,
   in-school and grace. The two tables must never be mixed into one percentage.
4. **`DEBT_ALL_STGP_ANY_MDN` and `DEBT_ALL_STGP_EVAL_MDN` are not undergraduate versus graduate.**
   The dictionary labels them "debt disbursed at all institutions" and "debt disbursed at this
   institution". `_ANY_` happens to be empty for every graduate credential, which is a coverage fact,
   not a definitional one. Using `_ANY_` silently drops all 38,621 master's rows.
5. **Scorecard earnings are conditional.** The label is "median earnings of graduates **working and
   not enrolled** 1 year after completing highest credential". Anyone without a job is out of the
   denominator, which makes the price look better than it is. Stated in the post, not used quietly.
6. **Only 14% of Scorecard rows carry both debt and earnings** (31,941 of 227,980, across 4,500
   institutions and 314 CIP codes). Sample composition is reported rather than described as "all
   programmes".

## Numbers already verified in the vet

- Median programme debt-to-earnings: **0.59 years of gross salary**. 25th percentile 0.42, 75th
  0.81, 95th 1.18.
- Direct Loan portfolio at 2026 Q2: **$1,563.0B**. In active repayment 39.2%, forbearance 30.4%,
  default 11.2%, deferment 9.9%, in-school 7.5%, grace 1.4%.
- Pre-pandemic 2019 Q3: repayment 56.9% of all dollars, **65.1% of post-school dollars**, meaning
  roughly a third were already not in active repayment in a normal year.
- Standard level plan of ten years or less, as a share of dollars: **38.7% (2013 Q3) to 21.4%
  (2019 Q4) to 21.9% (2026 Q2)**. The pause barely touched this, so the decline is structural.
- Income-driven plans over the same span: **20.0% to 50.1% to 61.5%**.

## Chart spine

**Chart 1, the sum.** Distribution of programme-level debt-to-earnings across the 31,941 programmes
with both figures, median marked at 0.59 years. This is the number the reader is allowed to believe.

**Chart 2, the break.** Direct Loan dollars by repayment plan, FY2013 to FY2026: standard ten-year
or less against income-driven against everything else. The calculator assumes the first band; it is
about one dollar in five and falling. Pause-robust, so this carries the structural claim.

**Chart 3, the second proof.** Direct Loan dollars by status over the same span, with the CARES
suspension visible. Two readings: even in 2019 a third of post-school dollars were not in active
repayment, and a schedule that can be switched off for three years was never binding.

**Chart 4, the close.** Median debt against median 1-year earnings for every one of the 31,941
programmes, with the diagonal where debt equals one full year of gross earnings.

To stop this being a restatement of chart 1, it has to do work chart 1 cannot. Chart 1 is the
distribution of a ratio; chart 4 is the joint distribution behind it, and it should show three
things at once:
- that debt and earnings largely travel together, which is *why* the ratio looks so stable and
  reassuring in chart 1;
- the programmes above the diagonal, where the debt exceeds a full year of gross earnings, named
  where they are interesting;
- colour by credential level, so the chart also carries the where-is-it-worst information rather
  than needing a fifth chart for it.

If, once drawn, it still reads as chart 1 with more ink, say so and swap it for the credential and
control breakout instead. A chart that repeats another chart is a wasted quarter of the post.

## Deliberately out of scope

Mass cancellation, the courts, and any administration. Income-driven repayment and its forgiveness
clause are in because they are the mechanism, and the tradeoff gets named once: lower payments now
against a longer or forgiven balance later. No side taken.

## What this post cannot say

It cannot say whether the degree caused the earnings. Scorecard is observational, has no
counterfactual, and covers only people who completed. "Is it worth it" is answered as a price
question and explicitly not as a causal one.
