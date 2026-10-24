"""Sales data generator (NumPy + Pandas).
Run:  python generate_data.py
Creates data/sales_data.csv with random sales records and a few missing values.
"""
import os
import numpy as np
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sales_data.csv")


def generate_sales_data(n=500, path=DATA_PATH, seed=42):
    np.random.seed(seed)

    dates = pd.date_range("2025-01-01", "2025-12-31", periods=n)
    categories = np.random.choice(["Electronics", "Clothing", "Grocery", "Furniture"], n)
    regions = np.random.choice(["North", "South", "East", "West"], n)
    segments = np.random.choice(["Retail", "Corporate", "Online"], n)
    quantity = np.random.randint(1, 20, n)
    unit_price = np.random.randint(100, 5000, n)
    revenue = (quantity * unit_price).astype(float)

    df = pd.DataFrame({
        "Date": dates.date,
        "Category": categories,
        "Region": regions,
        "Segment": segments,
        "Quantity": quantity,
        "Revenue": revenue,
    })

    # Missing values on purpose, so data cleaning can be demonstrated
    missing_idx = np.random.choice(n, 15, replace=False)
    df.loc[missing_idx, "Revenue"] = np.nan

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    p = generate_sales_data()
    print("Data saved at:", p)
