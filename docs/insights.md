# Insights

Jan 2014 - Dec 2017 | 9,994 line items | $2.30M revenue

## Summary

Apex Distribution did $2.30M in revenue and $286K in profit (12.5% margin) over four years. Revenue climbed from $484K in 2014 to $733K in 2017, but margins vary a lot by category. Technology and Office Supplies run above 17% margin. Furniture is the second-biggest category by revenue but only 2.5% margin. Discounts over 20% are deeply unprofitable (-37% margin as a group). Central region has the worst margin at 7.9%.

## 1. Furniture looks good on revenue, not on profit

Furniture brought in $742K (32% of revenue) but only $18K in profit, a 2.5% margin vs. 17.4% for Technology.

The pain is in specific sub-categories:

| Sub-category | Profit | Margin |
|--------------|--------|--------|
| Tables | -$17,725 | -8.6% |
| Bookcases | -$3,473 | -3.0% |
| Chairs | +$26,590 | 8.1% |

Furniture inflates top-line numbers without helping the bottom line. If that category keeps growing, total profit could actually drop.

Worth looking at: pricing and costs on Tables and Bookcases, tighter discount rules on Furniture, and shifting incentives toward Technology and Office Supplies.

Query: `sql/03_analysis_queries.sql`, Product Category Performance

## 2. Heavy discounting kills margin

| Discount | Line items | Margin |
|----------|-----------|--------|
| None | 4,798 | 29.5% |
| 1-10% | 94 | 16.6% |
| 11-20% | 3,709 | 11.6% |
| 21%+ | 1,393 | -37.3% |

About 14% of line items have discounts above 20%, and those orders lose money overall. That helps explain why 18.7% of all line items have negative profit.

Worth looking at: approval thresholds above 15%, and a review of which categories and regions get the steepest discounts.

Query: `sql/03_analysis_queries.sql`, Discount Impact

## 3. Central region underperforms on margin

| Region | Revenue | Margin |
|--------|---------|--------|
| West | $725K | 14.9% |
| East | $679K | 13.5% |
| South | $392K | 11.9% |
| Central | $501K | 7.9% |

Central is second in revenue but last in margin, about half the West's rate. Likely tied to Furniture volume and heavy discounting in that region.

Query: `sql/03_analysis_queries.sql`, Regional Performance

## Other notes

- Revenue grew 51% from 2014 to 2017. Profit grew faster ($50K to $93K).
- Consumer is the biggest segment by revenue. Home Office has the best margin.
- 793 customer IDs become 4,688 rows in the customer table because the same customer can ship to multiple locations. I modeled that at the ship-to level (see `data_dictionary.md`).
- 1,871 line items (18.7%) have negative profit, mostly Furniture and heavily discounted orders.
