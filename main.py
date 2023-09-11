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
                                return False
        except FileNotFoundError:
            return False

        # add new credentials
        credentials.append({"username": username, "salt": salt, "hash": hash})

        with open(self.path, "w") as file:
            json.dump({"credentials": credentials}, file, indent=4)

        return True


    def deleteCredentials(self, username):
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


    def changePassword(self, username, old_password, new_password):
        if not self.isValidCredentials(username, old_password):
            print("Wrong username or password!")
            return False

        return self.deleteCredentials(username) and self.addCredentials(username, new_password)


    # clear all credentials
    def wipeOut(self):
        with open(self.path, "w") as file:
            json.dump({"credentials": []}, file, indent=4)
        return True


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
                # If the 'users' table exists, print each row's username
                cursor.execute("SELECT username FROM users;")
                users = cursor.fetchall()
                if len(users) > 0:
                    print(f"Seems like the 'users' table already exists. It has {len(users)} accounts.")

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
            return True

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
            return False


    def addCredentials(self, username, password):
        salt = generate_salt()
        hash = hash_password_sha256(password, salt)

        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            # See if username is already in table
            username_exists = True
            while username_exists:
                cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
                username_exists = cursor.fetchone() is not None
                if username_exists:
                    # ask if they want to enter a new username
                    change_username = input(f"Username {username} already exists. Do you want to enter a new username? (yes/no) ")
                    if change_username == "yes":
                        username = input(f"Username {username} already exists. Enter a new username:")
                    else:
                        print("Exiting...")
                        return False

            # Add new credentials
            cursor.execute("INSERT INTO users VALUES (?, ?, ?);", (username, salt, hash))
            sqlite_connection.commit()
            sqlite_connection.close()
            return True

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return False


    def deleteCredentials(self, username):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            # See if username is in table
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
            username_exists = cursor.fetchone() is not None
            if not username_exists:
                print(f"Username {username} does not exist!")
                sqlite_connection.close()
                return False

            # Delete credentials
            cursor.execute(f"DELETE FROM users WHERE username = '{username}';")
            sqlite_connection.commit()
            sqlite_connection.close()
            return True

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return False


    def changePassword(self, username, old_password, new_password):
        if not self.isValidCredentials(username, old_password):
            print("Wrong username or password!")
            return False

        return self.deleteCredentials(username) and self.addCredentials(username, new_password)


    def isValidCredentials(self, username, password):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            # See if username is in table
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
            username_exists = cursor.fetchone() is not None
            if not username_exists:
                print(f"Username {username} does not exist!")
                sqlite_connection.close()
                return False

            # Check if password is correct
            cursor.execute(f"SELECT salt, hash FROM users WHERE username = '{username}';")
            salt, hash = cursor.fetchone()
            salted_password = password + salt
            sha256_hasher = hashlib.sha256()
            sha256_hasher.update(salted_password.encode('utf-8'))
            sqlite_connection.close()
            return hash == sha256_hasher.hexdigest()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return False




    # clear all credentials
    def wipeOut(self):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()
            cursor.execute("DROP TABLE users;")
            cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY UNIQUE, salt TEXT, hash TEXT);")
            sqlite_connection.commit()
            sqlite_connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return False

    # TODO: delete later
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


# TODO: hide user password while typing
def main():
    sql_pm = SQLite_Password_Manager()
    sql_pm.addCredentials("user1", "password1")
    sql_pm.addCredentials("user2", "password2")
    sql_pm.addCredentials("user3", "password3")

    print(sql_pm.isValidCredentials("user1", "password1"))
    print(sql_pm.isValidCredentials("user1", "as;ldjf;ak"))

    sql_pm.print()
    sql_pm.wipeOut()
    sql_pm.print()

    
main()
