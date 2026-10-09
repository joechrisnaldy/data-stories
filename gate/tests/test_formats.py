"""Formatters are where a published number is minted, so each one refuses input it cannot render honestly."""

import unittest

from gate.formats import FormatError, apply


class SignedTest(unittest.TestCase):
    def test_negative_reads_minus(self):
        self.assertEqual(apply("signed2", -0.43518), "minus 0.44")

    def test_positive_reads_plus(self):
        self.assertEqual(apply("signed2", 0.29462), "plus 0.29")

    def test_precision_suffix(self):
        self.assertEqual(apply("signed1", -5.3335), "minus 5.3")
        self.assertEqual(apply("signed3", 0.0351), "plus 0.035")

    def test_value_that_rounds_to_zero_has_no_sign(self):
        self.assertEqual(apply("signed2", -0.004), "0.00")


class DecimalTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(apply("dec2", 0.34129), "0.34")
        self.assertEqual(apply("dec1", 1.3), "1.3")

    def test_refuses_negative_because_the_blog_writes_minus(self):
        with self.assertRaises(FormatError):
            apply("dec2", -0.38)


class IntegerTest(unittest.TestCase):
    def test_integer_and_integral_float(self):
        self.assertEqual(apply("int", 196), "196")
        self.assertEqual(apply("int", 196.0), "196")

    def test_thousands_separator(self):
        self.assertEqual(apply("int", 14662), "14,662")

    def test_refuses_fractional(self):
        with self.assertRaises(FormatError):
            apply("int", 196.4)

    def test_refuses_bool(self):
        with self.assertRaises(FormatError):
            apply("int", True)


class RoundingTest(unittest.TestCase):
    def test_round0(self):
        self.assertEqual(apply("round0", 13.8298), "14")

    def test_ordinals(self):
        cases = {1.06: "1st", 2.13: "2nd", 3.0: "3rd", 4.0: "4th", 11.0: "11th", 12.0: "12th",
                 13.0: "13th", 21.0: "21st", 22.0: "22nd", 78.72: "79th", 100.0: "100th", 111.0: "111th"}
        for v, want in cases.items():
            self.assertEqual(apply("ordinal0", v), want, v)


class WordsTest(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(apply("words", 17), "seventeen")
        self.assertEqual(apply("words", 10), "ten")
        self.assertEqual(apply("words", 4.0), "four")
        self.assertEqual(apply("words", 21), "twenty-one")
        self.assertEqual(apply("words", 0), "zero")

    def test_refuses_fractional_and_out_of_range(self):
        for bad in (17.5, -1, 101):
            with self.assertRaises(FormatError, msg=bad):
                apply("words", bad)


class YearAndThousandsTest(unittest.TestCase):
    def test_year_has_no_separator(self):
        self.assertEqual(apply("year", 2023), "2023")

    def test_year_refuses_non_years(self):
        for bad in (23, 2023.5, 3000):
            with self.assertRaises(FormatError, msg=bad):
                apply("year", bad)

    def test_words_whole_thousands(self):
        self.assertEqual(apply("words", 40000), "forty thousand")
        with self.assertRaises(FormatError):
            apply("words", 40500)

    def test_percent(self):
        self.assertEqual(apply("pct0", 0.189), "19")
        self.assertEqual(apply("pct1", 0.0118), "1.2")

    def test_capwords(self):
        self.assertEqual(apply("capwords", 3), "Three")

    def test_roundwords(self):
        self.assertEqual(apply("roundwords", 13.83), "fourteen")


class SignificantTest(unittest.TestCase):
    def test_two_significant_figures(self):
        self.assertEqual(apply("sig2", 1132.68), "1,100")
        self.assertEqual(apply("sig2", 130296.84), "130,000")
        self.assertEqual(apply("sig2", 0.04117), "0.041")

    def test_refuses_negative(self):
        with self.assertRaises(FormatError):
            apply("sig2", -5)


class FractionTest(unittest.TestCase):
    def test_unit_and_plural_fractions(self):
        self.assertEqual(apply("fraction", 0.189), "a fifth")
        self.assertEqual(apply("fraction", 0.811), "four fifths")
        self.assertEqual(apply("fraction", 0.5), "a half")
        self.assertEqual(apply("fraction", 0.74), "three quarters")

    def test_refuses_value_far_from_any_simple_fraction(self):
        with self.assertRaises(FormatError):
            apply("fraction", 0.155)

    def test_refuses_out_of_unit_interval(self):
        with self.assertRaises(FormatError):
            apply("fraction", 1.2)


class RegistryTest(unittest.TestCase):
    def test_unknown_formatter(self):
        with self.assertRaises(FormatError):
            apply("signed9", 0.1)

    def test_refuses_non_numbers(self):
        for bad in (None, "0.44", float("nan")):
            with self.assertRaises(FormatError, msg=bad):
                apply("dec2", bad)


if __name__ == "__main__":
    unittest.main()


class NegativeTest(unittest.TestCase):
    """Review of v2: unsigned formatters printed an ASCII hyphen ('-5', '-0.00', '-3th'), which the
    prose rules forbid and which hides a sign from the sign check."""

    def test_unsigned_formatters_refuse_negatives(self):
        for name, v in (("int", -5), ("round0", -5.2), ("ordinal0", -3), ("pct0", -0.19), ("pct1", -0.19),
                        ("dec2", -0.5)):
            with self.subTest(name=name), self.assertRaises(FormatError):
                apply(name, v)

    def test_a_negative_that_rounds_to_zero_prints_a_plain_zero(self):
        self.assertEqual(apply("dec2", -0.004), "0.00")

    def test_percent_formatters_take_shares_only(self):
        # pct1 on 2.5 printed '250.0' and on 9.9 printed '990.0': a percentage passed in as a share
        for v in (2.5, 9.9, 1.01):
            with self.subTest(v=v), self.assertRaises(FormatError):
                apply("pct1", v)
        self.assertEqual(apply("pct0", 1.0), "100")
