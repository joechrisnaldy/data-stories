# Data

The data is not committed here (gitignored). Download it from Kaggle.

## Source

[US Public Food Assistance 1 - WIC](https://www.kaggle.com/datasets/jpmiller/publicassistance)
(JohnM / jpmiller), a curated mirror of real **USDA Food and Nutrition Service (FNS)** WIC
administrative report tables, plus Census SAIPE poverty estimates. Public US government data.

WIC is the Special Supplemental Nutrition Program for Women, Infants, and Children.

## Download

```bash
kaggle datasets download -d jpmiller/publicassistance -p .
unzip publicassistance.zip
```

## Structure

- `WICAgencies2013ytd/` ... `WICAgencies2016ytd/`: per fiscal year (Oct-Sept), one CSV per measure
  (Total_Number_of_Participants, Food_Costs, Rebates_Received, Average_Food_Cost_Per_Person,
  Infants_Fully_Breastfed / _Partially_Breastfed / _Fully_Formula-fed, Total_Infants, etc.). Rows =
  state agencies and Indian Tribal Organizations; columns = 12 monthly values + an annual summary.
- `est13_16us/`: Census Small Area Income and Poverty Estimates (SAIPE), 2013-2016.

## Reconciliation notes (IMPORTANT; verified against USDA)

These are aggregated administrative report tables, so two things must be handled before summing:

1. **Drop the "Mountain Plains" regional SUBTOTAL row.** The 7 FNS regions can appear as subtotal
   rows mixed into the state list; "Mountain Plains" is present and double-counts its member states.
   Exclude any of the 7 region names (Mountain Plains, Midwest, Northeast, Southeast, Southwest,
   Western, Mid-Atlantic) and any blank rows. Texas IS present (a stray blank duplicate row aside).
2. **`Food_Costs` is NET of rebates.** The dataset's food cost equals USDA FNS's published NET
   (post-rebate) "Food Costs" line. GROSS food cost = net + rebates. (This is why monthly
   `Average_Food_Cost_Per_Person` can go negative: a big rebate month nets below zero.)

After (1) and (2), the cleaned totals match USDA national figures exactly: FY2016 participation
7.70M, net food cost $3.95B, rebates $1.72B. See `docs/` for the verified USDA/GAO references.

## Note

Data covers FY2013-2016 (Oct 2012 - Sept 2016). The essay frames it as how the benefit works and
adds current USDA figures (FY2024) for context. Descriptive administrative data; not policy advocacy.
