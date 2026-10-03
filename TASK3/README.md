# CodeAlpha_DataVisualization

**Task:** Data Visualization (Task 3)
**Tools:** Python, matplotlib, seaborn
**Dataset:** `ecommerce_sales.csv` — synthetic e-commerce sales data, 2023–2024

## Charts produced
| # | Chart | Story it tells |
|---|---|---|
| 01 | Monthly sales trend | Revenue seasonality across 2023–2024 |
| 02 | Sales & profit by category | Which categories drive revenue vs. profit |
| 03 | Sales share by region (pie) | Regional contribution to total revenue |
| 04 | Discount vs profit (scatter) | The point where discounting starts losing money |
| 05 | Sales distribution (hist + boxplot) | Spread and outliers in order value |
| 06 | Correlation heatmap | Relationships between all numeric variables |
| 07 | Orders by segment & shipping mode | Order volume by customer type & shipping choice |
| 08 | Profit margin % by category (horizontal bar) | Electronics leads revenue but Beauty leads margin |

## How to run
```bash
pip install pandas matplotlib seaborn
python visualize.py
```

## Output
All 8 charts are saved as PNG files in `charts/`.

## Key takeaway
Electronics is the top revenue category by a wide margin, but it has the
**thinnest profit margin** — Beauty and Clothing are far smaller in volume but
much more profitable per dollar of sales. This is the kind of insight that's
much easier to see visually than in a raw table (see chart 08 and 02 together).

For the underlying statistical analysis and data-cleaning steps behind these
charts, see the companion **Task 2 (EDA)** project.

---
*Submitted as part of the CodeAlpha Data Analytics Internship.*
