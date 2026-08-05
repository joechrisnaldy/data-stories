# Data

Two sources, both the US Department of Education. Nothing is joined from anywhere else, so there is
no external series to reconcile. Files are not redistributed here; everything below reproduces from
scratch in a few minutes.

## The files

| File | What it is | Covers |
|---|---|---|
| `PortfoliobyLoanStatus.xls` | Direct Loan dollars and recipients by status, quarterly | FY2013 Q3 to FY2026 Q2 |
| `DLPortfoliobyRepaymentPlan.xls` | Direct Loan dollars and recipients by repayment plan, quarterly | FY2013 Q3 to FY2026 Q2 |
| `PortfolioSummary.xls` | Headline portfolio totals | same |
| `Most-Recent-Cohorts-Field-of-Study.csv` | One row per programme per institution per credential: median debt, median earnings | pooled recent cohorts |
| `CollegeScorecardDataDictionary.xlsx` | Variable labels. Read this before using any variable | current |
| `FieldOfStudyDataDocumentation.pdf` | Method notes, including the standard-plan assumption | June 2024 |

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
L=https://studentaid.gov/sites/default/files/fsawg/datacenter/library
for f in PortfolioSummary PortfoliobyLoanStatus DLPortfoliobyRepaymentPlan; do
  curl -sL -A "$UA" -o "$f.xls" "$L/$f.xls"
done

S=https://ed-public-download.scorecard.network/downloads
curl -sL -o fos.zip "$S/Most-Recent-Cohorts-Field-of-Study_06102026.zip" && unzip -oq fos.zip
curl -sL -A "$UA" -O https://collegescorecard.ed.gov/assets/CollegeScorecardDataDictionary.xlsx
curl -sL -A "$UA" -O https://collegescorecard.ed.gov/assets/FieldOfStudyDataDocumentation.pdf
```

Note that `studentaid.gov/data-center/student` itself is a JavaScript shell and returns no content
to `curl`. The `.xls` files sit on the `library` path above and download fine. A guessable name is
not a guarantee: `PortfoliobyRepaymentPlan.xls` 404s, the real name is `DLPortfoliobyRepaymentPlan.xls`.

## TRAP 1: recipient counts are loan-level

Both FSA workbooks carry the same warning: "Recipient counts are based at the loan level. As a
result, recipients may be counted multiple times across varying loan statuses."

**Handling: every share OF THE LOAN PORTFOLIO is a share of dollars outstanding.** The recipient
columns are read but never summed across categories. The post also quotes shares of programmes, of
graduates and of file rows; those are labelled where they occur, because "every percentage here is a
share of dollars" would be false.

## TRAP 2: the two FSA tables have different denominators

The workbook's Definitions tab states: "Repayment Plan summary includes Direct Loan or Federally
Managed borrowers in Repayment, Deferment and Forbearance categories and excludes borrowers in
Default, In-School, and Grace." Quote it exactly, serial comma included; an earlier version of this
file dropped that comma and shortened the opening, inside quotation marks, in a note whose whole job
is to teach the next reader to quote sources exactly. The loan-status table has no such exclusion.

| Table | 2026 Q2 total |
|---|---|
| Portfolio by loan status | $1,563B |
| Portfolio by repayment plan | $1,241B |

The $322B gap is close to, but not exactly, those three categories: at this quarter In-School
($116.8B) plus Grace ($22.1B) plus Default ($175.3B) is $314B. Do not describe the gap as exactly
the exclusions. **The two sets of percentages are reported separately and never combined into one
figure.**

A third denominator hides behind both: these are DIRECT LOANS only, $1,562.9B of a $1,723.9B federal
total that also holds $158.3B of FFEL and $2.7B of Perkins (`PortfolioSummary.xls`). Neither FSA
table used here is the whole of federal student debt.

## TRAP 3: the pandemic suspension makes any single recent quarter a policy artefact

Active repayment as a share of all dollars:

| Quarter | Repayment | Forbearance |
|---|---|---|
| 2019 Q4 (FY, ends 30 Sep 2019) | 55.2% | 9.9% |
| 2020 Q1 (FY, ends 31 Dec 2019, the last quarter wholly pre-suspension) | 58.2% | 9.9% |
| 2023 Q3 | **0.7%** | 76.4% |
| 2026 Q2 | 39.2% | 30.4% |

The 2020 to 2023 block is the CARES Act payment suspension, not borrower behaviour. **Handling: the
full series is always plotted, structural claims quote the pre-pandemic quarter, and the
load-bearing claim uses the repayment-plan mix.**

**Any average over the pause has to name its window.** The pause ran 13 March 2020 to 31 August
2023, and two fiscal quarter-ends straddle its edges. Over the thirteen snapshots lying wholly
inside it, FY2020 Q3 to FY2023 Q3, forbearance averaged 72.2%, its lowest quarter being 67.5%. Add
the quarter the suspension began in, when the pause was eighteen days old and forbearance still
stood at 12.7% against a 9.9% pre-pandemic level, and the same average is 67.9%. `build_analysis.py`
emits both, under
`traps.pause.forbearance_in_pause`, so the window is a recorded choice rather than a silent one.

**The post-pandemic forbearance rise is a separate episode, and it has already turned.** Forbearance
ran 3.9%, 16.3%, 6.5%, 12.1%, 33.8% through 2024, peaked at 38.0% in FY2025 Q3 (ends 30 June 2025),
and has fallen in each of the three quarters since to 30.4%. Do not call it a climb "through 2024
and 2025" and do not quote the current 30.4% as its top; that repeats, against the second episode,
exactly the endpoints-hide-the-path error this file exists to warn about.

**But equal endpoints are not stability.** The standard-plan share reads 21.9% in FY2020 Q1 and
21.9% now, which is a coincidence of the two endpoints, not evidence the suspension left it alone:
in between it fell to 17.5% and spiked to 28.3%. The cause is the file's own "Other" column, loans
"not currently listed on a repayment plan", which went 3.2% before the suspension to 21.9% at its
peak and 0.8% now, deflating every named share while it was large. Measured against dollars on a
NAMED plan the artefact mostly clears: 22.6% before against 22.1% now, moving between 21.1% and
29.0% over that same stretch. State that window. Over the full published series the named basis runs
21.1% to 44.3%, and 16 of the 52 quarters sit above 29.0%, so the pair 21.1 to 29.0 quoted bare
mixes a global minimum with a windowed maximum. Quote the named basis, name the window, and never
infer a path from two endpoints.

**And the reassignment was not proportional.** When the residual bucket emptied in FY2023 Q4, the
dollars went overwhelmingly to Level 10-yr-or-less and SAVE. Three of the nine named plans fell
outright that quarter on the raw basis, and seven of nine fell the quarter after. "Every named share
jumped" is a tempting summary and it is false.

**And mind the fiscal calendar.** The fiscal year begins 1 October, so Q4 ends 30 September. FY2019
Q4 is a September 2019 snapshot, five months before the suspension began on 13 March 2020, not the
quarter preceding it. An earlier version of this analysis used it as the pre-pandemic baseline and
understated the standard-plan share by half a point.

## TRAP 4: `_ANY_` and `_EVAL_` are not undergraduate and graduate

`DEBT_ALL_STGP_ANY_MDN` is empty for every graduate credential and `DEBT_ALL_STGP_EVAL_MDN` is not,
which invites the conclusion that one is undergraduate and the other covers graduate degrees. The
data dictionary says otherwise:

| Variable | Label |
|---|---|
| `DEBT_ALL_STGP_ANY_MDN` | Median Stafford and Grad PLUS loan debt disbursed **at all institutions** |
| `DEBT_ALL_STGP_EVAL_MDN` | Median Stafford and Grad PLUS loan debt disbursed **at this institution** |

The graduate gap is a coverage fact, not a definitional one. Using `_ANY_` drops the master's rows,
of which there are 38,621 in the file, though only 7,888 carry `_EVAL_` debt and fewer still carry
usable earnings, so the real loss is smaller than the row count suggests. The post uses `_ANY_`
because it follows the student rather than the school, and states that its coverage is undergraduate
only.

Both variables count Stafford and Grad PLUS DISBURSEMENTS. They are not everything a borrower owes:
Parent PLUS is a separate column, private loans are absent, and interest accrued after graduation is
not in either.

**The `_EVAL_` check agrees by cancellation, not by robustness.** It gives 0.577 overall against the
0.591 headline, which looks like confirmation. On the same undergraduate rows it gives 0.541, and
the graduate rows it adds pull the figure back up. Report it as a different measure landing nearby,
not as a check that passed.

**Read the label. Never infer a variable's meaning from its name or its missingness pattern.**

## TRAP 5: earnings are conditional on having a job

`EARN_MDN_HI_1YR` is the "median earnings of graduates **working and not enrolled** 1 year after
completing highest credential". Completers with no earnings that year are outside the denominator:
5.9% of non-enrolled graduates in the 31,941-programme sample. Note the denominator: WNE plus NWNE
is graduates NOT ENROLLED, so anyone who went straight on to further study is in neither. Every
payback figure in this post is therefore optimistic, and the post says so rather than hedging.

## A sixth thing, found by looking at the chart

`CONTROL` is documented in the dictionary as numeric codes 1 to 4, but the field-of-study CSV ships
the labels as text: `Public`, `Private, nonprofit`, `Private, for-profit`, `Foreign`. Mapping the
documented codes returns an empty breakout, silently. Read the column, not only the dictionary.

## Other things worth knowing

- **Federal fiscal quarters are not calendar quarters.** The fiscal year begins 1 October, so Q1
  ends 31 December of the *previous* calendar year, Q2 ends 31 March, Q3 30 June, Q4 30 September.
  Plotting the fiscal year as a calendar year shifts the pandemic suspension by a quarter.
- **The federal borrowing limits are visible in the data.** Median debt piles up at $27,000, which
  is a dependent undergraduate's four annual maximums of $5,500, $6,500, $7,500 and $7,500 added
  together, and at $31,000, the dependent aggregate ceiling (34 C.F.R. § 685.203). $27,000 is the
  single most common value, at 3,098 programmes exactly, 9.7% of the sample. Count exact values, not
  `round(-2)` buckets, which inflate it to 3,271. Programmes above $31,000 are not an error: an
  independent undergraduate may borrow up to $57,500 under the same section, and the figure is a
  median across a programme's borrowers rather than one person's balance.
- **Only 14% of field-of-study rows carry both debt and earnings**, 31,941 of 227,980, covering
  4,500 institutions and 314 fields. The rest are unreported, generally for small cohorts. This is
  not a census of American degrees.
- **Debt and earnings correlate only 0.25** (0.28 on ranks), so the price of a degree says little
  about what it pays.

## What the vet found

Nothing wrong with either source. Both are official statistical output with documented methods and
free downloads, and the post says so. Every trap above is packaging, coverage or definition, not
error. What the post argues is that the payback figure carries an assumption the publisher documents
plainly and that almost nobody passes along.
