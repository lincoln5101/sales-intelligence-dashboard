"""
data_validation.py
Sales Intelligence Dashboard — Data Quality Validation

Purpose:
    Inspect raw data files before loading into the database.
    Produces a validation report identifying nulls, duplicates, type issues,
    and business-rule violations.

Usage:
    python python/data_validation.py
    python python/data_validation.py --file data/raw/sales_data.csv
"""

import argparse
from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Load a CSV or Excel file from the raw data directory."""
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file_path, encoding="utf-8-sig")
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file type: {suffix}")


def validate_schema(df: pd.DataFrame, required_columns: list[str]) -> dict:
    """Check that expected columns exist in the raw file."""
    missing = [col for col in required_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in required_columns]
    return {
        "missing_columns": missing,
        "extra_columns": extra,
        "passed": len(missing) == 0,
    }


def validate_nulls(df: pd.DataFrame, critical_columns: list[str]) -> pd.DataFrame:
    """Return null counts for critical columns."""
    results = []
    for col in critical_columns:
        if col in df.columns:
            null_count = df[col].isna().sum()
            null_pct = round(null_count / len(df) * 100, 2)
            results.append({"column": col, "null_count": null_count, "null_pct": null_pct})
    return pd.DataFrame(results)


def validate_duplicates(df: pd.DataFrame, key_column: str) -> dict:
    """Check for duplicate primary keys."""
    if key_column not in df.columns:
        return {"duplicate_count": None, "passed": False, "message": f"Column '{key_column}' not found"}
    dup_count = df.duplicated(subset=[key_column]).sum()
    return {"duplicate_count": int(dup_count), "passed": dup_count == 0}


def validate_business_rules(df: pd.DataFrame) -> list[dict]:
    """Apply business-rule checks relevant to sales data."""
    checks = []

    if "Sales" in df.columns:
        negative_sales = (df["Sales"] < 0).sum()
        checks.append({
            "rule": "Sales values must be non-negative",
            "violations": int(negative_sales),
            "passed": negative_sales == 0,
        })

    if "Profit" in df.columns:
        checks.append({
            "rule": "Rows with negative profit (flagged, not necessarily invalid)",
            "violations": int((df["Profit"] < 0).sum()),
            "passed": True,  # informational
        })

    if "Discount" in df.columns:
        invalid_discount = ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
        checks.append({
            "rule": "Discount must be between 0 and 1",
            "violations": int(invalid_discount),
            "passed": invalid_discount == 0,
        })

    return checks


def run_validation(file_path: Path, required_columns: list[str] | None = None) -> None:
    """Run full validation suite and print a summary report."""
    print(f"\n{'='*60}")
    print(f"DATA VALIDATION REPORT")
    print(f"File: {file_path.name}")
    print(f"{'='*60}\n")

    df = load_raw_data(file_path)

    # Overview
    print(f"Rows:    {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn names:\n  {list(df.columns)}\n")

    # Data types
    print("Data types:")
    print(df.dtypes.to_string())
    print()

    # Schema check
    if required_columns:
        schema_result = validate_schema(df, required_columns)
        status = "PASS" if schema_result["passed"] else "FAIL"
        print(f"Schema check: {status}")
        if schema_result["missing_columns"]:
            print(f"  Missing: {schema_result['missing_columns']}")
        if schema_result["extra_columns"]:
            print(f"  Extra:   {schema_result['extra_columns']}")
        print()

    # Null analysis
    print("Null analysis (critical columns):")
    critical = required_columns or list(df.columns)
    null_report = validate_nulls(df, critical)
    print(null_report.to_string(index=False))
    print()

    # Duplicate check
    key_col = "Row ID" if "Row ID" in df.columns else df.columns[0]
    dup_result = validate_duplicates(df, key_col)
    print(f"Duplicate check on '{key_col}': {dup_result['duplicate_count']} duplicates")
    print()

    # Business rules
    print("Business rule checks:")
    for check in validate_business_rules(df):
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['rule']}: {check['violations']} violations")

    print(f"\n{'='*60}")
    print("Validation complete.")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Validate raw sales data files.")
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Path to raw data file (defaults to first CSV in data/raw/)",
    )
    args = parser.parse_args()

    if args.file:
        file_path = args.file
    else:
        csv_files = list(RAW_DATA_DIR.glob("*.csv"))
        if not csv_files:
            print("No CSV files found in data/raw/. Place your dataset there and re-run.")
            return
        file_path = csv_files[0]

    # Default expected columns for Superstore-style datasets (update after dataset selection)
    required_columns = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "City", "State",
        "Postal Code", "Region", "Product ID", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit",
    ]

    run_validation(file_path, required_columns)


if __name__ == "__main__":
    main()
