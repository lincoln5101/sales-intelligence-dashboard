# Power BI Build Guide — Apex Distribution Executive Dashboard

**Estimated time:** 60–90 minutes  
**Prerequisites:** Power BI Desktop installed, ETL pipeline run (`python python/run_pipeline.py`)

---

## Quick validation targets

After building Page 1, your KPI cards should show:

| Measure | Expected Value |
|---------|----------------|
| Total Revenue | **$2,297,201** |
| Total Profit | **$286,397** |
| Profit Margin % | **12.5%** |
| Total Orders | **5,009** |
| Avg Order Value | **~$459** |

If these match, your model is correct.

---

## Step 1: Import data (10 min)

1. Open **Power BI Desktop**
2. **Home → Get data → Text/CSV**
3. Navigate to your project folder:
   ```
   .../sales-intelligence-dashboard/data/exports/
   ```
4. Select **`sales_executive.csv`** → **Open** → **Transform Data**

### Fix data types in Power Query

In Power Query Editor, select the `sales_executive` query and verify types:

| Column | Type |
|--------|------|
| `order_date`, `ship_date` | Date |
| `sales_amount`, `profit`, `unit_price`, `discount` | Decimal Number |
| `quantity`, `order_year`, `order_month` | Whole Number |
| Everything else | Text |

> **Tip:** You can paste the M code from `power_query/sales_executive.pq` into **Advanced Editor** (update the file path first).

5. **Home → Close & Apply**

6. *(Optional but recommended)* Import supporting tables the same way:
   - `monthly_kpis.csv`
   - `category_summary.csv`
   - `regional_summary.csv`

   These speed up some visuals but Page 1 can be built entirely from `sales_executive`.

7. **File → Save As** → `Apex_Distribution_Dashboard.pbix` in the `powerbi/` folder

---

## Step 2: Apply theme (2 min)

1. **View → Themes → Browse for themes**
2. Select `powerbi/theme/apex_distribution.json`
3. Colors update to Apex Distribution palette (steel blue primary, green/red semantics)

---

## Step 3: Create measures table (5 min)

Don't put measures on the fact table — use a dedicated table (professional practice).

1. **Modeling → New Table**
2. Enter:
   ```dax
   _Metrics = ROW ( "Placeholder", BLANK () )
   ```
3. Hide the Placeholder column: right-click → **Hide in report view**
4. Select **`_Metrics`** table in the Fields pane

### Add core measures

**Modeling → New Measure** — paste each measure from `dax/measures.dax`, one at a time.

**Minimum set for Page 1** (add these first):

```dax
Total Revenue = SUM ( sales_executive[sales_amount] )

Total Profit = SUM ( sales_executive[profit] )

Profit Margin % = DIVIDE ( [Total Profit], [Total Revenue], 0 )

Total Orders = DISTINCTCOUNT ( sales_executive[order_id] )

Avg Order Value = DIVIDE ( [Total Revenue], [Total Orders], 0 )
```

### Format measures

| Measure | Format (Measure tools ribbon) |
|---------|----------------------------|
| Total Revenue, Total Profit, Avg Order Value | **Currency** ($, 0 decimals) |
| Profit Margin % | **Percentage** (1 decimal) |
| Total Orders | **Whole number** |

---

## Step 4: Create date table (5 min)

Required for time intelligence (YoY) and a clean date slicer.

1. **Modeling → New Table**
2. Paste:
   ```dax
   Dim Date =
   ADDCOLUMNS (
       CALENDAR ( DATE ( 2014, 1, 1 ), DATE ( 2017, 12, 31 ) ),
       "Year",       YEAR ( [Date] ),
       "Quarter",    "Q" & FORMAT ( [Date], "Q" ),
       "QuarterNum", QUARTER ( [Date] ),
       "Month",      FORMAT ( [Date], "MMM" ),
       "MonthNum",   MONTH ( [Date] ),
       "YearMonth",  FORMAT ( [Date], "YYYY-MM" )
   )
   ```
3. **Select `Dim Date` → Modeling → Mark as date table → Date**
4. **Model view:** Drag relationship:
   - `Dim Date[Date]` → `sales_executive[order_date]` (Many-to-one, single direction)

---

## Step 5: Page 1 — Executive Overview (25 min)

### Rename the page

Right-click page tab → **Rename** → `Executive Overview`

### Canvas setup

- **Format page → Canvas → Page size:** 16:9
- **Background:** `#F3F2F1` (light gray) or white

### Row 1: KPI cards (5 cards across the top)

For each card: **Insert → Card visual**

| Card | Field | Format |
|------|-------|--------|
| 1 | `[Total Revenue]` | Title: "Total Revenue" |
| 2 | `[Total Profit]` | Title: "Total Profit" |
| 3 | `[Profit Margin %]` | Title: "Profit Margin" |
| 4 | `[Total Orders]` | Title: "Total Orders" |
| 5 | `[Avg Order Value]` | Title: "Avg Order Value" |

**Card formatting tips:**
- Callout value: **Segoe UI Semibold, 28pt**
- Category label: **10pt, gray**
- Add a subtle border or white background to each card

### Row 2: Trend + Region (left 60% + right 40%)

**Visual A — Revenue & Profit Trend (Line chart)**

1. **Insert → Line chart**
2. Fields:
   - **X-axis:** `Dim Date[YearMonth]` (or `sales_executive[year_month]`)
   - **Y-axis:** `[Total Revenue]` and `[Total Profit]`
3. Title: **"Revenue & Profit Trend"**
4. Legend: bottom
5. Colors: Revenue = `#4472C4`, Profit = `#70AD47`

**Visual B — Revenue by Region (Clustered bar chart)**

1. **Insert → Clustered bar chart**
2. Fields:
   - **Y-axis:** `sales_executive[region]`
   - **X-axis:** `[Total Revenue]`
3. Sort by Revenue descending
4. Title: **"Revenue by Region"**
5. Add **Data labels** → ON
6. Color by: `region` with West/East/Central/South distinct colors

### Row 3: Category + Top Customers

**Visual C — Revenue by Category (Donut chart)**

1. **Insert → Donut chart**
2. Fields:
   - **Legend:** `sales_executive[category]`
   - **Values:** `[Total Revenue]`
3. Title: **"Revenue by Category"**
4. Detail labels: **Percent of total** + **Category name**

**Visual D — Top 10 Customers (Table)**

1. **Insert → Table**
2. Fields:
   - `sales_executive[customer_name]`
   - `[Total Revenue]`
   - `[Total Profit]`
   - `[Profit Margin %]` *(add as calculated column or use measure with customer context)*
3. **Filters on this visual → customer_name → Filter type: Top N**
   - Show items: **Top 10**
   - By value: `[Total Revenue]`
4. Title: **"Top 10 Customers by Revenue"**
5. Conditional formatting on Profit: green if > 0, red if < 0

### Row 4: Slicers (across bottom or left sidebar)

Add 4 slicers (**Insert → Slicer**):

| Slicer | Field | Style |
|--------|-------|-------|
| Date | `Dim Date[Date]` | Between (range) |
| Region | `sales_executive[region]` | List |
| Segment | `sales_executive[segment]` | Dropdown |
| Category | `sales_executive[category]` | List |

**Slicer formatting:** Vertical orientation, responsive, bold header

### Header text box

**Insert → Text box:**
```
Apex Distribution Inc.  |  Executive Sales Intelligence  |  2014–2017
```
Font: Segoe UI Semibold, 14pt, color `#264478`

---

## Step 6: Page 2 — Product & Profitability (20 min)

Rename page → **Product & Profitability**

### Visual 1: Margin by Category (Clustered bar chart)

- **Y-axis:** `sales_executive[category]`
- **X-axis:** `[Profit Margin %]`
- Sort descending by margin
- **Analytics pane → Constant line** at 12.5% (company average) — dashed gray
- Title: **"Profit Margin by Category"**
- *Story: Furniture bar should be tiny (2.5%) vs Technology (17.4%)*

### Visual 2: Revenue vs Profit by Category (Clustered column chart)

- **X-axis:** `category`
- **Y-axis:** `[Total Revenue]` and `[Total Profit]` (two measures)
- Title: **"Revenue vs Profit by Category"**
- *Story: Furniture columns nearly equal height; Technology profit column much closer to revenue*

### Visual 3: Discount Impact (Clustered column chart)

- **X-axis:** `sales_executive[discount_band]`
- **Y-axis:** `[Profit Margin %]`
- Sort by discount_band logically (use Sort by column or custom sort)
- Title: **"Margin Erosion from Discounting"**
- Color: conditional — red if margin < 0
- *Story: "21%+" band shows negative margin*

### Visual 4: Sub-Category Matrix (Matrix visual)

- **Rows:** `category`, `sub_category`
- **Values:** `[Total Revenue]`, `[Total Profit]`, `[Profit Margin %]`
- **Conditional formatting** on Margin %: color scale (red → yellow → green)
- Title: **"Sub-Category Performance"**
- *Story: Tables and Bookcases show red margins*

### Visual 5: Monthly Profit Trend by Category (Line chart)

- **X-axis:** `year_month`
- **Y-axis:** `[Total Profit]`
- **Legend:** `category`
- Title: **"Profit Trend by Category"**

### Copy slicers from Page 1

Select all slicers on Page 1 → **Ctrl+C** → Page 2 → **Ctrl+V**

---

## Step 7: Page 3 — Customer Analysis (20 min)

Rename page → **Customer Analysis**

### Visual 1: Revenue by Segment (Stacked column)

- **X-axis:** `sales_executive[segment]`
- **Y-axis:** `[Total Revenue]`
- **Legend:** `sales_executive[region]` (optional — shows segment × region)
- Title: **"Revenue by Customer Segment"**

### Visual 2: Margin by Segment (Clustered bar)

- **Y-axis:** `segment`
- **X-axis:** `[Profit Margin %]`
- Title: **"Profitability by Segment"**

### Visual 3: Regional Customer Count (Card or bar)

- Use `regional_summary` table if imported:
  - Bar chart: `region` × `customers` (sum)
- Or from sales_executive: `[Total Customers]` by region
- Title: **"Customer Locations by Region"**

### Visual 4: Top 20 Customers — Pareto (Line and clustered column chart)

1. **Insert → Line and clustered column chart**
2. **Shared axis:** `customer_name`
3. **Column y-axis:** `[Total Revenue]`
4. **Line y-axis:** Use **Quick measure → Running total** on Revenue, show as % of grand total
   - Or filter to Top 20 customers first
5. **Filters:** Top 20 by `[Total Revenue]`
6. Title: **"Customer Concentration (Pareto)"**

### Visual 5: Customer Detail Table

- `customer_name`, `segment`, `region`, `city`
- `[Total Revenue]`, `[Total Profit]`, `[Profit Margin %]`
- Enable **search** on customer_name
- Title: **"Customer Detail"**

---

## Step 8: Polish & professional touches (10 min)

### Sync slicers across pages

1. **View → Sync slicers**
2. Check all pages for: Date, Region, Segment, Category
3. **Advanced options → Visible** on all pages

### Add KPI insight text boxes

On Executive Overview, add a small text box:
```
Key insight: Furniture drives 32% of revenue but only 2.5% margin.
Central region margin (7.9%) trails West (14.9%).
```

### Add "Last refreshed" footer

Text box (bottom right):
```
Data: Apex Distribution  |  Period: Jan 2014 – Dec 2017  |  Refreshed: [today's date]
```

### Page navigation (optional, impressive for portfolio)

1. **Insert → Buttons → Navigator**
2. Add page navigator buttons at top
3. Or use **View → Bookmarks** for a guided demo

### Tooltip page (optional)

1. New page → name `Tooltip` → **Page information → Allow use as tooltip**
2. Small card visuals with measure definitions
3. Assign as tooltip on KPI cards

---

## Step 9: Save screenshots for GitHub (5 min)

1. Go to each page at **fit-to-page** zoom
2. **File → Export → Export current page as image** (or screenshot)
3. Save to `powerbi/screenshots/`:
   - `01_executive_overview.png`
   - `02_product_profitability.png`
   - `03_customer_analysis.png`

4. Update `README.md` dashboard preview section with these images

---

## Step 10: Final checklist

- [ ] KPI cards match validation targets ($2.30M / 12.5%)
- [ ] Date slicer filters all visuals correctly
- [ ] Theme applied consistently
- [ ] All 3 pages named professionally (not "Page 1")
- [ ] Slicers synced across pages
- [ ] Screenshots saved to `powerbi/screenshots/`
- [ ] `.pbix` saved locally (gitignored — don't commit)

---

## Interview talking points

When presenting this dashboard:

1. **"I built the full pipeline"** — CSV → SQL star schema → Python validation → Power BI
2. **"Furniture is the story"** — walk from KPI card → category donut → margin bar on Page 2
3. **"I made a modeling decision"** — customer grain = ship-to location (780 customers in multiple regions)
4. **"Discount policy recommendation"** — show the 21%+ discount visual, cite -37% margin
5. **"I validated the data"** — mention 0 nulls, 1,871 loss-making lines flagged before dashboard

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Revenue shows wrong total | Check `sales_amount` is Decimal, not Text |
| Date slicer doesn't filter | Verify relationship `Dim Date` → `sales_executive` is active |
| Profit Margin shows 12,470% | Format as Percentage, not Whole number |
| Too many customer names on Pareto | Apply Top 20 filter on the visual |
| YoY measure returns blank | Ensure `Dim Date` is marked as date table and relationship exists |

---

## File reference

| File | Purpose |
|------|---------|
| `dax/measures.dax` | All DAX measures to copy |
| `theme/apex_distribution.json` | Importable color theme |
| `power_query/sales_executive.pq` | Power Query M with correct types |
| `dashboard_notes.md` | Quick reference checklist |
