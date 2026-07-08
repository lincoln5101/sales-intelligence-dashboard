-- 03_clean_transform.sql
-- Sales Intelligence Dashboard — ETL: Staging → Star Schema

-- Prerequisites: 01_create_schema.sql + staging data loaded

-- DATA QUALITY CHECKS

-- SELECT 'rows_in_staging' AS metric, COUNT(*) AS value FROM stg_sales_raw;
-- SELECT 'negative_profit_rows' AS metric, COUNT(*) AS value FROM stg_sales_raw WHERE profit < 0;

-- POPULATE dim_date
INSERT INTO dim_date (date_key, full_date, year, quarter, month, month_name, day_of_week, day_name, is_weekend)
WITH RECURSIVE
bounds AS (
    SELECT MIN(order_date) AS start_date, MAX(ship_date) AS end_date FROM stg_sales_raw
),
dates(d) AS (
    SELECT start_date FROM bounds
    UNION ALL
    SELECT date(d, '+1 day') FROM dates, bounds WHERE d < end_date
)
SELECT
    CAST(strftime('%Y%m%d', d) AS INTEGER),
    d,
    CAST(strftime('%Y', d) AS INTEGER),
    (CAST(strftime('%m', d) AS INTEGER) - 1) / 3 + 1,
    CAST(strftime('%m', d) AS INTEGER),
    CASE CAST(strftime('%m', d) AS INTEGER)
        WHEN 1 THEN 'January'   WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'   WHEN 5 THEN 'May'      WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'    WHEN 8 THEN 'August'   WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' WHEN 12 THEN 'December'
    END,
    CAST(strftime('%w', d) AS INTEGER),
    CASE CAST(strftime('%w', d) AS INTEGER)
        WHEN 0 THEN 'Sunday'    WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'   WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'  WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END,
    CASE WHEN CAST(strftime('%w', d) AS INTEGER) IN (0, 6) THEN 1 ELSE 0 END
FROM dates;

-- POPULATE dim_customer
INSERT INTO dim_customer (customer_key, customer_id, customer_name, segment, city, state, region, country)
SELECT
    ROW_NUMBER() OVER (ORDER BY customer_id, city, state, region),
    customer_id,
    customer_name,
    segment,
    city,
    state,
    region,
    country
FROM (
    SELECT DISTINCT customer_id, customer_name, segment, city, state, region, country
    FROM stg_sales_raw
);

-- POPULATE dim_product
INSERT INTO dim_product (product_key, product_id, product_name, category, sub_category)
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id, product_name),
    product_id,
    product_name,
    category,
    sub_category
FROM (
    SELECT DISTINCT product_id, product_name, category, sub_category
    FROM stg_sales_raw
);

-- POPULATE fact_sales
INSERT INTO fact_sales (
    sales_key, row_id, order_id, order_date_key, ship_date_key,
    customer_key, product_key, quantity, unit_price, discount,
    sales_amount, profit, ship_mode
)
SELECT
    s.row_id,
    s.row_id,
    s.order_id,
    CAST(strftime('%Y%m%d', s.order_date) AS INTEGER),
    CAST(strftime('%Y%m%d', s.ship_date) AS INTEGER),
    c.customer_key,
    p.product_key,
    s.quantity,
    ROUND(s.sales / (s.quantity * (1.0 - s.discount)), 2),
    s.discount,
    s.sales,
    s.profit,
    s.ship_mode
FROM stg_sales_raw s
JOIN dim_customer c
    ON  s.customer_id = c.customer_id
    AND s.city        = c.city
    AND s.state       = c.state
    AND s.region      = c.region
JOIN dim_product p
    ON  s.product_id    = p.product_id
    AND s.product_name  = p.product_name
    AND s.category      = p.category
    AND s.sub_category  = p.sub_category;
