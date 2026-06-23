import os
import json
import datetime

menu_logs_path=os.path.join(os.path.dirname(__file__),"..","Logs","menu_logs_.txt")
report_data_path = os.path.join(os.path.dirname(__file__), "..", "Database", "DayBook", "daybook.json")              

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
            with open(StaffDashboard.get_menu_path(), 'r') as file:
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
        with open(StaffDashboard.get_menu_path(), 'w') as file:
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
            print("4 -> Check Day Record")
            print("5 -> See Table Booking Record")
            print("6 -> Logout (Back to Main Menu)")

            choice = input("Select an action : ").strip()

            if choice == '6':
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
                        except ValueError as e:
                            print("Invalid price!")
                            with open (menu_logs_path,'a')as f:
                                f.write(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] Error  ->  {e}")
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
            
            elif choice == '4':
                try:
                    
                    with open(report_data_path, 'r') as f:
                        daybook_data = json.load(f)
                    
                    print("\n" + "=" * 50)
                    print("DAYBOOK REPORT".center(50))
                    print("=" * 50)
                    print("[1] View All Records")
                    print("[2] Search by Specific Date (YYYY-MM-DD)")
                    report_choice = input("Select option: ").strip()
                    
                    target_date = ""
                    if report_choice == '2':
                        target_date = input("Enter date (e.g., 2026-06-21) : ").strip()

                    print("-" * 65)
                    print(f"{'DATE & TIME':<18} | {'USERNAME':<15} | {'METHOD':<8} | {'AMOUNT'}")
                    print("-" * 65)
                    
                    total_revenue = 0
                    records_found = 0
                    
                    for record in daybook_data:
                        if report_choice == '1' or record.get('date', '').startswith(target_date):
                            date_str = record.get('date', 'N/A')
                            user_str = record.get('username', 'Unknown')
                            method_str = record.get('method', 'N/A')
                            amount = float(record.get('amount', 0))
            
                            print(f"{date_str:<18} | {user_str:<15} | {method_str:<8} | Rs. {amount:.2f}")
                            
                            total_revenue += amount
                            records_found += 1
                    
                    print("-" * 65)
                    if records_found == 0:
                        print("No records found for that selection.")
                    else:
                        print(f"Total Transactions : {records_found}")
                        print(f"Total Revenue      : Rs. {total_revenue:.2f}")
                    print("-" * 65)
                    
                except (FileNotFoundError, json.JSONDecodeError) as f:
                    print("No daybook records found yet! (File is empty or missing)")
                    with open (menu_logs_path,'w') as log_data:
                        log_data.write(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] Error -> {f}")
            
            elif choice=='5':

                table_json_data_path=os.path.join(os.path.dirname(__file__),"..","Database","Booking","bookings.json")
                try:
                    with open(table_json_data_path,'r') as f:
                        booking_data=json.load(f)
                    print("/n" + "=" * 50)
                    print("TABLE BOOKING REPORT".center(50))
                    print("=" * 50)
                    print("[1] View All Bookings")
                    print("[2] Search by specific Date (YYYY-MM-DD)")
                    table_report_choice=input("Select Option : ").strip()
                    date=""
                    if table_report_choice=='2':
                        date=input("Enter date (e.g. 2026-06-20) : ").strip()
                    print("-" * 75)
                    print(f"{'BOOKING ID':<12} | {'USERNAME':<15} | {'START TIME':<20} | {'STATUS'}")
                    print("-" * 75)
                    data_found=0
                    for booking in booking_data:
                        if table_report_choice=='1' or booking.get("booking_start_datetime","").startswith(date):
                            booking_id=booking.get("booking_id","N/A")
                            user=booking.get("username","Unknown")
                            start_time=booking.get("booking_start_datetime","N/A")
                            status=booking.get("status","N/A")
                            print(f" {booking_id:<12} | {user:<15} | {start_time:<20} | {status}")
                            data_found+=1
                    print("-" * 75)
                    if data_found==0:
                        print("No Booking Found ! ")
                    else:
                        print(f"Total Bookings Found : {data_found}")
                    print("-" * 75)
                except (FileNotFoundError,json.JSONDecodeError):
                    print("No Bookings Found ! (Database is empty or missing)")


class FoodMenu:
    @staticmethod
    def get_dynamic_items():
        raw_data = StaffDashboard.load_menu()
        return [FoodItem(d["item_id"], d["name"], d["portions_prices"]) for d in raw_data]

    @staticmethod
    def display_category(prefix, title):
        items = FoodMenu.get_dynamic_items()
        category_items = [item for item in items if item.item_id.startswith(prefix)]
        size = 85

        print("" + "=" * size)
        print(f" {title} MENU ".center(size, "="))
        print("=" * size)
        print(f"{'ID':<7}{'Item Name':<30}{'Portions & Prices'}")
        print("-" * size)

        if not category_items:
            print("No items found in this category.")
        else:
            print("Showing first 20 items (Scroll/Search ID for more)...")
            for item in category_items[:20]:
                portions = " / ".join([f"{k} : Rs.{v:<3}" for k, v in item.portions_prices.items()])
                print(f"{item.item_id:<7}{item.name:<30}{portions}")

        print("=" * size)

class OrderSystem:
    @staticmethod
    def find_item(user_text, items):
        user_text = user_text.strip().lower()

        for item in items:
            if item.item_id.lower() == user_text:
                return item
            if item.name.lower() == user_text:
                return item

        for item in items:
            if user_text in item.name.lower():
                return item

        return None

    @staticmethod
    def take_order(customer_username, applied_discount=0):
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
            prefix_map = {
                '1': ('B', 'BREAKFAST'),
                '2': ('L', 'LUNCH'),
                '3': ('D', 'DINNER'),
                '4': ('V', 'BEVERAGES')
            }

            if cat_choice in prefix_map:
                prefix, title = prefix_map[cat_choice]
                FoodMenu.display_category(prefix, title)
            elif cat_choice == '5':
                if not cart:
                    print("Your cart is empty. Please order something first.")
                    continue
                break
            else:
                print("Invalid choice.")
                continue

            items_available = FoodMenu.get_dynamic_items()

            while True:
                item_text = input(f"Enter Item ID or Item Name from {title} (or 'BACK' / 'X' to change category) : ").strip()

                if item_text.upper() == 'BACK':
                    break
                elif  item_text.upper()=='X':
                    break
                selected_item = OrderSystem.find_item(item_text, items_available)

                if not selected_item:
                    print("Invalid Item ID or Item Name! Try again.")
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
                except (ValueError, IndexError) as e:
                    print("Invalid selection.")
                    with open (menu_logs_path,'a') as f:
                        f.write(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] Error -> {e}")


        if not cart:
            return

        gst = subtotal * 0.05
        grand_total = subtotal + gst

        if applied_discount > 0:
            print(f"--> Applying Advance Booking Discount: -Rs. {applied_discount}")
            grand_total -= applied_discount

        if grand_total < 0:
            grand_total = 0

        OrderSystem.print_bill(customer_username,cart, subtotal, gst, applied_discount, grand_total)

        if input("Proceed to Payment? (Y/N): ").strip().upper() == 'Y':
            OrderSystem.process_payment(customer_username, grand_total)
    
    @staticmethod
    def print_bill(user_info,cart, subtotal, gst, discount, grand_total):
        print("" + "=" * 50)
        print("YOUR BILL".center(50))
        print("=" * 50)
        print(f"Name      : {user_info.get('fullname','N/A')}")
        print(f"Username  : {user_info.get('username','N/A')}")
        print(f"Phone     : {user_info.get('mobile','N/A')}")
        print(f"Address   : {user_info.get('address','N/A')}  ")
        print("=" * 50)

        for item in cart:
            print(f"{item['name']} ({item['portion']}) -> Rs. {item['cost']}")

        print("-" * 50)
        print(f"Subtotal : Rs. {subtotal:.2f}")
        print(f"GST (5%) : Rs. {gst:.2f}")
        if discount > 0:
            print(f"Discount : -Rs. {discount:.2f}")
        print(f"TOTAL DUE: Rs. {grand_total:.2f}")
        print("=" * 50)

    @staticmethod
    def process_payment(username, grand_total):
        method = {"1": "UPI", "2": "Cash", "3": "Card"}.get(
            input("Payment Methods: [1] UPI [2] Cash [3] Card : ").strip(),
            "Cash"
        )
        print(f"Paid Rs. {grand_total:.2f} via {method}. Thank you!")

        path = os.path.join(os.path.dirname(__file__), "..", "Database", "DayBook", "daybook.json")

        if isinstance(username, dict):
            actual_user = username.get("username", "Unknown")
        else:
            actual_user = username

        new_record = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            "username": actual_user,
            "amount": grand_total,
            "method": method
        }

        try:
            with open(path, 'r') as f:
                daybook_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            daybook_data = [] 

        daybook_data.append(new_record)

        with open(path, 'w') as f:
            json.dump(daybook_data, f, indent=4)