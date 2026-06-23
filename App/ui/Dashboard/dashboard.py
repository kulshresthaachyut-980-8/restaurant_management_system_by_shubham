from App.Authentication.signup import SignUpSystem
from App.Authentication.login import LoginSystem
from App.Menu.menu import StaffDashboard
from App.Database.Booking.booking import BookingSystem
from App.Database.DayBook.daybook import DayBookSystem

def main():
    while True:
        print("" + "=" * 50)
        print("SHUBH HUB RESTAURANT SYSTEM".center(50))
        print("=" * 50)
        print("1 -> Login")
        print("2 -> Sign Up")
        print("3 -> Exit")

        choice = input("Select an option : ").strip()

        if choice == '1':
            user = LoginSystem.login()
            if user:
                role = user.get("role", "").lower()

                if role == "admin":
                    StaffDashboard.manage_menu()
                elif role == "waitstaff":
                    BookingSystem.customer_dashboard(user)
                else:
                    print("Role not recognized. Please contact admin.")

        elif choice == '2':
            SignUpSystem.signup()

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()