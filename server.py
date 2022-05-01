"""Server for letters app."""

from flask import (Flask, render_template, request, flash, 
                                        session, redirect)
                  

from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import cloudinary.uploader

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dnw3idclo"

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """This is the homepage. """

    return render_template('homepage.html')


@app.route("/registration")
def show_registration_form():
    """Show registration form."""

    return render_template("register.html")


@app.route("/registration", methods=["POST"])
def create_user():
    """Create a user account."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    photo = request.files['my-file']
    
    response= send_user_profile_pic(photo)
    
    if 'secure_url' in response:
        photo_url = response['secure_url']
    else:
        photo_url = ""
    
    user = crud.get_user_by_email(email)
    if user:
        flash("You cannot create an account with that email. Please try again.")
    else:
        user = crud.create_user(fname=fname, lname=lname, email=email, password=password, photo=photo_url)
        db.session.add(user)
        db.session.commit()
        flash("Account created succesfully! Please log in.")

    return redirect("/")
    
    
@app.route("/login")
def show_login_page():
    """Show log in page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    # check if email and password are correct
    # if it is store the user's email in session
    if not user or user.password != password:
        flash("The email or password you enter is not valid. Please try again.")
        return redirect("/")
    else:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f'Welcome back, {user.email}!')
        
        return redirect(f"/user/{user.user_id}")


@app.route("/logout")
def log_out():
    """Allows user to log out."""
    
    session.clear()
   
    return redirect("/")


@app.route("/user/<user_id>")
def user_profile(user_id):
    """Display user profile for currently logged in user. """

    user = crud.get_user_by_id(user_id)
   
    return render_template("users_profile.html", user=user)

    
@app.route("/letter", methods=["POST"])
def create_a_letter():
    """Create a letter."""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email) #getting user object by email

    letter_body = request.form.get("letter_body")
    letter_title = request.form.get("title")
    creation_date = request.form.get("creation-date")
    delivery_date = request.form.get("delivery-date")
    publish = request.form.get("publish")
    
    
    if publish == "YES":
        publish = True
    elif publish == "NO":
        publish = False

    
    if user is None:
        flash("You must log in to write a letter.")
        return redirect("/")
        
    else:
        user_letter = crud.create_letter_for_user(
                        letter_title=letter_title,  #left side is parameter name, right side is variable from line 82
                        letter_body=letter_body, 
                        creation_date=creation_date, 
                        delivery_date=delivery_date, 
                        likes=0, 
                        read=False, 
                        publish=publish, 
                        user_id=user.user_id)  #user is the user object from line 79, user_id is a column in your users table
                       
        
        db.session.add(user_letter)
        db.session.commit()
        flash("Your letter was successfully created!")
    
    return redirect(f"/user/{user.user_id}")

@app.route("/letters/<letter_id>")
def display_letter(letter_id):
    """Display letter by letter id."""

    letter = crud.get_letter_by_id(letter_id)

    return render_template("letter.html", letter=letter)

@app.route("/public_letters")
def display_all_public_letters():
    """Display all published letters."""

    published = crud.get_published_letter()


    return render_template("public_letters.html", published=published)

@app.route("/add_like", methods=["POST"])
def add_like():
    """Enable user to like the letters."""

    
    liked_letter_id = request.form.get("like-letter")
    

    liked_letter = crud.get_letter_by_id(liked_letter_id) #get letter object by letter id
    liked_letter.likes = liked_letter.likes + 1 #updating the likes column for that letter object to add 1

    db.session.commit()

    return redirect("/public_letters")


@app.route("/write_letter")
def write_letters():
    """Write a letter."""

    
    return render_template("letter_page.html")

    
@app.route("/users_letters")
def users_letters():
    """Return all letters from user."""

    logged_in_email = session.get("user_email") 
    user = crud.get_user_by_email(logged_in_email)


    letters = crud.get_all_letters_by_user_id(user.user_id)

    return render_template("users_letters.html", letters=letters)






#  Helper function for my cloudinary request

def send_user_profile_pic(photo):
    """Process form data."""

    result = cloudinary.uploader.upload(photo,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME )
    return result


# 
# 
# 
# 





    
    
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
