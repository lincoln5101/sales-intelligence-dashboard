# Load raw CSV, build schema, transform, create views.
# Usage: python python/run_pipeline.py

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"
RAW_DEFAULT = PROJECT_ROOT / "data" / "raw" / "superstore_sales.csv"
DB_PATH = PROJECT_ROOT / "data" / "processed" / "sales_intelligence.db"


def run_sql_file(conn, sql_path):
    conn.executescript(sql_path.read_text())
    print(f"  Executed {sql_path.name}")


def load_staging(conn, raw_path):
    df = pd.read_csv(raw_path, encoding="utf-8-sig")

    column_map = {
        "Row ID": "row_id",
        "Order ID": "order_id",
        "Order Date": "order_date",
        "Ship Date": "ship_date",
        "Ship Mode": "ship_mode",
        "Customer ID": "customer_id",
        "Customer Name": "customer_name",
        "Segment": "segment",
        "Country": "country",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Region": "region",
        "Product ID": "product_id",
        "Category": "category",
        "Sub-Category": "sub_category",
        "Product Name": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
    }
    df = df.rename(columns=column_map)

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed").dt.strftime("%Y-%m-%d")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="mixed").dt.strftime("%Y-%m-%d")
    df["postal_code"] = df["postal_code"].astype(str)

    df.to_sql("stg_sales_raw", conn, if_exists="append", index=False)
    return len(df)


def print_summary(conn):
    tables = ["stg_sales_raw", "dim_date", "dim_customer", "dim_product", "fact_sales"]
    print("\n  Table row counts:")
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"    {table:20s} {count:>6,}")

    kpi = conn.execute("""
        SELECT
            ROUND(SUM(sales_amount), 0),
            ROUND(SUM(profit), 0),
            ROUND(SUM(profit) * 100.0 / SUM(sales_amount), 1)
        FROM fact_sales
    """).fetchone()
    print(f"\n  KPIs: Revenue=${kpi[0]:,.0f} | Profit=${kpi[1]:,.0f} | Margin={kpi[2]}%")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=RAW_DEFAULT)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    args = parser.parse_args()

    if not args.raw.exists():
        raise FileNotFoundError(f"Raw data not found: {args.raw}")

    args.db.parent.mkdir(parents=True, exist_ok=True)
    if args.db.exists():
        args.db.unlink()

    print(f"\nSales Intelligence ETL")
    print(f"  Source: {args.raw.name}")
    print(f"  Target: {args.db}\n")

    conn = sqlite3.connect(args.db)

    print("Step 1: Create schema")
    run_sql_file(conn, SQL_DIR / "01_create_schema.sql")

    print("\nStep 2: Load staging data")
    row_count = load_staging(conn, args.raw)
    print(f"  Loaded {row_count:,} rows")

    print("\nStep 3: Clean & transform")
    run_sql_file(conn, SQL_DIR / "02_clean_transform.sql")

    print("\nStep 4: Create Power BI views")
    run_sql_file(conn, SQL_DIR / "04_powerbi_views.sql")

    print_summary(conn)
    conn.close()
    print("\nDone. Run: python python/export_for_powerbi.py\n")


if __name__ == "__main__":
    main()
