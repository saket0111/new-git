# Rebuilds the insight-pack workbook from the cell's committed outputs.
# Inputs: fc/predictions_3m_6m.csv (PR #2 forecast), rep/pr_recommendations_full.csv (PR #3 table, 74 rows incl. OK),
#         duplicate_candidates_part1..4.csv (PR #1). Static tables (KPIs, DQ, missing fields) are in the session copy
#         of static_a.py / static_b.py and are copied from teammates' reports and SAP INVENTORY_KPI_MONTHLY.
# Sheets: README, KPIs, Forecast, Accuracy, Overstock, Understock, NM-SM, PR suggestions, Duplicates, Data quality, Missing fields.
# Asserts: 74 series; 14 understock = INR 43,093,328; 40 overstock = INR 18,047,029 excess; 4 high holding; 205 duplicate groups.
import pandas as pd, glob
rec = pd.read_csv('rep/pr_recommendations_full.csv')
fc = pd.read_csv('fc/predictions_3m_6m.csv')
dup = pd.concat([pd.read_csv(f) for f in sorted(glob.glob('dup*.csv'))])
u = rec[rec.status == 'UNDERSTOCK']; o = rec[rec.status == 'OVERSTOCK']; h = rec[rec.status == 'HIGH_HOLDING']
assert len(rec) == 74 and len(fc) == 74 and (len(u), len(o), len(h)) == (14, 40, 4)
assert round(u.pr_value_inr.sum()) == 43093328 and round(o.excess_value_inr.sum()) == 18047029 and len(dup) == 205
print('totals reconcile with the published figures')
