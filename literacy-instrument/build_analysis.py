"""Post 22 analysis: what the word "literate" actually certifies.

Every number quoted in the post is produced here and written to results.json. Nothing in the
draft may be recalled from memory.

Reads the four files in data/ (see data/README.md for their traps) and answers four questions:

  1. What is a published literacy rate actually made of?
  2. What happened when DHS changed who gets handed the card?
  3. How are the world's literacy statistics produced at all?
  4. Which countries are asked to prove it, and which are taken at their word?

    python3 build_analysis.py
"""

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"

# The eight columns of the DHS literacy table, mutually exclusive and exhaustive.
# SCH is the one the post is about: it is NOT a test result. It is an exemption.
COLS = {
    "ED_LITR_W_SCH": "above_secondary_not_tested",
    "ED_LITR_W_RDW": "read_whole_sentence",
    "ED_LITR_W_RDP": "read_part_of_sentence",
    "ED_LITR_W_NRD": "cannot_read_at_all",
    "ED_LITR_W_NCD": "no_card_in_language",
    "ED_LITR_W_BLD": "blind",
    "ED_LITR_W_MIS": "missing",
    "ED_LITR_W_LIT": "literate_published",
}

# The four countries the post names. Each has surveys on BOTH sides of the rule change, which is
# what makes the before-and-after readable. Ghana is the worked example.
NAMED = ["Ghana", "India", "Indonesia", "Nigeria"]

# The five columns every survey reports. The other three (no card, blind, missing) are omitted by
# DHS whenever they round to zero, which is most of the time: they are absent from 98, 44 and 31
# of the 226 surveys respectively. Requiring all eight silently dropped 65% of the data and made
# the four countries the post names disappear, so absent means zero here, not unknown.
REQUIRED = ["above_secondary_not_tested", "read_whole_sentence", "read_part_of_sentence",
            "cannot_read_at_all", "literate_published"]
OPTIONAL = ["no_card_in_language", "blind", "missing"]

# Tolerance for the two structural assertions, in percentage points. DHS publishes to one decimal,
# so eight rounded columns can drift from 100 by a few tenths without anything being wrong.
TOL_SUM = 0.35
TOL_IDENTITY = 0.15
# How close a survey's never-tested column must sit to one of the two education shares before the
# classifier will accept it. Both regimes match their own predictor to about 0.05 points and miss
# the other by 30-plus, so this is generous by two orders of magnitude.
TOL_RULE = 1.0


def load_dhs():
    """Survey-level literacy distributions, keyed by SurveyId."""
    rows = json.loads((DATA / "dhs_literacy.json").read_text())["Data"]
    out = {}
    for r in rows:
        field = COLS.get(r["IndicatorId"])
        if field is None:
            continue
        s = out.setdefault(r["SurveyId"], {
            "survey_id": r["SurveyId"], "country": r["CountryName"],
            "year": int(r["SurveyYear"]), "survey_type": r["SurveyType"],
        })
        s[field] = float(r["Value"])
    for s in out.values():
        for c in OPTIONAL:
            s.setdefault(c, 0.0)
    return out


def load_education():
    """The two education shares that discriminate between the coding rules."""
    rows = json.loads((DATA / "dhs_education.json").read_text())["Data"]
    out = {}
    for r in rows:
        key = {"ED_EDUC_W_SEH": "secondary_or_higher",
               "ED_EDUC_W_HGH": "above_secondary"}.get(r["IndicatorId"])
        if key:
            out.setdefault(r["SurveyId"], {})[key] = float(r["Value"])
    return out


def classify_rule(sch, edu):
    """Which coding rule did this survey use?

    DHS-VI and earlier did not administer the card test to anyone with secondary education OR
    above, so the never-tested column equals the share with secondary-or-higher. DHS-7 and DHS-8
    exempt only those ABOVE secondary. The API publishes no phase field, and the two regimes
    overlap in time (old surveys run to 2016, new ones start in 2015), so a fieldwork-year cutoff
    misclassifies surveys. Compare against both published education shares instead.
    """
    seh, above = edu.get("secondary_or_higher"), edu.get("above_secondary")
    if seh is None or above is None:
        return None
    d_old, d_new = abs(sch - seh), abs(sch - above)
    if min(d_old, d_new) > TOL_RULE:
        return None
    return "pre_dhs7_secondary_exempt" if d_old < d_new else "dhs7_plus_above_secondary_exempt"


def main():
    res = {}
    dhs, edu = load_dhs(), load_education()

    surveys, unclassified = [], []
    for sid, s in sorted(dhs.items()):
        if any(c not in s for c in REQUIRED):
            continue
        total = sum(s[c] for c in COLS.values() if c != "literate_published")
        identity = s["literate_published"] - s["read_whole_sentence"] - s["read_part_of_sentence"]
        # Two structural checks. If either fails the definitions have moved and every number
        # downstream is suspect, so fail loudly rather than publish a quiet wrong answer.
        assert abs(total - 100.0) < TOL_SUM, f"{sid}: columns sum to {total}, not 100"
        assert abs(identity - s["above_secondary_not_tested"]) < TOL_IDENTITY, (
            f"{sid}: literate - whole - part = {identity:.2f} but SCH = "
            f"{s['above_secondary_not_tested']:.2f}")
        rule = classify_rule(s["above_secondary_not_tested"], edu.get(sid, {}))
        if rule is None:
            unclassified.append(sid)
            continue
        s = dict(s, rule=rule, **edu[sid])
        # What share of the headline rate was never tested at all.
        s["share_of_literate_never_tested_pct"] = round(
            100 * s["above_secondary_not_tested"] / s["literate_published"], 1)
        surveys.append(s)

    res["method"] = {
        "universe": "Women age 15-49, the DHS interview universe. NOT the same population as "
                    "UNESCO's adult 15+ literacy rate, and the post must never present them as "
                    "one measure.",
        "values": "DHS's own published weighted percentages, read from its public API. Nothing "
                  "here is recomputed from microdata.",
        "surveys_classified": len(surveys),
        "surveys_unclassified": unclassified,
        "assertions": {
            "columns_sum_to_100": f"checked on all {len(surveys) + len(unclassified)} surveys, "
                                  f"tolerance {TOL_SUM} pts",
            "sch_equals_literate_minus_whole_minus_part":
                f"checked on all surveys, tolerance {TOL_IDENTITY} pts",
        },
    }

    # -- 1. what a literacy rate is made of -----------------------------------
    # Only new-rule surveys, and only the latest per country: mixing the two regimes in one
    # cross-section would compare two different instruments.
    new_rule = [s for s in surveys if s["rule"] == "dhs7_plus_above_secondary_exempt"]
    latest = {}
    for s in sorted(new_rule, key=lambda x: x["year"]):
        latest[s["country"]] = s
    latest = sorted(latest.values(), key=lambda s: s["literate_published"], reverse=True)

    res["composition"] = {
        "rule": "Latest survey per country among those using the current coding rule.",
        "n_countries": len(latest),
        "countries": [
            {k: s[k] for k in (
                "country", "survey_id", "year", "survey_type", "literate_published",
                "above_secondary_not_tested", "read_whole_sentence", "read_part_of_sentence",
                "cannot_read_at_all", "no_card_in_language", "blind", "missing",
                "share_of_literate_never_tested_pct")}
            for s in latest
        ],
    }
    # The single sharpest instance of "part of one sentence" doing the work.
    by_part = sorted(latest, key=lambda s: s["read_part_of_sentence"], reverse=True)
    res["composition"]["most_part_of_sentence"] = [
        {"country": s["country"], "survey_id": s["survey_id"],
         "read_part_of_sentence": s["read_part_of_sentence"],
         "literate_published": s["literate_published"],
         "part_share_of_literate_pct": round(
             100 * s["read_part_of_sentence"] / s["literate_published"], 1)}
        for s in by_part[:6]
    ]
    # statistics.median, not sorted(...)[n // 2]. With an even n the latter returns the upper of
    # the two middle values, which is not the median. Round 1 caught it rendering three wrong
    # numbers onto a chart. These are also INDEPENDENT column medians: no single country holds
    # all five, and the prose must never present them as one country's composition.
    res["composition"]["medians"] = {
        k: round(statistics.median(s[k] for s in latest), 1)
        for k in ("literate_published", "above_secondary_not_tested",
                  "read_whole_sentence", "read_part_of_sentence", "cannot_read_at_all")
    }
    # Shares OF THE LITERATE POPULATION, not of everyone. The final review caught the essay
    # quoting only the two small non-reading bands and never telling a prose-only reader that
    # whole-sentence reading is the dominant path. These are the counterweight.
    res["composition"]["median_share_of_literate_pct"] = {
        k: round(statistics.median(100 * s[k] / s["literate_published"] for s in latest), 1)
        for k in ("above_secondary_not_tested", "read_whole_sentence", "read_part_of_sentence")
    }
    res["composition"]["medians_note"] = (
        "Five independent column medians across the same set of countries, NOT the profile of any "
        "one country. They do not sum to 100 and the first three do not sum to the median "
        "published rate.")
    # The counterweight the design doc requires: the instrument also errs downward.
    res["composition"]["no_card_in_language"] = {
        "note": "Counted as NOT literate. A respondent who reads fluently in a language the "
                "interviewer had no card for is recorded as illiterate, so the instrument errs "
                "in both directions.",
        "max": max((round(s["no_card_in_language"], 1), s["country"]) for s in latest),
        "median": round(statistics.median(s["no_card_in_language"] for s in latest), 2),
        "n_countries_above_1pct": sum(1 for s in latest if s["no_card_in_language"] > 1.0),
    }

    # -- 2. the year the instrument changed ------------------------------------
    named = {}
    for c in NAMED:
        rounds = sorted((s for s in surveys if s["country"] == c), key=lambda s: s["year"])
        old = [s for s in rounds if s["rule"] == "pre_dhs7_secondary_exempt"]
        new = [s for s in rounds if s["rule"] == "dhs7_plus_above_secondary_exempt"]
        if not old or not new:
            continue
        a, b = old[-1], new[-1]
        named[c] = {
            "last_old_rule": {k: a[k] for k in (
                "survey_id", "year", "literate_published", "above_secondary_not_tested",
                "read_whole_sentence", "read_part_of_sentence", "cannot_read_at_all",
                "secondary_or_higher", "share_of_literate_never_tested_pct")},
            "latest_new_rule": {k: b[k] for k in (
                "survey_id", "year", "literate_published", "above_secondary_not_tested",
                "read_whole_sentence", "read_part_of_sentence", "cannot_read_at_all",
                "secondary_or_higher", "share_of_literate_never_tested_pct")},
            "change_in_published_literacy_pts": round(
                b["literate_published"] - a["literate_published"], 1),
            "change_in_secondary_or_higher_pts": round(
                b["secondary_or_higher"] - a["secondary_or_higher"], 1),
        }
    # NAMED is four worked examples, not the evidence base. 39 countries have surveys on both
    # sides of the rule change, and the final review caught the essay saying "one panel out of
    # four" as though four were all there is. Emit the whole set so the prose can be scoped
    # honestly and the stronger claim can be made from the full population.
    all_pairs = []
    by_country = {}
    for s in surveys:
        by_country.setdefault(s["country"], []).append(s)
    for country, rows in sorted(by_country.items()):
        rows.sort(key=lambda x: x["year"])
        old = [r for r in rows if r["rule"] == "pre_dhs7_secondary_exempt"]
        new = [r for r in rows if r["rule"] == "dhs7_plus_above_secondary_exempt"]
        if not old or not new:
            continue
        a, b = old[-1], new[-1]
        all_pairs.append({
            "country": country, "from_year": a["year"], "to_year": b["year"],
            "literacy_before": a["literate_published"], "literacy_after": b["literate_published"],
            "literacy_change_pts": round(b["literate_published"] - a["literate_published"], 1),
            "secondary_or_higher_change_pts": round(
                b["secondary_or_higher"] - a["secondary_or_higher"], 1),
        })
    fell = [p for p in all_pairs if p["literacy_change_pts"] < 0]
    ghana_signature = [p for p in fell if p["secondary_or_higher_change_pts"] > 5]
    res["rule_change_all_countries"] = {
        "note": "Every country with at least one survey under each rule. The four the essay walks "
                "through are worked examples chosen for readability, not the evidence base, and "
                "the essay must not imply otherwise.",
        "n_countries_with_pairs": len(all_pairs),
        "n_headline_fell": len(fell),
        "fell": sorted(fell, key=lambda p: p["literacy_change_pts"]),
        "n_education_rose_over_5pts_while_literacy_fell": len(ghana_signature),
        "education_rose_while_literacy_fell": [p["country"] for p in ghana_signature],
    }

    res["rule_change"] = {
        "dhs_note": "In DHS-VI and earlier surveys the question on the ability of the respondent "
                    "to read a sentence was not asked to women and men with secondary education "
                    "or higher than secondary. Thus estimates from earlier surveys may "
                    "overestimate literacy relative to DHS-7 and DHS-8 surveys. Care should be "
                    "taken in interpreting trends.",
        "dhs_note_source": "The DHS Program, Guide to DHS Statistics, Literacy, Changes over Time",
        "n_old_rule": sum(1 for s in surveys if s["rule"] == "pre_dhs7_secondary_exempt"),
        "n_new_rule": len(new_rule),
        "regimes_overlap_in_time": {
            "old_rule_years": [min(s["year"] for s in surveys if s["rule"] == "pre_dhs7_secondary_exempt"),
                               max(s["year"] for s in surveys if s["rule"] == "pre_dhs7_secondary_exempt")],
            "new_rule_years": [min(s["year"] for s in new_rule), max(s["year"] for s in new_rule)],
            "why_it_matters": "The two regimes overlap, so a fieldwork-year cutoff misclassifies "
                              "surveys. The classifier compares the never-tested column against "
                              "both published education shares instead.",
        },
        "countries": named,
    }
    # How well the classifier separates. Quoted in the data note as evidence it is not a guess.
    seps = []
    for s in surveys:
        d_old = abs(s["above_secondary_not_tested"] - s["secondary_or_higher"])
        d_new = abs(s["above_secondary_not_tested"] - s["above_secondary"])
        seps.append((min(d_old, d_new), max(d_old, d_new)))
    res["rule_change"]["classifier_separation"] = {
        "mean_distance_to_assigned_rule_pts": round(sum(a for a, _ in seps) / len(seps), 3),
        "mean_distance_to_other_rule_pts": round(sum(b for _, b in seps) / len(seps), 1),
        "worst_distance_to_assigned_rule_pts": round(max(a for a, _ in seps), 2),
    }

    # -- 3. how the world's literacy statistics are made -----------------------
    mode_rows = list(csv.DictReader((DATA / "mode_of_reporting.csv").open()))
    mode_col = [c for c in mode_rows[0] if c not in ("entity", "code", "year")][0]
    modes = Counter(r[mode_col] for r in mode_rows if r[mode_col])
    with_method = sum(v for k, v in modes.items() if k != "No data")
    res["how_measured"] = {
        "source": "UNESCO Institute for Statistics, via Our World in Data",
        "column": mode_col,
        "n_country_years": len(mode_rows),
        "n_country_years_with_a_method": with_method,
        "n_countries": len({r["entity"] for r in mode_rows}),
        "years": [min(r["year"] for r in mode_rows), max(r["year"] for r in mode_rows)],
        "counts": dict(modes.most_common()),
        "tested_share_pct": round(100 * modes["Literacy test"] / with_method, 1),
        "self_reported_share_pct": round(
            100 * (modes["Self-reported (head of household)"]
                   + modes["Self-reported (individual)"]) / with_method, 1),
        "proxy_share_pct": round(
            100 * modes["Self-reported (head of household)"] / with_method, 1),
    }

    # -- 4. who is asked to prove it -------------------------------------------
    ever_tested = sorted({r["entity"] for r in mode_rows if r[mode_col] == "Literacy test"})
    never_tested = sorted({r["entity"] for r in mode_rows if r["entity"] not in ever_tested})
    res["who_is_tested"] = {
        "n_ever_tested": len(ever_tested),
        "n_never_tested": len(never_tested),
        "ever_tested": ever_tested,
        "note": "Membership is 'ever administered a literacy test in any year UNESCO records', "
                "which is the most generous possible reading. It is not a claim about the "
                "country's current practice.",
    }
    # Round 1 killed a hand-written 13-name list here. It omitted Bosnia and Herzegovina and
    # Ukraine, both of which ARE recorded testing and both of which appear in this post's own
    # ever_tested list, so the draft asserted "every European country self-declares" while the
    # data underneath it said otherwise. Enumerate the continent, then count.
    EUROPE = {
        "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
        "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany",
        "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Liechtenstein", "Lithuania",
        "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
        "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia",
        "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom",
    }
    methods_by_country = {}
    for r in mode_rows:
        if r[mode_col] and r[mode_col] != "No data":
            methods_by_country.setdefault(r["entity"], set()).add(r[mode_col])
    eur = {c: sorted(m) for c, m in methods_by_country.items() if c in EUROPE}
    self_only = {"Self-reported (individual)", "Self-reported (head of household)"}
    res["who_is_tested"]["europe"] = {
        "n_in_file": len(eur),
        "ever_tested": sorted(c for c, m in eur.items() if "Literacy test" in m),
        "n_self_declared_only": sum(1 for m in eur.values() if set(m) <= self_only),
        "other": {c: m for c, m in eur.items()
                  if "Literacy test" not in m and not set(m) <= self_only},
        "methods": eur,
    }

    # Reporting method against the literacy level it produced. Each country's most recent
    # recorded method, paired with the UNESCO rate nearest that year.
    lit_by_country = {}
    for r in csv.DictReader((DATA / "dhs_vs_unesco.csv").open()):
        if r["se_adt_litr_zs"]:
            lit_by_country.setdefault(r["entity"], {})[int(r["year"])] = float(r["se_adt_litr_zs"])
    latest_mode = {}
    for r in mode_rows:
        if r[mode_col] and r[mode_col] != "No data":
            latest_mode[r["entity"]] = (int(r["year"]), r[mode_col])
    by_method = {}
    for country, (year, method) in latest_mode.items():
        years = lit_by_country.get(country)
        if not years:
            continue
        nearest = min(years, key=lambda k: abs(k - year))
        by_method.setdefault(method, []).append(
            {"country": country, "method_year": year, "literacy": years[nearest],
             "literacy_year": nearest})
    res["method_vs_level"] = {
        "note": "Each country's most recently recorded reporting method against the UNESCO adult "
                "literacy rate nearest that year.",
        "caution": "This has two readings and the data cannot separate them: testing may be "
                   "applied where literacy is already doubted (selection), and testing may "
                   "produce lower numbers than self-declaration (instrument). The post must "
                   "state both rather than assert the second.",
        "n_countries": sum(len(v) for v in by_method.values()),
        "n_countries_with_a_method": len(latest_mode),
        "n_dropped_for_no_literacy_value": len(latest_mode) - sum(len(v) for v in by_method.values()),
        "dropped": sorted(c for c in latest_mode if c not in lit_by_country),
        "by_method": {
            m: {"n": len(v),
                "median_literacy": round(statistics.median(x["literacy"] for x in v), 1),
                "min": round(min(x["literacy"] for x in v), 1),
                "max": round(max(x["literacy"] for x in v), 1),
                "countries": sorted(v, key=lambda x: x["literacy"])}
            for m, v in sorted(by_method.items(), key=lambda kv: -len(kv[1]))
        },
    }

    # Does "tested where doubted" actually hold? Round 1 refuted the tidy version: plenty of
    # low-literacy countries have never been tested either. Emit both tails so the prose has to
    # face the counterexamples rather than assert the pattern.
    ever_tested_set = set(ever_tested)
    paired = []
    for country, (year, _method) in latest_mode.items():
        years = lit_by_country.get(country)
        if not years:
            continue
        nearest = min(years, key=lambda k: abs(k - year))
        paired.append({"country": country, "literacy": round(years[nearest], 1),
                       "literacy_year": nearest, "ever_tested": country in ever_tested_set})
    high = [p for p in paired if p["literacy"] >= 95]
    low = [p for p in paired if p["literacy"] < 50]
    res["tested_where_doubted"] = {
        "note": "The tidy version of this pattern does not hold and the post must not assert it.",
        "n_paired": len(paired),
        "high_literacy_95_plus": {
            "n": len(high),
            "n_never_tested": sum(1 for p in high if not p["ever_tested"]),
            "ever_tested": sorted(p["country"] for p in high if p["ever_tested"]),
        },
        "low_literacy_under_50": {
            "n": len(low),
            "n_never_tested": sum(1 for p in low if not p["ever_tested"]),
            # The YEAR is not optional. Pairing is nearest-to-method-year and the method file ends
            # in 2016, so several of these values are a decade old: Burkina Faso reads 27.9 here
            # and 41.6 in its latest year in the same file. Quoting one without its year invites a
            # reader to take a 2007 figure as current.
            "never_tested_examples": sorted(
                ({"country": p["country"], "literacy": p["literacy"],
                  "literacy_year": p["literacy_year"]}
                 for p in low if not p["ever_tested"]),
                key=lambda p: p["literacy"])[:6],
        },
    }

    # -- 5. two instruments, one country ---------------------------------------
    cmp_rows = list(csv.DictReader((DATA / "dhs_vs_unesco.csv").open()))
    dcol = "literacy_rate__adult_total__pct_of_total_respondents__dhs_surveys"
    ucol = "se_adt_litr_zs"
    both = [(r["entity"], int(r["year"]), float(r[dcol]), float(r[ucol]))
            for r in cmp_rows if r[dcol] and r[ucol]]
    gaps = sorted(((u - d, e, y, d, u) for e, y, d, u in both), reverse=True)
    res["two_instruments"] = {
        "note": "DHS and UNESCO adult literacy for the same country-year. Different universes and "
                "different instruments, so this is a disagreement between measures, not an error "
                "in either.",
        "n_country_years": len(both), "n_countries": len({e for e, _, _, _ in both}),
        "years": [min(y for _, y, _, _ in both), max(y for _, y, _, _ in both)],
        "mean_gap_unesco_minus_dhs_pts": round(sum(g for g, *_ in gaps) / len(gaps), 2),
        "largest_unesco_higher": [
            {"country": e, "year": y, "dhs": d, "unesco": u, "gap_pts": round(g, 1)}
            for g, e, y, d, u in gaps[:5]],
        # Most extreme FIRST in both directions. gaps is sorted descending, so the DHS-higher tail
        # has to be reversed; taking gaps[-5:] as-is puts the LEAST extreme at index 0, and round 1
        # caught the draft quoting that element as though it were the maximum.
        "largest_dhs_higher": [
            {"country": e, "year": y, "dhs": d, "unesco": u, "gap_pts": round(g, 1)}
            for g, e, y, d, u in list(reversed(gaps))[:5]],
    }

    (HERE / "results.json").write_text(json.dumps(res, indent=2))

    # -- console summary, full tables, no truncation ---------------------------
    m = res["composition"]["medians"]
    print(f"\nClassified {len(surveys)} surveys "
          f"({res['rule_change']['n_old_rule']} old rule, {res['rule_change']['n_new_rule']} new); "
          f"unclassified {len(unclassified)}")
    cs = res["rule_change"]["classifier_separation"]
    print(f"Classifier: mean {cs['mean_distance_to_assigned_rule_pts']} pts to assigned rule, "
          f"{cs['mean_distance_to_other_rule_pts']} to the other, worst "
          f"{cs['worst_distance_to_assigned_rule_pts']}")
    print(f"\nComposition, {res['composition']['n_countries']} countries, current rule. Medians: "
          f"literate {m['literate_published']}, never tested {m['above_secondary_not_tested']}, "
          f"whole {m['read_whole_sentence']}, part {m['read_part_of_sentence']}, "
          f"cannot read {m['cannot_read_at_all']}")
    print(f"\n{'country':22s}{'survey':13s}{'LIT':>7s}{'nottest':>9s}{'whole':>7s}{'part':>7s}"
          f"{'cannot':>8s}{'%LIT untested':>15s}")
    for c in res["composition"]["countries"]:
        print(f"{c['country'][:22]:22s}{c['survey_id']:13s}{c['literate_published']:7.1f}"
              f"{c['above_secondary_not_tested']:9.1f}{c['read_whole_sentence']:7.1f}"
              f"{c['read_part_of_sentence']:7.1f}{c['cannot_read_at_all']:8.1f}"
              f"{c['share_of_literate_never_tested_pct']:15.1f}")
    print("\nThe rule change, countries with rounds on both sides:")
    for c, v in res["rule_change"]["countries"].items():
        a, b = v["last_old_rule"], v["latest_new_rule"]
        print(f"  {c:10s} {a['year']} -> {b['year']}: literacy {a['literate_published']:5.1f} -> "
              f"{b['literate_published']:5.1f} ({v['change_in_published_literacy_pts']:+.1f}), "
              f"never tested {a['above_secondary_not_tested']:5.1f} -> "
              f"{b['above_secondary_not_tested']:5.1f}, secondary+ "
              f"{a['secondary_or_higher']:5.1f} -> {b['secondary_or_higher']:5.1f} "
              f"({v['change_in_secondary_or_higher_pts']:+.1f})")
    h = res["how_measured"]
    print(f"\nHow the world's literacy rates are made ({h['n_country_years_with_a_method']} "
          f"country-years, {h['n_countries']} countries, {h['years'][0]}-{h['years'][1]}):")
    for k, v in h["counts"].items():
        print(f"  {v:4d}  {k}")
    print(f"  tested {h['tested_share_pct']}%, self-reported {h['self_reported_share_pct']}%, "
          f"of which head-of-household {h['proxy_share_pct']}%")
    w = res["who_is_tested"]
    print(f"\nEver tested: {w['n_ever_tested']} countries. Never: {w['n_never_tested']}.")
    e = w["europe"]
    print(f"  Europe: {e['n_in_file']} in file, {e['n_self_declared_only']} self-declared only, "
          f"ever tested {e['ever_tested']}, other {e['other']}")
    mv = res["method_vs_level"]
    print(f"\nReporting method against the literacy level it produced "
          f"({mv['n_countries']} countries):")
    for m, v in mv["by_method"].items():
        print(f"  {m:34s} n={v['n']:3d}  median {v['median_literacy']:5.1f}  "
              f"range {v['min']:.1f}-{v['max']:.1f}")
    t = res["two_instruments"]
    print(f"\nDHS vs UNESCO: {t['n_country_years']} country-years, {t['n_countries']} countries, "
          f"mean gap {t['mean_gap_unesco_minus_dhs_pts']:+.2f} pts")
    for r in t["largest_unesco_higher"][:3]:
        print(f"    {r['country']:16s} {r['year']}  DHS {r['dhs']:5.1f}  UNESCO {r['unesco']:5.1f}"
              f"  {r['gap_pts']:+.1f}")
    for r in t["largest_dhs_higher"][:2]:
        print(f"    {r['country']:16s} {r['year']}  DHS {r['dhs']:5.1f}  UNESCO {r['unesco']:5.1f}"
              f"  {r['gap_pts']:+.1f}")
    print("\nwrote results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
