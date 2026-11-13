"""Order creates and manages the OrderLine objects that belong to it."""

from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")
        self.order_id: str = order_id.strip().upper()
        # Composition: lines are created here, belong to this order, and are
        # removed through the order. Products themselves are NOT owned.
        self.__order_lines: list[OrderLine] = []

    @property
    def order_lines(self) -> list[OrderLine]:
        """Expose a snapshot; callers cannot change this order's collection."""
        return self.__order_lines.copy()

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the first matching line through its owning Order."""
        for line in self.__order_lines:
            if line.product.product_id == product_id.strip().upper():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        return round(sum(line.calculate_subtotal()
                         for line in self.__order_lines), 2)

    def display_order(self) -> None:
        print(f"Order: {self.order_id}")
        if not self.__order_lines:
            print("No order lines.")
        for line in self.__order_lines:
            print(f"  {line.product.name}: {line.quantity} x "
                  f"${line.product.price:.2f} = ${line.calculate_subtotal():.2f}")
        print(f"Total: ${self.calculate_total():.2f}")
