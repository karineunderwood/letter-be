"""Server for letters app."""

from flask import (Flask, render_template, request, flash, session, 
                  redirect)

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """  """

    # return "Test Homepage"
    return render_template('homepage.html')

# create a route to process form data and add it to my database

@app.route("/registration", methods=["POST"])
def create_user():
    """Create a user account."""

    fname = request.form.get("fname")
    lname = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.create_user(fname, lname, email, password)
    
    db.session.add(user)
    db.session.commit()

    return render_template("letter_page.html")
    # return render_template("users_profile.html")


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
    else:
        session["user_email"] = user.email
        flash(f'Welcome back, {user.email}!')

    return redirect('users_profile.html')







@app.route("/write_letter", methods=["POST"])
def create_a_letter():
    """Create a letter."""

    letter_body = request.form.get("letter_body")
    letter_title = request.form.get("letter_title")
    creation_date = request.form.get("creation_date")
    delivery_date = request.form.get("delivery_date")
    # print(letter_body)
    # print(letter_title)
    # print(creation_date)
    # print(delivery_date)

    return render_template("users_profile.html")
# may have to redirect to the users profile when I create it.





    
    
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
