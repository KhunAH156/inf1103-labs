"""Physical products extend Product and implement the shipping interface."""

from math import isfinite
from typing import cast

from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """One Product superclass plus one interface-style ABC."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (not isinstance(weight, (int, float)) or
                not isfinite(weight) or weight < 0):
            raise ValueError("Weight must be a finite, non-negative number.")
        self.__weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("-" * 48)

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Example rate retained from Lab 7: $4 plus $2 per kilogram."""
        return round(4.0 + 2.0 * self.__weight, 2)

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object], supplier: Supplier) -> "PhysicalProduct":
        return cls(cast(str, data["id"]), cast(str, data["name"]),
                   cast(float, data["price"]), cast(int, data["stock"]),
                   cast(float, data["weight"]), supplier)
