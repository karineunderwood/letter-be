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
def create_an_account():
    """Create a user account."""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.create_user_account(fname, lname, email, password)

    return render_template("letter_page.html", user=user)
    # return "This is a test"




    
    
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
