# Insights

Jan 2014 - Dec 2017 | 9,994 line items | $2.30M revenue

## Summary

Apex Distribution did $2.30M in revenue and $286K in profit (12.5% margin) over four years. Revenue climbed from $484K in 2014 to $733K in 2017, but margins vary a lot by category. Technology and Office Supplies run above 17% margin. Furniture is the second-biggest category by revenue but only 2.5% margin. Discounts over 20% are deeply unprofitable (-37% margin as a group). Central region has the worst margin at 7.9%.

If leadership acted on the three recommendations below, estimated profit upside is roughly $55K to $90K (about 19% to 31% above the current $286K base), depending on how aggressively discount caps are enforced.

## 1. Furniture looks good on revenue, not on profit

Furniture brought in $742K (32% of revenue) but only $18K in profit, a 2.5% margin vs. 17.4% for Technology.

The pain is in specific sub-categories:

| Sub-category | Revenue | Profit | Margin |
|--------------|---------|--------|--------|
| Tables | $207K | -$17,725 | -8.6% |
| Bookcases | $115K | -$3,473 | -3.0% |
| Chairs | $328K | +$26,590 | 8.1% |

Furniture inflates top-line numbers without helping the bottom line. Tables and Bookcases alone lose $21K on $322K in sales.

### Recommended actions

| Action | Estimated impact |
|--------|------------------|
| Cap Tables discounts at 20%. Today 176 Table lines (55% of Table volume) run above 20% off and lose $31K; the rest of Tables earns $13K at 11.1% margin. | ~$31K profit swing (loss to profit on Tables) |
| Raise Tables list prices 5% where discounts are already low. | +$10K profit (assuming volume holds) |
| Bring Bookcases to breakeven through cost review or a 3 to 4% price increase on $115K in sales. | +$3.5K profit |
| Shift sales incentives so 10% of Furniture revenue (~$74K) moves to Technology or Office Supplies instead. | +$11K profit at current category margins |

Combined, fixing Tables discounting plus breakeven on Bookcases adds roughly $35K to $45K to total profit without growing revenue.

Query: `sql/03_analysis_queries.sql`, Product Category Performance

## 2. Heavy discounting kills margin

| Discount | Line items | Revenue | Profit | Margin |
|----------|-----------|---------|--------|--------|
| None | 4,798 | $1.17M | +$345K | 29.5% |
| 1-10% | 94 | $34K | +$6K | 16.6% |
| 11-20% | 3,709 | $735K | +$85K | 11.6% |
| 21%+ | 1,393 | $363K | -$135K | -37.3% |

About 14% of line items have discounts above 20%, and those orders lose money overall. That helps explain why 18.7% of all line items have negative profit.

21%+ discounts hit every category, but Furniture is worst: 542 lines lose $54K on $195K in sales. Office Supplies and Technology lose $47K and $34K respectively on their deep-discount lines.

### Recommended actions

| Action | Estimated impact |
|--------|------------------|
| Require VP approval for any discount above 15%; block above 20% unless margin-positive at order level. | Stops new losses on the $363K in 21%+ revenue that currently bleeds $135K |
| Reprice or walk the 1,393 existing 21%+ lines rather than renewing at the same terms. Even recovering half the loss is meaningful. | +$68K profit at 50% recovery |
| Start in Central: 643 deep-discount lines lose $52K there. Central's margin without those lines would be 24.8% on the remaining $372K base vs. 7.9% today. | +$52K profit if Central enforces the cap |

A full stop on 21%+ discounts recovers $135K in profit but puts $363K in revenue at risk (16% of total sales). The practical path is cap-and-reprice: keep the orders that can hit 11 to 20% margin, exit the rest.

Query: `sql/03_analysis_queries.sql`, Discount Impact

## 3. Central region underperforms on margin

| Region | Revenue | Profit | Margin |
|--------|---------|--------|--------|
| West | $725K | $108K | 14.9% |
| East | $679K | $92K | 13.5% |
| South | $392K | $47K | 11.9% |
| Central | $501K | $40K | 7.9% |

Central is second in revenue but last in margin, about half the West's rate. Central Furniture loses $2.9K on $164K in sales, but discounting is the bigger driver: Central accounts for 46% of all 21%+ discount lines (643 of 1,393) and 39% of the company-wide loss on those lines.

### Recommended actions

| Action | Estimated impact |
|--------|------------------|
| Enforce the 20% discount cap in Central first (see Section 2). | +$52K profit on current Central volume |
| Close the remaining gap to West's 14.9% margin through mix shift (less Furniture, more Technology) and tighter list pricing. | +$35K profit if Central matched West's margin rate on $501K in revenue |
| Pair Central sales reps with Technology specialists on deals over $5K to improve category mix. | Supports the +$35K margin-gap target over time |

Central-specific discount enforcement alone nearly closes the gap to West without any revenue growth.

Query: `sql/03_analysis_queries.sql`, Regional Performance

## 4. Consumer segment has room on margin

| Segment | Revenue | Margin |
|---------|---------|--------|
| Consumer | $1.16M | 11.5% |
| Corporate | $706K | 13.0% |
| Home Office | $430K | 14.0% |

Consumer drives half of all revenue but runs 2.5 points below Home Office on margin, mostly from the same discount patterns above.

### Recommended action

| Action | Estimated impact |
|--------|------------------|
| Apply the 15% discount cap to Consumer accounts first (largest volume, lowest margin). Closing half the gap to Home Office's 14.0% rate. | +$14K profit on $1.16M in Consumer revenue |

## Priority stack

If leadership can only do three things:

1. Cap discounts at 20% company-wide, starting in Central → up to $135K recovered (partial recovery likely $50K to $70K)
2. Fix Tables pricing and discounting → ~$31K to $41K
3. Breakeven on Bookcases → +$3.5K

Items 2 and 3 overlap with item 1 on Furniture lines, so the realistic combined upside is $55K to $90K, not the sum of every row above.

## Other notes

- Revenue grew 51% from 2014 to 2017. Profit grew faster ($50K to $93K).
- 793 customer IDs become 4,688 rows in the customer table because the same customer can ship to multiple locations. I modeled that at the ship-to level (see `data_dictionary.md`).
- 1,871 line items (18.7%) have negative profit, mostly Furniture and heavily discounted orders.
