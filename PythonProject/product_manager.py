"""product_manager.py - Add, update, delete, search, restock and list products."""
from models import create_product, validate_quantity

LOW_STOCK_LIMIT = 5


def add_product(products, product_id, name, price, category, quantity):
    product_id = str(product_id).strip()
    name = str(name).strip()
    if not product_id or not name:
        raise ValueError("Product ID and name cannot be empty.")
    if "," in product_id or "," in name:
        raise ValueError("Commas are not allowed in ID or name (they separate fields in the files).")
    if product_id in products:
        raise ValueError(f"Product ID '{product_id}' already exists.")
    product = create_product(product_id, name, price, category, quantity)
    products[product_id] = product
    return product


def get_product(products, product_id):
    if product_id not in products:
        raise ValueError(f"No product with ID '{product_id}'.")
    return products[product_id]


def update_product(products, product_id, new_name=None, new_price=None):
    """Change name and/or price. Blank / None means keep the old value."""
    product = get_product(products, product_id)
    if new_name:
        if "," in new_name:
            raise ValueError("Commas are not allowed in the name.")
        product.name = new_name
    if new_price:
        price = float(new_price)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        product.price = price
    return product


def delete_product(products, product_id):
    get_product(products, product_id)
    return products.pop(product_id)


def restock_product(products, product_id, quantity):
    product = get_product(products, product_id)
    product.quantity += validate_quantity(quantity)
    return product


def search_product(products, term):
    """Exact ID match first, otherwise name contains the search text."""
    term = term.strip()
    if term in products:
        return [products[term]]
    term = term.lower()
    return [p for p in products.values() if term in p.name.lower()]


def view_products(products):
    if not products:
        print("No products yet.")
        return
    print(f"\n{'ID':<8}{'Name':<24}{'Category':<13}{'Price':>9}{'Stock':>7}")
    print("-" * 61)
    for p in products.values():
        warning = "  <- LOW STOCK" if p.quantity <= LOW_STOCK_LIMIT else ""
        print(f"{p.product_id:<8}{p.name:<24}{p.category:<13}{p.price:>9.2f}{p.quantity:>7}{warning}")
