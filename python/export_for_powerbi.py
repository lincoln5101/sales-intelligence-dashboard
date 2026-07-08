"""
export_for_powerbi.py
Sales Intelligence Dashboard — Export Clean Data for Power BI

Purpose:
    Query analytical views from the SQLite database and export CSV files
    to data/exports/ for Power BI import.

Usage:
    python python/export_for_powerbi.py
    python python/export_for_powerbi.py --db data/processed/sales_intelligence.db
"""

import argparse
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = PROJECT_ROOT / "data" / "processed" / "sales_intelligence.db"
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"

# Views to export for Power BI import
VIEWS_TO_EXPORT = [
    ("vw_sales_executive", "sales_executive.csv"),
    ("vw_monthly_kpis", "monthly_kpis.csv"),
    ("vw_category_summary", "category_summary.csv"),
    ("vw_regional_summary", "regional_summary.csv"),
]


def export_view(conn: sqlite3.Connection, view_name: str, output_file: Path) -> int:
    """Export a SQL view to CSV. Returns row count."""
    df = pd.read_sql_query(f"SELECT * FROM {view_name}", conn)
    df.to_csv(output_file, index=False)
    return len(df)


def main():
    parser = argparse.ArgumentParser(description="Export database views for Power BI.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Path to SQLite database")
    args = parser.parse_args()

    if not args.db.exists():
        print(f"Database not found: {args.db}")
        print("Run the SQL scripts first to create and populate the database.")
        return

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)

    print(f"\nExporting views from: {args.db.name}")
    print(f"Output directory:     {EXPORT_DIR}\n")

    if not VIEWS_TO_EXPORT:
        print("No views configured yet. Uncomment VIEWS_TO_EXPORT after running 05_powerbi_views.sql.")
        conn.close()
        return

    for view_name, filename in VIEWS_TO_EXPORT:
        output_path = EXPORT_DIR / filename
        try:
            row_count = export_view(conn, view_name, output_path)
            print(f"  Exported {view_name} → {filename} ({row_count:,} rows)")
        except Exception as e:
            print(f"  FAILED {view_name}: {e}")

    conn.close()
    print("\nExport complete. Import CSVs into Power BI from data/exports/.\n")


if __name__ == "__main__":
    main()
