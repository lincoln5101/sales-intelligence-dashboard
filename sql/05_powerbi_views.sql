-- =============================================================================
-- 05_powerbi_views.sql
-- Sales Intelligence Dashboard — Power BI Export Views
-- =============================================================================

-- -----------------------------------------------------------------------------
-- vw_sales_executive: Primary denormalized table for Power BI
-- -----------------------------------------------------------------------------
CREATE VIEW vw_sales_executive AS
SELECT
    f.sales_key,
    f.row_id,
    f.order_id,
    d_ord.full_date       AS order_date,
    d_ord.year            AS order_year,
    d_ord.quarter         AS order_quarter,
    d_ord.month           AS order_month,
    d_ord.month_name,
    d_ord.year || '-' || printf('%02d', d_ord.month) AS year_month,
    d_ship.full_date      AS ship_date,
    c.customer_id,
    c.customer_name,
    c.segment,
    c.city,
    c.state,
    c.region,
    c.country,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    f.quantity,
    f.unit_price,
    f.discount,
    f.sales_amount,
    f.profit,
    f.ship_mode,
    ROUND(f.profit * 100.0 / f.sales_amount, 2) AS line_margin_pct,
    CASE
        WHEN f.discount = 0 THEN 'No Discount'
        WHEN f.discount <= 0.10 THEN '1-10%'
        WHEN f.discount <= 0.20 THEN '11-20%'
        ELSE '21%+'
    END AS discount_band,
    CASE WHEN f.profit < 0 THEN 1 ELSE 0 END AS is_loss_making
FROM fact_sales f
JOIN dim_date d_ord  ON f.order_date_key = d_ord.date_key
JOIN dim_date d_ship ON f.ship_date_key  = d_ship.date_key
JOIN dim_customer c  ON f.customer_key   = c.customer_key
JOIN dim_product p   ON f.product_key    = p.product_key;

-- -----------------------------------------------------------------------------
-- vw_monthly_kpis: Pre-aggregated monthly metrics
-- -----------------------------------------------------------------------------
CREATE VIEW vw_monthly_kpis AS
SELECT
    d.year,
    d.month,
    d.month_name,
    d.year || '-' || printf('%02d', d.month) AS year_month,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct,
    COUNT(DISTINCT f.order_id)    AS orders,
    COUNT(DISTINCT f.customer_key) AS customers
FROM fact_sales f
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year, d.month, d.month_name;

-- -----------------------------------------------------------------------------
-- vw_category_summary: Category rollup
-- -----------------------------------------------------------------------------
CREATE VIEW vw_category_summary AS
SELECT
    p.category,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct,
    COUNT(*) AS line_items,
    SUM(CASE WHEN f.profit < 0 THEN 1 ELSE 0 END) AS loss_making_lines
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category;

-- -----------------------------------------------------------------------------
-- vw_regional_summary: Region rollup for map/bar charts
-- -----------------------------------------------------------------------------
CREATE VIEW vw_regional_summary AS
SELECT
    c.region,
    d.year,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct,
    COUNT(DISTINCT f.customer_key) AS customers
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY c.region, d.year;
