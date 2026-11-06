"""Inventory manages a collection of products, not product-specific behaviour."""

from product import Product


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add a product unless its ID already exists."""
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
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            # Each concrete product knows how to display its own information.
            product.display_information()

    def to_list(self) -> list[dict]:
        """Return serializable data without exposing the private collection."""
        return [product.to_dict() for product in self.__products]
