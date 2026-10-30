"""models.py - Product classes, custom exceptions and quantity validation."""

CATEGORIES = {"Food", "Electronics", "Clothing"}


# ---------- Custom exceptions ----------
class InvalidQuantityError(Exception):
    """Raised when a quantity is zero, negative or not a number."""


class InsufficientStockError(Exception):
    """Raised when a customer wants more units than are in stock."""


def validate_quantity(value):
    """Convert value to a positive int, or raise InvalidQuantityError."""
    try:
        qty = int(value)
    except (ValueError, TypeError):
        raise InvalidQuantityError(f"'{value}' is not a valid whole number.")
    if qty <= 0:
        raise InvalidQuantityError("Quantity must be greater than zero.")
    return qty


# ---------- Product class hierarchy ----------
class Product:
    """Base class holding the details common to every product."""

    def __init__(self, product_id, name, price, category, quantity=0):
        self.product_id = str(product_id)
        self.name = name
        self.price = float(price)
        self.category = category
        self.quantity = int(quantity)

    def calculate_discount(self):
        """Return the discount AMOUNT for ONE unit. Subclasses override this."""
        raise NotImplementedError("Use FoodProduct, ElectronicProduct or ClothingProduct")

    def info_tuple(self):
        """Fixed product information as a tuple (ID, name, category)."""
        return (self.product_id, self.name, self.category)

    def __str__(self):
        return (f"{self.product_id} | {self.name} | {self.category} | "
                f"Rs.{self.price:.2f} | stock: {self.quantity}")


class FoodProduct(Product):
    DISCOUNT_RATE = 0.05  # 5%

    def calculate_discount(self):
        return self.price * self.DISCOUNT_RATE


class ElectronicProduct(Product):
    DISCOUNT_RATE = 0.10  # 10%

    def calculate_discount(self):
        return self.price * self.DISCOUNT_RATE


class ClothingProduct(Product):
    DISCOUNT_RATE = 0.15  # 15%

    def calculate_discount(self):
        return self.price * self.DISCOUNT_RATE


# Maps a category name to the class that handles it
CATEGORY_CLASSES = {
    "Food": FoodProduct,
    "Electronics": ElectronicProduct,
    "Clothing": ClothingProduct,
}


def create_product(product_id, name, price, category, quantity=0):
    """Build the correct Product subclass for a category (with validation)."""
    category = str(category).strip().title()
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Choose from: {', '.join(sorted(CATEGORIES))}")
    price = float(price)
    if price <= 0:
        raise ValueError("Price must be greater than zero.")
    quantity = int(quantity)
    if quantity < 0:
        raise ValueError("Stock cannot be negative.")
    return CATEGORY_CLASSES[category](product_id, name, price, category, quantity)


if __name__ == "__main__":
    # Quick self-test: shows polymorphism in action
    items = [
        create_product("T1", "Rice", 100, "Food"),
        create_product("T2", "Cable", 100, "Electronics"),
        create_product("T3", "Shirt", 100, "Clothing"),
    ]
    for item in items:
        print(item.name, "->", item.calculate_discount())
