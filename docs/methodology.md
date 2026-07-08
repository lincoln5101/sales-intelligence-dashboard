# Methodology

## End-to-End Pipeline

```
Raw CSV/Excel  →  Staging Tables  →  Clean & Transform  →  Star Schema  →  SQL Views  →  Power BI
     │                  │                    │                  │              │
  data/raw/         SQL load           03_clean_         dim_* +        05_powerbi_     Dashboard
                    (02_load)          transform.sql      fact_sales      views.sql
```

## Phase 1: Data Ingestion

- Source: Public dataset (see README for attribution)
- Tool: Python (`pandas`) for CSV/Excel loading; SQL for staging table inserts
- Output: `stg_sales_raw` staging table mirroring source file structure

## Phase 2: Data Validation

- Tool: `python/data_validation.py`
- Result: 9,994 rows, 0 nulls, 0 duplicate keys, 1,871 negative-profit rows flagged

## Phase 3: Data Modeling

- Approach: Star schema (dimensional modeling)
- Tables: `dim_date` (1,464 days), `dim_customer` (4,688 locations), `dim_product` (1,894 SKUs), `fact_sales` (9,994 line items)
- Key decision: Customer dimension grain = customer + ship-to location, because 780 of 793 customer IDs appear in multiple regions

## Phase 4: ETL / Transformation

- Tool: SQL (`03_clean_transform.sql`)
- Steps:
  1. Generate calendar dimension from date range in source data
  2. Deduplicate customers and products into dimension tables
  3. Join staging data to dimensions; load fact table
  4. Calculate derived fields (unit price, margin)

## Phase 5: Analysis

- Tool: SQL (`04_analysis_queries.sql`)
- Focus: KPIs, trends, segment analysis, discount impact
- Output: Query results inform dashboard design and insights doc

## Phase 6: Power BI Delivery

- Tool: Power BI Desktop
- Data source: CSV exports from `data/exports/` or direct SQLite connection
- Views: `vw_sales_executive`, `vw_monthly_kpis`, `vw_category_summary`

## Technology Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database | SQLite (default) | Zero setup, portable, portfolio-friendly |
| Alt database | SQL Server Express | Use if targeting enterprise SQL Server roles |
| ETL | SQL-first | Demonstrates core analyst SQL skills |
| Validation | Python | pandas is industry standard for data inspection |
| Visualization | Power BI | Widely used in corporate BI environments |

## Reproducibility

Anyone cloning this repo can:

1. `pip install -r requirements.txt`
2. Run `python python/run_pipeline.py` (raw CSV already in `data/raw/`)
3. Run `python python/export_for_powerbi.py`
4. Import exports into Power BI
