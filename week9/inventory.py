"""Inventory aggregates existing Product objects; it does not create them."""

from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """Return a snapshot for polymorphic iteration without exposing storage."""
        return self.__products.copy()

    def add_product(self, product: Product) -> bool:
        """Add an existing product unless its ID is already in this inventory."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id.strip().upper():
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        """Keep the Lab 7 method name for backwards compatibility."""
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        """Remove only this inventory's reference, never the product itself."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def display_all(self) -> None:
        print("Current Inventory")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()

    def display_all_products(self) -> None:
        """Lab 8's explicit polymorphic display operation."""
        self.display_all()

    def to_list(self) -> list[dict[str, object]]:
        return [product.to_dict() for product in self.__products]
