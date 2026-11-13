"""Abstract Product and its physical/digital specialisations.

Each product refers to an independently created Supplier. Both subclasses
honour the same stock contract: stock means available units or licences.
"""

from abc import ABC, abstractmethod
from math import isfinite

from supplier import Supplier


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ) -> None:
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if not isfinite(float(price)) or price < 0:
            raise ValueError("Price must be finite and non-negative.")
        if type(stock) is not int or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        if not isinstance(supplier, Supplier):
            raise TypeError("supplier must be a Supplier object.")

        self.__product_id: str = product_id.strip().upper()
        self.__name: str = name.strip()
        self.__price: float = round(float(price), 2)
        self.__stock: int = stock
        self.supplier: Supplier = supplier

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
        """Replace available unit/licence count; same contract for all Products."""
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print("-" * 48)
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Available stock: {self.stock}")
        self.supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return the product-specific method of fulfilment."""

    def __str__(self) -> str:
        return (
            f"[{type(self).__name__}] ID: {self.product_id} | Name: {self.name} | "
            f"Price: ${self.price:.2f} | Stock: {self.stock} | "
            f"Supplier: {self.supplier.name}"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict(),
        }

    @staticmethod
    def from_dict(
        data: dict[str, object],
        supplier_registry: dict[str, Supplier] | None = None,
    ) -> "Product":
        """Read modern records and older Week 8 records without type/supplier.

        Reuse one Supplier instance per supplier ID when a registry is supplied.
        Old records are treated as physical products of unspecified weight.
        """
        supplier_data = data.get("supplier")
        if supplier_data is None:
            supplier = Supplier(
                "UNKNOWN", "Unspecified Supplier", "not-provided@example.invalid"
            )
        elif isinstance(supplier_data, dict):
            supplier = Supplier.from_dict(supplier_data)
        else:
            raise ValueError("Invalid supplier record.")

        if supplier_registry is not None:
            previous = supplier_registry.get(supplier.supplier_id)
            if previous is not None:
                if previous.to_dict() != supplier.to_dict():
                    raise ValueError("Conflicting details for the same supplier ID.")
                supplier = previous
            else:
                supplier_registry[supplier.supplier_id] = supplier

        common = (
            str(data["id"]),
            str(data["name"]),
            float(data["price"]),
            data["stock"],
            supplier,
        )
        product_type = data.get("type", "physical")
        if product_type == "physical":
            return PhysicalProduct(*common, weight_kg=float(data.get("weight_kg", 0.0)))
        if product_type == "digital":
            return DigitalProduct(*common, download_link=str(data["download_link"]))
        raise ValueError(f"Unsupported product type: {product_type}")


class PhysicalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight_kg: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not isfinite(weight_kg) or weight_kg < 0:
            raise ValueError("Weight must be finite and non-negative.")
        self.weight_kg: float = weight_kg

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping required (weight: {self.weight_kg:g} kg)."

    def display_information(self) -> None:
        super().display_information()
        print(self.get_fulfilment_info())
        print("-" * 48)

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "physical", "weight_kg": self.weight_kg})
        return data


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_link: str,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not download_link.strip():
            raise ValueError("Digital products need a download link.")
        self.download_link: str = download_link.strip()

    def get_fulfilment_info(self) -> str:
        return f"Digital delivery via download link: {self.download_link}"

    def display_information(self) -> None:
        super().display_information()
        print(self.get_fulfilment_info())
        print("-" * 48)

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "digital", "download_link": self.download_link})
        return data
