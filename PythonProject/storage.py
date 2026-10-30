"""storage.py - Reads and writes products.txt, inventory.txt and sales.txt."""
import os
from models import create_product

PRODUCTS_FILE = "products.txt"    # id,name,price,category
INVENTORY_FILE = "inventory.txt"  # id,quantity
SALES_FILE = "sales.txt"          # date,product_id,quantity,amount


def ensure_file(path):
    """Create the file if it does not exist yet."""
    if not os.path.exists(path):
        open(path, "w", encoding="utf-8").close()


def read_records(path, expected_fields):
    """Return a list of field lists. Malformed lines are skipped with a warning."""
    ensure_file(path)
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != expected_fields:
                    print(f"Warning: {path} line {line_no} skipped (expected {expected_fields} fields).")
                    continue
                records.append((line_no, parts))
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warning: could not read {path} ({e}). Starting with no data from it.")
    return records


def load_data():
    """Load products and their stock into a dictionary {product_id: Product}."""
    products = {}

    for line_no, (pid, name, price, category) in read_records(PRODUCTS_FILE, 4):
        try:
            products[pid] = create_product(pid, name, price, category, 0)
        except ValueError as e:
            print(f"Warning: {PRODUCTS_FILE} line {line_no} skipped ({e}).")

    for line_no, (pid, qty) in read_records(INVENTORY_FILE, 2):
        try:
            qty = int(qty)
            if qty < 0:
                raise ValueError("negative stock")
        except ValueError:
            print(f"Warning: {INVENTORY_FILE} line {line_no} skipped (bad quantity).")
            continue
        if pid in products:
            products[pid].quantity = qty
        else:
            print(f"Warning: {INVENTORY_FILE} line {line_no} skipped (unknown product {pid}).")

    return products


def save_data(products):
    """Rewrite products.txt and inventory.txt from the dictionary."""
    try:
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as pf:
            for p in products.values():
                pf.write(f"{p.product_id},{p.name},{p.price:.2f},{p.category}\n")
        with open(INVENTORY_FILE, "w", encoding="utf-8") as inv:
            for p in products.values():
                inv.write(f"{p.product_id},{p.quantity}\n")
    except OSError as e:
        print(f"Error: could not save data ({e}).")


def append_sale(date, product_id, quantity, amount):
    """Add one sale record to the end of sales.txt."""
    try:
        with open(SALES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{date},{product_id},{quantity},{amount:.2f}\n")
    except OSError as e:
        print(f"Error: could not save sale ({e}).")


def load_sales():
    """Return sales as a list of tuples (date, product_id, quantity, amount)."""
    sales = []
    for line_no, (date, pid, qty, amount) in read_records(SALES_FILE, 4):
        try:
            sales.append((date, pid, int(qty), float(amount)))
        except ValueError:
            print(f"Warning: {SALES_FILE} line {line_no} skipped (bad number).")
    return sales
