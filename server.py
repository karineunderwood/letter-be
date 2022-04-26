"""Server for letters app."""

from flask import (Flask, render_template, request, flash, session, 
                  redirect)

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

     
    user = crud.get_user_by_email(email)
    if user:
        flash("You cannot create an account with that email. Please try again.")
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created succesfully! Please log in.")

    return redirect("/")
    # return render_template("register.html")
    


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



# Create a route to show the form
# @app.route("/form-upload")
# def show_form_upload():
#     """Show upload form"""

#     return render_template("register.html")


# Create a route to process the form
@app.route("/posto-form-data", methods=["POST"])
def post_user_profile_pic():
    """Process form data."""

    user_picture = request.files['my-file']
    result = cloudinary.uploader.upload(user_picture,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME )

    img_url = result['secure_url']
    return redirect("/", img_url=img_url)

@app.route("/letter", methods=["POST"])
def create_a_letter():
    """Create a letter."""

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email) #getting user object by email

    letter_body = request.form.get("letter_body")
    letter_title = request.form.get("title")
    creation_date = request.form.get("creation-date")
    delivery_date = request.form.get("delivery-date")
    
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
                        publish=False, 
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



@app.route("/write_letter")
def write_letters():
    """Write a letter."""

    return render_template("letter_page.html")

    

@app.route("/all_letters")
def all_letters():
    """Return all letters."""

    logged_in_email = session.get("user_email") 
    user = crud.get_user_by_email(logged_in_email)


    letters = crud.get_all_letters_by_user_id(user.user_id)

    return render_template("all_letters.html", letters=letters)

# @app.route("/show_form_img")
# def show_form_image():
#     """Show form."""

#     return render_template("users_profile")







    
    
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
