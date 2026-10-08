import json
import os

# Code lives in BASE_DIR. Data lives in DATA_DIR, which defaults to the same
# folder when run locally, but can be pointed at a mounted volume in Docker.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

LINE = "-" * 48


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
def load_inventory(filepath=INVENTORY_FILE):
    """Return the list of product dicts from the JSON file, or [] if none."""
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        print(f"{filename} not found. Starting with an empty inventory.")
        return []

    print(f"{filename} found.")
    try:
        with open(filepath, "r") as file:
            inventory = json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"{filename} is unreadable or corrupted. Starting with an empty inventory.")
        return []

    if not isinstance(inventory, list):
        print(f"{filename} has an unexpected format. Starting with an empty inventory.")
        return []

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filepath=INVENTORY_FILE):
    """Write the inventory list to the JSON file. Returns True on success."""
    try:
        with open(filepath, "w") as file:
            json.dump(inventory, file, indent=4)
        return True
    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False


# ---------------------------------------------------------------------------
# Data manipulation (pure functions: take the inventory, return a result)
# ---------------------------------------------------------------------------
def search_product(inventory, product_id):
    """Return the product dict with this ID, or None."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Return a new inventory list with the product appended."""
    new_product = {"id": product_id, "name": name, "price": price, "stock": stock}
    return inventory + [new_product]


def update_stock(inventory, product_id, new_stock):
    """Return a new inventory list with that product's stock replaced."""
    return [
        {**product, "stock": new_stock} if product["id"] == product_id else product
        for product in inventory
    ]


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def format_product(product):
    return (f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}")


def display_all(inventory):
    print("Current Inventory")
    print(LINE)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(format_product(product))
    print(LINE)


def display_product(product):
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)


def show_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_product_id(prompt):
    return get_text(prompt).upper()


def get_price(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Price cannot be negative.")
                continue
            return round(value, 2)
        except ValueError:
            print("Invalid input. Please enter a valid price.")


def get_quantity(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Quantity cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------
def handle_add(inventory):
    print("Add New Product")
    product_id = get_product_id("Product ID: ")
    if search_product(inventory, product_id):
        print(f"Product {product_id} already exists. Use Update Stock instead.")
        return inventory
    name = get_text("Product Name: ")
    price = get_price("Price: ")
    stock = get_quantity("Stock Quantity: ")
    print("Product added successfully!")
    return add_product(inventory, product_id, name, price, stock)


def handle_update(inventory):
    print("Update Stock")
    product_id = get_product_id("Enter Product ID: ")
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return inventory
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = get_quantity("New Stock Quantity: ")
    print("Stock updated successfully!")
    return update_stock(inventory, product_id, new_stock)


def handle_search(inventory):
    print("Search Product")
    product_id = get_product_id("Enter Product ID: ")
    product = search_product(inventory, product_id)
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        display_product(product)


def handle_exit(inventory):
    print("Saving inventory before exit...")
    if save_inventory(inventory):
        print("Inventory saved successfully.")
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    try:
        while True:
            show_menu()
            choice = input("Enter option: ").strip()

            if choice == "1":
                display_all(inventory)
            elif choice == "2":
                inventory = handle_add(inventory)
            elif choice == "3":
                inventory = handle_update(inventory)
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
        # Ctrl+C, or no interactive terminal (e.g. docker run without -it)
        print()
        handle_exit(inventory)


if __name__ == "__main__":
    main()