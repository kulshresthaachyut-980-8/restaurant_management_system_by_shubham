import os
import json
import uuid
from getpass import getpass
import pwinput

class SignUpSystem:
    @staticmethod
    def get_user_path():
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "..", "Database", "User", "user_data.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    @staticmethod
    def load_users():
        try:
            with open(SignUpSystem.get_user_path(), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_users(data):
        with open(SignUpSystem.get_user_path(), "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def signup():
        print("" + "=" * 50)
        print("SIGN UP".center(50))
        print("=" * 50)

        fullname = input("Enter Full Name : ").strip()
        username = input("Create Username : ").strip()
        mobile = input("Enter Mobile Number : ").strip()
        address = input("Enter Address : ").strip()
        password = pwinput.pwinput(prompt="Create Password : ",mask='x').strip()

        role = "waitstaff"

        users = SignUpSystem.load_users()
        for user in users:
            if user.get("username") == username:
                print("Username already exists. Try another one.")
                return

        new_user = {
            "uid": uuid.uuid4().hex[:6].upper(),
            "fullname": fullname,
            "username": username,
            "mobile": mobile,
            "address": address,
            "password": password,
            "role": role
        }

        users.append(new_user)
        SignUpSystem.save_users(users)

        print(f"Account created successfully!")
        print(f"Your UID is : {new_user['uid']}")
        print("Role set to : waitstaff")

    @staticmethod
    def promote_to_admin():
        print("" + "=" * 50)
        print("PROMOTE USER TO ADMIN".center(50))
        print("=" * 50)

        username = input("Enter Username : ").strip()
        uid = input("Enter UID : ").strip().upper()

        users = SignUpSystem.load_users()
        found = False

        for user in users:
            if user.get("username") == username and user.get("uid", "").upper() == uid:
                user["role"] = "admin"
                found = True
                break

        if found:
            SignUpSystem.save_users(users)
            print("User role updated to admin successfully.")
        else:
            print("No matching user found.")

    @staticmethod
    def get_user_by_username(username):
        users = SignUpSystem.load_users()
        for user in users:
            if user.get("username") == username:
                return user
        return None