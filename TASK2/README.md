# CodeAlpha_EDA

**Task:** Exploratory Data Analysis (Task 2)
**Tools:** Python, pandas, numpy, matplotlib, seaborn
**Dataset:** `ecommerce_sales.csv` — synthetic e-commerce sales data, 2023–2024

## Process
1. **Structure check** — shape, column types, sample rows.
2. **Data quality check** — missing values, duplicate rows, ID uniqueness.
3. **Cleaning** — dropped 15 duplicate rows; filled missing `customer_age` and
   `customer_rating` with the column median.
4. **Summary statistics** — descriptive stats for all numeric columns, value
   counts for categorical columns.
5. **Hypotheses tested:**
   - Do higher discounts reduce profit? → **Yes**, correlation = -0.48.
   - Which category has the highest average order value? → **Electronics** (~$2,243/order).
   - Does shipping mode preference differ by customer segment? → Barely — all
     segments favor Standard shipping (~58–60%).
   - Do ratings differ meaningfully by category? → Not much — all hover around 4.0–4.1.
6. **Outlier/anomaly detection** — IQR method flags ~10.5% of orders as high-value
   outliers; 7.0% of orders have negative profit (over-discounted).

## How to run
```bash
pip install pandas numpy matplotlib seaborn
python eda_analysis.py
```

## Output
- `eda_report.txt` — full text report of every step above
- `charts/eda_diagnostics.png` — rating distribution + sales outlier boxplot

For polished, presentation-ready charts and data storytelling, see the
companion **Task 3 (Data Visualization)** project, which uses this same dataset.

---
*Submitted as part of the CodeAlpha Data Analytics Internship.*
