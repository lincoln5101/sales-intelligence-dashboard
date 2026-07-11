# Generate chart previews from export data (optional, if you need placeholder images).
# Usage: python python/generate_preview_charts.py

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = PROJECT_ROOT / "data" / "exports"
SCREENSHOT_DIR = PROJECT_ROOT / "powerbi" / "screenshots"

COLORS = {
    "primary": "#4472C4",
    "positive": "#70AD47",
    "negative": "#C00000",
    "accent": "#ED7D31",
    "neutral": "#A5A5A5",
    "regions": {"West": "#4472C4", "East": "#70AD47", "Central": "#ED7D31", "South": "#A5A5A5"},
    "categories": {"Technology": "#4472C4", "Furniture": "#ED7D31", "Office Supplies": "#70AD47"},
}


def fmt_currency(x, _pos):
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    return f"${x/1_000:.0f}K"


def add_title(fig, title, subtitle="Apex Distribution Inc.  |  2014–2017"):
    fig.suptitle(title, fontsize=14, fontweight="bold", color="#264478", y=0.98)
    fig.text(0.5, 0.93, subtitle, ha="center", fontsize=9, color="#605E5C")


def chart_executive_overview():
    monthly = pd.read_csv(EXPORT_DIR / "monthly_kpis.csv")
    regional = pd.read_csv(EXPORT_DIR / "regional_summary.csv")
    category = pd.read_csv(EXPORT_DIR / "category_summary.csv")
    sales = pd.read_csv(EXPORT_DIR / "sales_executive.csv")

    fig = plt.figure(figsize=(16, 9), facecolor="#F3F2F1")
    gs = fig.add_gridspec(3, 4, hspace=0.45, wspace=0.35, left=0.06, right=0.96, top=0.88, bottom=0.08)

    # KPI cards
    total_rev = sales["sales_amount"].sum()
    total_profit = sales["profit"].sum()
    margin = total_profit / total_rev * 100
    orders = sales["order_id"].nunique()
    aov = total_rev / orders

    kpis = [
        ("Total Revenue", f"${total_rev:,.0f}"),
        ("Total Profit", f"${total_profit:,.0f}"),
        ("Profit Margin", f"{margin:.1f}%"),
        ("Total Orders", f"{orders:,}"),
        ("Avg Order Value", f"${aov:,.0f}"),
    ]
    for i, (label, value) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i % 4 if i < 4 else i - 4])
        if i == 4:
            ax = fig.add_subplot(gs[0, 3])
        ax.set_facecolor("white")
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=18, fontweight="bold", color="#252423")
        ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=9, color="#605E5C")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#EDEBE9")

    # Revenue & profit trend
    ax1 = fig.add_subplot(gs[1, :2])
    ax1.plot(monthly["year_month"], monthly["revenue"] / 1000, color=COLORS["primary"], linewidth=2, label="Revenue")
    ax1.plot(monthly["year_month"], monthly["profit"] / 1000, color=COLORS["positive"], linewidth=2, label="Profit")
    ax1.set_title("Revenue & Profit Trend", fontsize=11, fontweight="bold")
    ax1.set_ylabel("$ Thousands")
    ax1.legend(loc="upper left", frameon=False)
    ax1.tick_params(axis="x", rotation=45, labelsize=7)
    ax1.set_facecolor("white")

    # Revenue by region
    ax2 = fig.add_subplot(gs[1, 2:])
    reg = regional.groupby("region")["revenue"].sum().sort_values(ascending=True)
    bar_colors = [COLORS["regions"].get(r, COLORS["neutral"]) for r in reg.index]
    ax2.barh(reg.index, reg.values / 1000, color=bar_colors)
    ax2.set_title("Revenue by Region", fontsize=11, fontweight="bold")
    ax2.set_xlabel("$ Thousands")
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_currency))
    ax2.set_facecolor("white")

    # Category donut (bar substitute)
    ax3 = fig.add_subplot(gs[2, 0])
    cat_colors = [COLORS["categories"].get(c, COLORS["neutral"]) for c in category["category"]]
    ax3.pie(category["revenue"], labels=category["category"], autopct="%1.0f%%", colors=cat_colors, startangle=90)
    ax3.set_title("Revenue by Category", fontsize=11, fontweight="bold")

    # Margin by category
    ax4 = fig.add_subplot(gs[2, 1])
    cat_sorted = category.sort_values("margin_pct")
    bar_c = [COLORS["categories"].get(c, COLORS["neutral"]) for c in cat_sorted["category"]]
    ax4.barh(cat_sorted["category"], cat_sorted["margin_pct"], color=bar_c)
    ax4.axvline(margin, color=COLORS["neutral"], linestyle="--", linewidth=1, label=f"Avg {margin:.1f}%")
    ax4.set_title("Margin by Category", fontsize=11, fontweight="bold")
    ax4.set_xlabel("Margin %")
    ax4.set_facecolor("white")

    # Top customers
    ax5 = fig.add_subplot(gs[2, 2:])
    top = sales.groupby("customer_name").agg(revenue=("sales_amount", "sum"), profit=("profit", "sum")).reset_index()
    top = top.nlargest(10, "revenue")
    x = range(len(top))
    ax5.bar(x, top["revenue"] / 1000, color=COLORS["primary"], label="Revenue", alpha=0.85)
    ax5.bar(x, top["profit"] / 1000, color=COLORS["positive"], label="Profit", alpha=0.85)
    ax5.set_xticks(x)
    ax5.set_xticklabels(top["customer_name"], rotation=45, ha="right", fontsize=7)
    ax5.set_title("Top 10 Customers", fontsize=11, fontweight="bold")
    ax5.set_ylabel("$ Thousands")
    ax5.legend(frameon=False)
    ax5.set_facecolor("white")

    add_title(fig, "Executive Overview")
    out = SCREENSHOT_DIR / "01_executive_overview.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved {out.name}")


def chart_product_profitability():
    sales = pd.read_csv(EXPORT_DIR / "sales_executive.csv")

    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor="#F3F2F1")
    fig.subplots_adjust(hspace=0.38, wspace=0.3, top=0.88, bottom=0.1)

    # Discount impact
    disc = sales.groupby("discount_band").agg(
        revenue=("sales_amount", "sum"), profit=("profit", "sum")
    ).reset_index()
    disc["margin"] = disc["profit"] / disc["revenue"] * 100
    order = ["No Discount", "1-10%", "11-20%", "21%+"]
    disc["discount_band"] = pd.Categorical(disc["discount_band"], categories=order, ordered=True)
    disc = disc.sort_values("discount_band")
    colors = [COLORS["positive"] if m >= 0 else COLORS["negative"] for m in disc["margin"]]
    axes[0, 0].bar(disc["discount_band"], disc["margin"], color=colors)
    axes[0, 0].axhline(0, color="black", linewidth=0.5)
    axes[0, 0].set_title("Margin by Discount Band", fontweight="bold")
    axes[0, 0].set_ylabel("Margin %")
    axes[0, 0].set_facecolor("white")

    # Sub-category margins
    sub = sales.groupby(["category", "sub_category"]).agg(
        revenue=("sales_amount", "sum"), profit=("profit", "sum")
    ).reset_index()
    sub["margin"] = sub["profit"] / sub["revenue"] * 100
    sub = sub[sub["revenue"] > 5000].nsmallest(8, "margin")
    labels = sub["sub_category"] + " (" + sub["category"].str[:3] + ")"
    bar_colors = [COLORS["negative"] if m < 0 else COLORS["accent"] for m in sub["margin"]]
    axes[0, 1].barh(labels, sub["margin"], color=bar_colors)
    axes[0, 1].set_title("Lowest-Margin Sub-Categories", fontweight="bold")
    axes[0, 1].set_xlabel("Margin %")
    axes[0, 1].set_facecolor("white")

    # Revenue vs profit by category
    cat = sales.groupby("category").agg(revenue=("sales_amount", "sum"), profit=("profit", "sum")).reset_index()
    x = range(len(cat))
    w = 0.35
    axes[1, 0].bar([i - w/2 for i in x], cat["revenue"]/1000, w, color=COLORS["primary"], label="Revenue")
    axes[1, 0].bar([i + w/2 for i in x], cat["profit"]/1000, w, color=COLORS["positive"], label="Profit")
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(cat["category"])
    axes[1, 0].set_title("Revenue vs Profit by Category", fontweight="bold")
    axes[1, 0].set_ylabel("$ Thousands")
    axes[1, 0].legend(frameon=False)
    axes[1, 0].set_facecolor("white")

    # Profit trend by category
    sales["order_date"] = pd.to_datetime(sales["order_date"])
    sales["ym"] = sales["order_date"].dt.to_period("M").astype(str)
    trend = sales.groupby(["ym", "category"])["profit"].sum().reset_index()
    for cat in trend["category"].unique():
        data = trend[trend["category"] == cat]
        axes[1, 1].plot(data["ym"], data["profit"]/1000, label=cat,
                        color=COLORS["categories"].get(cat, COLORS["neutral"]), linewidth=1.5)
    axes[1, 1].set_title("Profit Trend by Category", fontweight="bold")
    axes[1, 1].set_ylabel("$ Thousands")
    axes[1, 1].tick_params(axis="x", rotation=45, labelsize=6)
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].set_facecolor("white")

    add_title(fig, "Product & Profitability Analysis")
    out = SCREENSHOT_DIR / "02_product_profitability.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved {out.name}")


def chart_customer_analysis():
    sales = pd.read_csv(EXPORT_DIR / "sales_executive.csv")

    fig, axes = plt.subplots(2, 2, figsize=(16, 9), facecolor="#F3F2F1")
    fig.subplots_adjust(hspace=0.38, wspace=0.3, top=0.88, bottom=0.1)

    # Revenue by segment
    seg = sales.groupby("segment")["sales_amount"].sum().sort_values(ascending=True)
    axes[0, 0].barh(seg.index, seg.values / 1000, color=COLORS["primary"])
    axes[0, 0].set_title("Revenue by Segment", fontweight="bold")
    axes[0, 0].set_xlabel("$ Thousands")
    axes[0, 0].set_facecolor("white")

    # Margin by segment
    seg2 = sales.groupby("segment").agg(revenue=("sales_amount", "sum"), profit=("profit", "sum")).reset_index()
    seg2["margin"] = seg2["profit"] / seg2["revenue"] * 100
    axes[0, 1].bar(seg2["segment"], seg2["margin"], color=[COLORS["primary"], COLORS["positive"], COLORS["accent"]])
    axes[0, 1].set_title("Margin by Segment", fontweight="bold")
    axes[0, 1].set_ylabel("Margin %")
    axes[0, 1].set_facecolor("white")

    # Revenue by segment and region
    seg_reg = sales.groupby(["segment", "region"])["sales_amount"].sum().unstack(fill_value=0)
    seg_reg.plot(kind="bar", ax=axes[1, 0], color=[COLORS["regions"].get(r, COLORS["neutral"]) for r in seg_reg.columns])
    axes[1, 0].set_title("Revenue by Segment & Region", fontweight="bold")
    axes[1, 0].set_ylabel("$ ")
    axes[1, 0].tick_params(axis="x", rotation=0)
    axes[1, 0].legend(title="Region", frameon=False, fontsize=8)
    axes[1, 0].set_facecolor("white")
    axes[1, 0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_currency))

    # Pareto top 15
    cust = sales.groupby("customer_name")["sales_amount"].sum().sort_values(ascending=False)
    top15 = cust.head(15)
    cum_pct = top15.cumsum() / cust.sum() * 100
    ax = axes[1, 1]
    ax.bar(range(len(top15)), top15.values / 1000, color=COLORS["primary"], alpha=0.8)
    ax2 = ax.twinx()
    ax2.plot(range(len(top15)), cum_pct.values, color=COLORS["accent"], marker="o", linewidth=2)
    ax2.axhline(80, color=COLORS["negative"], linestyle="--", linewidth=1, alpha=0.7)
    ax.set_xticks(range(len(top15)))
    ax.set_xticklabels([n[:12] for n in top15.index], rotation=45, ha="right", fontsize=7)
    ax.set_title("Customer Concentration (Top 15)", fontweight="bold")
    ax.set_ylabel("$ Thousands")
    ax2.set_ylabel("Cumulative %")
    ax.set_facecolor("white")

    add_title(fig, "Customer Analysis")
    out = SCREENSHOT_DIR / "03_customer_analysis.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved {out.name}")


def main():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=0.9)
    print("\nGenerating dashboard preview charts...")
    chart_executive_overview()
    chart_product_profitability()
    chart_customer_analysis()
    print("\nDone. Replace these with Power BI screenshots when ready.\n")


if __name__ == "__main__":
    main()
