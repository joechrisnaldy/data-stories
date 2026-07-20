# Data

This post does not use a single Kaggle dataset. It is built from four real, public, primary
sources, hand-curated into the small CSVs here. Every number was verified against the primary
source (exact quote on file in `docs/`). No synthetic data is used. (A synthetic Kaggle dataset on
this topic was reviewed and rejected: it was 74% future rows to 2060 and its outcomes were
formula-generated, so it could not support any real claim.)

## Sources

### `cdc_yrbs_sadness.csv`
Share of US high school students who reported persistent feelings of sadness or hopelessness (felt
so sad or hopeless almost every day for 2+ weeks that they stopped usual activities), by year and
sex. Question H26. Odd years 2011-2023, Total/Female/Male, with 95% CIs.
- Centers for Disease Control and Prevention. YRBS Explorer (national high school), question H26.
  https://yrbs-explorer.services.cdc.gov/
- 2023 values independently confirmed in CDC MMWR su7304a9 (Verlenden et al., 2024).
  https://www.cdc.gov/mmwr/volumes/73/su/su7304a9.htm

### `pew_certainty.csv`
US teens saying social media has a "mostly negative" effect, split by target (people their age vs
themselves), 2022 and 2025. The 2022 personal figure (9%) is medium-confidence and is not charted.
- Pew Research Center. (2025, April 22). Social media and teens' mental health: What teens and
  their parents say. https://www.pewresearch.org/internet/2025/04/22/teens-social-media-and-mental-health/

### `orben_2019_betas.csv`
Standardized median regression coefficients (beta) of everyday behaviors on adolescent well-being
from a specification-curve analysis. Negative beta = associated with lower well-being. To keep the
comparison honest, the charted bars all come from ONE dataset (the US YRBS); "wearing glasses" is
from the UK MCS (beta -0.061) and is kept here for reference but noted separately in the essay.
- Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being and digital
  technology use. Nature Human Behaviour, 3(2), 173-182. https://doi.org/10.1038/s41562-018-0506-1

### `parry_2021_selfreport.csv`
Agreement between self-reported and objectively logged digital media use: the accuracy split of 49
comparisons (over/under/accurate within 5%), and the meta-analytic correlations for general and
problematic use.
- Parry, D. A., Davidson, B. I., Sewall, C. J. R., Fisher, J. T., Mieczkowski, H., & Quintana,
  D. S. (2021). A systematic review and meta-analysis of discrepancies between logged and
  self-reported digital media use. Nature Human Behaviour, 5(11), 1535-1547.
  https://doi.org/10.1038/s41562-021-01117-5

## Key honesty notes (carried into the essay)

- The Surgeon General's 2023 advisory does NOT claim proven harm; it states the evidence on safety
  is not yet sufficient and calls for more research.
- Teen distress eased slightly from 2021 to 2023; the trend is not monotonic.
- Parry et al. found self-reports are imprecise in BOTH directions; there is no statistically
  supported systematic over-estimation (ratio of means R = 1.21 but P = 0.129, CI spans both).
- Orben's "variance explained" is partial eta-squared; the specification counts are the number
  IDENTIFIED (hundreds of millions for the MCS), of which a tractable subset was actually run.
