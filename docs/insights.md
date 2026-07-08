# Key Insights

> Analysis period: January 2014 – December 2017 | 9,994 order line items | $2.30M revenue

## Executive Summary

Apex Distribution generated **$2.30M in revenue** and **$286K in profit** (12.5% margin) across four years of sales. Revenue grew steadily from $484K (2014) to $733K (2017), but profitability is uneven: **Technology** and **Office Supplies** drive margins above 17%, while **Furniture** contributes only 2.5% margin despite being the second-largest category by revenue. Heavy discounting above 20% destroys profitability, producing a **-37% margin** on those transactions. Central region underperforms all others at 7.9% margin.

---

## Insight 1: Furniture Is a Revenue Trap

**Finding:**  
Furniture generates $742K in revenue (32% of total) but only $18K in profit — a **2.5% margin** vs. 17.4% for Technology. Sub-categories **Tables** (-8.6% margin, -$17.7K profit) and **Bookcases** (-3.0% margin) are actively losing money.

**Business Impact:**  
Furniture creates the illusion of strong sales volume while eroding overall company profitability. Without intervention, revenue growth in this category could actually reduce total profit.

**Recommended Action:**  
Audit Tables and Bookcases pricing and supplier costs. Consider raising prices, renegotiating COGS, or reducing discount authorization for Furniture SKUs. Shift sales incentives toward Technology and Office Supplies.

**Supporting Query:** `sql/04_analysis_queries.sql` — Product Category Performance

---

## Insight 2: Heavy Discounting Destroys Profit

**Finding:**  
| Discount Band | Line Items | Margin |
|---------------|-----------|--------|
| No Discount   | 4,798     | **29.5%** |
| 1–10%         | 94        | 16.6% |
| 11–20%        | 3,709     | 11.6% |
| 21%+          | 1,393     | **-37.3%** |

1,393 line items (14%) carry discounts above 20%, and as a group they are deeply unprofitable.

**Business Impact:**  
Sales reps may be using steep discounts to close deals — especially on Furniture — without visibility into margin impact. This directly explains why 18.7% of all line items have negative profit.

**Recommended Action:**  
Implement discount approval thresholds above 15%. Build a margin-at-quote calculator for the sales team. Review the 1,393 heavily discounted transactions for patterns (category, region, rep).

**Supporting Query:** `sql/04_analysis_queries.sql` — Discount Impact on Profitability

---

## Insight 3: Central Region Underperforms

**Finding:**  
| Region  | Revenue | Margin |
|---------|---------|--------|
| West    | $725K   | 14.9%  |
| East    | $679K   | 13.5%  |
| South   | $392K   | 11.9%  |
| Central | $501K   | **7.9%** |

Central has the second-highest revenue but the lowest margin by a wide margin — nearly half the West's profitability rate.

**Business Impact:**  
Resource allocation and sales strategy in Central may be optimized for volume over profit. This region likely drives the Furniture discount problem.

**Recommended Action:**  
Conduct a regional profitability review. Compare product mix and discount rates in Central vs. West. Consider regional pricing or category mix targets.

**Supporting Query:** `sql/04_analysis_queries.sql` — Regional Performance by Year

---

## Additional Observations

- **Revenue is growing consistently** — 2014 ($484K) → 2017 ($733K), a 51% increase over four years. Profit grew even faster ($50K → $93K).
- **Consumer segment** is the largest by revenue; Corporate and Home Office segments have comparable margins.
- **Data modeling note:** 793 unique customer IDs expand to 4,688 customer-location combinations because customers ship to multiple regions. This was handled in the ETL by modeling geography at the ship-to level (see `docs/data_dictionary.md`).
- **1,871 line items (18.7%)** have negative profit — concentrated in Furniture and heavily discounted orders.
