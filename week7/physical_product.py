"""Physical products extend Product and implement the shipping interface."""

from math import isfinite

from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    """One Product superclass plus one interface-style ABC."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        if (not isinstance(weight, (int, float)) or
                not isfinite(weight) or weight < 0):
            raise ValueError("Weight must be a finite, non-negative number.")
        self.__weight = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        """Override and reuse Product's display before adding physical details."""
        super().display_information()
        print("Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")
        print("-" * 48)

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Example rate: $4 base charge plus $2 per kilogram."""
        return round(4.0 + 2.0 * self.__weight, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": "physical", "weight": self.__weight})
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["weight"])
