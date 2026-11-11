"""The house chase of design R2 to R7 and R9 (docs/2026-11-09-genz-house-chase-design.md), as pure functions.

No file access here: build_analysis.py reads the frozen data through profile_data.py and passes plain mappings in.
Checked by test_chase.py.
"""
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

Bracket = tuple[int, int, str]          # (first age, last age, label)


@dataclass(frozen=True)
class ChaseResult:
    start: int                     # the year the saver turned 25 (R1)
    finished: bool                 # the balance reached the target by the last year (R6)
    catch_year: int | None         # the first year it did, or None
    years: int                     # years of saving to the catch year, or so far when unfinished (R6)
    share_reached: float           # balance over target at the catch year, or at the last year (R6)
    progress: tuple[float, ...]    # balance over target after 1, 2, ... years, through the last year (R7)


def bracket_of(age: int, brackets: Sequence[Bracket]) -> str:
    """R2: the income bracket that holds the saver's age."""
    for first, last, label in brackets:
        if first <= age <= last:
            return label
    raise SystemExit(f"no income bracket for age {age}")


def contributions(start: int, last: int, share: float, income: Mapping[str, Mapping[int, float]],
                  brackets: Sequence[Bracket], extra: Mapping[str, Mapping[int, float]] | None = None) -> dict[int, float]:
    """R2, R3, R9: each year's saving, share x the median income of the saver's bracket, plus the bracket's extra."""
    out = {}
    for t in range(start, last + 1):
        label = bracket_of(25 + t - start, brackets)
        try:
            add = extra[label][t] if extra is not None else 0.0
            out[t] = share * income[label][t] + add
        except KeyError as e:
            raise SystemExit(f"no {label} value for {t} ({e})") from e
    return out


def run_chase(start: int, last: int, contribution: Mapping[int, float], target: Mapping[int, float],
              rate: Mapping[int, float]) -> ChaseResult:
    """R4, R6, R7: B(t) = B(t-1) x (1 + r(t)) + c(t) x (1 + r(t)/2), from nothing, until B(t) >= T(t)."""
    balance, catch, progress = 0.0, None, []
    for t in range(start, last + 1):
        try:
            r, c, goal = rate[t], contribution[t], target[t]
        except KeyError as e:
            raise SystemExit(f"chase from {start}: no input for {t} ({e})") from e
        balance = balance * (1 + r) + c * (1 + r / 2)
        progress.append(balance / goal)
        if catch is None and balance >= goal:
            catch = t
    years = (catch if catch is not None else last) - start + 1
    return ChaseResult(start, catch is not None, catch, years, progress[years - 1], tuple(progress))
