"""Digital products extend Product but do not implement shipping."""

from math import isfinite

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        if (not isinstance(download_size, (int, float)) or
                not isfinite(download_size) or download_size < 0):
            raise ValueError("Download size must be a finite, non-negative number.")
        self.__download_size = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        """Override and reuse Product's display before adding digital details."""
        super().display_information()
        print("Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print("-" * 48)

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"],
                   data["stock"], data["download_size"])
