"""
generate_data.py
Creates a realistic synthetic e-commerce sales dataset used by
Task 2 (EDA) and Task 3 (Data Visualization).

Run this first: python generate_data.py
Produces: ecommerce_sales.csv in this same folder.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000

categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Beauty", "Sports"]
category_weights = [0.25, 0.20, 0.18, 0.12, 0.13, 0.12]

regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.22, 0.24, 0.20, 0.18, 0.16]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.55, 0.28, 0.17]

ship_modes = ["Standard", "Express", "Same Day"]
ship_weights = [0.6, 0.3, 0.1]

price_ranges = {
    "Electronics": (50, 1200),
    "Clothing": (10, 150),
    "Home & Kitchen": (15, 400),
    "Books": (5, 60),
    "Beauty": (5, 120),
    "Sports": (10, 300),
}

dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")

rows = []
for i in range(N):
    order_date = pd.Timestamp(np.random.choice(dates))
    category = np.random.choice(categories, p=category_weights)
    region = np.random.choice(regions, p=region_weights)
    segment = np.random.choice(segments, p=segment_weights)
    ship_mode = np.random.choice(ship_modes, p=ship_weights)

    low, high = price_ranges[category]
    unit_price = round(np.random.uniform(low, high), 2)
    quantity = np.random.randint(1, 8)

    base_discount = np.random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.3],
                                      p=[0.35, 0.2, 0.2, 0.12, 0.08, 0.05])
    if order_date.month in (11, 12):
        base_discount = min(base_discount + 0.05, 0.5)

    sales = round(unit_price * quantity * (1 - base_discount), 2)

    margin_map = {
        "Electronics": 0.12, "Clothing": 0.25, "Home & Kitchen": 0.18,
        "Books": 0.15, "Beauty": 0.30, "Sports": 0.20
    }
    margin = margin_map[category] - base_discount * 0.8
    profit = round(sales * margin, 2)

    customer_age = np.random.randint(18, 70)
    if np.random.rand() < 0.03:
        customer_age = np.nan

    rating = round(np.random.normal(4.1, 0.8), 1)
    rating = min(max(rating, 1.0), 5.0)
    if np.random.rand() < 0.05:
        rating = np.nan

    rows.append({
        "order_id": f"ORD{100000+i}",
        "order_date": order_date.date(),
        "category": category,
        "region": region,
        "customer_segment": segment,
        "ship_mode": ship_mode,
        "unit_price": unit_price,
        "quantity": quantity,
        "discount": base_discount,
        "sales": sales,
        "profit": profit,
        "customer_age": customer_age,
        "customer_rating": rating,
    })

df = pd.DataFrame(rows)

dupes = df.sample(15, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

df.to_csv("ecommerce_sales.csv", index=False)
print(f"Dataset created: {df.shape[0]} rows, {df.shape[1]} columns -> ecommerce_sales.csv")
