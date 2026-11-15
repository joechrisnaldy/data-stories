"""Unit checks for rentbuy.py, the model of design R1 to R13 and R15, on small made-up series.

Run from the post folder: python3 -m unittest test_rentbuy -v
"""
import math
import unittest

import rentbuy as rb


def rising(n: int, start: float, step: float) -> list[float]:
    return [start + step * t for t in range(n)]


class Payment(unittest.TestCase):
    def test_payment_formula(self) -> None:
        # R4: m = B x (i/12) / (1 - (1 + i/12)^(-n)); 100,000 at 6% over 360 months is the textbook 599.55
        self.assertAlmostEqual(rb.payment(100_000.0, 0.06, 360), 599.5505251527569, places=9)
        # with one month left the payment is the balance plus a month of interest
        self.assertAlmostEqual(rb.payment(1.0, 0.06, 1), 1.005, places=12)
        self.assertEqual(rb.payment(1.0, 0.06, 0), 0.0)

    def test_zero_balance_after_360_payments(self) -> None:
        sched = rb.loan_schedule(360, 7.33, None)
        self.assertLess(abs(sched[-1].balance), 1e-12)
        self.assertGreater(sched[-2].balance, 0.0)
        first = sched[0].payment
        self.assertTrue(all(abs(m.payment - first) < 1e-12 for m in sched))

    def test_payment_is_zero_after_month_360(self) -> None:
        sched = rb.loan_schedule(372, 7.33, None)
        self.assertTrue(all(m.payment == 0.0 for m in sched[360:]))
        self.assertGreater(sched[359].payment, 0.0)

    def test_balance_grows_by_the_month_rate_and_falls_by_the_payment(self) -> None:
        sched = rb.loan_schedule(2, 9.0, None)
        b1 = rb.LOAN * (1 + 0.09 / 12) - sched[0].payment
        self.assertAlmostEqual(sched[0].balance, b1, places=15)
        self.assertAlmostEqual(sched[1].balance, b1 * (1 + 0.09 / 12) - sched[1].payment, places=15)


class Refinancing(unittest.TestCase):
    @staticmethod
    def terms(n: int, rates: dict[int, float], base: float = 8.0, points: float = 1.0) -> rb.Refinancing:
        month = [rates.get(t, base) for t in range(1, n + 1)]
        return rb.Refinancing(month_rate_pct=tuple(month), month_points=tuple([points] * n), c_np=0.005)

    def refis(self, sched: list) -> list[int]:
        return [t for t, m in enumerate(sched, 1) if m.refi_cost > 0]

    def test_keeps_the_payoff_date(self) -> None:
        sched = rb.loan_schedule(360, 8.0, self.terms(360, {24: 6.5}))
        self.assertEqual(self.refis(sched), [24])
        self.assertEqual(sched[23].rate_pct, 6.5)
        # R9: the new payment follows R4 with the months left (336), so the balance still ends at month 360
        self.assertAlmostEqual(sched[24].payment, rb.payment(sched[23].balance, 0.065, 336), places=15)
        self.assertLess(abs(sched[359].balance), 1e-12)
        self.assertGreater(sched[358].balance, 0.0)
        # R9: cost = (p / 100 + c_np) x the balance, paid that month
        self.assertAlmostEqual(sched[23].refi_cost, (1.0 / 100 + 0.005) * sched[23].balance, places=15)

    def test_not_before_twelve_months(self) -> None:
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {11: 5.0}))), [])
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {12: 5.0}))), [12])

    def test_needs_a_full_percentage_point(self) -> None:
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {24: 7.01}))), [])
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {24: 7.0}))), [24])

    def test_needs_sixty_months_left(self) -> None:
        # after the payment of month 300, 60 months remain; after month 301, 59
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {301: 5.0}))), [])
        self.assertEqual(self.refis(rb.loan_schedule(360, 8.0, self.terms(360, {300: 5.0}))), [300])

    def test_twelve_months_between_refinancings_and_the_new_rate_is_the_reference(self) -> None:
        sched = rb.loan_schedule(360, 8.0, self.terms(360, {24: 6.5, 35: 5.0, 36: 5.6, 48: 4.0}))
        # month 35 is 11 months after the first refinancing; month 36 is 12 but 5.6 is not a point below 6.5
        self.assertEqual(self.refis(sched), [24, 48])
        sched = rb.loan_schedule(360, 8.0, self.terms(360, {24: 6.5, 36: 5.5}))
        self.assertEqual(self.refis(sched), [24, 36])
        self.assertLess(abs(sched[359].balance), 1e-12)

    def test_no_refinancing_without_terms(self) -> None:
        self.assertEqual(self.refis(rb.loan_schedule(360, 15.0, None)), [])


class MonthlyIdentity(unittest.TestCase):
    def test_both_households_spend_the_same_on_housing_plus_investing(self) -> None:
        n = 36
        value = rising(n, 1.0, 0.01)
        rent = rising(n, 0.004, 0.0002)          # passes the buyer's outlay within the first year or two
        run = rb.simulate(value, rent, [0.02] * n, [0.005] * n, 6.0, 0.03, None)
        for f in run.flows:
            self.assertAlmostEqual(f.outlay + f.buyer_invests, f.rent + f.renter_invests, places=15)
            self.assertTrue(f.buyer_invests == 0.0 or f.renter_invests == 0.0)
        self.assertTrue(any(f.buyer_invests > 0 for f in run.flows))
        self.assertTrue(any(f.renter_invests > 0 for f in run.flows))

    def test_outlay_is_payment_plus_carrying_costs_plus_refinancing_cost(self) -> None:
        n = 24
        refi = Refinancing.terms(n, {13: 6.0})
        value = rising(n, 1.0, 0.02)
        run = rb.simulate(value, [0.001] * n, [0.03] * n, [0.0] * n, 8.0, 0.02, refi)
        for lm, f, v in zip(run.loan, run.flows, value):
            self.assertAlmostEqual(f.outlay, lm.payment + 0.03 * v / 12 + lm.refi_cost, places=15)
        self.assertGreater(run.loan[12].refi_cost, 0.0)


class NetWorth(unittest.TestCase):
    def test_day_one_and_year_end(self) -> None:
        n = 24
        value = rising(n, 1.0, 0.005)
        ret = [0.01] * n
        run = rb.simulate(value, [0.002] * n, [0.02] * n, ret, 7.0, 0.015, None)
        self.assertAlmostEqual(run.day_one, 0.20 + 0.015, places=15)
        # R8: the day-one sum is invested at the start of month 1, so it earns month 1's return
        self.assertAlmostEqual(run.year_ends[0].renter_day_one, 0.215 * 1.01 ** 12, places=12)
        ye = run.year_ends[1]
        self.assertEqual(ye.h, 2)
        # R10: the buyer's net worth = V x (1 - 0.06) - the loan balance + the buyer's fund, at the end of December
        self.assertAlmostEqual(ye.buyer_nw, value[23] * 0.94 - run.loan[23].balance + ye.buyer_fund, places=15)
        self.assertEqual(ye.renter_nw, ye.renter_fund)

    def test_selling_cost_is_a_parameter(self) -> None:
        n = 12
        run = rb.simulate([1.0] * n, [0.002] * n, [0.02] * n, [0.0] * n, 7.0, 0.01, None, sell=0.05)
        ye = run.year_ends[0]
        self.assertAlmostEqual(ye.buyer_nw, 0.95 - ye.balance + ye.buyer_fund, places=15)


class Fund(unittest.TestCase):
    def test_the_balance_earns_the_month_return_before_the_month_investment_is_added(self) -> None:
        # R8 worked by hand: 1.0 x 1.10 + 0.5 = 1.6, then 1.6 x 1.20 + 0.5 = 2.42
        out = rb.grow(1.0, [0.5, 0.5], [0.10, 0.20])
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out[0], 1.6, places=12)
        self.assertAlmostEqual(out[1], 2.42, places=12)

    def test_simulate_grows_both_funds_as_written_out(self) -> None:
        # R8 written out here, not through rb.grow: each month a fund earns R(t), then the month's gap is added; the
        # renter starts from the day-one sum and the buyer from nothing
        n = 36
        value = rising(n, 1.0, 0.01)
        rent = rising(n, 0.004, 0.0002)          # below the buyer's outlay at first, above it later
        ret = [0.02 if t % 2 else -0.01 for t in range(n)]
        run = rb.simulate(value, rent, [0.02] * n, ret, 6.0, 0.03, None)
        self.assertTrue(any(f.renter_invests > 0 for f in run.flows))
        self.assertTrue(any(f.buyer_invests > 0 for f in run.flows))
        renter, buyer = run.day_one, 0.0
        for t, (f, r) in enumerate(zip(run.flows, ret, strict=True), 1):
            renter = renter * (1 + r) + f.renter_invests
            buyer = buyer * (1 + r) + f.buyer_invests
            if t % 12 == 0:
                ye = run.year_ends[t // 12 - 1]
                self.assertAlmostEqual(ye.renter_fund, renter, places=12)
                self.assertAlmostEqual(ye.buyer_fund, buyer, places=12)


class ShareToTie(unittest.TestCase):
    FLOWS = (0.01, 0.0, 0.02, 0.015, 0.0, 0.03)
    RETURNS = (0.01, -0.02, 0.03, 0.0, 0.015, -0.01)

    def fund(self, share: float) -> float:
        return rb.grow(0.25, [share * f for f in self.FLOWS], self.RETURNS)[-1]

    def test_renter_fund_is_linear_in_the_share(self) -> None:
        w0, w1 = self.fund(0.0), self.fund(1.0)
        for x in (0.1, 0.35, 0.8):
            self.assertAlmostEqual(self.fund(x), w0 + x * (w1 - w0), places=15)

    def test_the_share_found_ties_the_two_net_worths(self) -> None:
        w0, w1 = self.fund(0.0), self.fund(1.0)
        buyer = w0 + 0.4 * (w1 - w0)
        label, share, raw = rb.share_to_tie(buyer, w0, w1, True)
        self.assertEqual(label, rb.SHARE)
        self.assertAlmostEqual(share, 0.4, places=12)
        self.assertAlmostEqual(self.fund(share), buyer, places=12)
        self.assertEqual(share, raw)

    def test_edge_cases(self) -> None:
        self.assertEqual(rb.share_to_tie(2.0, 1.0, 1.5, True)[0], rb.CANNOT_TIE)          # s = 2
        self.assertAlmostEqual(rb.share_to_tie(2.0, 1.0, 1.5, True)[2], 2.0)
        self.assertEqual(rb.share_to_tie(0.9, 1.0, 1.5, True)[:2], (rb.ZERO, 0.0))        # s < 0
        self.assertEqual(rb.share_to_tie(1.0, 1.0, 1.5, True)[:2], (rb.ZERO, 0.0))        # s = 0: day-one sum ties
        self.assertEqual(rb.share_to_tie(1.5, 1.0, 1.5, True)[:2], (rb.SHARE, 1.0))       # s = 1 ties at the whole gap
        self.assertEqual(rb.share_to_tie(1.2, 1.0, 1.0, False), (rb.NO_GAP, None, None))

    def test_simulate_tracks_the_day_one_sum_and_the_full_gap(self) -> None:
        n = 24
        value = [1.0] * n
        rent = rising(n, 0.002, 0.0004)
        ret = [0.004 * ((-1) ** t) + 0.003 for t in range(n)]
        run = rb.simulate(value, rent, [0.02] * n, ret, 6.0, 0.02, None)
        gaps = [max(f.renter_invests, 0.0) for f in run.flows]
        self.assertAlmostEqual(run.year_ends[1].renter_fund, rb.grow(run.day_one, gaps, ret)[-1], places=15)
        self.assertAlmostEqual(run.year_ends[1].renter_day_one, rb.grow(run.day_one, [0.0] * n, ret)[-1], places=15)
        self.assertTrue(run.year_ends[1].any_gap)

    def test_no_gap_counts_only_positive_gaps_up_to_the_year_end(self) -> None:
        # R12 through simulate: the rent exceeds the buyer's outlay through year 1 and falls below it in year 2, so the
        # renter has no positive gap at the first year-end and one at the last. The second rent path equals the outlay
        # in month 1, a zero gap, which is not a positive gap either.
        n = 24
        value, carry, ret = [1.0] * n, [0.02] * n, [0.004] * n
        outlay = [f.outlay for f in rb.simulate(value, [0.0] * n, carry, ret, 6.0, 0.02, None).flows]
        rent = [o + 0.001 if t < 12 else o - 0.001 for t, o in enumerate(outlay)]
        for path in (rent, [outlay[0]] + rent[1:]):
            run = rb.simulate(value, path, carry, ret, 6.0, 0.02, None)
            first = run.year_ends[0]
            self.assertIs(first.any_gap, False)
            self.assertIs(run.year_ends[-1].any_gap, True)
            self.assertEqual(rb.share_to_tie(first.buyer_nw, first.renter_day_one, first.renter_fund, first.any_gap),
                             (rb.NO_GAP, None, None))

    def test_a_positive_gap_in_the_year_end_month_counts_for_that_year(self) -> None:
        # R12: months 1 to 12h belong to year h, so a positive gap only in month 12 counts at the first year-end
        n = 24
        value, carry, ret = [1.0] * n, [0.02] * n, [0.004] * n
        outlay = [f.outlay for f in rb.simulate(value, [0.0] * n, carry, ret, 6.0, 0.02, None).flows]
        rent = [o - 0.001 if t == 11 else o + 0.001 for t, o in enumerate(outlay)]
        run = rb.simulate(value, rent, carry, ret, 6.0, 0.02, None)
        self.assertEqual([t for t, f in enumerate(run.flows) if f.renter_invests > 0], [11])
        self.assertIs(run.year_ends[0].any_gap, True)


class Bridge(unittest.TestCase):
    def test_depreciation_is_carried_past_january_1975(self) -> None:
        months = rb.months_from(1973, 4)                      # January 1973 to December 1976
        d = {1973: 0.012, 1974: 0.024}
        factors = rb.depreciation(months, d)
        self.assertEqual(factors[0], 1.0)                     # R2: D(1) = 1
        full = (1 - 0.012 / 12) ** 12 * (1 - 0.024 / 12) ** 12
        jan75 = months.index((1975, 1))
        self.assertAlmostEqual(factors[jan75], full, places=15)
        self.assertTrue(all(f == factors[jan75] for f in factors[jan75:]))
        # D(t) multiplies the bridge months BEFORE month t, so December 1974 lacks its own factor
        self.assertAlmostEqual(factors[jan75 - 1], full / (1 - 0.024 / 12), places=15)

    def test_no_depreciation_for_a_start_from_1975(self) -> None:
        self.assertEqual(rb.depreciation(rb.months_from(1975, 2), {}), [1.0] * 24)

    def test_quarters_interpolate_log_linearly_between_mid_year_points(self) -> None:
        annual = {1971: 10.0, 1972: 20.0, 1973: 40.0}
        # 1972Q1's midpoint is 1972.125: 0.625 of the way from mid-1971 to mid-1972
        self.assertAlmostEqual(rb.interpolate_quarter(annual, (1972, 1)), 10.0 * 2 ** 0.625, places=12)
        self.assertAlmostEqual(rb.interpolate_quarter(annual, (1972, 2)), 10.0 * 2 ** 0.875, places=12)
        self.assertAlmostEqual(rb.interpolate_quarter(annual, (1972, 3)), 20.0 * 2 ** 0.125, places=12)
        self.assertAlmostEqual(rb.interpolate_quarter(annual, (1972, 4)), 20.0 * 2 ** 0.375, places=12)

    def test_value_index_joins_the_fhfa_index(self) -> None:
        annual = {1973: 10.0, 1974: 12.0, 1975: 15.0}
        fhfa = {(1975, 1): 60.0, (1975, 2): 61.0}
        index = rb.value_index(annual, fhfa, (1975, 1), [(1974, 3), (1974, 4)])
        c = rb.interpolate_quarter
        self.assertAlmostEqual(index[(1974, 4)], 60.0 * c(annual, (1974, 4)) / c(annual, (1975, 1)), places=12)
        self.assertEqual(index[(1975, 2)], 61.0)

    def test_value_path(self) -> None:
        months = rb.months_from(1974, 2)
        index = {(y, q): 100.0 + 10 * (y - 1974) + q for y in (1974, 1975) for q in (1, 2, 3, 4)}
        v = rb.value_path(months, index, rb.depreciation(months, {1974: 0.012}))
        self.assertEqual(v[0], 1.0)
        self.assertAlmostEqual(v[-1], 114.0 / 101.0 * (1 - 0.001) ** 12, places=15)


class RentRatio(unittest.TestCase):
    def test_extension_follows_rent_over_price_and_skips_an_unpublished_month(self) -> None:
        ratio = {(2018, 1): 0.041, (2018, 2): 0.040}
        oer = {(2018, 4): 100.0, (2018, 5): 101.0, (2018, 6): 102.0, (2018, 7): 103.0, (2018, 8): None,
               (2018, 9): 105.0}
        po = {(2018, 2): 200.0, (2018, 3): 210.0}
        k = rb.extend_ratio(ratio, (2018, 2), oer, po, [(2018, 1), (2018, 2), (2018, 3)])
        self.assertEqual(k[(2018, 1)], 0.041)
        self.assertAlmostEqual(k[(2018, 3)], 0.040 * (104.0 / 101.0) / (210.0 / 200.0), places=15)

    def test_ratio_rent(self) -> None:
        self.assertEqual(rb.ratio_rent([0.06, 0.03], [1.0, 2.0]), [0.005, 0.005])


class Monotonicity(unittest.TestCase):
    def test_a_lower_rent_never_lowers_the_renters_lead(self) -> None:
        # R3's check: with k_A below k_B in every month, renter minus buyer is higher under A at every year-end
        n = 120
        value = [1.003 ** t for t in range(n)]
        rent_a = rb.ratio_rent([0.04] * n, value)
        rent_b = rb.ratio_rent([0.07] * n, value)
        refi = Refinancing.terms(n, {t: 6.0 for t in range(30, n + 1)}, base=9.0)
        ret = [0.012 if t % 3 else -0.02 for t in range(n)]
        a = rb.simulate(value, rent_a, [0.025] * n, ret, 9.0, 0.02, refi)
        b = rb.simulate(value, rent_b, [0.025] * n, ret, 9.0, 0.02, refi)
        self.assertTrue(rb.lead_higher(a, b))
        self.assertFalse(rb.lead_higher(b, a))
        for ya, yb in zip(a.year_ends, b.year_ends):
            self.assertGreater(ya.renter_nw - ya.buyer_nw, yb.renter_nw - yb.buyer_nw)


class Verdicts(unittest.TestCase):
    def test_who_is_ahead_under_one_level(self) -> None:
        self.assertEqual(rb.ahead(1.2, 1.0), rb.BUY)
        self.assertEqual(rb.ahead(1.0, 1.2), rb.RENT)
        self.assertIsNone(rb.ahead(1.0, 1.0))

    def test_verdict_rule(self) -> None:
        self.assertEqual(rb.verdict(rb.BUY, rb.BUY), rb.BUY)
        self.assertEqual(rb.verdict(rb.RENT, rb.RENT), rb.RENT)
        self.assertEqual(rb.verdict(rb.BUY, rb.RENT), rb.DEPENDS)
        self.assertEqual(rb.verdict(rb.RENT, rb.BUY), rb.DEPENDS)
        self.assertEqual(rb.verdict(None, rb.BUY), rb.DEPENDS)
        self.assertEqual(rb.verdict(None, None), rb.DEPENDS)

    def test_break_even(self) -> None:
        self.assertEqual(rb.break_even([False, True, True]), (2, True))
        self.assertEqual(rb.break_even([False, True, False]), (2, False))
        self.assertEqual(rb.break_even([True]), (1, True))
        self.assertEqual(rb.break_even([False, False]), (None, None))


class Inputs(unittest.TestCase):
    def test_weekly_means_skip_weeks_without_a_value(self) -> None:
        weeks = [((2022, 11, 3), 0.8), ((2022, 11, 10), 0.9), ((2022, 11, 17), None), ((2022, 12, 1), None),
                 ((2023, 1, 5), 0.5)]
        by_year, by_month = rb.weekly_means(weeks), rb.weekly_means(weeks, by_month=True)
        self.assertEqual(sorted(by_year), [2022, 2023])
        self.assertEqual(sorted(by_month), [(2022, 11), (2023, 1)])
        self.assertAlmostEqual(by_year[2022], 0.85, places=15)
        self.assertAlmostEqual(by_month[(2022, 11)], 0.85, places=15)
        self.assertEqual(by_year[2023], 0.5)

    def test_straight_line_fill(self) -> None:
        filled = rb.fill_straight({1973: 0.017, 1975: 0.015, 1981: 0.011, 1983: 0.012}, range(1972, 1984))
        self.assertEqual(filled[1972], 0.017)                 # R7a: 1972 takes the 1973 value
        self.assertAlmostEqual(filled[1974], 0.016, places=15)
        self.assertAlmostEqual(filled[1982], 0.0115, places=15)
        self.assertAlmostEqual(filled[1978], 0.015 + 3 / 6 * (0.011 - 0.015), places=15)
        with self.assertRaises(SystemExit):
            rb.fill_straight({1973: 0.017}, [1974])

    def test_acs_ratio_names_every_year_without_both_cells(self) -> None:
        # R7a, A2: 2005 to 2009 take B25103_001 over B25077_001; a year without both cells stops the build rather
        # than falling back to the straight line
        cells = {(2005, "B25103_001"): 1500.0, (2005, "B25077_001"): 150_000.0, (2006, "B25077_001"): 160_000.0,
                 (2007, "B25103_001"): 1700.0}
        self.assertEqual(rb.acs_ratio(cells, [2005], "B25103_001", "B25077_001"), {2005: 0.01})
        with self.assertRaises(SystemExit) as stop:
            rb.acs_ratio(cells, [2005, 2006, 2007], "B25103_001", "B25077_001")
        message = str(stop.exception)
        self.assertIn("2006 B25103_001", message)
        self.assertIn("2007 B25077_001", message)
        self.assertNotIn("2005", message)

    def test_insurance_ramp(self) -> None:
        path = rb.insurance_path(0.0037, 0.0050, range(2004, 2025))
        self.assertEqual((path[2004], path[2005], path[2022], path[2024]), (0.0037, 0.0037, 0.0050, 0.0050))
        self.assertAlmostEqual(path[2010], 0.0037 + 5 / 17 * 0.0013, places=15)

    def test_upkeep_charges_improvements_from_1975(self) -> None:
        u = rb.upkeep({1974: 0.006, 1975: 0.006}, {1974: 0.009, 1975: 0.009}, [1974, 1975])
        self.assertEqual(u, {1974: 0.006, 1975: 0.015})

    def test_share_of_stock_uses_four_quarter_ends(self) -> None:
        stock = {(1972, q): 100.0 * q for q in (1, 2, 3, 4)}
        self.assertEqual(rb.share_of_stock({1972: 5.0}, stock, [1972]), {1972: 0.02})
        with self.assertRaises(SystemExit):
            rb.share_of_stock({1973: 5.0}, stock, [1973])

    def test_fund_return_takes_off_a_twelfth_of_the_fee(self) -> None:
        r = rb.fund_returns([(1990, 1)], {(1990, 1): 1.5}, {1990: 0.0027})
        self.assertAlmostEqual(r[0], 0.015 - 0.0027 / 12, places=15)

    def test_chain_skips_an_unpublished_month(self) -> None:
        keys = [(1982, 11), (1982, 12), (1983, 1), (1983, 2), (1983, 3)]
        early = {(1982, 11): 90.0, (1982, 12): 91.0}
        late = {(1982, 12): 100.0, (1983, 1): 101.0, (1983, 2): None, (1983, 3): 103.0}
        c = rb.chain(early, late, keys, (1982, 12))
        self.assertEqual(c[(1982, 12)], 91.0)
        self.assertAlmostEqual(c[(1983, 1)], 91.0 * 1.01, places=12)
        self.assertEqual(c[(1983, 2)], c[(1983, 1)])          # the skipped month holds the previous level
        self.assertAlmostEqual(c[(1983, 3)] / c[(1983, 1)], 103.0 / 101.0, places=12)

    def test_other_loan_costs(self) -> None:
        # R5: mean of cost / (amount x 1,000) less the mean points as a share of the loan
        c = rb.other_loan_costs({2018: 3000.0, 2019: 4000.0}, {2018: 200.0, 2019: 250.0}, 0.6)
        self.assertAlmostEqual(c, (0.015 + 0.016) / 2 - 0.006, places=15)
        self.assertAlmostEqual(rb.buying_cost(0.9, 0.01), (0.009 + 0.01) * 0.8, places=15)

    def test_month_one_split_of_the_owners_example(self) -> None:
        # R13: rent k/12 against the payment plus carrying costs; built here to give 200 / 700
        rate, carry = 6.0, 0.02
        outlay = rb.payment(rb.LOAN, rate / 100, rb.TERM) + carry / 12
        k = 12 * outlay * 200 / 700
        self.assertAlmostEqual(rb.month_one_split(k, rate, carry), 100 * 2 / 7, places=12)

    def test_household_dollars(self) -> None:
        price = rb.household_price(119_600.0, 100.0, [110.0, 120.0, 130.0, 140.0])
        self.assertAlmostEqual(price, 119_600.0 * 100.0 / 125.0, places=9)
        self.assertAlmostEqual(rb.in_dollars_of(0.5, price, 200.0, 400.0), 0.5 * price * 2.0, places=9)


if __name__ == "__main__":
    unittest.main()
