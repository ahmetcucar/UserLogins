import os
from abc import ABC, abstractmethod
import hashlib

# This is a helper function that generates a random salt
# in order to make the hash more secure
def generate_salt():
    return os.urandom(32).hex()


# This is a helper function that hashes a password using the SHA256 algorithm
def hash_password_sha256(password, salt):
    salted_password = password + salt
    sha256_hasher = hashlib.sha256()
    sha256_hasher.update(salted_password.encode('utf-8'))
    return sha256_hasher.hexdigest()


# This is the abstract class that both password managers will inherit from
class PasswordManager(ABC):
    @abstractmethod
    def add_credentials(self, username, password):
        pass

    @abstractmethod
    def delete_credentials(self, username):
        pass

    @abstractmethod
    def change_password(self, username, old_password, new_password):
        pass

    @abstractmethod
    def verify_credentials(self, username, password):
        pass

    @abstractmethod
    def wipe_credentials(self):
        pass
