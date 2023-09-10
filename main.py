import hashlib
import json
import os
from abc import ABC, abstractmethod
import sqlite3


def generate_salt():
    return os.urandom(32).hex()


def hash_password_sha256(password, salt):
    salted_password = password + salt
    sha256_hasher = hashlib.sha256()
    sha256_hasher.update(salted_password.encode('utf-8'))
    return sha256_hasher.hexdigest()


class Password_Manager(ABC):
    @abstractmethod
    def addCredentials(self, username, password):
        pass

    @abstractmethod
    def deleteCredentials(self, username):
        pass

    @abstractmethod
    def changePassword(self, username, old_password, new_password):
        pass

    @abstractmethod
    def isValidCredentials(self, username, password):
        pass

    @abstractmethod
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


class SQLite_Password_Manager(Password_Manager):
    def __init__(self, db_name = "userlogins.db"):
        self.db_name = db_name
        self.setupDB()

    def setupDB(self):
        try:
            # Create or connect to the SQLite database file
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()
            print(f"Successfully entered {self.db_name}")

            # Check if the 'users' table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            table_exists = cursor.fetchone() is not None

            if table_exists:
                # If the 'users' table exists, print its contents
                cursor.execute("SELECT * FROM users;")
                users = cursor.fetchall()
                print(f"Seems like the 'users' table already exists. It has {len(users)} accounts.")
                print("Here are the accounts:")
                for user in users:
                    print(f"--> {user}")

                # TODO: use wipeOut() method to clear all credentials

                # Ask the user if they want to delete the 'users' table and create a new one
                answer = input("Do you want to delete the 'users' table and create a new one? (yes/no) ")
                if answer == "yes":
                    cursor.execute("DROP TABLE users;")
                    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY UNIQUE, salt TEXT, hash TEXT);")
                    print("The 'users' table was deleted and a new one was created.")

            else:
                # If the 'users' table does not exist, create it
                cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY UNIQUE, salt TEXT, hash TEXT);")
                print("The 'users' table was created.")

            sqlite_connection.commit()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)


    def addCredentials(self, username, password):
        salt = generate_salt()
        hash = hash_password_sha256(password, salt)

        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()
            cursor.execute("INSERT INTO users VALUES (?, ?, ?);", (username, salt, hash))
            sqlite_connection.commit()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)


    def deleteCredentials(self, username):
        pass


    def changePassword(self, username, old_password, new_password):
        pass


    def isValidCredentials(self, username, password):
        pass


    def wipeOut(self):
        pass


    def print(self):
        # print every entry in the database
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            for user in users:
                print(user)
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)



def main():
    sql_pm = SQLite_Password_Manager()
    

main()