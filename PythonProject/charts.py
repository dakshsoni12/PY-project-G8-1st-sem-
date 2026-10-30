#!/usr/bin/env python3
"""charts.py - Matplotlib charts built from the results of analysis.py."""
import matplotlib.pyplot as plt

from analysis import best_sellers, category_sales, monthly_revenue


def bar_best_sellers(sales, products):
    data = best_sellers(sales, products)
    if not data:
        print("No sales data to chart.")
        return
    names = [name for name, _units in data]
    units = [u for _name, u in data]
    plt.figure(figsize=(8, 5))
    plt.bar(names, units, color="steelblue")
    plt.title("Best-Selling Products")
    plt.xlabel("Product")
    plt.ylabel("Units sold")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


def pie_categories(sales, products):
    data = category_sales(sales, products)
    if not data:
        print("No sales data to chart.")
        return
    plt.figure(figsize=(6, 6))
    plt.pie(list(data.values()), labels=list(data.keys()), autopct="%1.1f%%", startangle=90)
    plt.title("Revenue by Category")
    plt.tight_layout()
    plt.show()


def line_monthly(sales):
    data = monthly_revenue(sales)
    if not data:
        print("No sales data to chart.")
        return
    plt.figure(figsize=(8, 5))
    plt.plot(list(data.keys()), list(data.values()), marker="o", color="darkgreen")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (Rs.)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def show_all_charts(sales, products):
    bar_best_sellers(sales, products)
    pie_categories(sales, products)
    line_monthly(sales)


if __name__ == "__main__":
    # Standalone demo: uses real data if available, otherwise sample data.
    from models import create_product
    from storage import load_data, load_sales

    demo_products = load_data()
    demo_sales = load_sales()

    if not demo_sales:
        print("(sales.txt is empty - showing SAMPLE data)")
        demo_products = {
            "P101": create_product("P101", "Basmati Rice", 120, "Food", 50),
            "P102": create_product("P102", "USB Cable", 250, "Electronics", 20),
            "P103": create_product("P103", "Cotton T-Shirt", 499, "Clothing", 35),
        }
        demo_sales = [
            ("2026-08-05", "P101", 4, 456.00),
            ("2026-08-19", "P102", 2, 450.00),
            ("2026-09-02", "P103", 1, 424.15),
            ("2026-09-14", "P101", 6, 684.00),
            ("2026-10-01", "P102", 5, 1125.00),
            ("2026-10-12", "P103", 3, 1272.45),
        ]

    show_all_charts(demo_sales, demo_products)