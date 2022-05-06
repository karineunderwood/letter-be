"""CRUD operations"""

# Initialize the first steps.
# Always create a docstring to inform what the file is about.
# then import the functions
# I imported the classes I created in model.py and also connect_to_db function.

from model import db, User, Letter, Favorite, connect_to_db


def create_user(fname, lname, email, password, photo):
    """Create user's account."""

    user_account = User(fname=fname, lname=lname, email=email, password=password, photo=photo)
    

    return user_account

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):

    return User.query.get(user_id)

def create_letter_for_user(letter_title, letter_body, creation_date, delivery_date, likes, read, publish, user_id):
    """Create letter for users."""

    letter = Letter(
        letter_title=letter_title,
        letter_body=letter_body,
        creation_date=creation_date,
        delivery_date=delivery_date, 
        likes=likes,
        read=read, 
        publish=publish,
        user_id=user_id)

    return letter    

def get_letter_by_id(letter_id):
    """Return a letter by letter id."""

    return Letter.query.get(letter_id)

def get_all_letters_by_user_id(user_id):
    """Return all letters from the user."""

    return Letter.query.filter(Letter.user_id == user_id).all()

def get_published_letter():
    """Return all published letters."""

    return Letter.query.filter(Letter.publish == True).order_by(Letter.letter_id).all()


def get_all_letter_by_delivery_date():
    """Get all letter by delivery date"""

    return Letter.query.filter(Letter.delivery_date == "2022-05-05").all()






# Always make sure to use this at the bottom
# This will connect to the database when running crud.py interactively
# Here I'm importing Flask app = Flask(__name__)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)