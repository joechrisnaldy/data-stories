"""Post 32's model: weekly output against weekly hours, the cost of two teams, and one week under each overtime rule.

Every input comes from build_analysis.py, which reads it from docs/sources.json (stored, quoted documents); nothing
here holds a figure of its own. docs/provenance-audit.md says where each input is defined.

The output curve (Pencavel 2014, Table 4, column ii): below the knot, output is proportional to hours; past it,
the output of one more hour falls in a straight line, reaching zero at the peak. Output is counted in productive
hours: hours worked at the pace of a week below the knot.

The cost test (one week). Wages are paid for every hour at the straight-time rate, plus the overtime premium on
hours past the overtime threshold for non-exempt staff. Every benefit is treated as a per-person cost, the benefit
cost per hour worked times the hours of a standard week: the release does not say which benefits scale with hours,
and this choice favours the team with fewer, longer-working people. Exempt staff are paid the same at any hours.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Curve:
    knot: float     # weekly hours up to which output is proportional to hours
    peak: float     # weekly hours at which output peaks

    def __post_init__(self) -> None:
        if not 0 < self.knot < self.peak:
            raise ValueError(f"a curve needs 0 < knot < peak, got knot {self.knot} and peak {self.peak}")


@dataclass(frozen=True)
class Team:
    people: int
    hours: float    # weekly hours per person


@dataclass(frozen=True)
class Costs:
    wage: float             # wages and salaries per hour worked (straight time)
    benefits: float         # benefit costs per hour worked
    benefit_hours: float    # the standard week over which per-hour benefits become a per-person cost
    overtime_after: float   # weekly hours past which non-exempt staff are owed overtime pay
    overtime_rate: float    # overtime pay as a multiple of the regular rate


@dataclass(frozen=True)
class UsWeek:
    regular_hours: float
    overtime_hours: float
    pay_in_hourly_wages: float


@dataclass(frozen=True)
class IndonesiaWeek:
    regular_hours: float
    first_overtime_hours: float
    later_overtime_hours: float
    pay_in_hourly_wages: float
    over_day_cap: bool
    hours_over_week_cap: float


def productive_hours(hours: float, curve: Curve) -> float:
    """Weekly output in productive hours for one person working `hours` a week."""
    if hours <= curve.knot:
        return hours
    over = hours - curve.knot
    return curve.knot + over - over ** 2 / (2 * (curve.peak - curve.knot))


def team_productive_hours(team: Team, curve: Curve) -> float:
    return team.people * productive_hours(team.hours, curve)


def nonexempt_week_cost(team: Team, costs: Costs) -> float:
    overtime = max(0.0, team.hours - costs.overtime_after)
    wages = team.hours * costs.wage + overtime * (costs.overtime_rate - 1) * costs.wage
    return team.people * (wages + costs.benefits * costs.benefit_hours)


def exempt_week_cost(team: Team, costs: Costs) -> float:
    return team.people * (costs.wage + costs.benefits) * costs.benefit_hours


def exempt_break_even(long: Team, short: Team, costs: Costs, curve: Curve) -> float:
    """The extra weekly cost per long-hours worker (tired-staff, error and turnover costs the output curve leaves
    out) at which the long-hours team costs as much per productive hour as the short-hours team."""
    target = exempt_week_cost(short, costs) / team_productive_hours(short, curve)
    return (target * team_productive_hours(long, curve) - exempt_week_cost(long, costs)) / long.people


def payback_weeks(hiring_cost: float, weekly_saving: float) -> float:
    if weekly_saving <= 0:
        raise ValueError(f"no payback without a weekly saving, got {weekly_saving}")
    return hiring_cost / weekly_saving


def us_week(hours_per_day: float, days: int, overtime_after: float, overtime_rate: float) -> UsWeek:
    total = hours_per_day * days
    overtime = max(0.0, total - overtime_after)
    return UsWeek(total - overtime, overtime, (total - overtime) + overtime * overtime_rate)


def indonesia_week(hours_per_day: float, days: int, normal_day_hours: float, first_hour_rate: float,
                   later_rate: float, cap_day: float, cap_week: float) -> IndonesiaWeek:
    daily_overtime = max(0.0, hours_per_day - normal_day_hours)
    first = min(1.0, daily_overtime) * days
    later = (daily_overtime - min(1.0, daily_overtime)) * days
    regular = min(hours_per_day, normal_day_hours) * days
    return IndonesiaWeek(regular, first, later, regular + first * first_hour_rate + later * later_rate,
                         daily_overtime > cap_day, max(0.0, daily_overtime * days - cap_week))
