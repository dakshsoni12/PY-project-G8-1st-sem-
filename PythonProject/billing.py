"""billing.py - Cart, bill generation and stock update after a sale."""
from datetime import datetime
from models import InsufficientStockError, validate_quantity


def add_to_cart(products, cart, product_id, quantity):
    """Validate and add (product_id, quantity) to the cart list."""
    qty = validate_quantity(quantity)
    if product_id not in products:
        raise ValueError(f"No product with ID '{product_id}'.")
    product = products[product_id]
    already_in_cart = sum(q for pid, q in cart if pid == product_id)
    remaining = product.quantity - already_in_cart
    if qty > remaining:
        raise InsufficientStockError(
            f"Only {remaining} unit(s) of '{product.name}' available.")
    cart.append((product_id, qty))


def generate_bill(products, cart):
    """Build the bill as a dictionary. Does NOT change stock."""
    items = []
    subtotal = 0.0
    total_discount = 0.0
    for product_id, qty in cart:
        p = products[product_id]
        discount = p.calculate_discount() * qty   # polymorphic call
        line_total = p.price * qty - discount
        subtotal += p.price * qty
        total_discount += discount
        items.append({
            "product_id": product_id,
            "name": p.name,
            "unit_price": p.price,
            "quantity": qty,
            "discount": discount,
            "line_total": line_total,
        })
    return {
        "items": items,
        "subtotal": subtotal,
        "total_discount": total_discount,
        "grand_total": subtotal - total_discount,
    }


def print_bill(bill):
    print("\n" + "=" * 66)
    print(f"{'CUSTOMER BILL':^66}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M'):^66}")
    print("=" * 66)
    print(f"{'Item':<20}{'Qty':>5}{'Price':>10}{'Discount':>11}{'Amount':>12}")
    print("-" * 66)
    for it in bill["items"]:
        print(f"{it['name']:<20}{it['quantity']:>5}{it['unit_price']:>10.2f}"
              f"{it['discount']:>11.2f}{it['line_total']:>12.2f}")
    print("-" * 66)
    print(f"{'Subtotal:':<46}{bill['subtotal']:>20.2f}")
    print(f"{'Total discount:':<46}{bill['total_discount']:>20.2f}")
    print(f"{'GRAND TOTAL:':<46}{bill['grand_total']:>20.2f}")
    print("=" * 66)


def finalize_sale(products, bill):
    """Reduce stock and return sale records (date, product_id, qty, amount).

    Checks everything first, so stock is never left half-updated or negative.
    """
    needed = {}
    for it in bill["items"]:
        needed[it["product_id"]] = needed.get(it["product_id"], 0) + it["quantity"]
    for pid, qty in needed.items():
        if products[pid].quantity < qty:
            raise InsufficientStockError(f"Not enough stock for '{products[pid].name}'.")

    date = datetime.now().strftime("%Y-%m-%d")
    records = []
    for it in bill["items"]:
        products[it["product_id"]].quantity -= it["quantity"]
        records.append((date, it["product_id"], it["quantity"], it["line_total"]))
    return records
