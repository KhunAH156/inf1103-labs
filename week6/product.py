"""Product class: represents and manages one product."""


class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if price < 0 or stock < 0:
            raise ValueError("Price and stock cannot be negative.")
        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price = round(float(price), 2)
        self.__stock = int(stock)

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
        """Replace the current stock quantity (as in the Week 5 program)."""
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print("-" * 48)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print("-" * 48)

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self) -> dict:
        """Convert this product to the original Week 5 JSON format."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(data["id"], data["name"], data["price"], data["stock"])
