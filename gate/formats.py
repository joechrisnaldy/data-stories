"""The fixed registry of formatters a placeholder may use.

A formatter is where a published number is minted, so each one refuses input it cannot render
honestly rather than guessing. Derived arithmetic does not belong here: the build script emits the
quantity and the template only formats it.
"""

import math
from fractions import Fraction


class FormatError(ValueError):
    pass


def _number(v) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v or math.isinf(v):
        raise FormatError(f"not a finite number: {v!r}")
    return float(v)


def _integral(v) -> int:
    x = _number(v)
    if abs(x - round(x)) > 1e-9:
        raise FormatError(f"not an integer: {v!r}")
    return int(round(x))


def _signed(places: int):
    def fmt(v) -> str:
        x = round(_number(v), places)
        if x == 0:
            return f"{0:.{places}f}"
        return f"{'minus' if x < 0 else 'plus'} {abs(x):.{places}f}"
    return fmt


def _unsigned(v, name: str) -> float:
    """Unsigned formatters print no sign at all: a negative would come out as an ASCII hyphen."""
    x = _number(v)
    if x < 0:
        raise FormatError(f"{name} refuses negative {v!r}; this blog writes 'minus', use a signed formatter "
                          "or emit the magnitude from the build")
    return x


def _dec(places: int):
    def fmt(v) -> str:
        x = _number(v)
        if round(x, places) == 0:
            return f"{0:.{places}f}"          # never '-0.00'
        return f"{_unsigned(x, f'dec{places}'):.{places}f}"
    return fmt


def _int(v) -> str:
    _unsigned(v, "int")
    return f"{_integral(v):,}"


def _round0(v) -> str:
    return f"{round(_unsigned(v, 'round0')):,}"


def _ordinal0(v) -> str:
    n = round(_unsigned(v, "ordinal0"))
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
         "fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _words(v) -> str:
    n = _integral(v)
    if 1000 <= n <= 100000 and n % 1000 == 0:
        return f"{_words(n // 1000)} thousand"
    if not 0 <= n <= 100:
        raise FormatError(f"words covers 0 to 100 and whole thousands to 100,000, got {n}")
    if n == 100:
        return "one hundred"
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return _TENS[tens] + ("" if ones == 0 else f"-{_ONES[ones]}")


def _year(v) -> str:
    n = _integral(v)
    if not 1000 <= n <= 2100:
        raise FormatError(f"not a plausible year: {v!r}")
    return str(n)


def _pct(places: int):
    def fmt(v) -> str:
        x = _unsigned(v, f"pct{places}")
        if x > 1:
            raise FormatError(f"pct{places} expects a share between 0 and 1 (0.19), got {v!r}: if it is already "
                              "a percentage, or a share above 1, emit a key ending _pct from the build")
        return f"{x * 100:.{places}f}"
    return fmt


def _capwords(v) -> str:
    w = _words(v)
    return w[0].upper() + w[1:]


def _roundwords(v) -> str:
    return _words(round(_number(v)))


def _sig2(v) -> str:
    x = _number(v)
    if x <= 0:
        raise FormatError(f"sig2 needs a positive number, got {v!r}")
    places = 1 - int(math.floor(math.log10(x)))
    r = round(x, places)
    return f"{r:,.0f}" if places <= 0 else f"{r:.{places}f}"


_FRACTION_NAMES = {2: ("half", "halves"), 3: ("third", "thirds"), 4: ("quarter", "quarters"),
                   5: ("fifth", "fifths"), 10: ("tenth", "tenths")}
FRACTION_TOLERANCE = 0.025


def _fraction(v) -> str:
    x = _number(v)
    if not 0 < x < 1:
        raise FormatError(f"fraction needs a value strictly between 0 and 1, got {v!r}")
    candidates = sorted({Fraction(k, d) for d in _FRACTION_NAMES for k in range(1, d)},
                        key=lambda f: (abs(float(f) - x), f.denominator))
    best = candidates[0]
    if abs(float(best) - x) > FRACTION_TOLERANCE:
        raise FormatError(f"{x:.3f} is not within {FRACTION_TOLERANCE} of any simple fraction")
    one, many = _FRACTION_NAMES[best.denominator]
    return f"a {one}" if best.numerator == 1 else f"{_ONES[best.numerator]} {many}"


REGISTRY = {
    **{f"signed{p}": _signed(p) for p in (1, 2, 3)},
    **{f"dec{p}": _dec(p) for p in (0, 1, 2, 3)},
    "int": _int,
    "round0": _round0,
    "ordinal0": _ordinal0,
    "words": _words,
    "roundwords": _roundwords,
    "capwords": _capwords,
    **{f"pct{p}": _pct(p) for p in (0, 1)},
    "year": _year,
    "sig2": _sig2,
    "fraction": _fraction,
}


def apply(name: str, value) -> str:
    if name not in REGISTRY:
        raise FormatError(f"unknown formatter {name!r}; known: {', '.join(sorted(REGISTRY))}")
    return REGISTRY[name](value)
