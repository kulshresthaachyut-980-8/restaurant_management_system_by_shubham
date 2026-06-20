import os
import json
import pwinput

class LoginSystem:
    @staticmethod
    def get_user_path():
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "..", "Database", "User", "user_data.json")
        return path

    @staticmethod
    def load_users():
        try:
            with open(LoginSystem.get_user_path(), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def login():
        print("" + "=" * 50)
        print("LOGIN".center(50))
        print("=" * 50)

        username = input("Enter Username : ").strip()
        password = pwinput.pwinput(prompt="Enter Password : ",mask='*').strip()

        users = LoginSystem.load_users()

        for user in users:
            if user.get("username") == username and user.get("password") == password:
                print(f"Login successful. Welcome, {user.get('fullname', username)}!")
                return user

        print("Invalid username or password.")
        return 0