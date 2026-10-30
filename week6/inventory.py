"""Inventory class: manages a collection of Product objects."""

from product import Product


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add a Product unless its ID already exists."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id.strip().upper():
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            print(product)
        print("-" * 48)

    def to_list(self) -> list[dict]:
        """Return serializable data without exposing the private collection."""
        return [product.to_dict() for product in self.__products]
