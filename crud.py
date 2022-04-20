"""CRUD operations"""

# Initialize the first steps.
# Always create a docstring to inform what the file is about.
# then import the functions
# I imported the classes I created in model.py and also connect_to_db function.

from model import db, User, Letter, Favorite, connect_to_db


def create_user_account(fname, lname, email, password):
    """Create user's account."""

    user_account = User(fname=fname, lname=lname, email=email, password=password)

    return user_account

def create_letter_for_user(letter_title, letter_body, creation_date, delivery_date):
    """Create letter for users."""

    user_letter = Letter(letter_title=letter_title, letter_body=letter_body, creation_date=creation_date, delivery_date=delivery_date)

    return user_letter    













# Always make sure to use this at the bottom
# This will connect to the database when running crud.py interactively
# Here I'm importing Flask app = Flask(__name__)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)