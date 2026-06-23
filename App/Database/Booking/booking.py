import json
import os
from datetime import datetime, timedelta

class BookingSystem:
    TOTAL_TABLES = 5
    BOOKING_CHARGE = 450
    DISCOUNT_AMOUNT = 400

    @staticmethod
    def get_path():
        p = os.path.join(os.path.dirname(__file__),"bookings.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    @staticmethod
    def load_bookings():
        try:
            with open(BookingSystem.get_path(), 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    @staticmethod
    def display_table_layout(bookings, new_start, new_end):
        restaurant_tables = {"T1": 2, "T2": 2, "T3": 4, "T4": 4, "T5": 6}
        booked_tables = []
        for b in bookings:
            if b.get('status') == 'Active' and 'table_id' in b:
                b_start = datetime.strptime(b['start_datetime'], "%Y-%m-%d %H:%M:%S")
                b_end = datetime.strptime(b['end_datetime'], "%Y-%m-%d %H:%M:%S")
                if (new_start < b_end) and (new_end > b_start):
                    booked_tables.append(b['table_id'])
        
        print("\n=================================================")
        print("                RESTAURANT LAYOUT                ")
        print("=================================================\n")
        
        row_string = ""
        count = 0
        available_count = 0
        
        for table_id, capacity in restaurant_tables.items():
            if table_id in booked_tables:
                symbol = "X"
            else:
                symbol = "O"
                available_count += 1
                
            row_string += f"[ {table_id}({capacity}P): {symbol} ]    "
            count += 1
            if count % 3 == 0:
                print(row_string)
                row_string = ""
                
        if row_string:
            print(row_string)
            
        print("\n-------------------------------------------------")
        print(" Legend: [ O ] = Available | [ X ] = Booked ")
        print("-------------------------------------------------\n")
        
        return available_count, booked_tables
    @staticmethod
    def save_bookings(data):
        with open(BookingSystem.get_path(), 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def customer_dashboard(user):
        from App.Menu.menu import OrderSystem

        while True:
            print("" + "=" * 50)
            print("CUSTOMER DASHBOARD".center(50))
            print("=" * 50)
            print("1 -> View Menu & Order Food")
            print("2 -> Book a Table in Advance")
            print("3 -> Arrive at Booked Table (Claim Discount)")
            print("4 -> Logout")

            c_opt = input("Select action: ").strip()

            if c_opt == '1':
                OrderSystem.take_order(user, applied_discount=0)

            elif c_opt == '2':
                BookingSystem.book_table(user)

            elif c_opt == '3':
                discount = BookingSystem.arrive_and_get_discount(user)
                if discount > 0:
                    print("Taking you to the ordering screen...")
                    OrderSystem.take_order(user, applied_discount=discount)

            elif c_opt == '4':
                break

            else:
                print("Invalid choice.")

    @staticmethod
    def book_table(user):
        print("" + "=" * 50)
        print("TABLE BOOKING".center(50))
        print("=" * 50)

        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        time_str = input("Enter time (HH:MM in 24-hour format): ").strip()

        try:
            booking_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date/time format.")
            return

        now = datetime.now()
        min_time = now + timedelta(hours=4)

        if booking_dt < min_time:
            print("Error: You must book at least 4 hours in advance.")
            print(f"Earliest possible booking is: {min_time.strftime('%Y-%m-%d %H:%M')}")
            return

        end_dt = booking_dt + timedelta(hours=2)
        bookings = BookingSystem.load_bookings()

        available_count, booked_tables = BookingSystem.display_table_layout(bookings, booking_dt, end_dt)

        if available_count == 0:
            print("Sorry, all tables are fully booked for this time slot.")
            return

        while True:
            chosen_table = input("Which table would you like to book? (e.g., T1): ").strip().upper()
            
            if chosen_table not in ["T1", "T2", "T3", "T4", "T5"]:
                print("Invalid table. Please choose between T1 and T5.")
                continue
                
            if chosen_table in booked_tables:
                print(f"Sorry, {chosen_table} is already booked (marked with an X). Pick an available table.")
                continue
                
            break 

        print(f"Table available: {booking_dt.strftime('%d-%b %I:%M %p')} to {end_dt.strftime('%d-%b %I:%M %p')}.")
        print(f"Advance Booking Charge: Rs. {BookingSystem.BOOKING_CHARGE}")
        print(f"Arrive on time to get Rs. {BookingSystem.DISCOUNT_AMOUNT} discounted from your food bill!")

        pay = input("Type 'PAY'/ 'P' to confirm and pay advance: ").strip().upper()
        if pay == 'PAY' or pay == "P":
            booking = {
                "booking_id": os.urandom(3).hex().upper(),
                "table_id": chosen_table,
                "uid": user.get("uid", ""),
                "username": user.get("username", ""),
                "fullname": user.get("fullname", ""),
                "mobile": user.get("mobile", ""),
                "address": user.get("address", ""),
                "start_datetime": booking_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "end_datetime": end_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Active"
            }
            bookings.append(booking)
            BookingSystem.save_bookings(bookings)
            
            from App.Database.DayBook.daybook import DayBookSystem
            DayBookSystem.add_record({
                "date": now.strftime("%Y-%m-%d %H:%M"),
                "username": user.get("username", ""),
                "fullname": user.get("fullname", ""),
                "amount": BookingSystem.BOOKING_CHARGE,
                "type": "Booking",
                "status": "Paid"
            })

            print(f"Booking confirmed! Your Booking ID is: {booking['booking_id']}")
        else:
            print("Booking cancelled.")

    @staticmethod
    def arrive_and_get_discount(user):
        bookings = BookingSystem.load_bookings()
        now = datetime.now()
        discount = 0

        for b in bookings:
            if b.get('username') == user.get("username") and b.get('status') == 'Active':
                b_start = datetime.strptime(b['start_datetime'], "%Y-%m-%d %H:%M:%S")
                grace_period_end = b_start + timedelta(minutes=15)

                if now > grace_period_end:
                    print(f"You are late for your {b_start.strftime('%I:%M %p')} booking.")
                    print("It has been cancelled and your advance is forfeited.")
                    b['status'] = 'Cancelled (Late)'

                elif now >= (b_start - timedelta(minutes=30)) and now <= grace_period_end:
                    print("Welcome! Your table is ready.")
                    print(f"You get Rs. {BookingSystem.DISCOUNT_AMOUNT} off your food order!")
                    b['status'] = 'Completed'
                    discount = BookingSystem.DISCOUNT_AMOUNT

                else:
                    print(f"You are too early for your {b_start.strftime('%I:%M %p')} booking. Please wait.")
                    return 0

        BookingSystem.save_bookings(bookings)

        if discount == 0:
            print("No active/valid bookings found for this time.")

        return discount