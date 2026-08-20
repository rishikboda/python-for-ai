class Inventory:
    def __init__(self):
        self.items = {}

    def add_stock(self, item, quantity):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
        print(f"Added {quantity} of {item}.")

    def sell_item(self, item, quantity):
        # Bug lives somewhere in here!
        if item in self.items:
            self.items[item] -= quantity
            print(f"Sold {quantity} of {item}.")
        else:
            print(f"Sorry, {item} is not in stock.")

    def display_inventory(self):
        print("\n--- Current Inventory ---")
        for item, quantity in self.items.items():
            print(f"{item}: {quantity}")

# Testing the code
shop = Inventory()
shop.add_stock("Laptops", 5)
shop.sell_item("Laptop", 7)  # Problem: Can you sell more than you have?
shop.display_inventory()