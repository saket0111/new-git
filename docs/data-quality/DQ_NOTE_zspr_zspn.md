# Data-quality note: SAP stores & spares extract (ZSPR / ZSPN)

Source: SAP HANA schema `VEDANTA_POC` (read-only). Profiled 2026-11-24. No source value was altered; issues are flagged only.

## Scope and row counts
| Table | Rows before | Rows after ZSPR/ZSPN filter | Note |
|---|---|---|---|
| DIM_MATERIAL | 6,000 | 6,000 (ZSPR 3,728 / ZSPN 2,272) | extract already holds only these two types |
| FACT_MATERIAL_MOVEMENT (4 parts) | 1,664,301 | 1,664,301 | every row joins to a ZSPR/ZSPN material; 0 orphans |
| of which consumption (261 issue / 262 reversal) | | 1,490,852 | forecast target = quantity |
| FACT_INVENTORY_SNAPSHOT (3 parts) | 1,249,812 | 1,249,812 | 36 month-ends 2023-01-31 to 2025-12-31, 6 plants |
| FACT_PURCHASE_REQUISITION | 180,690 | 180,690 | 5,773 materials |
| FACT_PURCHASE_ORDER | 172,044 | 172,044 | every PO links to a PR |

Duplicate rows removed: 0 (no duplicate keys in movements, snapshots, PR or PO).

## Checks
- Missing plant / material / posting date: 0 / 0 / 0. Plants: 6 (HZL_DEMO_01..06) plus aggregate row ALL_PLANTS in DIM_PLANT (not used in facts).
- Missing category (material group): 0. 12 groups. Business-category mapping is `PROPOSED - business to confirm`.
- Negative or zero quantity: 0 (quantities are unsigned; sign comes from movement type: 261/102/702 reduce stock, 262/101/701 add).
- Negative closing stock: 0. Zero-stock snapshot rows: 157,833.
- Missing criticality / unit cost / planned delivery days: 0. Lead time range 5 to 205 days. 0 non-positive costs.
- PR status: APPROVED 172,044; APPROVED_AWAITING_PO 1,413; CANCELLED 7,233. PO status: RECEIVED 144,418; PARTIALLY_RECEIVED 17,796; OPEN 8,784; OPEN_DELAYED 1,046.

## Issues found (flagged, not fixed)
1. **2023 is back-cast.** All 2023 movement rows have IS_BACKCAST_PERIOD=Y (132,526 rows). Actual history is Jan-2024 to Dec-2025 = 24 months.
2. **Gapped history.** 5,214 of 6,000 materials have months with no consumption between first and last posting (62,475 gap-months). Mean 18.1 active months vs 28.5 months span. Gaps are treated as zero demand.
3. **Net-negative months.** 643 material-months (426 materials) where reversals (262) exceed issues (261); 870 net-zero months.
4. **Unit of measure.** No UoM on movement rows. UoM is per material group in REF_MATERIAL_GROUP: EA (10 groups), SET (FASTENERS), L (LUBRICANTS). Fractional quantities occur only on L items (1,987 of 4,036 consumption rows), so units look consistent. Do not sum across UoM.
5. **Duplicate-code candidates.** 205 identical-description groups covering 428 codes (223 redundant); 100 groups mix ZSPR and ZSPN. No two materials share SOURCE_MATERIAL_ID, and unit costs often differ, so these need business review. List: `data/clean/duplicate_candidates.csv`.
6. **Master vs movements.** LAST_CONSUMPTION_DATE differs from the last 261/262 posting for 219 materials. All 21 OBSOLETE materials have no 2025 consumption (consistent); 1,031 NM/OBSOLETE material-plant rows still hold stock at 2025-12-31.

## Months of consumption history per material (months with a 261/262 posting)
| Months | Materials (all periods) |
|---|---|
| <6 | 291 |
| 6-11 | 1,207 |
| 12-23 | 2,953 |
| 24-35 | 1,377 |
| 36+ | 172 |

Actual-only (excluding back-cast): >=12 months 3,932 materials; >=18 months 1,553; >=24 months 215. Per-material history needs `sql/clean_consumption_extract.sql` (row-level table not committed, see below).

## Forecast horizon support (rule of thumb: at least 2x horizon in months of history)
- 3-month: supported for materials with >=6 months (5,709 with all periods).
- 6-month: >=12 months (4,502 all-period; 3,932 actual-only).
- 12-month: >=24 months (1,549 all-period; only 215 actual-only). Needs commander decision on using back-cast.

## Fields absent from the extract
- Unit of measure on movement, stock, PR and PO rows (only a per-group base UoM exists).
- PO quantity, PO material and PO plant (FACT_PURCHASE_ORDER links via PR only; price is present).
- Vendor part number and vendor on the material master (duplicate checks use description and source code only).
- Plant-specific lead time, safety stock and reorder point (master is plant-agnostic).
- Confirmed business category.
- Present and usable: unit cost (INR), criticality (VITAL/ESSENTIAL/DESIRABLE), planned delivery days, ABC/XYZ, NM/SM class.

## Why the row-level cleaned table is not in this commit
The HANA tools available return at most 1,000 rows per query and the Google Cloud export path is not connected, so the 1.49M-row consumption table cannot be moved into the repository from here. `sql/clean_consumption_extract.sql` reproduces it exactly (read-only). Once Google Cloud is connected, `hana_export_query_to_gcs` can land it in a bucket.
