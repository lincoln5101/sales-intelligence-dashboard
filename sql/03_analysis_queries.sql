-- 03_analysis_queries.sql
-- Analysis queries for the sales dashboard

-- Executive summary KPIs
SELECT
    ROUND(SUM(sales_amount), 2)                                         AS total_revenue,
    ROUND(SUM(profit), 2)                                               AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(sales_amount), 2)                   AS profit_margin_pct,
    COUNT(DISTINCT order_id)                                            AS total_orders,
    COUNT(DISTINCT customer_key)                                        AS total_customers,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2)              AS avg_order_value
FROM fact_sales;

-- Revenue & Profit by Year-Month
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct
FROM fact_sales f
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Top 10 Customers by Revenue
SELECT
    c.customer_name,
    c.segment,
    c.region,
    ROUND(SUM(f.sales_amount), 2) AS total_revenue,
    ROUND(SUM(f.profit), 2)       AS total_profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_name, c.segment, c.region
ORDER BY total_revenue DESC
LIMIT 10;

-- Product Category Performance
SELECT
    p.category,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct,
    COUNT(*)                      AS line_items
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- Sub-Category Performance (lowest margin categories)
SELECT
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category, p.sub_category
ORDER BY margin_pct ASC
LIMIT 10;

-- Regional Performance by Year
SELECT
    c.region,
    d.year,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2)       AS profit
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_date d ON f.order_date_key = d.date_key
GROUP BY c.region, d.year
ORDER BY c.region, d.year;

-- Discount Impact on Profitability
SELECT
    CASE
        WHEN f.discount = 0 THEN 'No Discount'
        WHEN f.discount <= 0.10 THEN '1-10%'
        WHEN f.discount <= 0.20 THEN '11-20%'
        ELSE '21%+'
    END AS discount_band,
    COUNT(*) AS line_items,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(SUM(f.profit), 2) AS profit,
    ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct,
    ROUND(SUM(f.profit) * 100.0 / SUM(f.sales_amount), 2) AS margin_pct
FROM fact_sales f
GROUP BY discount_band
ORDER BY avg_discount_pct;

-- Ship Mode Analysis
SELECT
    f.ship_mode,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.sales_amount), 2) AS revenue,
    ROUND(AVG(julianday(d_ship.full_date) - julianday(d_ord.full_date)), 1) AS avg_days_to_ship
FROM fact_sales f
JOIN dim_date d_ord  ON f.order_date_key = d_ord.date_key
JOIN dim_date d_ship ON f.ship_date_key  = d_ship.date_key
GROUP BY f.ship_mode
ORDER BY revenue DESC;
