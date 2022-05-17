"""Server for letters app."""

from flask import (Flask, jsonify, render_template, request, flash, 
                                        session, redirect)
import random 

from datetime import date 

from model import connect_to_db, db
import crud
import send_emails
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
    
    if not user or user.password != password:
        flash("The email or password you enter is not valid. Please try again.")
        return redirect("/login")
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
    user = crud.get_user_by_email(logged_in_email) 

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
                        letter_title=letter_title,  
                        letter_body=letter_body, 
                        creation_date=creation_date, 
                        delivery_date=delivery_date, 
                        likes=0, 
                        read=False, 
                        publish=publish, 
                        user_id=user.user_id)  
                       
        
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
    

    liked_letter = crud.get_letter_by_id(liked_letter_id) 
    liked_letter.likes = liked_letter.likes + 1 

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


@app.route("/show_affirmations")
def show_affirmation_quotes():
    """Show to the user affirmation quotes for the day."""

    affirmations = [
        "Instead of worrying about what you cannot control, shift your energy to what you can create. - Roy T. Bennett, The Light in the Heart",
        "I deserve the best, and I accept it now. All my needs and desires are met before I even ask. - Louise Hay",
        "I am surrounded by love. - Louise Hay",
        "I am one with the very power that created me. - Louise Hay",
        "There is no path to happiness; Happiness is the path. - Buddha",
        "Happiness is a warm puppy. - Charles M. Schulz",
        "You are loved just for being who you are, just for existing. -Ram Dass",
        "The perfect moment is this one. - Jon Kabat-Zinn",
        "All our dreams can come true, if we have the courage to pursue them. - Walt Disney",
        "I people are doubting how far you can go, go so far that you can't hear them anymore. - Michele Ruiz"
         ]

    return random.choice(affirmations)

@app.route("/random_letter_choice")
def pick_random_choice_for_letter():
    """Generate a random option for user to write a letter."""

    choose_title = ["Time-machine", 
                    "Self-reflection", 
                    "Reminder to yourself",
                    "Your next birthday",
                    "Your future child",
                    "Your best friend",
                    "Your Career life in 10 years.",
                    "To your partner/spouse, on your 20th anniversary."
                    ]

    return f"The letter you will write today is about: {random.choice(choose_title)}"

@app.route("/send_email", methods= ["POST"])
def send_user_email():
    """Send user the letter as an email."""
    letter_body = request.json.get("letterBody")
    
    if "user_email" in session:
        response_code = send_emails.send_letter_to_user(session["user_email"],letter_body)
        
        if response_code == 202:
            return "Your email was successfully sent!"
        else:
            return "Unfortunately we are unable to send the email at this time."
    
    else:
        redirect("/")
    
 




"""Helper function for my cloudinary request"""

def send_user_profile_pic(photo):
    """Process form data."""

    result = cloudinary.uploader.upload(photo,
                                        api_key=CLOUDINARY_KEY,
                                        api_secret=CLOUDINARY_SECRET,
                                        cloud_name=CLOUD_NAME )
    return result





def send_daily_letters():
    letters = crud.get_all_letter_by_delivery_date(date.today())
    for letter in letters:
        send_emails.send_letter_to_user(letter.email, letter.letter_body)


    
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    