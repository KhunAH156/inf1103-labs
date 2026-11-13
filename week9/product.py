"""Abstract Product class containing behaviour shared by every product type."""

from abc import ABC, abstractmethod
from math import isfinite

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if not isinstance(product_id, str) or not isinstance(name, str):
            raise ValueError("Product ID and name must be text.")
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if not isinstance(price, (int, float)) or not isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        if type(stock) is not int or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        if not isinstance(supplier, Supplier):
            raise TypeError("Each product requires a Supplier object.")

        self.__product_id: str = product_id.strip().upper()
        self.__name: str = name.strip()
        self.__price: float = round(float(price), 2)
        self.__stock: int = stock
        # Association: references a separately created Supplier; does not own it.
        self.__supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        """Replace current stock for every Product subtype (LSP contract)."""
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name} ({self.__supplier.supplier_id})")

    def display_supplier_information(self) -> None:
        """Collaborate with Supplier without treating it as a part of Product."""
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return the delivery method; every concrete product implements it."""

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict[str, object]:
        """Serialize common fields and the associated supplier's data."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }
