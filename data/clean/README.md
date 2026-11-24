# data/clean - what is here and what is not

All values are as read from SAP HANA schema `VEDANTA_POC` (read-only). Nothing was altered; issues are flagged in `docs/data-quality/DQ_NOTE_zspr_zspn.md`.

| File | Content | Coverage |
|---|---|---|
| `duplicate_candidates_part1..4.csv` | Potential duplicate material codes (identical description). Columns: group_id, description, types_in_group, material_ids | COMPLETE: 205 groups, 428 codes. Status is POTENTIAL, business to confirm. Concatenate the four parts (one header each). |
| `consumption_qty_sample_wide_part1..2.txt` | Monthly consumption QUANTITY (net 261 minus 262), pipe-delimited: material, plant, type, status, 24 values Jan-2024..Dec-2025 | SAMPLE ONLY: 74 material-plant series (1,776 monthly rows; ZSPR 984 / ZSPN 792) used to exercise the forecasting engine. NOT the full table. |

## Not committed: the full cleaned consumption table
It has about 1.49M movement rows (6,000 materials x 6 plants). The HANA tools return at most 1,000 rows per query and Google Cloud (bucket export) is not connected, so it cannot be moved into the repo from here. `sql/clean_consumption_extract.sql` reproduces it exactly, read-only.

## Reading the sample
- Gaps are shown as 0 only where the source has no 261/262 posting in that month (flagged, not imputed).
- Target is quantity, never price.
- 2023 is back-cast in the source (IS_BACKCAST_PERIOD=Y) and is excluded from this sample.
