"""A line is an owned part of an Order, but merely references its Product."""

from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Order line requires a Product object.")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return round(self.product.price * self.quantity, 2)
