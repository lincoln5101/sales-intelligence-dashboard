# Methodology

## Pipeline

```
Raw CSV -> Staging -> Clean & transform -> Star schema -> SQL views -> Power BI
```

## Steps

**1. Load data**

Superstore CSV loaded with Python/pandas into `stg_sales_raw`.

**2. Validate**

`python/data_validation.py` checks nulls, duplicates, and basic business rules. Result: 9,994 rows, no nulls, no duplicate keys, 1,871 negative-profit rows flagged.

**3. Model**

Star schema:

| Table | Rows |
|-------|------|
| dim_date | 1,464 |
| dim_customer | 4,688 |
| dim_product | 1,894 |
| fact_sales | 9,994 |

Customer grain is customer + ship-to location because 780 of 793 customer IDs show up in more than one region.

**4. Transform**

SQL (`02_clean_transform.sql`): build date/customer/product dimensions, load fact table, calculate unit price.

**5. Analyze**

SQL (`03_analysis_queries.sql`): KPIs, trends, category/region/discount analysis.

**6. Power BI**

Export views to CSV with `export_for_powerbi.py`, build dashboard in Power BI Desktop.

## Tech choices

| | Choice | Why |
|---|--------|-----|
| Database | SQLite | Easy to set up, portable |
| ETL | SQL | Keeps the SQL work visible |
| Validation | Python/pandas | Quick to inspect raw data |
| Viz | Power BI | Common in BI roles |

## Reproduce it

```bash
pip install -r requirements.txt
python python/run_pipeline.py
python python/export_for_powerbi.py
```

Raw CSV is already in `data/raw/`. Import the exports into Power BI or open the `.pbix` file.
