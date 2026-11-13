"""Original inventory menu, extended for suppliers, product types and orders."""

import json
import os

from inventory import Inventory
from order import Order
from product import DigitalProduct, PhysicalProduct, Product
from supplier import Supplier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


def load_inventory(filepath: str = INVENTORY_FILE) -> Inventory:
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
        suppliers: dict[str, Supplier] = {}
        products = [Product.from_dict(item, suppliers) for item in data]
        for product in products:
            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID in inventory file.")
    except (json.JSONDecodeError, OSError, ValueError, TypeError, KeyError):
        print(f"{filename} is unreadable or corrupted. Starting with an empty inventory.")
        return Inventory()

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filepath: str = INVENTORY_FILE) -> bool:
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
    print("7. Create Order")
    print("----------------------------")


def get_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_product_id(prompt: str) -> str:
    return get_text(prompt).upper()


def get_price(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if not (0 <= value < float("inf")):
                print("Price must be a finite, non-negative number.")
                continue
            return round(value, 2)
        except ValueError:
            print("Invalid input. Please enter a valid price.")


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


def get_supplier(inventory: Inventory) -> Supplier:
    supplier_id = get_product_id("Supplier ID: ")
    for product in inventory.products:
        if product.supplier.supplier_id == supplier_id:
            print(f"Reusing supplier: {product.supplier.name}")
            return product.supplier
    name = get_text("Supplier name: ")
    email = get_text("Supplier email: ")
    return Supplier(supplier_id, name, email)


def handle_add(inventory: Inventory) -> None:
    print("Add New Product")
    product_id = get_product_id("Product ID: ")
    if inventory.find_product(product_id) is not None:
        print(f"Product {product_id} already exists. Use Update Stock instead.")
        return
    name = get_text("Product Name: ")
    price = get_price("Price: ")
    stock = get_quantity("Stock Quantity: ")
    supplier = get_supplier(inventory)
    while True:
        kind = get_text("Type (P for physical / D for digital): ").upper()
        if kind in {"P", "D"}:
            break
        print("Please enter P or D.")
    if kind == "P":
        weight = get_price("Weight in kg (0 if unknown): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        link = get_text("Download link: ")
        product = DigitalProduct(product_id, name, price, stock, supplier, link)
    if inventory.add_product(product):
        print("Product added successfully!")


def handle_update(inventory: Inventory) -> None:
    print("Update Stock")
    product_id = get_product_id("Enter Product ID: ")
    product = inventory.find_product(product_id)
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
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        product.display_information()


def handle_order(inventory: Inventory) -> None:
    """Create an in-memory order; the lab does not require persisted orders."""
    order = Order(get_text("Order ID: "))
    while True:
        product_id = get_product_id("Product ID (or DONE to finish): ")
        if product_id == "DONE":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_quantity("Order quantity: ")
        if quantity == 0:
            print("Quantity must be greater than zero.")
            continue
        order.add_order_line(product, quantity)
        print("Order line added.")
    order.display_information()
    print("This lab's orders are demonstrations and do not change inventory stock.")


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
                    print(f"Inventory saved to {os.path.basename(INVENTORY_FILE)}.")
            elif choice == "6":
                handle_exit(inventory)
                break
            elif choice == "7":
                handle_order(inventory)
            else:
                print("Invalid option. Please enter a number from 1 to 7.")
    except (KeyboardInterrupt, EOFError):
        print()
        handle_exit(inventory)


if __name__ == "__main__":
    main()
