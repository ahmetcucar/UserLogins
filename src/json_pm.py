import json
import src.password_manager as password_manager


# This is the JSON password manager class that implements the abstract PasswordManager class
# It uses a JSON file to store the credentials, which is not very efficient
class JsonPasswordManager(password_manager.PasswordManager):
    def __init__(self, path = "data/data.json"):
        self.path = path
        self.wipe_credentials()


    def add_credentials(self, username, password):
        salt = password_manager.generate_salt()
        hash = password_manager.hash_password_sha256(password, salt)

        # read data.json
        credentials = []
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                if "credentials" in data:
                    credentials = data["credentials"]

                    # handle duplicate usernames
                    if len(credentials) > 0:
                        for entry in credentials:
                            if entry["username"] == username:
                                print("Username already exists!")
                                return False
        except FileNotFoundError:
            return False

        # add new credentials
        credentials.append({"username": username, "salt": salt, "hash": hash})

        with open(self.path, "w") as file:
            json.dump({"credentials": credentials}, file, indent=4)

        return True


    def delete_credentials(self, username):
        with open(self.path, "r") as file:
            data = json.load(file)
            credentials = data["credentials"]
            for entry in credentials:
                if entry["username"] == username:
                    credentials.remove(entry)
                    with open(self.path, "w") as file:
                        json.dump({"credentials": credentials}, file, indent=4)
                    return True
            print(f"Username {username} does not exist!")
            return False


    def change_password(self, username, old_password, new_password):
        if not self.verify_credentials(username, old_password):
            print("Wrong username or password!")
            return False

        if old_password == new_password:
            print("Old and new passwords are the same!")
            return False

        return self.delete_credentials(username) and self.add_credentials(username, new_password)


    # clear all credentials
    def wipe_credentials(self):
        with open(self.path, "w") as file:
            json.dump({"credentials": []}, file, indent=4)
        return True


    def verify_credentials(self, username, password):
        with open(self.path, "r") as file:
            data = json.load(file)
            credentials = data["credentials"]
            for entry in credentials:
                if entry["username"] == username:
                    salt = entry["salt"]
                    hash = entry["hash"]
                    return hash == password_manager.hash_password_sha256(password, salt)
            return False
