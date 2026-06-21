import os
import json
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except Exception:
    class Dummy:
        RESET_ALL = ""
        LIGHTGREEN_EX = ""
        LIGHTYELLOW_EX = ""
        LIGHTRED_EX = ""
        LIGHTCYAN_EX = ""
        YELLOW = ""
        GREEN = ""
        RED = ""
        CYAN = ""
        MAGENTA = ""
        BLUE = ""
        WHITE = ""
    Fore = Dummy()
    Style = Dummy()

class FoodItem:
    def __init__(self, item_id, name, portions_prices):
        self.item_id = item_id
        self.name = name
        self.portions_prices = portions_prices

class StaffDashboard:
    @staticmethod
    def get_menu_path():
        current_dir = os.path.dirname(__file__)
        menu_path = os.path.join(current_dir, "..", "Database", "Menu", "menu_data.json")
        os.makedirs(os.path.dirname(menu_path), exist_ok=True)
        return menu_path

    @staticmethod
    def load_menu():
        try:
            with open(StaffDashboard.get_menu_path(), "r") as file:
                data = json.load(file)
                if data:
                    return data
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        default_menu = []
        categories = {"B": "Breakfast", "L": "Lunch", "D": "Dinner", "V": "Beverage"}

        for prefix, cat_name in categories.items():
            for i in range(1, 100):
                default_menu.append({
                    "item_id": f"{prefix}{i}",
                    "name": f"{cat_name} Item {i}",
                    "portions_prices": {"Full": 99}
                })

        StaffDashboard.save_menu(default_menu)
        return default_menu

    @staticmethod
    def save_menu(menu_data):
        with open(StaffDashboard.get_menu_path(), "w") as file:
            json.dump(menu_data, file, indent=4)

    @staticmethod
    def manage_menu():
        while True:
            print("" + "=" * 50)
            print("STAFF MENU MANAGER".center(50))
            print("=" * 50)
            print("1 -> Add New Menu Item")
            print("2 -> Update Item Price")
            print("3 -> Delete Menu Item")
            print("4 -> Logout (Back to Main Menu)")

            choice = input("Select an action : ").strip()
            if choice == '4':
                break

            menu_data = StaffDashboard.load_menu()

            if choice == '1':
                item_id = input("Enter New Item ID (e.g., B5) : ").strip().upper()
                name = input("Enter Item Name : ").strip()
                portion = input("Enter Portion Size : ").strip()
                try:
                    price = int(input(f"Enter Price for {portion} : "))
                    menu_data.append({
                        "item_id": item_id,
                        "name": name,
                        "portions_prices": {portion: price}
                    })
                    StaffDashboard.save_menu(menu_data)
                    print(f"Success! {name} added to the menu.")
                except ValueError:
                    print("Invalid price!")

            elif choice == '2':
                item_id = input("Enter Item ID to Update : ").strip().upper()
                found = False
                for item in menu_data:
                    if item["item_id"] == item_id:
                        found = True
                        portion = input(f"Updating {item['name']}. Enter Portion name : ").strip()
                        try:
                            item["portions_prices"][portion] = int(input("New Price : "))
                            StaffDashboard.save_menu(menu_data)
                            print("Price updated successfully!")
                        except ValueError:
                            print("Invalid price!")
                        break
                if not found:
                    print("Item ID not found.")

            elif choice == '3':
                item_id = input("Enter Item ID to Delete : ").strip().upper()
                original_len = len(menu_data)
                menu_data = [item for item in menu_data if item["item_id"] != item_id]
                if len(menu_data) < original_len:
                    StaffDashboard.save_menu(menu_data)
                    print("Item deleted successfully!")
                else:
                    print("Item ID not found.")

            else:
                print("Invalid choice.")

class FoodMenu:
    @staticmethod
    def get_dynamic_items():
        raw_data = StaffDashboard.load_menu()
        return [FoodItem(d["item_id"], d["name"], d["portions_prices"]) for d in raw_data]

    @staticmethod
    def display_category(prefix, title):
        items = FoodMenu.get_dynamic_items()
        category_items = [item for item in items if item.item_id.startswith(prefix)]

        color_map = {
            "BREAKFAST": Fore.LIGHTGREEN_EX,
            "LUNCH": Fore.LIGHTYELLOW_EX,
            "DINNER": Fore.LIGHTRED_EX,
            "BEVERAGES": Fore.LIGHTCYAN_EX
        }

        color = color_map.get(title.upper(), "")
        size = 85

        print("" + "=" * size)
        print(color + f" {title} MENU ".center(size, "="))
        print("=" * size)
        print(f"{'ID':<8}{'Item Name':<30}{'Portions & Prices'}")
        print("-" * size)

        if not category_items:
            print("No items found in this category.")
        else:
            print("Showing first 20 items (Scroll/Search ID for more)...")
            for item in category_items[:20]:
                portions = "  |  ".join([f"{k}: Rs.{v}" for k, v in item.portions_prices.items()])
                print(f"{item.item_id:<8}{item.name:<30}{portions}")

        print("=" * size)

class OrderSystem:
    @staticmethod
    def take_order(user, applied_discount=0):
        cart = []
        subtotal = 0

        while True:
            print("" + "=" * 50)
            print("ORDERING SYSTEM".center(50))
            print("=" * 50)
            print("1 -> Breakfast Menu (B1 - B20)")
            print("2 -> Lunch Menu (L1 - L20)")
            print("3 -> Dinner Menu (D1 - D20)")
            print("4 -> Beverage Menu (V1 - V20)")
            print("5 -> View Cart & Proceed to Pay")

            cat_choice = input("Select a category to view (or 5 to pay): ").strip()
            prefix_map = {'1': ('B', 'BREAKFAST'), '2': ('L', 'LUNCH'), '3': ('D', 'DINNER'), '4': ('V', 'BEVERAGES')}

            if cat_choice in prefix_map:
                prefix, title = prefix_map[cat_choice]
                FoodMenu.display_category(prefix, title)

                items_available = FoodMenu.get_dynamic_items()
                while True:
                    item_id = input(f"Enter Item ID to order from {title} (or 'BACK' to change category) : ").strip().upper()
                    if item_id == 'BACK':
                        break

                    selected_item = next((i for i in items_available if i.item_id == item_id), None)
                    if not selected_item:
                        print("Invalid Item ID! Try again.")
                        continue

                    portions = list(selected_item.portions_prices.keys())
                    for i, p in enumerate(portions, 1):
                        print(f"  {i}. {p} (Rs. {selected_item.portions_prices[p]})")

                    try:
                        p_choice = int(input("Select portion number : ")) - 1
                        sel_p = portions[p_choice]
                        qty = int(input("How many? : "))
                        cost = selected_item.portions_prices[sel_p] * qty
                        subtotal += cost
                        cart.append({"name": selected_item.name, "portion": sel_p, "cost": cost})
                        print(f"Added! Subtotal: Rs. {subtotal}")
                    except (ValueError, IndexError):
                        print("Invalid selection.")

            elif cat_choice == '5':
                if not cart:
                    print("Your cart is empty. Please order something first.")
                    continue
                break
            else:
                print("Invalid choice.")

        gst = subtotal * 0.05
        grand_total = subtotal + gst

        if applied_discount > 0:
            print(f"--> Applying Advance Booking Discount: -Rs. {applied_discount}")
            grand_total -= applied_discount

        if grand_total < 0:
            grand_total = 0

        OrderSystem.print_bill(user, cart, subtotal, gst, applied_discount, grand_total)

        if input("Proceed to Payment? (Y/N): ").strip().upper() == 'Y':
            OrderSystem.process_payment(user, grand_total)

    @staticmethod
    def print_bill(user, cart, subtotal, gst, discount, grand_total):
        print("" + "=" * 55)
        print("YOUR BILL".center(55))
        print("=" * 55)
        print(f"Name   : {user.get('fullname', 'N/A')}")
        print(f"User   : {user.get('username', 'N/A')}")
        print(f"Mobile : {user.get('mobile', 'N/A')}")
        print(f"Address: {user.get('address', 'N/A')}")
        print("-" * 55)

        for item in cart:
            print(f"{item['name']} ({item['portion']}) -> Rs. {item['cost']}")

        print("-" * 55)
        print(f"Subtotal : Rs. {subtotal:.2f}")
        print(f"GST (5%) : Rs. {gst:.2f}")
        if discount > 0:
            print(f"Discount : -Rs. {discount:.2f}")
        print(f"TOTAL DUE: Rs. {grand_total:.2f}")
        print("=" * 55)

    @staticmethod
    def process_payment(user, grand_total):
        method = {"1": "UPI", "2": "Cash", "3": "Card"}.get(
            input("Payment Methods: [1] UPI [2] Cash [3] Card : ").strip(),
            "Cash"
        )
        print(f"Paid Rs. {grand_total:.2f} via {method}. Thank you!")

        from App.Database.DayBook.daybook import DayBookSystem
        DayBookSystem.add_record({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "username": user.get("username", ""),
            "fullname": user.get("fullname", ""),
            "amount": grand_total,
            "type": "Payment",
            "status": method
        })