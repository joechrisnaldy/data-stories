"""Unit checks for chase.py, the house chase of design R2 to R7 and R9, on small made-up inputs.

Run from the post folder: python3 -m unittest test_chase
"""
import unittest

import chase as ch

BRACKETS = ((25, 34, "25 to 34"), (35, 44, "35 to 44"), (45, 54, "45 to 54"))


class Recurrence(unittest.TestCase):
    def test_contribution_mid_year_earns_half_the_rate(self) -> None:
        # R4: B(t) = B(t-1) x (1 + r) + c x (1 + r/2); 10 a year at 10%: 10.5, then 10.5 x 1.1 + 10.5 = 22.05
        res = ch.run_chase(2000, 2001, {2000: 10.0, 2001: 10.0}, {2000: 100.0, 2001: 100.0}, {2000: 0.10, 2001: 0.10})
        self.assertAlmostEqual(res.progress[0] * 100.0, 10.5)
        self.assertAlmostEqual(res.progress[1] * 100.0, 22.05)

    def test_no_interest_is_a_plain_sum(self) -> None:
        res = ch.run_chase(2000, 2002, dict.fromkeys(range(2000, 2003), 5.0), dict.fromkeys(range(2000, 2003), 100.0),
                           dict.fromkeys(range(2000, 2003), 0.0))
        self.assertEqual([round(p * 100, 9) for p in res.progress], [5.0, 10.0, 15.0])


class StoppingRule(unittest.TestCase):
    def test_ends_in_the_first_year_the_balance_reaches_a_moving_target(self) -> None:
        # R6: balances 10, 20, 30 against targets 12, 18, 25: reached in the second year
        res = ch.run_chase(2000, 2002, dict.fromkeys(range(2000, 2003), 10.0), {2000: 12.0, 2001: 18.0, 2002: 25.0},
                           dict.fromkeys(range(2000, 2003), 0.0))
        self.assertTrue(res.finished)
        self.assertEqual((res.catch_year, res.years), (2001, 2))
        self.assertAlmostEqual(res.share_reached, 20.0 / 18.0)

    def test_reaching_the_target_exactly_counts(self) -> None:
        res = ch.run_chase(2000, 2000, {2000: 10.0}, {2000: 10.0}, {2000: 0.0})
        self.assertEqual((res.finished, res.catch_year, res.years), (True, 2000, 1))

    def test_unfinished_chase_reports_years_so_far_and_share_reached(self) -> None:
        # R6: never reached by the last year: years so far = last - start + 1, share = B(last) / T(last)
        res = ch.run_chase(2023, 2025, dict.fromkeys(range(2023, 2026), 10.0), dict.fromkeys(range(2023, 2026), 100.0),
                           dict.fromkeys(range(2023, 2026), 0.0))
        self.assertFalse(res.finished)
        self.assertIsNone(res.catch_year)
        self.assertEqual(res.years, 3)
        self.assertAlmostEqual(res.share_reached, 0.30)

    def test_progress_runs_to_the_last_year_after_the_catch(self) -> None:
        # R7 needs the share after N years even for a chase that ended sooner
        res = ch.run_chase(2000, 2003, dict.fromkeys(range(2000, 2004), 10.0), dict.fromkeys(range(2000, 2004), 10.0),
                           dict.fromkeys(range(2000, 2004), 0.0))
        self.assertEqual(res.years, 1)
        self.assertEqual(len(res.progress), 4)
        self.assertAlmostEqual(res.progress[2], 3.0)

    def test_a_missing_year_stops_the_chase(self) -> None:
        with self.assertRaises(SystemExit):
            ch.run_chase(2000, 2001, {2000: 10.0}, {2000: 100.0, 2001: 100.0}, {2000: 0.0, 2001: 0.0})


class Saver(unittest.TestCase):
    def test_bracket_follows_the_saver_age(self) -> None:
        self.assertEqual(ch.bracket_of(25, BRACKETS), "25 to 34")
        self.assertEqual(ch.bracket_of(34, BRACKETS), "25 to 34")
        self.assertEqual(ch.bracket_of(35, BRACKETS), "35 to 44")
        with self.assertRaises(SystemExit):
            ch.bracket_of(55, BRACKETS)

    def test_contributions_switch_bracket_at_35_and_add_extra(self) -> None:
        # R2: aged 25 in 2000, so 34 in 2009 and 35 in 2010; R9 adds the bracket's extra on top of the share
        years = range(2000, 2012)
        income = {"25 to 34": dict.fromkeys(years, 100.0), "35 to 44": dict.fromkeys(years, 200.0)}
        extra = {"25 to 34": dict.fromkeys(years, 1.0), "35 to 44": dict.fromkeys(years, 2.0)}
        c = ch.contributions(2000, 2011, 0.10, income, BRACKETS)
        self.assertEqual((c[2009], c[2010]), (10.0, 20.0))
        c2 = ch.contributions(2000, 2011, 0.10, income, BRACKETS, extra)
        self.assertEqual((c2[2009], c2[2010]), (11.0, 22.0))


if __name__ == "__main__":
    unittest.main()
