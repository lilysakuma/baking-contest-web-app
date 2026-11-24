import unittest
import os
import tempfile
import runpy
import sqlite3
from pathlib import Path
from app import app


class BakingContestTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for each test
        self.original_dir = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()

        init_path = Path(__file__).resolve().parent / "init_db.py"

        os.chdir(self.temp_dir.name)
        runpy.run_path(str(init_path))

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        # Clean up after each test
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def add_test_user(self):
        # Add a fake contestant to use in the tests
        return self.client.post("/add_user", data={
            "name": "Emma Baker",
            "age": "22",
            "phone": "850-555-0101",
            "security": "1",
            "password": "Demo123"
        })

    def add_test_entry(self):
        # Add a baking entry for the fake contestant
        return self.client.post("/add_entry", data={
            "username": "Emma Baker",
            "item": "Chocolate Chip Cookies",
            "excellent": "15",
            "ok": "4",
            "bad": "1"
        })

    def test_homepage(self):
        # Make sure the homepage loads
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        # Make sure a valid user can be added
        response = self.add_test_user()

        self.assertIn(
            b"New baking contest user added successfully!",
            response.data
        )

        # Check that the user was saved in the database
        with sqlite3.connect("contest.db") as conn:
            user = conn.execute(
                "SELECT Name, Age FROM BakingContestPeople"
            ).fetchone()

        self.assertEqual(user, ("Emma Baker", 22))

    def test_invalid_user(self):
        # Make sure invalid user information is rejected
        response = self.client.post("/add_user", data={
            "name": "",
            "age": "-5",
            "phone": "",
            "security": "7",
            "password": ""
        })

        self.assertIn(b"Name cannot be empty.", response.data)
        self.assertIn(
            b"Age must be between 1 and 120.",
            response.data
        )
        self.assertIn(
            b"Security level must be 1, 2, or 3.",
            response.data
        )
        self.assertIn(b"Phone number cannot be empty.", response.data)
        self.assertIn(b"Password cannot be empty.", response.data)

        # Make sure the invalid user was not saved
        with sqlite3.connect("contest.db") as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM BakingContestPeople"
            ).fetchone()[0]

        self.assertEqual(count, 0)

    def test_add_entry(self):
        # Register a user before adding an entry
        self.add_test_user()
        response = self.add_test_entry()

        self.assertIn(
            b"New baking contest entry added successfully!",
            response.data
        )

        # Check that the entry and votes were saved correctly
        with sqlite3.connect("contest.db") as conn:
            entry = conn.execute("""
                SELECT NameOfBakingItem, NumExcellentVotes,
                       NumOkVotes, NumBadVotes
                FROM BakingContestEntry
            """).fetchone()

        self.assertEqual(
            entry, ("Chocolate Chip Cookies", 15, 4, 1)
        )

    def test_invalid_votes(self):
        # Make sure invalid vote counts are rejected
        self.add_test_user()

        response = self.client.post("/add_entry", data={
            "username": "Emma Baker",
            "item": "Brownies",
            "excellent": "-5",
            "ok": "abc",
            "bad": "2.5"
        })

        self.assertIn(
            b"Excellent votes must be a nonnegative integer.",
            response.data
        )
        self.assertIn(
            b"OK votes must be a nonnegative integer.",
            response.data
        )
        self.assertIn(
            b"Bad votes must be a nonnegative integer.",
            response.data
        )

        with sqlite3.connect("contest.db") as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM BakingContestEntry"
            ).fetchone()[0]

        self.assertEqual(count, 0)

    def test_unregistered_user(self):
        # Make sure unregistered users cannot submit entries
        response = self.client.post("/add_entry", data={
            "username": "Unknown Person",
            "item": "Brownies",
            "excellent": "10",
            "ok": "2",
            "bad": "0"
        })

        self.assertIn(
            b"The user does not exist in the database.",
            response.data
        )

    def test_list_users(self):
        # Make sure registered users appear on the website
        self.add_test_user()
        response = self.client.get("/list_users")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emma Baker", response.data)

    def test_list_results(self):
        # Make sure baking entries appear on the results page
        self.add_test_user()
        self.add_test_entry()

        response = self.client.get("/list_results")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Chocolate Chip Cookies", response.data)


if __name__ == "__main__":
    unittest.main()