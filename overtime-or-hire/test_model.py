"""Tests for model.py, the output curve and the cost test. Run from the post folder: python3 -m unittest test_model"""
import unittest

from model import (Costs, Curve, Team, exempt_break_even, exempt_week_cost, indonesia_week, nonexempt_week_cost,
                   payback_weeks, productive_hours, team_productive_hours, us_week)

CURVE = Curve(knot=49, peak=63)
COSTS = Costs(wage=36.97, benefits=17.03, benefit_hours=40, overtime_after=40, overtime_rate=1.5)
LONG, SHORT = Team(people=2, hours=60), Team(people=3, hours=40)


class CurveTest(unittest.TestCase):
    def test_hours_up_to_the_knot_count_in_full(self):
        for h in (0, 24, 40, 49):
            self.assertAlmostEqual(productive_hours(h, CURVE), h)

    def test_each_hour_past_the_knot_counts_less_until_the_peak(self):
        self.assertAlmostEqual(productive_hours(60, CURVE), 60 - 11 ** 2 / 28)
        self.assertAlmostEqual(productive_hours(63, CURVE), 56)

    def test_output_peaks_at_the_peak(self):
        grid = [h / 10 for h in range(0, 1001)]
        best = max(grid, key=lambda h: productive_hours(h, CURVE))
        self.assertAlmostEqual(best, 63)

    def test_seventy_hours_give_what_fifty_six_give(self):
        self.assertAlmostEqual(productive_hours(70, CURVE), productive_hours(56, CURVE))

    def test_a_curve_must_peak_after_its_knot(self):
        with self.assertRaises(ValueError):
            Curve(knot=49, peak=49)


class TeamTest(unittest.TestCase):
    def test_team_output_is_people_times_each_persons_output(self):
        self.assertAlmostEqual(team_productive_hours(LONG, CURVE), 2 * (60 - 121 / 28))
        self.assertAlmostEqual(team_productive_hours(SHORT, CURVE), 120)


class CostTest(unittest.TestCase):
    def test_short_team_costs_wages_plus_benefits_per_productive_hour(self):
        per_hour = nonexempt_week_cost(SHORT, COSTS) / team_productive_hours(SHORT, CURVE)
        self.assertAlmostEqual(per_hour, 36.97 + 17.03)

    def test_long_team_pays_the_premium_on_hours_past_forty(self):
        expected = 2 * (60 * 36.97 + 20 * 0.5 * 36.97 + 40 * 17.03)
        self.assertAlmostEqual(nonexempt_week_cost(LONG, COSTS), expected)

    def test_exempt_pay_does_not_change_with_hours(self):
        self.assertAlmostEqual(exempt_week_cost(LONG, COSTS), 2 * 40 * (36.97 + 17.03))
        self.assertAlmostEqual(exempt_week_cost(Team(people=2, hours=40), COSTS), exempt_week_cost(LONG, COSTS))

    def test_exempt_break_even_equalises_cost_per_productive_hour(self):
        extra = exempt_break_even(LONG, SHORT, COSTS, CURVE)
        long_per_hour = (exempt_week_cost(LONG, COSTS) + LONG.people * extra) / team_productive_hours(LONG, CURVE)
        short_per_hour = exempt_week_cost(SHORT, COSTS) / team_productive_hours(SHORT, CURVE)
        self.assertAlmostEqual(long_per_hour, short_per_hour)
        self.assertGreater(extra, 0)

    def test_payback_divides_the_hiring_cost_by_the_weekly_saving(self):
        self.assertAlmostEqual(payback_weeks(1000, 250), 4)

    def test_no_payback_without_a_saving(self):
        with self.assertRaises(ValueError):
            payback_weeks(1000, 0)


class WeekRulesTest(unittest.TestCase):
    def test_us_week_of_five_twelve_hour_days(self):
        week = us_week(hours_per_day=12, days=5, overtime_after=40, overtime_rate=1.5)
        self.assertEqual((week.regular_hours, week.overtime_hours), (40, 20))
        self.assertAlmostEqual(week.pay_in_hourly_wages, 40 + 20 * 1.5)

    def test_indonesian_week_of_five_twelve_hour_days(self):
        week = indonesia_week(hours_per_day=12, days=5, normal_day_hours=8, first_hour_rate=1.5, later_rate=2,
                              cap_day=4, cap_week=18)
        self.assertEqual((week.regular_hours, week.first_overtime_hours, week.later_overtime_hours), (40, 5, 15))
        self.assertAlmostEqual(week.pay_in_hourly_wages, 40 + 5 * 1.5 + 15 * 2)
        self.assertFalse(week.over_day_cap)
        self.assertEqual(week.hours_over_week_cap, 2)

    def test_indonesian_week_without_overtime(self):
        week = indonesia_week(hours_per_day=7, days=5, normal_day_hours=8, first_hour_rate=1.5, later_rate=2,
                              cap_day=4, cap_week=18)
        self.assertEqual((week.regular_hours, week.first_overtime_hours, week.later_overtime_hours), (35, 0, 0))
        self.assertAlmostEqual(week.pay_in_hourly_wages, 35)
        self.assertFalse(week.over_day_cap)
        self.assertEqual(week.hours_over_week_cap, 0)

    def test_indonesian_week_over_both_caps(self):
        week = indonesia_week(hours_per_day=13, days=5, normal_day_hours=8, first_hour_rate=1.5, later_rate=2,
                              cap_day=4, cap_week=18)
        self.assertEqual((week.first_overtime_hours, week.later_overtime_hours), (5, 20))
        self.assertTrue(week.over_day_cap)
        self.assertEqual(week.hours_over_week_cap, 7)


if __name__ == "__main__":
    unittest.main()
