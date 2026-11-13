"""Digital products extend Product but do not implement shipping."""

from math import isfinite
from typing import cast

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (not isinstance(download_size, (int, float)) or
                not isfinite(download_size) or download_size < 0):
            raise ValueError("Download size must be a finite, non-negative number.")
        self.__download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print("Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print("-" * 48)

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download."

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object], supplier: Supplier) -> "DigitalProduct":
        return cls(cast(str, data["id"]), cast(str, data["name"]),
                   cast(float, data["price"]), cast(int, data["stock"]),
                   cast(float, data["download_size"]), supplier)
