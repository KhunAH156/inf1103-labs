import os
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.txt")

inventory = 0
failed_attempts = 0
print("-----------------------------------")
print("Welcome to the Inventory Auditor!")
print("-----------------------------------")

def load_inventory(filepath=INVENTORY_FILE):
    
    if not os.path.exists(filepath):
        print("No saved inventory found. Starting with an empty inventory.")
        return 0, []
 
    total = 0
    history = []
    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("total="):
                    total = int(line.split("=", 1)[1])
                elif line.startswith("history="):
                    values = line.split("=", 1)[1]
                    if values:
                        history = [int(v) for v in values.split(",")]
    except ValueError:
        print("Saved inventory file is corrupted. Starting with an empty inventory.")
        return 0, []
 
    print(f"Loaded saved inventory: {total} units, {len(history)} past transaction(s).")
    return total, history

def save_inventory(total, history, filepath=INVENTORY_FILE):
    """Write the final total and the full transaction history to disk."""
    with open(filepath, "w") as file:
        file.write(f"total={total}\n")
        file.write("history=" + ",".join(str(v) for v in history) + "\n")
    print(f"Inventory successfully saved to {os.path.basename(filepath)}")

def get_valid_input():
    while True:
        user_input = input("Enter inventory amount or 'quit' to exit: ")

        if user_input.lower() == "quit":
            return "quit"

        try:
            value = int(user_input)

            if value < 0:
                print("Input cannot be negative. Please enter a valid number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("-----------------------------------")
    print("Inventory Audit Report")
    print("-----------------------------------")
    print(f"Total Inventory: {total_units}")
    print(f"Failed/Rejected Entries: {failed_attempts}")

while True:
    result = get_valid_input()

    if result == "quit":
        generate_report(inventory, failed_attempts)
        break

    inventory = process_delivery(inventory, result)

    tax = calculate_tax(result)

    print(f"Delivery: {result}")
    print(f"Tax: {tax:.2f}")
    print(f"Current inventory: {inventory}")

    if inventory > 500:
        print(f"Inventory limit exceeded: {inventory}")
        generate_report(inventory, failed_attempts)
        break