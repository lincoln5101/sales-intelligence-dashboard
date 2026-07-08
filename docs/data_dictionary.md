# Data Dictionary

> **Status:** Template — populate after dataset selection and schema design.

## Overview

This project uses a **star schema** with one fact table and multiple dimension tables. The grain of `fact_sales` is **one row per order line item**.

---

## Dimension Tables

### dim_date

| Column | Type | Description |
|--------|------|-------------|
| date_key | INTEGER | Primary key (YYYYMMDD) |
| full_date | DATE | Calendar date |
| year | INTEGER | Year (e.g., 2023) |
| quarter | INTEGER | Quarter (1–4) |
| month | INTEGER | Month (1–12) |
| month_name | TEXT | Month name (e.g., January) |
| day_of_week | INTEGER | Day of week (1=Monday) |
| day_name | TEXT | Day name (e.g., Monday) |
| is_weekend | INTEGER | 1 if Saturday/Sunday |

### dim_customer

| Column | Type | Description |
|--------|------|-------------|
| customer_key | INTEGER | Surrogate primary key |
| customer_id | TEXT | Business key (not unique — same ID may ship to multiple locations) |
| customer_name | TEXT | Customer display name |
| segment | TEXT | Consumer, Corporate, or Home Office |
| city | TEXT | Customer city |
| state | TEXT | US state abbreviation |
| region | TEXT | Central, East, South, West |
| country | TEXT | Country (default: United States) |

**Modeling note:** The source data contains 793 unique `customer_id` values but 4,688 unique customer-location combinations. A single customer (e.g., Alex Avila) may appear in multiple cities and regions. The dimension grain is **customer + ship-to location**, joined on `(customer_id, city, state, region)`.

### dim_product

| Column | Type | Description |
|--------|------|-------------|
| product_key | INTEGER | Surrogate primary key |
| product_id | TEXT | Business key (32 IDs have minor name variations) |
| product_name | TEXT | Product display name |
| category | TEXT | Top-level category |
| sub_category | TEXT | Sub-category within category |

---

## Fact Table

### fact_sales

| Column | Type | Description |
|--------|------|-------------|
| sales_key | INTEGER | Surrogate primary key |
| order_id | TEXT | Order identifier (multiple line items per order) |
| order_date_key | INTEGER | FK → dim_date |
| ship_date_key | INTEGER | FK → dim_date (nullable) |
| customer_key | INTEGER | FK → dim_customer |
| product_key | INTEGER | FK → dim_product |
| quantity | INTEGER | Units ordered |
| unit_price | REAL | Price per unit before discount |
| discount | REAL | Discount rate (0.0 to 1.0) |
| sales_amount | REAL | Revenue = quantity × unit_price × (1 − discount) |
| profit | REAL | Profit after cost of goods |
| ship_mode | TEXT | Shipping method |

---

## Derived Metrics (calculated in SQL or Power BI)

| Metric | Formula |
|--------|---------|
| Profit Margin % | profit / sales_amount × 100 |
| Average Order Value | SUM(sales_amount) / COUNT(DISTINCT order_id) |
| Discount Amount | sales_amount × discount / (1 − discount) |
