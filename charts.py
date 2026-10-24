"""Chart functions. Each one draws on a Matplotlib Figure given to it,
so the same code works for Tkinter embedding and for saving PNG files.
"""
import seaborn as sns
from matplotlib.ticker import FuncFormatter

from analyzer import SalesAnalyzer

money = FuncFormatter(lambda x, _: f"{x/1000:,.0f}K")


def _empty(fig, msg="Selected filter ke liye data nahi hai"):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, msg, ha="center", va="center", fontsize=13)
    ax.axis("off")


def line_chart(fig, df):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    m = SalesAnalyzer.monthly_sales(df)
    ax.plot(m.index, m.values, marker="o", color="#2563eb", linewidth=2)
    ax.set_title("Monthly Sales Trend (Line Plot)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(money)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()


def area_chart(fig, df):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    m = SalesAnalyzer.monthly_sales(df)
    ax.fill_between(m.index, m.values, color="#93c5fd", alpha=0.8)
    ax.plot(m.index, m.values, color="#1d4ed8")
    ax.set_title("Monthly Sales Trend (Area Chart)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(money)
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()


def bar_chart(fig, df, column="Category", note=""):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    s = SalesAnalyzer.sales_by(df, column)
    bars = ax.bar(s.index, s.values, color=["#2563eb", "#16a34a", "#f59e0b", "#dc2626"][:len(s)])
    ax.bar_label(bars, labels=[f"{v/1000:,.0f}K" for v in s.values], padding=3)
    ax.set_title(f"Sales by {column} (Bar Plot)" + (f"  [{note}]" if note else ""))
    ax.set_xlabel(column)
    ax.set_ylabel("Revenue")
    ax.yaxis.set_major_formatter(money)
    fig.tight_layout()


def pie_chart(fig, df, column="Segment"):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    s = SalesAnalyzer.sales_by(df, column)
    ax.pie(s.values, labels=s.index, autopct="%1.1f%%", startangle=90,
           wedgeprops={"edgecolor": "white"})
    ax.set_title(f"Sales Distribution by {column} (Pie Chart)")
    fig.tight_layout()


def histogram(fig, df):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.hist(df["Revenue"], bins=20, color="#8b5cf6", edgecolor="white")
    ax.set_title("Order Revenue Distribution (Histogram)")
    ax.set_xlabel("Revenue per order")
    ax.set_ylabel("Number of orders")
    fig.tight_layout()


def heatmap(fig, df):
    if df.empty:
        return _empty(fig)
    fig.clear()
    ax = fig.add_subplot(111)
    mat = SalesAnalyzer.region_category_matrix(df)
    sns.heatmap(mat, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Revenue: Region vs Category (Seaborn Heatmap)")
    fig.tight_layout()
