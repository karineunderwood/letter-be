"""Models for letter to your future self app."""

from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)


    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Letter(db.Model):
    """A letter."""

    __tablename__ = "letters"

    letter_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    letter_title = db.Column(db.String)
    letter_body = db.Column(db.String)
    creation_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    likes = db.Column(db.Integer)
    read = db.Column(db.Boolean)
    publish = db.Column(db.Boolean)

    # create a relationship
    user = db.relationship("User", back_populates="letters")

    def __repr__(self):
        return f'<Letter letter_id={self.letter_id} letter_title={self.letter_title}>'

class Favorite(db.Model):
    """ A favorite."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer)
    letter_id = db.Column(db.Integer, db.ForeignKey("letter.letter_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    # create a relationship

    letter = db.relationship("Letter", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id}>'




if __name__ == "__main__":
    from server import app
