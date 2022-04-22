"""Models for letter to your future self app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    letters = db.relationship("Letter", back_populates="user")
    favorites = db.relationship("Letter", secondary="favorites", back_populates="user")
    
    def __repr__(self):
        """Show info about user."""

        return f'<User user_id={self.user_id} email={self.email}>'

class Letter(db.Model):
    """A letter."""

    __tablename__ = "letters"

    letter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    letter_title = db.Column(db.String)
    letter_body = db.Column(db.String)
    creation_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)
    likes = db.Column(db.Integer)
    read = db.Column(db.Boolean)
    publish = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # create a relationship
    user = db.relationship("User", back_populates="letters")
    
    def __repr__(self):
        """Show info about letter."""

        return f'<Letter letter_id={self.letter_id} letter_title={self.letter_title}>'

# This is an association table. 
class Favorite(db.Model):
    """ A favorite."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True)
    letter_id = db.Column(db.Integer, db.ForeignKey("letters.letter_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # create a relationship
    # letter = db.relationship("Letter", back_populates="favorites")
    # user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id}>'


def connect_to_db(flask_app, db_uri="postgresql:///letters", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")

if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)




