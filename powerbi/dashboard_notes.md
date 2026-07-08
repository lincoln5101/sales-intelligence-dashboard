# Power BI — Build Notes

**Full walkthrough:** [BUILD_GUIDE.md](BUILD_GUIDE.md) (start here)

## Quick Start

1. Open Power BI Desktop
2. Import `data/exports/sales_executive.csv`
3. Apply theme: `theme/apex_distribution.json`
4. Add measures from `dax/measures.dax`
5. Build 3 pages following BUILD_GUIDE.md

## Data Files

| File | Rows | Use |
|------|------|-----|
| `sales_executive.csv` | 9,994 | Primary table — all 3 pages |
| `monthly_kpis.csv` | 48 | Optional — faster trend charts |
| `category_summary.csv` | 3 | Optional — category cards |
| `regional_summary.csv` | 16 | Optional — regional analysis |

## Build Checklist

- [ ] Import `sales_executive.csv` with correct data types
- [ ] Apply `apex_distribution.json` theme
- [ ] Create `_Metrics` table and core DAX measures
- [ ] Create `Dim Date` table + relationship
- [ ] Page 1: Executive Overview (5 KPI cards + 4 visuals + slicers)
- [ ] Page 2: Product & Profitability (margin, discount, sub-category)
- [ ] Page 3: Customer Analysis (segment, Pareto, detail table)
- [ ] Sync slicers across pages
- [ ] Validate KPIs: $2.30M revenue, 12.5% margin
- [ ] Replace preview PNGs with Power BI screenshots
- [ ] Save `.pbix` locally (gitignored)

## Validation Targets

| Measure | Expected |
|---------|----------|
| Total Revenue | $2,297,201 |
| Total Profit | $286,397 |
| Profit Margin % | 12.5% |
| Total Orders | 5,009 |

## Supporting Files

| File | Purpose |
|------|---------|
| [BUILD_GUIDE.md](BUILD_GUIDE.md) | Step-by-step page build instructions |
| [dax/measures.dax](dax/measures.dax) | All DAX measures |
| [theme/apex_distribution.json](theme/apex_distribution.json) | Color theme |
| [power_query/sales_executive.pq](power_query/sales_executive.pq) | Power Query M code |

## Preview Charts

Run `python python/generate_preview_charts.py` to regenerate placeholder screenshots in `screenshots/` from export data.
