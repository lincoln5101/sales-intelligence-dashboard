-- =============================================================================
-- 01_create_schema.sql
-- Sales Intelligence Dashboard — Database Schema (SQLite)
-- =============================================================================
-- Company: Apex Distribution Inc. (fictional framing of Superstore sample data)
-- Run: sqlite3 data/processed/sales_intelligence.db < sql/01_create_schema.sql
-- =============================================================================

PRAGMA foreign_keys = ON;

-- Drop existing objects (idempotent rebuild)
DROP VIEW IF EXISTS vw_category_summary;
DROP VIEW IF EXISTS vw_monthly_kpis;
DROP VIEW IF EXISTS vw_sales_executive;
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS stg_sales_raw;

-- -----------------------------------------------------------------------------
-- STAGING TABLE (mirrors raw CSV structure)
-- -----------------------------------------------------------------------------
CREATE TABLE stg_sales_raw (
    row_id          INTEGER PRIMARY KEY,
    order_id        TEXT NOT NULL,
    order_date      TEXT NOT NULL,          -- ISO format: YYYY-MM-DD
    ship_date       TEXT NOT NULL,
    ship_mode       TEXT NOT NULL,
    customer_id     TEXT NOT NULL,
    customer_name   TEXT NOT NULL,
    segment         TEXT NOT NULL,
    country         TEXT NOT NULL DEFAULT 'United States',
    city            TEXT NOT NULL,
    state           TEXT NOT NULL,
    postal_code     TEXT,
    region          TEXT NOT NULL,
    product_id      TEXT NOT NULL,
    category        TEXT NOT NULL,
    sub_category    TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    sales           REAL NOT NULL,
    quantity        INTEGER NOT NULL,
    discount        REAL NOT NULL DEFAULT 0,
    profit          REAL NOT NULL
);

-- -----------------------------------------------------------------------------
-- DIMENSION: Calendar
-- -----------------------------------------------------------------------------
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,      -- YYYYMMDD
    full_date       TEXT NOT NULL UNIQUE,     -- YYYY-MM-DD
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL,
    month           INTEGER NOT NULL,
    month_name      TEXT NOT NULL,
    day_of_week     INTEGER NOT NULL,         -- 0=Sunday … 6=Saturday
    day_name        TEXT NOT NULL,
    is_weekend      INTEGER NOT NULL          -- 0=weekday, 1=weekend
);

-- -----------------------------------------------------------------------------
-- DIMENSION: Customer
-- -----------------------------------------------------------------------------
CREATE TABLE dim_customer (
    customer_key    INTEGER PRIMARY KEY,
    customer_id     TEXT NOT NULL,
    customer_name   TEXT NOT NULL,
    segment         TEXT NOT NULL,
    city            TEXT NOT NULL,
    state           TEXT NOT NULL,
    region          TEXT NOT NULL,
    country         TEXT NOT NULL DEFAULT 'United States',
    UNIQUE (customer_id, city, state, region)
);

-- -----------------------------------------------------------------------------
-- DIMENSION: Product
-- -----------------------------------------------------------------------------
CREATE TABLE dim_product (
    product_key     INTEGER PRIMARY KEY,
    product_id      TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    category        TEXT NOT NULL,
    sub_category    TEXT NOT NULL,
    UNIQUE (product_id, product_name, category, sub_category)
);

-- -----------------------------------------------------------------------------
-- FACT: Sales (grain = one order line item)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_sales (
    sales_key       INTEGER PRIMARY KEY,
    row_id          INTEGER NOT NULL UNIQUE,
    order_id        TEXT NOT NULL,
    order_date_key  INTEGER NOT NULL,
    ship_date_key   INTEGER NOT NULL,
    customer_key    INTEGER NOT NULL,
    product_key     INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    discount        REAL NOT NULL DEFAULT 0,
    sales_amount    REAL NOT NULL,
    profit          REAL NOT NULL,
    ship_mode       TEXT NOT NULL,
    FOREIGN KEY (order_date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (ship_date_key)  REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key)   REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key)    REFERENCES dim_product(product_key)
);

-- -----------------------------------------------------------------------------
-- INDEXES
-- -----------------------------------------------------------------------------
CREATE INDEX idx_fact_sales_order_date  ON fact_sales(order_date_key);
CREATE INDEX idx_fact_sales_customer    ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product     ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_order_id    ON fact_sales(order_id);
