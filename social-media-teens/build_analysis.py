"""Post 11 analysis: 'Everyone Knows Social Media Is Wrecking Teens. The Evidence Doesn't.'
Loads the four verified real-source CSVs (CDC YRBS, Pew, Orben & Przybylski 2019, Parry et al. 2021),
prints full tables, and writes results.json for the four charts. No synthetic data; every number is
traceable to a primary source (see data/README.md and docs/)."""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
D = BASE / "data"

# --- Pillar 1: the certainty (Pew) ---
pew = pd.read_csv(D / "pew_certainty.csv")
print("=== Pew: teens saying social media is 'mostly negative' ===")
print(pew.to_string(index=False))
certainty = {
    "peers_2022": int(pew.query("target=='people their age (peers)' and year==2022").pct.iloc[0]),
    "peers_2025": int(pew.query("target=='people their age (peers)' and year==2025").pct.iloc[0]),
    "self_2025": int(pew.query("target=='them personally' and year==2025").pct.iloc[0]),
}

# --- Pillar 2: the crisis (CDC YRBS) ---
cdc = pd.read_csv(D / "cdc_yrbs_sadness.csv")
print("\n=== CDC YRBS: persistent sadness/hopelessness (%), by group ===")
piv = cdc.pivot(index="year", columns="group", values="pct")[["Total", "Female", "Male"]]
print(piv.to_string())
crisis = {g: [{"year": int(r.year), "pct": float(r.pct), "lo": float(r.ci_low), "hi": float(r.ci_high)}
              for r in cdc[cdc.group == g].sort_values("year").itertuples()]
          for g in ["Total", "Female", "Male"]}
crisis_summary = {"total_2011": 28.5, "total_2021": 42.3, "total_2023": 39.7,
                  "female_2011": 35.9, "female_2021": 56.6, "female_2023": 52.6,
                  "male_2011": 21.5, "male_2021": 28.6, "male_2023": 27.7,
                  "female_male_gap_2023": round(52.6 - 27.7, 1)}

# --- Pillar 3: the contested link (Orben & Przybylski 2019); YRBS-only for a fair comparison ---
orben = pd.read_csv(D / "orben_2019_betas.csv")
yrbs = orben[orben.dataset == "YRBS"].sort_values("beta").reset_index(drop=True)
print("\n=== Orben & Przybylski 2019: standardized beta on well-being (YRBS only, ascending) ===")
print(yrbs[["behavior", "beta", "is_technology"]].to_string(index=False))
contested = {"variance_explained_pct": 0.4,
             "tech_beta_yrbs": float(yrbs.query("is_technology==1").beta.iloc[0]),
             "bars": [{"behavior": r.behavior, "beta": float(r.beta), "is_tech": int(r.is_technology)}
                      for r in yrbs.itertuples()],
             "glasses_mcs_beta": -0.061}

# --- Pillar 4: the broken ruler (Parry et al. 2021) ---
parry = pd.read_csv(D / "parry_2021_selfreport.csv")
acc = parry[parry.metric == "accuracy_of_49_comparisons"]
cor = parry[parry.metric == "correlation"]
print("\n=== Parry et al. 2021: accuracy of 49 self-report vs logged comparisons ===")
print(acc[["category", "value"]].to_string(index=False))
print("--- correlations ---")
print(cor[["category", "value", "ci_low", "ci_high"]].to_string(index=False))
ruler = {"accuracy": [{"category": r.category, "pct": float(r.value)} for r in acc.itertuples()],
         "correlations": [{"measure": r.category, "r": float(r.value), "lo": float(r.ci_low),
                           "hi": float(r.ci_high)} for r in cor.itertuples()]}

out = {"certainty": certainty, "crisis": crisis, "crisis_summary": crisis_summary,
       "contested": contested, "ruler": ruler}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("\nwrote results.json")
print("certainty:", certainty)
print("crisis 2023 female-male gap:", crisis_summary["female_male_gap_2023"], "pts")
print("tech beta (YRBS):", contested["tech_beta_yrbs"], "| variance explained:", contested["variance_explained_pct"], "%")
print("ruler accuracy:", [(a["category"], a["pct"]) for a in ruler["accuracy"]])
