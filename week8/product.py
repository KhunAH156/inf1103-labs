"""Abstract Product class containing behaviour shared by every product type."""

from abc import ABC, abstractmethod
from math import isfinite


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if not isinstance(product_id, str) or not isinstance(name, str):
            raise ValueError("Product ID and name must be text.")
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if not isinstance(price, (int, float)) or not isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        if type(stock) is not int or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")

        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price = round(float(price), 2)
        self.__stock = stock

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

    def update_stock(self, quantity: int) -> None:
        """Replace the current stock quantity, as in Lab 6."""
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        """Display fields common to all product types."""
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return the delivery method; every concrete product must implement it."""

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        """Serialize attributes common to all product types."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
