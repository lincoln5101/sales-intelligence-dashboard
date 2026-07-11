# Executive Sales Intelligence Dashboard

Sales analytics project for a fictional company, Apex Distribution Inc. Raw Superstore data goes through SQL and Python, then into a Power BI dashboard.

## What this is

I built a full pipeline: load CSV data, validate it, model it in a star schema, run analysis queries, and feed everything into an executive dashboard in Power BI. The dashboard covers revenue, profit, margins, customers, and products from 2014 to 2017.

## Business problem

Leadership at Apex Distribution didn't have one place to see how the business was doing. Sales data lived in spreadsheets. This project answers:

- How much revenue and profit are we making, and what's our margin?
- Which regions, segments, and categories are up or down?
- Which customers and products actually drive value?
- How much do discounts hurt profitability?

More context in [docs/business_problem.md](docs/business_problem.md).

## Tools

| Tool | What I used it for |
|------|-------------------|
| Python | Data validation, EDA, exports |
| SQL (SQLite) | Schema, ETL, analysis queries |
| pandas | Loading and checking data |
| Power BI | Dashboard and DAX measures |
| Git / GitHub | Version control |

## Data

| | |
|---|---|
| Source | [Tableau Superstore sample](https://community.tableau.com/s/question/0D54T00000CWeX8SAL/sample-superstore-sales-excelxls) |
| File | `data/raw/superstore_sales.csv` |
| Rows | 9,994 line items |
| Period | Jan 2014 - Dec 2017 |

I reframed the Superstore data as Apex Distribution Inc. for the project. Original data is from Tableau.

## Pipeline

```
Raw CSV -> Staging -> Star schema -> SQL views -> Power BI
```

Details in [docs/methodology.md](docs/methodology.md).

## Dashboard

| Home | Executive Overview | Product & Profitability | Customer Analysis |
|------|--------------------|-------------------------|-------------------|
| ![Home](powerbi/screenshots/00_home_navigation.png) | ![Executive Overview](powerbi/screenshots/01_executive_overview.png) | ![Product](powerbi/screenshots/02_product_profitability.png) | ![Customer](powerbi/screenshots/03_customer_analysis.png) |

## Headline numbers

| | |
|---|---|
| Revenue | $2,297,201 |
| Profit | $286,397 |
| Margin | 12.5% |
| Orders | 5,009 |

Main takeaways:

1. Furniture is 32% of revenue but only 2.5% margin. Tables alone loses $17.7K; capping Tables discounts at 20% could swing that sub-category by ~$31K.
2. Discounts over 20% run at -37% margin and cost the business $135K on $363K in sales. Central accounts for $52K of that loss.
3. Central region does $501K in revenue at 7.9% margin vs. 14.9% in the West. Tightening Central discount policy alone could recover most of the gap.

Estimated upside from the top three actions: $55K to $90K in additional profit (19% to 31% above current). Full write-up in [docs/insights.md](docs/insights.md).

## How to run it

Requirements: Python 3.10+, Power BI Desktop if you want to open the dashboard

```bash
git clone https://github.com/lincoln5101/sales-intelligence-dashboard.git
cd sales-intelligence-dashboard

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the pipeline:

```bash
python python/data_validation.py
python python/run_pipeline.py
python python/export_for_powerbi.py
```

Import the CSVs from `data/exports/` into Power BI, or open `powerbi/Sales Intelligence Dashboard.pbix`.

For EDA:

```bash
jupyter notebook python/exploratory_analysis.ipynb
```

## Project structure

```
sales-intelligence-dashboard/
├── data/raw/              # Source CSV
├── data/processed/        # SQLite database (generated)
├── data/exports/          # CSV exports for Power BI
├── sql/                   # Schema, ETL, queries, views
├── python/                # Validation, pipeline, exports
├── powerbi/               # Dashboard file and screenshots
└── docs/                  # Business context, dictionary, insights
```

## Author

Lincoln Sheets
