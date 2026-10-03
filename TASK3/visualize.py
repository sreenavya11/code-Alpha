"""
visualize.py
CodeAlpha Data Analytics Internship - Task 3: Data Visualization

Dataset: E-commerce Sales (ecommerce_sales.csv)

Produces a set of presentation-ready charts telling the story of the business:
where revenue comes from, where profit comes from, and where the risks are.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("ecommerce_sales.csv", parse_dates=["order_date"])
df = df.drop_duplicates()
df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())
df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())

# 1. Monthly sales trend
df["order_month"] = df["order_date"].dt.to_period("M")
monthly = df.groupby("order_month")["sales"].sum()
plt.figure(figsize=(10, 5))
monthly.plot(kind="line", marker="o", color="#2563eb")
plt.title("Monthly Sales Trend (2023-2024)", fontsize=13, fontweight="bold")
plt.ylabel("Total Sales ($)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("charts/01_monthly_sales_trend.png")
plt.close()

# 2. Sales & Profit by category
cat_summary = df.groupby("category")[["sales", "profit"]].sum().sort_values("sales", ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
cat_summary.plot(kind="bar", ax=ax, color=["#2563eb", "#16a34a"])
plt.title("Sales & Profit by Category", fontsize=13, fontweight="bold")
plt.ylabel("Amount ($)")
plt.xlabel("Category")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("charts/02_sales_profit_by_category.png")
plt.close()

# 3. Regional sales share
region_summary = df.groupby("region")["sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 7))
plt.pie(region_summary, labels=region_summary.index, autopct="%1.1f%%",
        colors=sns.color_palette("Blues_r", len(region_summary)), startangle=90)
plt.title("Sales Share by Region", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/03_sales_share_by_region.png")
plt.close()

# 4. Discount vs Profit
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df.sample(800, random_state=1), x="discount", y="profit",
                 hue="category", alpha=0.6, palette="tab10", s=25)
plt.title("Discount vs Profit — Where Discounting Turns Unprofitable", fontsize=12, fontweight="bold")
plt.xlabel("Discount")
plt.ylabel("Profit ($)")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("charts/04_discount_vs_profit.png")
plt.close()

# 5. Sales distribution
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
sns.histplot(df["sales"], bins=40, kde=True, ax=axes[0], color="#2563eb")
axes[0].set_title("Distribution of Sales")
sns.boxplot(x=df["sales"], ax=axes[1], color="#f59e0b")
axes[1].set_title("Sales Outliers")
plt.tight_layout()
plt.savefig("charts/05_sales_distribution.png")
plt.close()

# 6. Correlation heatmap
num_cols = ["unit_price", "quantity", "discount", "sales", "profit", "customer_age", "customer_rating"]
corr = df[num_cols].corr()
plt.figure(figsize=(7, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Correlation Heatmap", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/06_correlation_heatmap.png")
plt.close()

# 7. Orders by segment & shipping mode
seg_ship = df.groupby(["customer_segment", "ship_mode"]).size().unstack()
seg_ship.plot(kind="bar", figsize=(9, 5), color=sns.color_palette("Set2", 3))
plt.title("Orders by Customer Segment & Shipping Mode", fontsize=13, fontweight="bold")
plt.ylabel("Number of Orders")
plt.xlabel("Customer Segment")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/07_segment_shipmode.png")
plt.close()

# 8. Profit margin % by category (a focused "story" chart)
cat_summary["margin_pct"] = (cat_summary["profit"] / cat_summary["sales"] * 100)
plt.figure(figsize=(9, 5))
colors = sns.color_palette("RdYlGn", len(cat_summary))
order = cat_summary.sort_values("margin_pct")
bars = plt.barh(order.index, order["margin_pct"], color=colors)
plt.title("Profit Margin % by Category — Revenue Leader Isn't the Margin Leader", fontsize=12, fontweight="bold")
plt.xlabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("charts/08_profit_margin_by_category.png")
plt.close()

print("8 charts saved to charts/ folder.")
