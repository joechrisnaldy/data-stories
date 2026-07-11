# External data

The primary Kaggle dataset has study costs only. These two small tables supply the salary
and employment sides, joined by country. Both are committed here with their provenance.

## `oecd_avg_wages_2024.csv`

- **What:** average annual wage per full-time-equivalent dependent employee.
- **Source:** OECD, "Average annual wages" (dataset AV_AN_WAGE), 2024, in USD, PPP-adjusted.
- **Coverage:** 34 OECD countries; 30 of them overlap the cost data's destinations.
- **Note:** economy-wide, not by field of study and not a new-graduate wage. Accessed
  2026-07-11.

## `employment_rate.csv`

- **What:** employment rate, ages 15-64, percent of the working-age population.
- **Source:** OECD employment rate indicator (working-age 15-64), latest available
  (2024-2025), compiled via OECD / Eurostat / ILO. Sweden from Eurostat 2024 (omitted in the
  primary table).
- **Note:** economy-wide, not new-graduate specific and not by field. Used as a relative
  reality-check overlay (stronger versus weaker job markets), not an absolute claim.

Both are joined to the cost data on country, with a small alias map (United States to USA,
United Kingdom to UK, Korea to South Korea, Czechia to Czech Republic).
