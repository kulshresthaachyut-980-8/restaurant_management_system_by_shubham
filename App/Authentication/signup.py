import os
import json
import uuid
import pwinput
import datetime


logs_path=os.path.join(os.path.dirname(__file__),"..","Logs","singup_logs.txt")

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
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print("Somthing Went Wrong")
            with open(logs_path,'w')as log:
                log.print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Error : {e}")
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
        while True:
            fullname = input("Enter Full Name : ").strip()
            if not fullname or not fullname.replace(" ","").isalpha():
                print("Invalid Name. it Contains Only Alphabets & Spaces.")
                continue
            tem_name=fullname.lower()
            repetion=False
            for letters in "abcdefghijklmnopqrstuvwxyz":
                if letters*3 in tem_name:
                    repetion=True
                    break
            if repetion==True:
                print("invalid name. Letters Cannot reapet more than twice. ")
                continue
            else:
                break

        while True:
            username = input("Create Username : ").strip()
            if not username.isalnum():
                print("Error: Username will Contains letters and numbers (no space or symbols). ")
                continue
            users = SignUpSystem.load_users()
            username_repetion=False
            for user in users:
                if user.get("username") == username:
                    username_repetion=True
                    break
                if username_repetion==True:
                    print("Username already exists. Try another one.")
                    continue
            else:
                break

            
        while True:
            password = pwinput.pwinput(prompt="Create Password : ",mask='x').strip()
            if len(password)<6:
                print("Password is too Weak. It must be at least 6 Characters long.")
                continue
            if password.lower()==tem_name:
                print("Password Should be Diffrent from your Username.")
                continue
            else:
                break


        while True:
            mobile = input("Enter Mobile Number : ").strip()
            tem_mobile=mobile.replace("+91", "").replace("-", "").replace(" ", "")
            if not tem_mobile.isdigit() or len(tem_mobile)!=10:
                print("Mobile Number is Not Valid. It must be 10 digits (excluding +91).")
                continue
            mob_repetion=False
            for digits in "0123456789":
                if digits*5 in tem_mobile:
                    mob_repetion=True
                    break
                if mob_repetion==True:
                    print("Invalid Mobile. Digits Cannot repete 5 times in a row.")
                    continue
            else:
                break


        while True:
            address = input("Enter Address : ").strip()
            if len(address)<4:
                print("Address Must be 4 Charactes long.")
            else:
                break
        role = "waitstaff"

        

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