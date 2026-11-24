# Monthly insight pack: SAP stores and spares (ZSPR / ZSPN), Nov 2026

Position date 31 Dec 2025. SAP access read-only. No PR raised in SAP.

## Deliverables (binary, held in the session, NOT in git)
- `Insight_Pack_ZSPR_ZSPN_2026-11.xlsx`: sheets README, KPIs, Forecast, Accuracy, Overstock, Understock, NM-SM, PR suggestions, Duplicates, Data quality, Missing fields.
- `Insight_Pack_ZSPR_ZSPN_2026-11.pptx`: 5 slides (headline KPIs, forecast, key risks, recommended PRs, data and limits).

The GitHub tool available to this seat writes text only and would corrupt a .xlsx/.pptx, so the binaries are not committed here. Attach them from the session.

`build_workbook.py` here is a reconciliation check only: it re-derives the headline counts and values from the PR #2 / PR #3 / PR #1 outputs and asserts they equal the published figures. It does not generate the workbook.

## Where every number comes from
| Figure | Source |
|---|---|
| Gross inventory value, days on hand, turnover, critical-spares availability, SAP excess | SAP `VEDANTA_POC.INVENTORY_KPI_MONTHLY`, 2025-12-31, ALL_PLANTS (labelled SIMULATED_BASELINE) |
| 3m / 6m forecast, WAPE | Demand Planner, PR #2 (`predictions/`) |
| 14 understock, 40 overstock, 4 high holding, PR values, NM/SM, MRP classes | PR & Replenishment Advisor, PR #3 (`recommendations/`) |
| Data-quality, duplicates (205 groups / 428 codes) | Data Steward, PR #1 |

## Limits
- Only 74 of 34,707 material-plant series are forecast. No 12-month forecast (engine needs more than 24 months; series have 24).
- Missing from the extract: vendor, plant-specific lead time, PO quantity, unit of measure, budget.
- Slow/non-moving/obsolete value in the SAP KPI table (INR 135.2 / 31.6 / 42.9 Cr) differs from the row-level classification (174.3 / 49.1 / 32.2 Cr). Both are shown and neither is adjusted.
- The session dashboard could not be read back from this seat; figures match the teammates' published reports, not a dashboard read-back.
