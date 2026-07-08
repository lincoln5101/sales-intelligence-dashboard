// Paste into Power Query Advanced Editor when importing sales_executive.csv
// Home → Transform Data → sales_executive query → Advanced Editor

let
    Source = Csv.Document(
        File.Contents("FULL_PATH_TO/data/exports/sales_executive.csv"),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"sales_key", Int64.Type},
        {"row_id", Int64.Type},
        {"order_id", type text},
        {"order_date", type date},
        {"order_year", Int64.Type},
        {"order_quarter", Int64.Type},
        {"order_month", Int64.Type},
        {"month_name", type text},
        {"year_month", type text},
        {"ship_date", type date},
        {"customer_id", type text},
        {"customer_name", type text},
        {"segment", type text},
        {"city", type text},
        {"state", type text},
        {"region", type text},
        {"country", type text},
        {"product_id", type text},
        {"product_name", type text},
        {"category", type text},
        {"sub_category", type text},
        {"quantity", Int64.Type},
        {"unit_price", type number},
        {"discount", type number},
        {"sales_amount", type number},
        {"profit", type number},
        {"ship_mode", type text},
        {"line_margin_pct", type number},
        {"discount_band", type text},
        {"is_loss_making", Int64.Type}
    }),
    SortedDates = Table.Sort(ChangedTypes, {{"order_date", Order.Ascending}})
in
    SortedDates
