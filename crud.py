"""CRUD operations"""

# Initialize the first steps.
# Always create a docstring to inform what the file is about.
# then import the functions
# I imported the classes I created in model.py and also connect_to_db function.

from model import db, User, Letter, Favorite, connect_to_db

















# Always make sure to use this at the bottom
# This will connect to the database when running crud.py interactively
# Here I'm importing Flask app = Flask(__name__)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)