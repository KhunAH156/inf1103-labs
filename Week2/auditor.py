inventory = 0
failed_attempts = 0
print("-----------------------------------")
print("Welcome to the Inventory Auditor!")
print("-----------------------------------")

while (True):
    user_input = input("Enter inventory amount or 'quit' to exit: ")
    if user_input.lower() == 'quit':
        print(f"Exiting... Total inventory: {inventory}, Failed attempts: {failed_attempts}")
        break
    try:
        
        if int(user_input) < 0:
            print("Input cannot be negative. Please enter a valid number.")
            failed_attempts += 1
            print(f"Current inventory: {inventory}")
        else:
            inventory += int(user_input)
            print(f"Current inventory: {inventory}")

        if inventory >= 500:
            print(f"Inventory limit reached: {inventory}. Cannot add more items.")
            inventory -= int(user_input)
            break

    except ValueError:
        print("Invalid input. Please enter a valid number for inventory amount.")
        failed_attempts += 1
        print(f"Current inventory: {inventory}")