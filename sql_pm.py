from abc import ABC, abstractmethod
import password_manager
import sqlite3


class SqlitePasswordManager(password_manager.PasswordManager):
    def __init__(self, db_name = "userlogins.db"):
        self.db_name = db_name
        self.setupDB()

    def setupDB(self):
        try:
            # Create or connect to the SQLite database file
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()
            print(f"Successfully entered {self.db_name}\n")

            # Check if the 'users' table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            table_exists = cursor.fetchone() is not None

            if table_exists:
                # If the 'users' table exists, print each row's username
                cursor.execute("SELECT username FROM users;")
                users = cursor.fetchall()
                if len(users) > 0:
                    print(f"Seems like the 'users' table already exists. It has {len(users)} accounts.")

                    # Ask the user if they want to delete the 'users' table and create a new one
                    answer = input("Do you want to delete the 'users' table and create a new one? (yes/no) ")
                    if answer == "yes":
                        self.wipe_credentials()
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


    def add_credentials(self, username, password):
        salt = password_manager.generate_salt()
        hash = password_manager.hash_password_sha256(password, salt)

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


    def delete_credentials(self, username):
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


    def change_password(self, username, old_password, new_password):
        if not self.verify_credentials(username, old_password):
            print("Wrong username or password!")
            return False

        return self.delete_credentials(username) and self.add_credentials(username, new_password)


    def verify_credentials(self, username, password):
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
            sqlite_connection.close()
            return hash == password_manager.hash_password_sha256(password, salt)

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return False


    # clear all credentials
    def wipe_credentials(self):
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
