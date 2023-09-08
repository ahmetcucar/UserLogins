import hashlib
import json
import os

class JSON_Password_Manager:
    def __init__(self, path):
        self.path = path

    #TODO

# register new account
def addCredentials(username, password):
    salt = generate_salt()
    hash = hash_password_sha256(password, salt)

    # read data.json
    credentials = []
    try:
        with open("./data.json", "r") as file:
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

    with open("./data.json", "w") as file:
        json.dump({"credentials": credentials}, file, indent=4)


def deleteCredentials(username):
    with open("./data.json", "r") as file:
        data = json.load(file)
        credentials = data["credentials"]
        for entry in credentials:
            if entry["username"] == username:
                credentials.remove(entry)
                with open("./data.json", "w") as file:
                    json.dump({"credentials": credentials}, file, indent=4)
                return
        print(f"Username {username} does not exist!")


def changePassword(username, old_password, new_password):
    if not isValidCredentials(username, old_password):
        print("Wrong username or password!")
        return

    deleteCredentials(username)
    addCredentials(username, new_password)

# clear all credentials
def wipeOut():
    with open("./data.json", "w") as file:
        json.dump({"credentials": []}, file, indent=4)


def isValidCredentials(username, password):
    with open("./data.json", "r") as file:
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
    wipeOut()
    addCredentials("ahmet", "ucar")
    
    deleteCredentials("ahmet")


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