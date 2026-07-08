# Dashboard Design

## Target Audience

C-suite and VP-level stakeholders at Apex Distribution Inc. The dashboard should answer "How are we performing?" in under 30 seconds, with drill-down for deeper investigation.

## Design Principles

1. **Executive-first layout** — KPI cards at top, trends in middle, detail tables at bottom
2. **Consistent color semantics** — green for positive, red for negative, neutral grays for context
3. **Minimal clutter** — no chart junk; every visual answers a specific question
4. **Mobile-aware** — single-page overview works on laptop screens (standard exec use case)

---

## Page 1: Executive Overview

### KPI Cards (top row)

| KPI | Measure (DAX) | Format |
|-----|---------------|--------|
| Total Revenue | `SUM(sales_amount)` | $#,##0 |
| Total Profit | `SUM(profit)` | $#,##0 |
| Profit Margin | `DIVIDE(SUM(profit), SUM(sales_amount))` | 0.0% |
| Total Orders | `DISTINCTCOUNT(order_id)` | #,##0 |
| Avg Order Value | `DIVIDE(SUM(sales_amount), DISTINCTCOUNT(order_id))` | $#,##0 |

### Visuals

| Visual | Type | Purpose |
|--------|------|---------|
| Revenue & Profit Trend | Line chart (monthly) | Spot growth/decline |
| Revenue by Region | Map or bar chart | Geographic performance |
| Revenue by Category | Donut or stacked bar | Product mix |
| Top 10 Customers | Table | Customer concentration risk |

### Filters (slicers)

- Date range (order_date)
- Region
- Customer segment
- Product category

---

## Page 2: Product & Profitability Analysis

| Visual | Type | Purpose |
|--------|------|---------|
| Margin by Category | Bar chart | Identify low-margin categories |
| Discount vs Profit | Scatter plot | Discount impact on profitability |
| Sub-Category Ranking | Matrix/table | Granular product performance |
| Profit Trend by Category | Small multiples line charts | Category-level trends |

---

## Page 3: Customer Analysis

| Visual | Type | Purpose |
|--------|------|---------|
| Revenue by Segment | Stacked column | Segment contribution |
| Customer Pareto (80/20) | Combo chart | Concentration analysis |
| Top Customers Table | Table with conditional formatting | Account management priorities |
| New vs Returning (if applicable) | Card or bar | Customer acquisition |

---

## Color Palette (suggested)

| Use | Color | Hex |
|-----|-------|-----|
| Primary | Steel Blue | `#4472C4` |
| Positive | Green | `#70AD47` |
| Negative | Red | `#C00000` |
| Neutral | Gray | `#A5A5A5` |
| Accent | Orange | `#ED7D31` |

---

## DAX Measures to Create

```dax
Total Revenue = SUM(vw_sales_executive[sales_amount])

Total Profit = SUM(vw_sales_executive[profit])

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0)

Total Orders = DISTINCTCOUNT(vw_sales_executive[order_id])

Avg Order Value =
    DIVIDE([Total Revenue], [Total Orders], 0)

Revenue YoY % =
    VAR CurrentYear = [Total Revenue]
    VAR PriorYear = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[full_date]))
    RETURN DIVIDE(CurrentYear - PriorYear, PriorYear, 0)
```

---

## Screenshots

Save dashboard screenshots to `powerbi/screenshots/` and reference them in the README.

---

*Refine page layout after connecting to actual data and validating measure calculations.*
