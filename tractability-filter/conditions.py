"""Pre-registered condition list and tractability coding for Post 23.

Committed BEFORE any regression is run, per docs/2026-08-10-tractability-filter-design.md
section 3.2. Section 3.6 of that document records, against myself, that a vetting table of
trials per unit of burden was read before this coding was written down, so the coding is
theory-driven but not blind. The headline evidence of the post does not depend on it.

Coding rule, applied to every condition identically:

  T1 TARGET   Is there a validated biological target or identified causal agent that an
              intervention can act on? A pathogen, receptor, protein, tumour, or defined
              autoimmune process. Yes or no.
  T2 ENDPOINT Is the primary outcome objectively instrument-measurable rather than
              patient-reported or clinician-rated on a scale? Survival, viral load, HbA1c,
              FEV1, MRI lesion count, seizure count, audiometry: yes. A pain score, mood
              scale or functional rating: no.

A note on wording, added in round 4 and CORRECTED in round 5 after a refuter read all 34 entries.

Round 4's version claimed that no condition here was coded on the "identified causal agent" limb
alone. That is false. HIV/AIDS, tuberculosis and malaria are coded t1=True on notes that name a
pathogen or parasite and no drug target at all, and "identified" is the rule's own word from that
limb. Two notes below refuse on "no validated causal target" (Depressive disorders and Alcohol use
disorders, plus Anxiety disorders and Bipolar disorder which inherit it through "As above"), while
only Road injury and Falls refuse in the rule's own word, "biological".

The uncomfortable consequence, stated rather than smoothed over: if a pathogen satisfies the second
limb, a crash is arguably an identified causal agent too, and Road injury's t1=False becomes a
judgement rather than a reading of the rule. The pre-registration forbids reclassifying a condition
after seeing its residual, so nothing here is changed. What the post does instead is report the
sensitivity: recoding road injury and falls as having a target takes the effect from t -3.05 to
-1.06 and the variation accounted for from 28 percent to 10. That is the largest single thing
anyone can do to this result and it is in the method notes.

  class = "tractable"  if T1 and T2
          "partly"     if exactly one
          "intractable" if neither

`ct_terms` lists alternate ClinicalTrials.gov condition queries. The build uses the term
returning the MOST studies, so the test is loaded against the thesis by construction.

`ghe_name` must match a WHO Global Health Estimates cause label exactly. Codes are NOT used:
GHE code 970 is Epilepsy and 980 is Multiple sclerosis, the reverse of the obvious guess.
"""

CONDITIONS = [
    # ---- cardiovascular, metabolic, respiratory -------------------------------------
    dict(ghe_name="Ischaemic heart disease", nih="Heart Disease - Coronary Heart Disease", nih_alt=["Heart Disease"],
         ct_terms=["coronary artery disease", "ischemic heart disease",
                   "coronary artery disease OR ischemic heart disease"],
         t1=True, t2=True,
         note="Atherosclerotic process and lipid targets; endpoints are events and mortality."),
    dict(ghe_name="Stroke", nih="Stroke",
         ct_terms=["stroke", "cerebrovascular accident", "stroke OR cerebrovascular accident"],
         t1=True, t2=True,
         note="Thrombus or haemorrhage as target; imaging and mortality endpoints."),
    dict(ghe_name="Diabetes mellitus", nih="Diabetes",
         ct_terms=["diabetes mellitus", "diabetes", "type 2 diabetes OR type 1 diabetes"],
         t1=True, t2=True, note="Glucose and insulin pathways; HbA1c is objective."),
    dict(ghe_name="Chronic obstructive pulmonary disease", nih="Chronic Obstructive Pulmonary Disease",
         ct_terms=["COPD", "chronic obstructive pulmonary disease", "emphysema OR COPD"],
         t1=True, t2=True, note="Airway obstruction; FEV1 and exacerbation counts."),
    dict(ghe_name="Asthma", nih="Asthma",
         ct_terms=["asthma"], t1=True, t2=True,
         note="Airway inflammation with defined mediators; FEV1 and exacerbations."),
    dict(ghe_name="Cirrhosis of the liver", nih="Liver Disease",
         ct_terms=["liver cirrhosis", "cirrhosis", "liver cirrhosis OR cirrhosis"],
         t1=True, t2=True, note="Fibrosis with histological and elastography endpoints."),

    # ---- cancers ---------------------------------------------------------------------
    dict(ghe_name="Trachea, bronchus, lung cancers", nih="Lung Cancer",
         ct_terms=["lung cancer", "lung neoplasms", "lung cancer OR lung neoplasms"],
         t1=True, t2=True, note="Tumour as target; survival and response are objective."),
    dict(ghe_name="Breast cancer", nih="Breast Cancer",
         ct_terms=["breast cancer", "breast neoplasms"], t1=True, t2=True, note="As above."),
    dict(ghe_name="Colon and rectum cancers", nih="Colorectal Cancer",
         ct_terms=["colorectal cancer", "colonic neoplasms OR rectal neoplasms"],
         t1=True, t2=True, note="As above."),
    dict(ghe_name="Prostate cancer", nih="Prostate Cancer",
         ct_terms=["prostate cancer", "prostatic neoplasms"], t1=True, t2=True, note="As above."),
    dict(ghe_name="Pancreas cancer", nih="Pancreatic Cancer",
         ct_terms=["pancreatic cancer", "pancreatic neoplasms"], t1=True, t2=True, note="As above."),
    dict(ghe_name="Leukaemia", nih=None,   # no general leukaemia category exists in RCDC; money analysis excludes it
         ct_terms=["leukemia", "leukaemia", "leukemia OR leukaemia"], t1=True, t2=True,
         note="As above."),

    # ---- infectious ------------------------------------------------------------------
    dict(ghe_name="HIV/AIDS", nih="HIV/AIDS",
         ct_terms=["HIV infections", "HIV", "HIV OR AIDS"], t1=True, t2=True,
         note="Identified pathogen; viral load is objective."),
    dict(ghe_name="Tuberculosis", nih="Tuberculosis",
         ct_terms=["tuberculosis"], t1=True, t2=True, note="Identified pathogen; culture conversion."),
    dict(ghe_name="Malaria", nih="Malaria",
         ct_terms=["malaria"], t1=True, t2=True, note="Identified parasite; parasitaemia is objective."),

    # ---- neurological ----------------------------------------------------------------
    dict(ghe_name="Multiple sclerosis", nih="Multiple Sclerosis",
         ct_terms=["multiple sclerosis"], t1=True, t2=True,
         note="Autoimmune demyelination; MRI lesion count and relapse rate."),
    dict(ghe_name="Epilepsy", nih="Epilepsy",
         ct_terms=["epilepsy", "seizures", "epilepsy OR seizures"], t1=True, t2=True,
         note="Ion channel and focus targets; seizure counts and EEG."),
    dict(ghe_name="Alzheimer disease and other dementias",
         nih="Alzheimer's Disease including Alzheimer's Disease Related Dementias (AD/ADRD)",
         ct_terms=["dementia", "alzheimer disease", "dementia OR alzheimer disease"],
         t1=True, t2=False,
         note="Amyloid and tau are targets, but primary endpoints remain cognitive and "
              "functional rating scales."),
    dict(ghe_name="Parkinson disease", nih="Parkinson's Disease",
         ct_terms=["parkinson disease", "parkinsons disease"], t1=True, t2=False,
         note="Dopaminergic target; UPDRS is a clinician-rated scale."),
    dict(ghe_name="Migraine", nih="Migraine",
         ct_terms=["migraine", "migraine disorders"], t1=True, t2=False,
         note="CGRP is a validated target; headache days are patient-reported."),

    # ---- mental and substance use ----------------------------------------------------
    dict(ghe_name="Depressive disorders", nih="Depression",
         ct_terms=["depression", "depressive disorder", "major depressive disorder OR depression"],
         t1=False, t2=False,
         note="No validated causal target; endpoints are rating scales."),
    dict(ghe_name="Anxiety disorders", nih="Anxiety Disorders",
         ct_terms=["anxiety disorder", "anxiety", "anxiety OR anxiety disorders"],
         t1=False, t2=False, note="As above."),
    dict(ghe_name="Bipolar disorder", nih="Bipolar Disorder",
         ct_terms=["bipolar disorder"], t1=False, t2=False, note="As above."),
    dict(ghe_name="Schizophrenia", nih="Schizophrenia",
         ct_terms=["schizophrenia"], t1=True, t2=False,
         note="Dopamine D2 is a validated drug target; PANSS is a rating scale."),
    dict(ghe_name="Alcohol use disorders", nih="Alcoholism, Alcohol Use and Health",
         ct_terms=["alcohol use disorder", "alcoholism", "alcohol use disorder OR alcoholism"],
         t1=False, t2=False,
         note="No validated causal target; drinking days are self-reported."),
    dict(ghe_name="Drug use disorders", nih="Substance Misuse", nih_alt=["Opioids", "Drug Abuse (NIDA only)"],
         ct_terms=["substance use disorder", "drug use disorder", "opioid use disorder",
                   "substance use disorder OR drug abuse"],
         t1=True, t2=True,
         note="BORDERLINE, declared in advance. Coded tractable because opioid use disorder has "
              "receptor targets and urine toxicology is objective, even though measured effort is "
              "low. Cuts against the thesis and stays in."),

    # ---- musculoskeletal and sense organ ---------------------------------------------
    dict(ghe_name="Back and neck pain", nih="Back Pain", nih_alt=["Chronic Pain"],
         ct_terms=["back pain", "low back pain", "neck pain", "back pain OR neck pain",
                   "chronic low back pain", "spinal pain"],
         t1=False, t2=False,
         note="No validated target for the common presentation; pain scores are self-reported."),
    dict(ghe_name="Osteoarthritis", nih="Osteoarthritis",
         ct_terms=["osteoarthritis"], t1=False, t2=True,
         note="No validated disease-modifying target; radiographic joint space is objective."),
    dict(ghe_name="Rheumatoid arthritis", nih="Rheumatoid Arthritis",
         ct_terms=["rheumatoid arthritis"], t1=True, t2=True,
         note="TNF and IL-6 are validated targets; inflammatory markers and radiographic "
              "progression are objective."),
    dict(ghe_name="Other hearing loss", nih="Hearing Loss",
         ct_terms=["hearing loss", "deafness", "hearing loss OR deafness",
                   "sensorineural hearing loss"],
         t1=False, t2=True,
         note="No validated target for restoring hair cells; audiometry is objective. The clearest "
              "case where an objective endpoint exists but nothing to aim at does."),
    dict(ghe_name="Uncorrected refractive errors", nih="Eye Disease and Disorders of Vision",
         ct_terms=["refractive error", "myopia", "refractive errors OR myopia"],
         t1=True, t2=True,
         note="BORDERLINE, declared in advance. Coded tractable, but the remaining problem is "
              "delivery of spectacles rather than discovery, which depresses trial counts for a "
              "reason the coding does not capture. Cuts against the thesis and stays in."),

    # ---- injuries --------------------------------------------------------------------
    dict(ghe_name="Road injury", nih="Physical Injury - Accidents and Adverse Effects",
         ct_terms=["road traffic accident", "motor vehicle accident", "traffic accident",
                   "road traffic accident OR motor vehicle accident", "road traffic injury"],
         t1=False, t2=True,
         note="No biological target; deaths and injuries are objectively counted."),
    dict(ghe_name="Falls", nih="Physical Injury - Accidents and Adverse Effects",
         ct_terms=["accidental falls", "falls", "fall prevention", "accidental falls OR falls"],
         t1=False, t2=True, note="No biological target; falls are objectively counted."),
    dict(ghe_name="Self-harm", nih="Suicide",
         ct_terms=["suicide", "self-harm", "suicide OR self-harm", "suicidal ideation"],
         t1=False, t2=False,
         note="No validated target; the objective endpoint is too rare to power trials, so "
              "measured outcomes are ideation scales."),
]


def tclass(c):
    """Tractability class from the two pre-registered axes."""
    return "tractable" if (c["t1"] and c["t2"]) else ("intractable" if not (c["t1"] or c["t2"]) else "partly")


CLASS_ORDER = ["tractable", "partly", "intractable"]
