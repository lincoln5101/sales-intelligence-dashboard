# Check raw data before loading into the database.
# Usage: python python/data_validation.py

import argparse
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_raw_data(file_path):
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file_path, encoding="utf-8-sig")
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(file_path)
    raise ValueError(f"Unsupported file type: {suffix}")


def validate_schema(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in required_columns]
    return {"missing_columns": missing, "extra_columns": extra, "passed": len(missing) == 0}


def validate_nulls(df, critical_columns):
    results = []
    for col in critical_columns:
        if col in df.columns:
            null_count = df[col].isna().sum()
            null_pct = round(null_count / len(df) * 100, 2)
            results.append({"column": col, "null_count": null_count, "null_pct": null_pct})
    return pd.DataFrame(results)


def validate_duplicates(df, key_column):
    if key_column not in df.columns:
        return {"duplicate_count": None, "passed": False}
    dup_count = df.duplicated(subset=[key_column]).sum()
    return {"duplicate_count": int(dup_count), "passed": dup_count == 0}


def validate_business_rules(df):
    checks = []

    if "Sales" in df.columns:
        negative_sales = (df["Sales"] < 0).sum()
        checks.append({
            "rule": "Sales must be non-negative",
            "violations": int(negative_sales),
            "passed": negative_sales == 0,
        })

    if "Profit" in df.columns:
        checks.append({
            "rule": "Negative profit rows (informational)",
            "violations": int((df["Profit"] < 0).sum()),
            "passed": True,
        })

    if "Discount" in df.columns:
        invalid_discount = ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
        checks.append({
            "rule": "Discount between 0 and 1",
            "violations": int(invalid_discount),
            "passed": invalid_discount == 0,
        })

    return checks


def run_validation(file_path, required_columns=None):
    print(f"\nValidation report: {file_path.name}\n")

    df = load_raw_data(file_path)
    print(f"Rows: {len(df):,}  Columns: {len(df.columns)}\n")

    if required_columns:
        schema_result = validate_schema(df, required_columns)
        status = "PASS" if schema_result["passed"] else "FAIL"
        print(f"Schema: {status}")
        if schema_result["missing_columns"]:
            print(f"  Missing: {schema_result['missing_columns']}")
        if schema_result["extra_columns"]:
            print(f"  Extra: {schema_result['extra_columns']}")
        print()

    critical = required_columns or list(df.columns)
    null_report = validate_nulls(df, critical)
    print("Nulls:")
    print(null_report.to_string(index=False))
    print()

    key_col = "Row ID" if "Row ID" in df.columns else df.columns[0]
    dup_result = validate_duplicates(df, key_col)
    print(f"Duplicates on '{key_col}': {dup_result['duplicate_count']}\n")

    print("Business rules:")
    for check in validate_business_rules(df):
        status = "PASS" if check["passed"] else "FAIL"
        print(f"  [{status}] {check['rule']}: {check['violations']}")

    print("\nDone.\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=None)
    args = parser.parse_args()

    if args.file:
        file_path = args.file
    else:
        csv_files = list(RAW_DATA_DIR.glob("*.csv"))
        if not csv_files:
            print("No CSV files in data/raw/")
            return
        file_path = csv_files[0]

    required_columns = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "City", "State",
        "Postal Code", "Region", "Product ID", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit",
    ]

    run_validation(file_path, required_columns)


if __name__ == "__main__":
    main()
