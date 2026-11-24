# PR and replenishment recommendations (read-only analysis, no SAP writes)

Position date: stock as of 2025-12-31 (latest snapshot in the extract). Forecast: engine output on **consumption quantity** for 2026-01..2026-06, 74 material-plant series (`fc/predictions_6m.csv`, the Data Steward sample). Only these 74 series have a forecast, so only these get a PR quantity.

## Formulas
- Lead time (days) = `PLANNED_DELIVERY_DAYS` + 21 days PR-to-PO lag (observed mean over 126,796 non-back-cast PR/PO pairs). Actual PO-to-first-receipt averages 40.7 days against 38.4 promised, 2.2 days late.
- Daily demand = 6-month forecast total / 181 (negatives clipped to 0).
- Safety stock = z x monthly std dev (last 12 actual months) x sqrt(lead time / 30). z = 2.05 VITAL, 1.65 ESSENTIAL, 1.28 DESIRABLE. The z values are my assumption, not an SAP field.
- Reorder point (ROP) = daily demand x lead time + safety stock.
- Inventory position = closing qty - blocked + open PO qty (on-order) + open PR qty - backorder.
- UNDERSTOCK when position <= ROP. PR quantity = (ROP + 3 months of forecast demand) - position, raised to MOQ and rounded up to the order multiple. PR date = extract date (raise now) because the position is already at or below ROP.
- OVERSTOCK when cover > 12 months of forecast demand and excess over order-up-to + 3 months is positive. HIGH_HOLDING: cover > 12 months but within that allowance.
- OK rows carry a projected ROP-crossing date at the forecast run-rate (a watch date, not an order).

## Limits and open points
- SAP master `REORDER_POINT_QTY` and `SAFETY_STOCK_QTY` in DIM_MATERIAL are far above these (e.g. ROP 564 vs 14.5 here for HZL1000860). Against the master values almost every series would be understock. Master parameters need review by the business.
- 6 series had engine negative flags (clipped to 0), all classed overstock: HZL1002485/02, 1004485/05, 1004488/05, 1004506/04, 1003916/05, 1000872/05. Treat as unconfirmed.
- Stock date is 31 Dec 2025. Re-pull the snapshot before anyone acts on "raise now".
- Not in the extract: vendor, plant-specific lead time, PO quantity, unit of measure, budget. No PR was raised in SAP.
- Series without a forecast (everything outside the 74-series sample) get no PR quantity.
