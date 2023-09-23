import sys
import os
import unittest

# Add parent directory to path and import json_pm
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from src import json_pm


class Test(unittest.TestCase):
    def test_add_credentials(self):
        pm = json_pm.JsonPasswordManager("data/test.json")
        self.assertTrue(pm.add_credentials("user1", "test"))
        self.assertFalse(pm.add_credentials("user1", "test"))
        pm.wipe_credentials()

    def test_delete_credentials(self):
        pm = json_pm.JsonPasswordManager("data/test.json")
        pm.add_credentials("user1", "test")
        self.assertTrue(pm.delete_credentials("user1"))
        self.assertFalse(pm.delete_credentials("user1"))
        self.assertFalse(pm.delete_credentials("user2"))
        pm.wipe_credentials()

    def test_change_password(self):
        pm = json_pm.JsonPasswordManager("data/test.json")
        pm.add_credentials("user1", "test")
        self.assertTrue(pm.change_password("user1", "test", "test2"))
        self.assertFalse(pm.change_password("user1", "test", "test2"))
        self.assertFalse(pm.change_password("user1", "test2", "test2"))
        self.assertFalse(pm.change_password("user2", "test", "test2"))
        pm.wipe_credentials()

    def test_wipe_credentials(self):
        pm = json_pm.JsonPasswordManager("data/test.json")
        pm.add_credentials("user1", "test")
        self.assertTrue(pm.wipe_credentials())

    def test_verify_credentials(self):
        pm = json_pm.JsonPasswordManager("data/test.json")
        pm.add_credentials("user1", "test")
        self.assertTrue(pm.verify_credentials("user1", "test"))
        self.assertFalse(pm.verify_credentials("user1", "test2"))
        self.assertFalse(pm.verify_credentials("user2", "test"))


if __name__ == "__main__":
    unittest.main()

