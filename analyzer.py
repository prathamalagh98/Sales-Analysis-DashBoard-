"""SalesAnalyzer class: loading, cleaning, filtering and summarising sales data.
Covers: classes (Unit 2), NumPy/Pandas (Unit 2), lambda/map/filter/reduce (Unit 1).
"""
from functools import reduce

import numpy as np
import pandas as pd


class SalesAnalyzer:
    REQUIRED_COLUMNS = ["Date", "Category", "Region", "Segment", "Quantity", "Revenue"]

    def __init__(self, csv_path=None):
        self.df = pd.DataFrame()
        self.missing_filled = 0
        if csv_path:
            self.load(csv_path)

    # ---------- loading & cleaning ----------
    def load(self, csv_path):
        df = pd.read_csv(csv_path)
        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError("CSV me ye columns missing hain: " + ", ".join(missing))
        df["Date"] = pd.to_datetime(df["Date"])
        self.df = self._clean(df)
        return self.df

    def _clean(self, df):
        """Fill missing numeric values with the median (as in Experiment 4b)."""
        self.missing_filled = int(df[["Quantity", "Revenue"]].isnull().sum().sum())
        for col in ("Quantity", "Revenue"):
            df[col] = df[col].fillna(df[col].median())
        df = df.dropna(subset=["Date", "Category", "Region", "Segment"])
        df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
        return df.reset_index(drop=True)

    # ---------- filtering ----------
    def filtered(self, category="All", region="All"):
        df = self.df
        if category != "All":
            df = df[df["Category"] == category]
        if region != "All":
            df = df[df["Region"] == region]
        return df

    def unique_values(self, column):
        return ["All"] + sorted(self.df[column].unique().tolist())

    # ---------- statistics ----------
    @staticmethod
    def total_revenue(df):
        return float(np.sum(df["Revenue"].to_numpy()))

    @staticmethod
    def average_revenue(df):
        return float(np.mean(df["Revenue"].to_numpy())) if len(df) else 0.0

    @staticmethod
    def total_quantity(df):
        return int(df["Quantity"].sum())

    @staticmethod
    def best(df, column):
        if df.empty:
            return "-"
        return df.groupby(column)["Revenue"].sum().idxmax()

    @staticmethod
    def monthly_sales(df):
        return df.groupby("Month")["Revenue"].sum()

    @staticmethod
    def sales_by(df, column):
        return df.groupby(column)["Revenue"].sum().sort_values(ascending=False)

    @staticmethod
    def region_category_matrix(df):
        return df.pivot_table(index="Region", columns="Category",
                              values="Revenue", aggfunc="sum", fill_value=0)

    @staticmethod
    def big_orders_total(df, limit=30000):
        """Unit 1 demo: filter + map + reduce with lambda."""
        revenues = df["Revenue"].tolist()
        big = list(filter(lambda r: r >= limit, revenues))
        in_thousands = list(map(lambda r: r / 1000, big))
        total = reduce(lambda a, b: a + b, in_thousands, 0)
        return len(big), total
