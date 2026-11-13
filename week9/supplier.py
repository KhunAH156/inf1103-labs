"""Supplier objects exist independently and can be associated with products."""


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str):
            raise ValueError("Contact email must be text.")
        email = contact_email.strip()
        if email.count("@") != 1 or " " in email or not email.split("@")[1]:
            raise ValueError("Enter a valid supplier contact email.")

        self.__supplier_id: str = supplier_id.strip().upper()
        self.__name: str = name.strip()
        self.__contact_email: str = email

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Supplier Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])
