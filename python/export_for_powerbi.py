# Export SQL views to CSV for Power BI.
# Usage: python python/export_for_powerbi.py

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = PROJECT_ROOT / "data" / "processed" / "sales_intelligence.db"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"

VIEWS_TO_EXPORT = [
    ("vw_sales_executive", "sales_executive.csv"),
    ("vw_monthly_kpis", "monthly_kpis.csv"),
    ("vw_category_summary", "category_summary.csv"),
    ("vw_regional_summary", "regional_summary.csv"),
]


def export_view(conn, view_name, output_file):
    df = pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
    df.to_csv(output_file, index=False)
    return len(df)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    if not args.db.exists():
        print(f"Database not found: {args.db}")
        print("Run run_pipeline.py first.")
        return

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)

    print(f"\nExporting from {args.db.name} to {EXPORT_DIR}\n")

    for view_name, filename in VIEWS_TO_EXPORT:
        output_path = EXPORT_DIR / filename
        try:
            row_count = export_view(conn, view_name, output_path)
            print(f"  {view_name} -> {filename} ({row_count:,} rows)")
        except Exception as e:
            print(f"  FAILED {view_name}: {e}")

    conn.close()
    print("\nDone.\n")


if __name__ == "__main__":
    main()
