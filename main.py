import hashlib
import json
import os


def addCredentials(username, password):
    salt = generate_salt()
    hash = hash_password_sha256(password, salt)

    credentials = []
    try:
        with open("./data.json", "r") as file:
            data = json.load(file)
            if "credentials" in data:
                credentials = data["credentials"]
    except FileNotFoundError:
        pass

    #TODO: handle duplicate usernames

    credentials.append({"username": username, "salt": salt, "hash": hash})

    with open("./data.json", "w") as file:
        json.dump({"credentials": credentials}, file, indent=4)

# TODO: delete account

# TODO: change password

# TODO: wipe out all data


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
    addCredentials("ahmet", "ucar")
    addCredentials("ahmet", "ucar")
    addCredentials("hello", "world")
    addCredentials("foo", "bar")
    addCredentials("valerie", "lange")
    addCredentials("henry", "ford")

    username = input("Enter username: ")
    password = input("Enter password: ")
    if isValidCredentials(username, password):
        print("Welcome,", username)
    else:
        print("Wrong username or password! Get lost!")

main()