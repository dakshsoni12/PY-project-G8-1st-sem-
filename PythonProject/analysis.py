#!/usr/bin/env python3
"""analysis.py - Sales analysis: revenue, best sellers, category and monthly totals.

All functions take plain data, so they are easy to test:
    sales    = list of tuples (date, product_id, quantity, amount)  -> storage.load_sales()
    products = dictionary {product_id: Product}                     -> storage.load_data()
"""


def total_revenue(sales):
    """Sum of all sale amounts."""
    return sum(amount for _date, _pid, _qty, amount in sales)


def best_sellers(sales, products=None, top_n=5):
    """Top products by units sold. Returns [(product_id_or_name, units), ...]."""
    units = {}
    for _date, pid, qty, _amount in sales:
        units[pid] = units.get(pid, 0) + qty
    ranked = sorted(units.items(), key=lambda item: item[1], reverse=True)[:top_n]
    if products:  # show names instead of IDs when we can
        ranked = [(products[pid].name if pid in products else pid, q) for pid, q in ranked]
    return ranked


def category_sales(sales, products):
    """Revenue per category. Returns {category: revenue}."""
    totals = {}
    for _date, pid, _qty, amount in sales:
        category = products[pid].category if pid in products else "Unknown"
        totals[category] = totals.get(category, 0.0) + amount
    return totals


def monthly_revenue(sales):
    """Revenue per month (YYYY-MM), sorted by month. Returns {month: revenue}."""
    totals = {}
    for date, _pid, _qty, amount in sales:
        month = date[:7]
        totals[month] = totals.get(month, 0.0) + amount
    return dict(sorted(totals.items()))


def print_report(sales, products):
    """Print every analysis result in a readable form."""
    if not sales:
        print("No sales recorded yet.")
        return
    print("\n===== SALES REPORT =====")
    print(f"Total revenue: Rs.{total_revenue(sales):.2f}")

    print("\nBest-selling products (units):")
    for name, units in best_sellers(sales, products):
        print(f"  {name:<22}{units:>5}")

    print("\nRevenue by category:")
    for category, amount in category_sales(sales, products).items():
        print(f"  {category:<22}{amount:>10.2f}")

    print("\nRevenue by month:")
    for month, amount in monthly_revenue(sales).items():
        print(f"  {month:<22}{amount:>10.2f}")


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

    print_report(demo_sales, demo_products)