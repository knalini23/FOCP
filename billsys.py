import os
from datetime import datetime

class CafeteriaBillingSystem:
    def __init__(self):
        self.menu = self.load_menu_from_file("menu.txt")
        self.order = {}

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def load_menu_from_file(self, filename):
        """Load menu items from a file."""
        menu = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    item, price = line.strip().split(", ")
                    menu[len(menu) + 1] = (item, float(price))
        except FileNotFoundError:
            print(f"Menu file '{filename}' not found.")
        return menu

    def display_menu(self):
        """Display the menu."""
        print("\n--- Cafeteria Menu ---")
        for number, (item, price) in self.menu.items():
            print(f"{number}. {item:10} - ${price:.2f}")
        print("7. Finish Order")
        print("----------------------")

    def take_order(self):
    
        while True:
            try:
                choice = int(input("\nEnter the item number (or 7 to finish ordering): "))
                if choice == 7:
                    if not self.order:
                        print("You must add at least one item to continue with billing.")
                        input("Press Enter to go back to the menu...")
                        self.clear_screen()
                        continue
                    break
                if choice in self.menu:
                    item, price = self.menu[choice]
                    quantity = int(input(f"Enter quantity for {item}: "))
                    item_name = item.strip()  # Ensure item name is stored as a string
                    if item_name in self.order:
                        self.order[item_name] += quantity
                    else:
                        self.order[item_name] = quantity
                else:
                    print("Invalid choice. Please select a valid item number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def modify_order(self):
        """Modify the customer's order."""
        while True:
            self.clear_screen()
            print("\n--- Modify Order ---")
            print("1. Add more items")
            print("2. Delete an item")
            print("3. Update item quantity")
            print("4. View current order")
            print("5. Finalize order")
            choice = input("Select an option: ")
    
            if choice == "1":
                self.clear_screen()
                self.display_menu()
                self.take_order()
            elif choice == "2":
                item_to_delete = input("Enter the item name to delete: ").strip().title()
                if item_to_delete in self.order:
                    del self.order[item_to_delete]
                    print(f"{item_to_delete} removed from the order.")
                else:
                    print(f"{item_to_delete} not found in the order.")
            elif choice == "3":
                item_to_update = input("Enter the item name to update: ").strip().title()
                if item_to_update in self.order:
                    new_quantity = int(input(f"Enter new quantity for {item_to_update}: "))
                    self.order[item_to_update] = new_quantity
                    print(f"{item_to_update} quantity updated to {new_quantity}.")
                else:
                    print(f"{item_to_update} not found in the order.")
            elif choice == "4":
                self.print_order_summary()
                input("\nPress Enter to continue...")
            elif choice == "5":
                print("Order finalized.")
                break
            else:
                print("Invalid choice. Please try again.")


    def calculate_total(self):
        """Calculate the total cost of the order."""
        total = 0
        for item, quantity in self.order.items():
            # Match item name from menu with case-insensitivity
            match = next((price for name, price in self.menu.values() if name.strip().lower() == item.strip().lower()), None)
            if match is not None:
                total += match * quantity
            else:
                print(f"Warning: {item} not found in the menu. Skipping.")
        return total


    def process_payment(self, total):
        """Handle the payment process."""
        while True:
            try:
                payment = float(input(f"\nEnter payment amount (${total:.2f} required): "))
                if payment >= total:
                    change = payment - total
                    return payment, change
                else:
                    print(f"Insufficient amount. You still owe ${total - payment:.2f}.")
            except ValueError:
                print("Invalid input. Please enter a valid amount.")

    def print_order_summary(self):
        """Print the current order summary."""
        print("\n--- Current Order ---")
        print(f"{'Item':10}{'Qty':>5}{'Price':>10}{'Total':>10}")
        print("-" * 35)
        for item, quantity in self.order.items():
            price = next(price for name, price in self.menu.values() if name == item)
            cost = price * quantity
            print(f"{item:10}{quantity:>5}{price:>10.2f}{cost:>10.2f}")
        print("-" * 35)

    def print_invoice(self, total, payment, change):
        """Print the final invoice."""
        self.clear_screen()  # Ensure the terminal is cleared before showing the invoice
        print("\n\t--- Final Invoice ---")
        print(f"{'Item':10}{'Qty':>5}{'Price':>10}{'Total':>10}")
        print("-" * 35)
        for item, quantity in self.order.items():
            price = next(price for name, price in self.menu.values() if name == item)
            cost = price * quantity
            print(f"{item:10}{quantity:>5}{price:>10.2f}{cost:>10.2f}")
        print("-" * 35)
        print(f"{'Total':>25}: ${total:.2f}")
        print(f"{'Payment':>25}: ${payment:.2f}")
        print(f"{'Change':>25}: ${change:.2f}")
        print("-" * 35)
        print("Thank you for dining with us!\n")

        self.record_invoice(total, payment, change)

    def record_invoice(self, total, payment, change):
        """Record the invoice details in a file."""
        with open("invoices.txt", "a") as file:
            invoice_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n--- Invoice at {invoice_time} ---\n")
            for item, quantity in self.order.items():
                price = next(price for name, price in self.menu.values() if name == item)
                cost = price * quantity
                file.write(f"{item:10} | {quantity:>5} | ${price:>10.2f} | ${cost:>10.2f}\n")
            file.write(f"{'Total':>25}: ${total:.2f}\n")
            file.write(f"{'Payment':>25}: ${payment:.2f}\n")
            file.write(f"{'Change':>25}: ${change:.2f}\n")
            file.write("-" * 35 + "\n")

    def run(self):
        """Run the main billing system."""
        self.clear_screen()  # Clear the screen at the very start
        print("Welcome to the Cafeteria Billing System!")
        while True:
            self.display_menu()
            self.take_order()
            while True:
                self.modify_order()
                total = self.calculate_total()
                print(f"Current total: ${total:.2f}")
                proceed = input("Do you want to finalize the order and proceed to payment? (yes'y'/no'n'): ").lower()
                if proceed == "y":
                    payment, change = self.process_payment(total)
                    self.print_invoice(total, payment, change)
                    return
                elif proceed == "n":
                    print("You can continue modifying the order.")
                    break
                else:
                    print("Invalid choice. Please enter 'yes/y' or 'no/n'.")

if __name__ == "__main__":
    system = CafeteriaBillingSystem()
    system.run()
