# Data Dictionary

Star schema. One row in `fact_sales` = one order line item.

## dim_date

| Column | Type | Notes |
|--------|------|-------|
| date_key | INTEGER | PK, YYYYMMDD |
| full_date | DATE | Calendar date |
| year | INTEGER | |
| quarter | INTEGER | 1-4 |
| month | INTEGER | 1-12 |
| month_name | TEXT | |
| day_of_week | INTEGER | 0=Sunday |
| day_name | TEXT | |
| is_weekend | INTEGER | 0 or 1 |

## dim_customer

| Column | Type | Notes |
|--------|------|-------|
| customer_key | INTEGER | PK |
| customer_id | TEXT | Not unique alone |
| customer_name | TEXT | |
| segment | TEXT | Consumer, Corporate, Home Office |
| city | TEXT | |
| state | TEXT | |
| region | TEXT | Central, East, South, West |
| country | TEXT | |

Same customer_id can appear in multiple cities/regions (793 IDs, 4,688 location rows). Join on `(customer_id, city, state, region)`.

## dim_product

| Column | Type | Notes |
|--------|------|-------|
| product_key | INTEGER | PK |
| product_id | TEXT | |
| product_name | TEXT | |
| category | TEXT | |
| sub_category | TEXT | |

## fact_sales

| Column | Type | Notes |
|--------|------|-------|
| sales_key | INTEGER | PK |
| order_id | TEXT | |
| order_date_key | INTEGER | FK to dim_date |
| ship_date_key | INTEGER | FK to dim_date |
| customer_key | INTEGER | FK to dim_customer |
| product_key | INTEGER | FK to dim_product |
| quantity | INTEGER | |
| unit_price | REAL | |
| discount | REAL | 0.0 to 1.0 |
| sales_amount | REAL | Revenue |
| profit | REAL | |
| ship_mode | TEXT | |

## Calculated metrics

| Metric | Formula |
|--------|---------|
| Profit margin % | profit / sales_amount * 100 |
| Avg order value | SUM(sales_amount) / COUNT(DISTINCT order_id) |
