import sys

print("=== Inventory System Analysis ===")

inventory = {}

# Parse arguments
for arg in sys.argv[1:]:
    if ":" not in arg:
        print(f"Error - invalid parameter '{arg}'")
        continue

    parts = arg.split(":")

    if len(parts) != 2:
        print(f"Error - invalid parameter '{arg}'")
        continue

    item = parts[0]
    quantity = parts[1]

    if item in inventory:
        print(f"Redundant item '{item}' - discarding")
        continue

    try:
        inventory[item] = int(quantity)
    except ValueError as error:
        print(f"Quantity error for '{item}': {error}")

# Display inventory
print("Got inventory:", inventory)

# List of items
items = list(inventory.keys())
print("Item list:", items)

# Total quantity
total = sum(inventory.values())
print(f"Total quantity of the {len(items)} items:", total)

# Percentages
for item in inventory:
    percentage = round(inventory[item] * 100 / total, 1)
    print(f"Item {item} represents {percentage}%")

# Most abundant
most_item = None
most_quantity = None

for item in inventory:
    if most_item is None or inventory[item] > most_quantity:
        most_item = item
        most_quantity = inventory[item]

print(f"Item most abundant: {most_item} with quantity {most_quantity}")

# Least abundant
least_item = None
least_quantity = None

for item in inventory:
    if least_item is None or inventory[item] < least_quantity:
        least_item = item
        least_quantity = inventory[item]

print(f"Item least abundant: {least_item} with quantity {least_quantity}")

# Add new item 
inventory.update({"magic_item": 1})
print("Updated inventory:", inventory)