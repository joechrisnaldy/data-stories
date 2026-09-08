"""The gate is only worth anything if it catches the defects that actually shipped.

Each case below is real text from this repository's history, with the round that caught it. A gate
that passes these is a gate that would have made that round unnecessary.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from checks import numbers, samples  # noqa: E402

CAUGHT_LATE = [
    # round 3: two correlations, two different samples (n=76 and n=85), neither named
    ("Outside that world heat ran the same way in both eras, minus 0.21 then and minus 0.29 now, "
     "which is the other half of the contrast."),
    # round 2: temperature n=196 compared with latitude n=159 as if one sample
    ("On the same countries, absolute latitude does better at plus 0.60, and an Africa dummy does "
     "better still at minus 0.68."),
]

SHOULD_PASS = [
    # names one shared sample
    "Fit them together with an interaction term and the slopes come out at plus 0.15 for the "
    "never-colonised and minus 0.33 for the colonised, a gap with a t statistic of minus 5.3 "
    "across 163 countries.",
    # names the shared sample up front
    "On the 159 countries AJR's file records all three for, temperature manages minus 0.46, "
    "absolute latitude does better at plus 0.60, and a plain Africa dummy does better still at "
    "minus 0.68.",
    # "on each side" is an explicit shared-sample phrase
    "The urbanisation measure points the same way on a much smaller sample, 43 countries on each "
    "side: minus 0.42 among former colonies against plus 0.28 among the rest.",
    # the repaired round-3 sentence
    "Outside that world heat did not reverse: across the 69 places measurable in both eras it runs "
    "minus 0.15 then and minus 0.04 now, neither clear of chance.",
]


def main() -> int:
    bad = 0
    for s in CAUGHT_LATE:
        if not samples.check(s + " "):
            print(f"MISS: gate does not catch a defect that shipped: {s[:80]}")
            bad += 1
    for s in SHOULD_PASS:
        f = samples.check(s + " ")
        if f:
            print(f"FALSE POSITIVE: {f[0][:150]}")
            bad += 1

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results = json.load(open(os.path.join(here, "results.json")))
    # round 2 shipped an Africa dummy that no script computed; the gate must notice a stray figure
    if not numbers.check("An Africa dummy does better still at minus 0.9137.", results):
        print("MISS: gate does not flag a figure absent from results.json")
        bad += 1
    # and must not flag one that is present
    if numbers.check("the correlation is minus 0.44 across 196 countries.", results):
        print("FALSE POSITIVE: gate flags a figure that results.json does produce")
        bad += 1

    print("gate self-test: PASS" if not bad else f"gate self-test: {bad} FAILURE(S)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
