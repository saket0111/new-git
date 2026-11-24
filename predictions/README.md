# ZSPR/ZSPN consumption-quantity forecast (Jan-Dec 2026 window)

Target: monthly NET CONSUMPTION QUANTITY (movement 261 minus 262). Price is never a target.
Engine: Context Flow AutoML (on-prem runner, AutoGluon time series, WeightedEnsemble champion). All numbers in the CSVs are engine output, unedited. Nothing here is hand-forecast.

## Scope actually forecast
74 material-plant series (41 ZSPR, 33 ZSPN; 40 materials), each with 24 actual months (Jan 2024 - Dec 2025). This is the Data Steward's sample, not the 6,000-material population: the full cleaned table (~1.49M posting rows) cannot leave HANA while Google Cloud is not connected and HANA tools cap at 1,000 rows/query. Population forecast is NOT done.

## Files
- forecast_zspn_3m_6m.csv, forecast_zspr_3m_6m.csv: per material-plant. m3_* = months from the 3m run, m6_* = months from the separate 6m run, h3_total / h6_total = sum of those months. The two runs are independent models, so Jan-Mar differ between them. engine_negative_flag=Y marks any series where the engine returned a negative month (a count cannot be negative; planner must floor or review, values are left as the engine gave them).

## Accuracy (engine hold-out, last h months of the 24 per series, 74 series)
| Horizon | WAPE | MASE | Bias | 80% interval coverage | Champion WQL |
|---|---|---|---|---|---|
| 3m (222 pts) | 0.443 | 0.731 | -3.20 | 0.892 | 0.331 |
| 6m (444 pts) | 0.542 | 0.934 | -2.33 | 0.863 | 0.369 |
Accuracy as 1-WAPE: 55.7% (3m), 45.8% (6m). Negative bias = under-forecasting. Per material-class accuracy not published: the per-row backtest sits in a GCS bucket and Google Cloud is not connected here.

## Horizons and exclusions
| Horizon | Rule | Result |
|---|---|---|
| 3m | engine ran; history >= 2x horizon | 74 of 74 sample series forecast |
| 6m | engine ran; history >= 2x horizon | 74 of 74 sample series forecast |
| 12m | engine REFUSED: "Every series is too short for a 12-step forecast. Each series needs more than 24 rows." | 0 forecast. All 74 excluded: only 24 actual months. 2023 is back-cast, not actuals, and was not used. |
Population-level exclusions (counts from the data-quality note, actual months only): fewer than 6 months -> excluded from 3m (291 materials incl. back-cast count); fewer than 12 months -> excluded from 6m; 12m excluded for every material until >24 actual months exist. Material-by-material exclusion list for the 6,000 needs the full table (not in repo).

## NM/SM classification
The forecasting engine does not classify non-moving/slow-moving. The class here is SAP's own NM_SM_CLASS on DIM_MATERIAL (ZSPR+ZSPN): ACTIVE 5,026, SM 769, NM 184, OBSOLETE 21. All 40 sampled materials are ACTIVE, so the sample says nothing about NM/SM.

## Known caveats
- Gapped months were treated as zero demand (Data Steward note), which makes series intermittent; high WAPE reflects that.
- No shutdown, seasonality or project-timeline covariates exist in the extract: manual adjustments are not applied.
