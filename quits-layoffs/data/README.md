# Data

Two kinds of input, kept strictly separate in [`build_analysis.py`](../build_analysis.py).

## 1. The panel (computed here)

**QLmonthly**, monthly quit and layoff transition rates built from Current Population Survey
microdata by **Kathrin Ellieroth** (Colby College) and **Amanda Michaud** (Federal Reserve Bank of
Minneapolis).

- **582 monthly rows, January 1978 to June 2026**, no nulls in either file (but see the October 2025
  note below, which is the one row that cannot be a survey estimate)
- Project site: [qlmonthly.com](https://sites.google.com/qlmonthly.com/home)
- Files: [github.com/qlmonthly/Data](https://github.com/qlmonthly/Data)
- Also published on FRED as release 738, "Quits and Layoffs to Nonemployment Based on the Consumer
  Population Survey (CPS)", series including `EMELPSA`, `EMEQPSA`, `EMSHRNLP`
- Paper: Ellieroth, K., & Michaud, A. (2026). *Quits, layoffs, and labor supply* (Institute Working
  Paper 94). Federal Reserve Bank of Minneapolis. https://doi.org/10.21034/iwp.94

### Download

```bash
curl -sL -o qlmonthly_prime.dta https://raw.githubusercontent.com/qlmonthly/Data/main/qlmonthly_prime.dta
curl -sL -o qlmonthly_all.dta   https://raw.githubusercontent.com/qlmonthly/Data/main/qlmonthly_all.dta
```

The `.dta` files are read directly by `pandas.read_stata`, no extra dependency needed. The files are
gitignored here; the commands above reproduce them.

### Variables

| Column | Meaning |
|---|---|
| `eqall_seats` | Employment-to-non-employment **quits**, % of employment per month, seasonally adjusted |
| `elall_seats` | Employment-to-non-employment **layoffs**, same units |
| `share_layoff_n_seats` | Share of newly **laid-off** workers flowing to **non-participation** rather than unemployment |
| `share_quit_n_seats` | Share of newly **quit** workers flowing to non-participation |

`qlmonthly_prime.dta` is prime age; `qlmonthly_all.dta` is all workers 16+. The authors define prime
age as **25 to 55**, not the more usual 25 to 54 (IWP 94, p. 11: "prime-age population (25-55 years
old)").

### The October 2025 row

BLS did not collect the Current Population Survey for the **October 2025** reference period, because
of a lapse in appropriations, and will not collect it retroactively
([BLS shutdown impact note](https://www.bls.gov/cps/methods/2025-federal-government-shutdown-impact-cps.htm)).
CPS tables show a dash for that month.

This panel nonetheless carries populated October and November 2025 rows (October: `eqall_seats`
0.780001, `elall_seats` 0.954295, `share_layoff_n_seats` 0.356355), and neither the project site nor
the working paper documents how they were produced. November also depends on October microdata,
because these are month-to-month transition rates.

`build_analysis.py` sizes the exposure rather than ignoring it: the only published figure that
touches those rows is the trailing twelve-month quits average, 0.8128% with them and 0.8149% without.
Nothing in the essay turns on the difference.

### Why this is not JOLTS

JOLTS is establishment-based and counts a quit even when the worker walks straight into another job.
This series is household-based and counts only separations that end in **non-employment**, so it can
follow the person. The authors put it as the CPS tracking what happens to people while JOLTS tracks
what happens to a job. JOLTS also starts only in December 2000; this series starts in 1978.

## 2. Verified external constants (not computed here)

Every external figure used in the essay is held as a named constant in `build_analysis.py` with its
source recorded, and each has a primary-source verbatim quote on file in [`../docs/`](../docs/).
Sources are BLS (JOLTS definitions and releases, the Employment Situation, the Monthly Labor Review),
the Federal Reserve Banks of Minneapolis, St. Louis and Richmond, and the Board of Governors.
Nothing is recalled from memory.

## Realism checks that this panel passed

Run [`profile_data.py`](../profile_data.py). Every recession appears with a plausible magnitude, and
COVID is unmistakable: prime-age layoffs reach **10.71% in April 2020**, 8.49 times the 48-year
average, while quits collapse from 1.03% to 0.32%. No generated file behaves like that.

Two figures from the paper also reproduce on these files, which is a useful check that the published
`.dta` is the same data the paper was written from. Table 2's 1978 to 2024 prime-age means (quits
0.85, layoffs 1.27) match to two decimals.

The paper's quits-layoffs correlation of -0.46 does **not** reproduce on the raw monthly series,
which gives -0.30. It only comes close on six-month centred averages (-0.44 on the full file, -0.45
restricted to the paper's 1978 to 2024 window), which is how the paper's figures are built. Because
the two are different specifications and neither rebuild lands exactly on -0.46, the essay quotes
-0.30 as its own computation and attributes -0.46 to the paper, rather than claiming to reproduce it.
Anything that plots the raw series has to quote -0.30.
