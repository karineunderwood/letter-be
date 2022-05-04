from psycopg2 import connect
import unittest
import server
from server import app
from model import db, connect_to_db

class LetterTests(unittest.TestCase):
    """Tests for my letter site."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        connect_to_db(app,"postgresql:///letters")

    def test_homepage(self):
        """Can the homepage be reached?"""

        result = self.client.get("/")
        self.assertIn(b"Welcome to Letter Be!", result.data)

    def test_login(self):
        """Show the login page, but not write a letter"""

        result = self.client.get("/login")
        self.assertIn(b"Log In", result.data)
        self.assertNotIn(b"Your exciting journey starts here!", result.data )

   
        



if __name__ == "__main__":
    unittest.main()