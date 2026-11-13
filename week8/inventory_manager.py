"""Main program: menu, input validation, and JSON loading/saving."""

import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

# Maps the saved identifier to the class responsible for restoring its data.
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def load_inventory(filepath=INVENTORY_FILE) -> Inventory:
    inventory = Inventory()
    filename = os.path.basename(filepath)
    if not os.path.exists(filepath):
        print(f"{filename} not found. Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Expected a list of products.")

        # Validate every entry before returning a populated Inventory.
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Every product must be a JSON object.")
            product_type = item["type"]
            if product_type not in PRODUCT_TYPES:
                raise ValueError(f"Unknown product type: {product_type}")
            product = PRODUCT_TYPES[product_type].from_dict(item)
            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID in inventory file.")
    except (json.JSONDecodeError, OSError, ValueError, TypeError, KeyError):
        print(f"{filename} is unreadable or corrupted. Starting with an empty inventory.")
        return Inventory()

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filepath=INVENTORY_FILE) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False


def show_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def get_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_product_id(prompt: str) -> str:
    return get_text(prompt).upper()


def get_non_negative_number(prompt: str, label: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if not (0 <= value < float("inf")):
                print(f"{label} must be a finite, non-negative number.")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {label.lower()}.")


def get_price(prompt: str) -> float:
    return round(get_non_negative_number(prompt, "Price"), 2)


def get_quantity(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Quantity cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_product_type() -> str:
    while True:
        print("Select Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        choice = input("Enter option (1 or 2): ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Invalid option. Choose 1 or 2.")


def handle_add(inventory: Inventory) -> None:
    print("Add New Product")
    product_type = get_product_type()
    product_id = get_product_id("Product ID: ")
    if inventory.search_product(product_id) is not None:
        print(f"Product {product_id} already exists. Use Update Stock instead.")
        return

    name = get_text("Product Name: ")
    price = get_price("Price: ")
    stock = get_quantity("Stock Quantity: ")
    if product_type == "physical":
        weight = get_non_negative_number("Weight (kg): ", "Weight")
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = get_non_negative_number("Download Size (MB): ", "Download size")
        product = DigitalProduct(product_id, name, price, stock, download_size)

    if inventory.add_product(product):
        print("Product added successfully!")


def handle_update(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = get_product_id("Enter Product ID: ")
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    new_stock = get_quantity("New Stock Quantity: ")
    product.update_stock(new_stock)
    print("Stock updated successfully!")


def handle_search(inventory: Inventory) -> None:
    print("Search Product")
    product_id = get_product_id("Enter Product ID: ")
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        product.display_information()


def handle_exit(inventory: Inventory) -> None:
    print("Saving inventory before exit...")
    if save_inventory(inventory):
        print("Inventory saved successfully.")
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
    try:
        while True:
            show_menu()
            choice = input("Enter option: ").strip()
            if choice == "1":
                inventory.display_all()
            elif choice == "2":
                handle_add(inventory)
            elif choice == "3":
                handle_update(inventory)
            elif choice == "4":
                handle_search(inventory)
            elif choice == "5":
                print("Saving inventory...")
                if save_inventory(inventory):
                    print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
            elif choice == "6":
                handle_exit(inventory)
                break
            else:
                print("Invalid option. Please enter a number from 1 to 6.")
    except (KeyboardInterrupt, EOFError):
        print()
        handle_exit(inventory)


if __name__ == "__main__":
    main()
