"""
eda_analysis.py
CodeAlpha Data Analytics Internship - Task 2: Exploratory Data Analysis (EDA)

Dataset: E-commerce Sales (ecommerce_sales.csv)

Steps:
  1. Understand structure (shape, dtypes)
  2. Check data quality (missing values, duplicates)
  3. Clean the data
  4. Summary statistics
  5. Ask & answer meaningful questions using stats + light visuals
  6. Detect outliers / anomalies
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

df = pd.read_csv("ecommerce_sales.csv", parse_dates=["order_date"])

report = []
def log(msg=""):
    print(msg)
    report.append(str(msg))

log("=" * 60)
log("STEP 1: DATA STRUCTURE")
log("=" * 60)
log(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
log(f"\nColumn types:\n{df.dtypes}")
log(f"\nFirst 3 rows:\n{df.head(3).to_string()}")

log("\n" + "=" * 60)
log("STEP 2: DATA QUALITY CHECK")
log("=" * 60)
missing = df.isnull().sum()
missing = missing[missing > 0]
log(f"Missing values:\n{missing if len(missing) else 'None'}")
log(f"\nDuplicate rows: {df.duplicated().sum()}")
log(f"Unique order_ids vs total rows: {df['order_id'].nunique()} / {len(df)}")

log("\n" + "=" * 60)
log("STEP 3: CLEANING")
log("=" * 60)
before = len(df)
df = df.drop_duplicates()
df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())
df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())
log(f"Removed {before - len(df)} duplicate rows.")
log("Filled missing customer_age / customer_rating with column median.")

log("\n" + "=" * 60)
log("STEP 4: SUMMARY STATISTICS")
log("=" * 60)
num_cols = ["unit_price", "quantity", "discount", "sales", "profit",
            "customer_age", "customer_rating"]
log(df[num_cols].describe().round(2).to_string())

log("\nCategorical value counts:")
for col in ["category", "region", "customer_segment", "ship_mode"]:
    log(f"\n{col}:\n{df[col].value_counts().to_string()}")

log("\n" + "=" * 60)
log("STEP 5: HYPOTHESES / QUESTIONS")
log("=" * 60)

# H1: Higher discounts hurt profit
corr_disc_profit = df["discount"].corr(df["profit"])
log(f"\nH1: Does discount reduce profit? Correlation(discount, profit) = {corr_disc_profit:.2f}")
log("  -> " + ("Supported: negative correlation, higher discounts reduce profit."
                if corr_disc_profit < -0.2 else "Weak/no relationship."))

# H2: Electronics has the highest average order value
avg_by_cat = df.groupby("category")["sales"].mean().sort_values(ascending=False)
log(f"\nH2: Which category has the highest average order value?\n{avg_by_cat.round(2).to_string()}")

# H3: Express/Same Day shipping used more by Corporate customers?
seg_ship = pd.crosstab(df["customer_segment"], df["ship_mode"], normalize="index") * 100
log(f"\nH3: Shipping mode preference by segment (% of orders):\n{seg_ship.round(1).to_string()}")

# H4: Ratings differ meaningfully across categories?
rating_by_cat = df.groupby("category")["customer_rating"].mean().sort_values(ascending=False)
log(f"\nH4: Average customer rating by category:\n{rating_by_cat.round(2).to_string()}")

log("\n" + "=" * 60)
log("STEP 6: OUTLIER / ANOMALY DETECTION")
log("=" * 60)
q1, q3 = df["sales"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["sales"] < lower) | (df["sales"] > upper)]
log(f"Sales outliers (IQR method): {len(outliers)} rows ({len(outliers)/len(df)*100:.1f}% of data)")
log(f"Valid sales range (non-outlier): {lower:.2f} to {upper:.2f}")

neg_profit = df[df["profit"] < 0]
log(f"\nOrders with negative profit: {len(neg_profit)} ({len(neg_profit)/len(df)*100:.1f}%)")

# a couple of light diagnostic plots to support the EDA (not polished storytelling - see Task 3 for that)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
missing_counts = df.isnull().sum()
sns.histplot(df["customer_rating"], bins=20, ax=axes[0], color="#64748b")
axes[0].set_title("Distribution: customer_rating")
sns.boxplot(x=df["sales"], ax=axes[1], color="#f59e0b")
axes[1].set_title("Outlier check: sales")
plt.tight_layout()
plt.savefig("charts/eda_diagnostics.png")
plt.close()

log("\nDiagnostic plot saved to charts/eda_diagnostics.png")

with open("eda_report.txt", "w") as f:
    f.write("\n".join(report))

print("\nDone. Full report saved to eda_report.txt")
