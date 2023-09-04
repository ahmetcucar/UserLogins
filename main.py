import hashlib
import os


class PasswordManager:
    def __init__(self):
        self.__credentials = {}
        self.__salts = {}

    def add(self, username, password):
        salt = generate_salt()
        hash = hash_password_sha256(password, salt)
        self.__credentials[username] = hash
        self.__salts[username] = salt

    def isValidCredentials(self, username, password):
        if username not in self.__credentials:
            return False
        salt = self.__salts[username]
        hash = hash_password_sha256(password, salt)
        return hash == self.__credentials[username]


def generate_salt():
    return os.urandom(32).hex()


def hash_password_sha256(password, salt):
    salted_password = password + salt
    sha256_hasher = hashlib.sha256()
    sha256_hasher.update(salted_password.encode('utf-8'))
    return sha256_hasher.hexdigest()


def main():
    pm = PasswordManager()
    pm.add("ahmet", "ucar")
    pm.add("hello", "world")
    pm.add("foo", "bar")

    username = input("Enter username: ")
    password = input("Enter password: ")
    if pm.isValidCredentials(username, password):
        print("Welcome,", username)
    else:
        print("Wrong username or password! Get lost!")

main()
