"""Tests for profile_data.py's band and weight rules, without the survey file. Run: python3 -m unittest test_profile_data"""
import unittest

import pandas as pd

from profile_data import PANDEMIC_YEAR, band, weights


class BandTest(unittest.TestCase):
    def test_each_band_starts_and_ends_where_its_label_says(self):
        hours = pd.Series([1, 34, 35, 40, 41, 49, 50, 59, 60, 160])
        expected = ["1 to 34", "1 to 34", "35 to 40", "35 to 40", "41 to 49", "41 to 49", "50 to 59", "50 to 59",
                    "60 or more", "60 or more"]
        self.assertEqual(list(band(hours)), expected)

    def test_zero_and_hours_vary_fall_in_no_band(self):
        self.assertTrue(band(pd.Series([0, -4])).isna().all())


class WeightTest(unittest.TestCase):
    def test_the_pandemic_year_uses_its_own_weight_and_no_other_year_does(self):
        d = pd.DataFrame({"TUYEAR": [PANDEMIC_YEAR - 1, PANDEMIC_YEAR, PANDEMIC_YEAR + 1],
                          "TUFNWGTP": [10.0, -1.0, 30.0], "TU20FWGT": [99.0, 20.0, -1.0]})
        self.assertEqual(list(weights(d)), [10.0, 20.0, 30.0])


if __name__ == "__main__":
    unittest.main()
