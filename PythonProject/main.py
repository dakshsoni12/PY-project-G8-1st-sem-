"""main.py - Menu-driven console program. Run this file: python main.py"""
from models import CATEGORIES, InvalidQuantityError, InsufficientStockError, validate_quantity
from storage import load_data, save_data, append_sale
from product_manager import (add_product, update_product, delete_product,
                             restock_product, search_product, view_products)
from billing import add_to_cart, generate_bill, print_bill, finalize_sale


def ask(prompt):
    return input(prompt).strip()


def menu_add(products):
    pid = ask("Product ID: ")
    name = ask("Name: ")
    price = ask("Price: ")
    print("Categories:", ", ".join(sorted(CATEGORIES)))
    category = ask("Category: ")
    quantity = validate_quantity(ask("Opening stock: "))
    add_product(products, pid, name, price, category, quantity)
    save_data(products)
    print("Product added.")


def menu_search(products):
    results = search_product(products, ask("Search by ID or name: "))
    if not results:
        print("No match found.")
    for p in results:
        print(p)


def menu_update(products):
    pid = ask("Product ID to update: ")
    name = ask("New name (blank = keep): ")
    price = ask("New price (blank = keep): ")
    update_product(products, pid, name, price)
    save_data(products)
    print("Product updated.")


def menu_delete(products):
    pid = ask("Product ID to delete: ")
    delete_product(products, pid)
    save_data(products)
    print("Product deleted.")


def menu_restock(products):
    pid = ask("Product ID to restock: ")
    qty = ask("Quantity to add: ")
    p = restock_product(products, pid, qty)
    save_data(products)
    print(f"Stock of {p.name} is now {p.quantity}.")


def menu_sell(products):
    cart = []
    while True:
        term = ask("Product ID or name (blank to finish): ")
        if term == "":
            break
        matches = search_product(products, term)
        if not matches:
            print("No product found.")
            continue
        if len(matches) > 1:
            print("Several matches, type the exact ID:")
            for m in matches:
                print("  ", m)
            continue
        product = matches[0]
        qty = ask(f"Quantity of {product.name}: ")
        try:
            add_to_cart(products, cart, product.product_id, qty)
            print("Added to cart.")
        except (InvalidQuantityError, InsufficientStockError, ValueError) as e:
            print("Error:", e)

    if not cart:
        print("Cart is empty. Sale cancelled.")
        return

    bill = generate_bill(products, cart)
    print_bill(bill)
    records = finalize_sale(products, bill)
    for date, pid, qty, amount in records:
        append_sale(date, pid, qty, amount)
    save_data(products)
    print("Sale recorded.")


MENU = """
===== SHOP BILLING AND INVENTORY =====
1. Add product
2. View products / stock
3. Search product
4. Update product
5. Delete product
6. Restock
7. Sell (new bill)
0. Exit
"""

ACTIONS = {
    "1": menu_add, "2": view_products, "3": menu_search, "4": menu_update,
    "5": menu_delete, "6": menu_restock, "7": menu_sell,
}


def main():
    products = load_data()
    while True:
        print(MENU)
        choice = ask("Choose an option: ")
        if choice == "0":
            save_data(products)
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action(products)
        except (ValueError, InvalidQuantityError, InsufficientStockError) as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
