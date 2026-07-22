"""Post 13 analysis: the lung-cancer survey as a selection-bias FOIL.
Reads the raw Kaggle file (mysarahmadbhat/lung-cancer) and computes the numbers that make the trap
visible: the target is ~87% cancer with no control group, smoking is NOT a significant predictor
(Fisher OR ~1.4, p ~0.4), and it ranks LAST of 15 features by correlation with cancer.
These are used ONLY to illustrate why the file cannot answer 'does smoking cause cancer', never as
evidence about real causation. Writes results.json for the two foil charts (1 and 2)."""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

warnings.filterwarnings("ignore")
BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "survey lung cancer.csv")
df.columns = [c.strip() for c in df.columns]

SYM = [c for c in df.columns if c not in ("GENDER", "AGE", "LUNG_CANCER")]
d = df.copy()
for c in SYM:
    d[c] = d[c].map({1: 0, 2: 1})          # survey codes NO=1 / YES=2  ->  0 / 1
d["CANCER"] = d["LUNG_CANCER"].str.strip().map({"YES": 1, "NO": 0})
d["MALE"] = (d["GENDER"].str.strip() == "M").astype(int)

# --- headline foil facts ---
n = len(df)
dupes = int(df.duplicated().sum())
cancer_rate = float(d["CANCER"].mean())
p_smoker = float(d[d.SMOKING == 1]["CANCER"].mean())
p_non = float(d[d.SMOKING == 0]["CANCER"].mean())
tab = pd.crosstab(d["SMOKING"], d["CANCER"]).reindex(index=[0, 1], columns=[0, 1]).fillna(0).values
odds, pval = stats.fisher_exact(tab)

print("=== the file, as learners use it (raw) ===")
print(f"rows={n}  exact duplicate rows={dupes}  cancer rate={cancer_rate:.3f} "
      f"({int(d.CANCER.sum())} YES / {int((1-d.CANCER).sum())} NO)")
print(f"P(cancer | smoker)={p_smoker:.3f}  P(cancer | non-smoker)={p_non:.3f}")
print(f"Fisher exact: OR={odds:.2f}  p={pval:.3f}  (smoking vs cancer)")

# --- feature ranking by correlation with cancer (chart 1) ---
LABEL = {
    "ALLERGY": "Allergy", "ALCOHOL CONSUMING": "Alcohol", "SWALLOWING DIFFICULTY": "Swallowing difficulty",
    "WHEEZING": "Wheezing", "COUGHING": "Coughing", "CHEST PAIN": "Chest pain",
    "PEER_PRESSURE": "Peer pressure", "YELLOW_FINGERS": "Yellow fingers", "FATIGUE": "Fatigue",
    "ANXIETY": "Anxiety", "CHRONIC DISEASE": "Chronic disease", "AGE": "Age", "MALE": "Male",
    "SHORTNESS OF BREATH": "Shortness of breath", "SMOKING": "Smoking",
}
feats = SYM + ["MALE", "AGE"]
rows = [{"feature": LABEL.get(c, c), "raw": c,
         "corr": float(np.corrcoef(d[c], d["CANCER"])[0, 1])} for c in feats]
rank = sorted(rows, key=lambda r: abs(r["corr"]), reverse=True)
print("\n=== features ranked by correlation with cancer (SMOKING should be last) ===")
for i, r in enumerate(rank, 1):
    print(f"{i:2d}. {r['feature']:22s} {r['corr']:+.3f}")
smoking_rank = 1 + next(i for i, r in enumerate(rank) if r["raw"] == "SMOKING")
print(f"\nSMOKING rank = {smoking_rank} of {len(rank)}")


# --- robustness: does a SMARTER (adjusted) analysis rescue a smoking signal? ---
# Honesty check for the method notes: adjusting for symptoms (which are CONSEQUENCES of cancer,
# i.e. colliders) in an already-selected sample can MANUFACTURE an association rather than recover a
# real one. The nudge to "significance" is also fragile: it vanishes once the 33 duplicate rows go.
def _ll(dd, cols):
    y = dd["CANCER"].values
    if cols:
        X = dd[cols].astype(float).values
        p = LogisticRegression(C=1e6, solver="lbfgs", max_iter=5000).fit(X, y).predict_proba(X)[:, 1]
    else:
        p = np.full(len(y), y.mean())
    return -log_loss(y, p, normalize=False)


def _adjusted_smoking(dd):
    ctrl = ["AGE", "MALE", "ALLERGY", "ALCOHOL CONSUMING", "WHEEZING", "COUGHING", "CHEST PAIN"]
    X = dd[ctrl + ["SMOKING"]].astype(float).values
    beta = LogisticRegression(C=1e6, solver="lbfgs", max_iter=5000).fit(
        X, dd["CANCER"].values).coef_[0][-1]
    lr = 2 * (_ll(dd, ctrl + ["SMOKING"]) - _ll(dd, ctrl))   # likelihood-ratio test for adding smoking
    return float(np.exp(beta)), float(stats.chi2.sf(lr, 1))


adj_or_raw, adj_p_raw = _adjusted_smoking(d)
d_dedup = d[~df.duplicated().values]
adj_or_dd, adj_p_dd = _adjusted_smoking(d_dedup)
ROBUST = {"adj_or_raw": round(adj_or_raw, 2), "adj_p_raw": round(adj_p_raw, 3),
          "adj_or_dedup": round(adj_or_dd, 2), "adj_p_dedup": round(adj_p_dd, 3)}
print(f"adjusted smoking (age+sex+symptoms): raw OR={adj_or_raw:.2f} p={adj_p_raw:.3f} (n={len(d)}) | "
      f"dedup OR={adj_or_dd:.2f} p={adj_p_dd:.3f} (n={len(d_dedup)})")

# --- verified real epidemiology (external constants; see docs + sourcing dossier). ---
# Every value here is pinned to a primary-source verbatim quote (verified-or-omit).
REAL = {
    # smoking's share of lung cancer: NCI PDQ "9 of 10 cases in men, 8 of 10 in women"; CDC "80-90% of deaths"
    "share_men_cases": "9 out of 10", "share_women_cases": "8 out of 10",
    "share_band_low": 80, "share_band_high": 90,
    # relative risk of DYING of lung cancer vs never-smokers (mortality), rising with intensity
    "rr_never": 1.0,
    "rr_lt1_cig": 9.1,       # Inoue-Choi et al. 2017 JAMA Intern Med, <1 cig/day HR 9.12 (NIH-AARP, n=290,215)
    "rr_1to10_cig": 11.6,    # Inoue-Choi et al. 2017, 1-10 cig/day HR 11.61
    "rr_regular": 25.0,      # Thun et al. 2013 NEJM, contemporary current smokers ~25x (women 25.66 / men 24.97)
    "rr_britdoctors": 15.9,  # Doll & Peto 2004 BMJ, current cigarette smokers lung-cancer mortality ratio (Table 6)
    # what the Kaggle file "detected" (this analysis; not significant) -- for the contrast line
    "file_or": None,         # set below from the foil computation
    # burden + history
    "us_lung_deaths_2026est": 124990,   # NCI SEER 2026 estimate
    "die_years_younger": 10,            # Doll & Peto 2004: cigarette smokers died ~10 years younger
    # Indonesia (GATS 2021, Ministry of Health / WHO / CDC)
    "id_men_pct": 65.5, "id_overall_pct": 34.5, "id_women_pct": 3.3,
    "id_users_m": 70.2, "id_daily_men_pct": 52.3, "id_init_age": 15.9,
}
REAL["file_or"] = round(float(odds), 2)

out = {
    "foil": {
        "n": n, "dupes": dupes, "cancer_rate": round(cancer_rate, 4),
        "n_cancer": int(d.CANCER.sum()), "n_nocancer": int((1 - d.CANCER).sum()),
        "p_cancer_smoker": round(p_smoker, 4), "p_cancer_nonsmoker": round(p_non, 4),
        "n_smoker": int((d.SMOKING == 1).sum()), "n_nonsmoker": int((d.SMOKING == 0).sum()),
        "fisher_or": round(float(odds), 3), "fisher_p": round(float(pval), 3),
        "smoking_rank": smoking_rank, "n_features": len(rank),
    },
    # ranked features for chart 1 (label + corr), most to least correlated with cancer
    "ranking": [{"feature": r["feature"], "corr": round(r["corr"], 4),
                 "is_smoking": r["raw"] == "SMOKING"} for r in rank],
    # real-epidemiology figures (charts 3-4), verified against primaries (see docs + References)
    "real": REAL,
    # robustness: even an adjusted model only nudges smoking to a fragile, collider-driven signal
    "robustness": ROBUST,
}
(BASE / "results.json").write_text(json.dumps(out, indent=2))
print("\nwrote results.json (foil + verified real epidemiology + robustness)")
