"""Compute every number quoted in Post 24 and write results.json.

Nothing in the draft may be a figure recalled from memory. If a number appears in the post, it
appears here first.  Run:  python3 build_analysis.py

O*NET rates IMPORTANCE (1 to 5), not hours. No output of this script measures time spent.
"""

import csv
import json
import os
import statistics as st

from conditions import (EXCLUDED_FROM_PEOPLE, HANDS_ON, PEOPLE_MANAGEMENT, WORK_CONTEXT,
                        is_supervisor, soc_major_group)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def read(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load():
    titles = {r["O*NET-SOC Code"]: r["Title"] for r in read("onet_occupation_data.csv")}
    imp = {}
    for r in read("onet_work_activities.csv"):
        if r["Scale ID"] == "IM":
            imp.setdefault(r["O*NET-SOC Code"], {})[r["Element ID"]] = float(r["Data Value"])
    zones = {r["O*NET-SOC Code"]: int(r["Job Zone"]) for r in read("onet_job_zones.csv")}
    names = {r["Element ID"]: r["Element Name"] for r in read("onet_content_model_reference.csv")}
    assert len(imp) > 800, f"only {len(imp)} occupations parsed"
    for e in list(PEOPLE_MANAGEMENT) + list(HANDS_ON):
        assert any(e in v for v in imp.values()), f"pre-registered element {e} absent from O*NET"
    return titles, imp, zones, names


def score(row, group):
    vals = [row[e] for e in group if e in row]
    return st.mean(vals) if vals else None


def main():
    titles, imp, zones, names = load()
    occs = [c for c in imp if c in titles]

    supers = sorted(c for c in occs if is_supervisor(titles[c]))
    assert supers, "no first-line supervisor occupations found"

    rows = []
    for s in supers:
        mg = soc_major_group(s)
        workers = [c for c in occs if soc_major_group(c) == mg and not is_supervisor(titles[c])]
        if len(workers) < 3:
            continue
        rows.append(dict(
            supervisor=titles[s], code=s, major_group=mg, n_workers=len(workers),
            sup_people=score(imp[s], PEOPLE_MANAGEMENT), sup_hands=score(imp[s], HANDS_ON),
            wrk_people=st.mean([score(imp[c], PEOPLE_MANAGEMENT) for c in workers]),
            wrk_hands=st.mean([score(imp[c], HANDS_ON) for c in workers])))
    for r in rows:
        r["d_people"] = r["sup_people"] - r["wrk_people"]
        r["d_hands"] = r["sup_hands"] - r["wrk_hands"]

    dp = [r["d_people"] for r in rows]
    dh = [r["d_hands"] for r in rows]
    promotion = dict(
        n_comparisons=len(rows),
        mean_shift_people=st.mean(dp), mean_shift_hands=st.mean(dh),
        median_shift_people=st.median(dp), median_shift_hands=st.median(dh),
        n_people_rises=sum(1 for x in dp if x > 0), n_hands_falls=sum(1 for x in dh if x < 0),
        ratio_people_to_hands=abs(st.mean(dp) / st.mean(dh)) if st.mean(dh) else None)

    # Per-element decomposition of the hands-on shift. Added before drafting because the headline
    # "+0.18" hides two opposite movements: physical work falls, computer and technical work rises.
    # Reporting only the net would be the kind of aggregation this series exists to complain about.
    per_element, phys_only = {}, []
    phys = [e for e in HANDS_ON if e != "4.A.3.b.1"]
    for s in supers:
        mg = soc_major_group(s)
        workers = [c for c in occs if soc_major_group(c) == mg and not is_supervisor(titles[c])]
        if len(workers) < 3:
            continue
        for e in HANDS_ON:
            if e in imp[s] and all(e in imp[c] for c in workers):
                per_element.setdefault(e, []).append(
                    imp[s][e] - st.mean([imp[c][e] for c in workers]))
        phys_only.append(st.mean([imp[s][e] for e in phys if e in imp[s]])
                         - st.mean([st.mean([imp[c][e] for e in phys if e in imp[c]])
                                    for c in workers]))
    hands_decomposition = {
        names.get(e, e): dict(mean_shift=st.mean(v), n_rising=sum(1 for x in v if x > 0), n=len(v))
        for e, v in per_element.items()}
    promotion["mean_shift_hands_excluding_computers"] = st.mean(phys_only)
    promotion["n_hands_excluding_computers_falls"] = sum(1 for x in phys_only if x < 0)

    # Act 2. What rises with job zone across all 911 occupations. Job zone is preparation
    # required, NOT position in a hierarchy: a surgeon is zone 5 and manages nobody. It cannot
    # carry the promotion argument and the post says so; it is here because it complicates the
    # tidy story, which is the reason to publish it.
    def pearson(a, b_):
        ma, mb = st.mean(a), st.mean(b_)
        num = sum((x - ma) * (y - mb) for x, y in zip(a, b_))
        den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b_)) ** 0.5
        return num / den if den else float("nan")

    gwas = sorted({e for c in occs for e in imp[c]})
    zone_corr = {}
    for e in gwas:
        have = [c for c in occs if c in zones and e in imp[c]]
        if len(have) >= 500:
            zone_corr[names.get(e, e)] = dict(
                r=pearson([imp[c][e] for c in have], [zones[c] for c in have]),
                n=len(have), element=e,
                is_people_management=e in PEOPLE_MANAGEMENT, is_hands_on=e in HANDS_ON)

    # Act 3. What the promotion makes you responsible for. Work Context, CX scale.
    # Added after act 1 was computed; flagged as post-hoc in conditions.py and the design document.
    ctx = {}
    for r in read("onet_work_context.csv"):
        if r["Element ID"] in WORK_CONTEXT and r["Scale ID"] == "CX":
            ctx.setdefault(r["O*NET-SOC Code"], {})[r["Element ID"]] = float(r["Data Value"])
    context_shift = {}
    for e, label in WORK_CONTEXT.items():
        sh = []
        for s in supers:
            mg = soc_major_group(s)
            wk = [c for c in ctx if soc_major_group(c) == mg and c in titles
                  and not is_supervisor(titles[c]) and e in ctx[c]]
            if s in ctx and e in ctx[s] and len(wk) >= 3:
                sh.append(ctx[s][e] - st.mean([ctx[c][e] for c in wk]))
        if sh:
            context_shift[label] = dict(mean_shift=st.mean(sh),
                                        n_rising=sum(1 for x in sh if x > 0), n=len(sh))

    # falsification conditions, scored explicitly
    scorecard = dict(
        fc1_people_does_not_rise=bool(st.mean(dp) <= 0),
        fc2_hands_falls_as_much_as_people_rises=bool(abs(st.mean(dh)) >= abs(st.mean(dp))),
        fc3_reverses_in_skilled_groups=bool(
            st.mean([r["d_people"] for r in rows if r["major_group"] in ("47", "49", "51")]) <= 0),
        fc2_note=("This is his original thesis: that the promotion swaps executing for managing. "
                  "It fires if hands-on falls by at least as much as people management rises."))

    out = dict(
        meta=dict(
            source="O*NET 31.0, onetcenter.org, CC BY 4.0",
            scale="Importance (IM), 1 to 5. NOT a measure of hours.",
            n_occupations=len(occs),
            people_activities={k: names.get(k, k) for k in PEOPLE_MANAGEMENT},
            hands_activities={k: names.get(k, k) for k in HANDS_ON},
            excluded_from_people=EXCLUDED_FROM_PEOPLE),
        promotion=promotion, hands_decomposition=hands_decomposition,
        context_shift=context_shift, zone_corr=zone_corr,
        by_major_group=rows, scorecard=scorecard)

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    print(f"{len(rows)} supervisor-to-workers comparisons, {len(occs)} occupations\n")
    print(f"{'major':6s} {'supervisor':52s} {'people':>7s} {'hands':>7s}")
    for r in sorted(rows, key=lambda r: -r["d_people"]):
        print(f"{r['major_group']:6s} {r['supervisor'][:51]:52s} {r['d_people']:+7.2f} {r['d_hands']:+7.2f}")
    print(f"\nmean shift: people {promotion['mean_shift_people']:+.2f}, "
          f"hands-on {promotion['mean_shift_hands']:+.2f}")
    print(f"people management rises in {promotion['n_people_rises']}/{len(rows)}, "
          f"hands-on falls in {promotion['n_hands_falls']}/{len(rows)}")
    print(f"\nhands-on decomposed (the net {promotion['mean_shift_hands']:+.2f} hides two "
          f"opposite movements):")
    for n, d in sorted(hands_decomposition.items(), key=lambda kv: -kv[1]["mean_shift"]):
        print(f"  {d['mean_shift']:+.2f}  {n[:58]:60s} rises in {d['n_rising']}/{d['n']}")
    print(f"  excluding Working with Computers: "
          f"{promotion['mean_shift_hands_excluding_computers']:+.2f}")
    print("\nwhat the promotion makes you responsible for (Work Context, CX 1 to 5):")
    for n, d in sorted(context_shift.items(), key=lambda kv: -kv[1]["mean_shift"]):
        print(f"  {d['mean_shift']:+.2f}  {n[:58]:60s} rises in {d['n_rising']}/{d['n']}")

    print("\nPRE-REGISTERED FALSIFICATION CONDITIONS")
    for k, v in scorecard.items():
        if isinstance(v, bool):
            print(f"  {'FIRED' if v else 'did not fire':>13s}  {k}")


if __name__ == "__main__":
    main()
