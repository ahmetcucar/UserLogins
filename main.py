import hashlib
import json
import os

class Password_Manager:
    def __init__(self):
        pass

    def addCredentials(self, username, password):
        pass

    def deleteCredentials(self, username):
        pass

    def changePassword(self, username, old_password, new_password):
        pass

    def isValidCredentials(self, username, password):
        pass

    def wipeOut(self):
        pass


class JSON_Password_Manager(Password_Manager):
    def __init__(self, path):
        self.path = path
        self.wipeOut()


    def addCredentials(self, username, password):
        salt = generate_salt()
        hash = hash_password_sha256(password, salt)

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
                                return
        except FileNotFoundError:
            pass

        # add new credentials
        credentials.append({"username": username, "salt": salt, "hash": hash})

        with open(self.path, "w") as file:
            json.dump({"credentials": credentials}, file, indent=4)


    def deleteCredentials(self, username):
        with open(self.path, "r") as file:
            data = json.load(file)
            credentials = data["credentials"]
            for entry in credentials:
                if entry["username"] == username:
                    credentials.remove(entry)
                    with open(self.path, "w") as file:
                        json.dump({"credentials": credentials}, file, indent=4)
                    return
            print(f"Username {username} does not exist!")


    def changePassword(self, username, old_password, new_password):
        if not self.isValidCredentials(username, old_password):
            print("Wrong username or password!")
            return

        self.deleteCredentials(username)
        self.addCredentials(username, new_password)


    # clear all credentials
    def wipeOut(self):
        with open(self.path, "w") as file:
            json.dump({"credentials": []}, file, indent=4)


    def isValidCredentials(self, username, password):
        with open(self.path, "r") as file:
            data = json.load(file)
            credentials = data["credentials"]
            for entry in credentials:
                if entry["username"] == username:
                    salt = entry["salt"]
                    hash = entry["hash"]
                    salted_password = password + salt
                    sha256_hasher = hashlib.sha256()
                    sha256_hasher.update(salted_password.encode('utf-8'))
                    if hash == sha256_hasher.hexdigest():
                        return True
                    else:
                        return False
            return False


def generate_salt():
    return os.urandom(32).hex()


def hash_password_sha256(password, salt):
    salted_password = password + salt
    sha256_hasher = hashlib.sha256()
    sha256_hasher.update(salted_password.encode('utf-8'))
    return sha256_hasher.hexdigest()


def main():
    json_pm = JSON_Password_Manager("./data.json")
    # json_pm.addCredentials("ahmet", "ucar")
    # json_pm.addCredentials("hocus", "pocus")

    # print(json_pm.isValidCredentials("ahmet", "ucar"))
    # print(json_pm.isValidCredentials("ahmet", "ucar2"))

    # # json_pm.isValidCredentials("hocus", "pocus")
    # # json_pm.isValidCredentials("hocus", "pocus2")

    # # json_pm.changePassword("ahmet", "ucar", "ucar2")
    # # json_pm.isValidCredentials("ahmet", "ucar")
    # # json_pm.isValidCredentials("ahmet", "ucar2")

    # json_pm.deleteCredentials("ahmet")


    # deleteCredentials("valerie")
    # addCredentials("hello", "world")
    # addCredentials("foo", "bar")
    # addCredentials("valerie", "lange")
    # addCredentials("henry", "ford")

    # username = input("Enter username: ")
    # password = input("Enter password: ")
    # if isValidCredentials(username, password):
    #     print("Welcome,", username)
    # else:
    #     print("Wrong username or password! Get lost!")

main()