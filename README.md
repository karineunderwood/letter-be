# Letter Be
## Summary

**Letter Be** is a web app where users can write letters to themselves or someone else and get the letter delivered in the future. With Letter Be, users can easily set up an account, write letters, upload picture for their profile, get daily motivational quotes in their profile page, read their past letters and  public letters from other users.   

## About the Developer

Letter Be was created by Karine Underwood 
[LinkedIn](https://www.linkedin.com/in/karine-underwood-622104219)

## Technologies
**Tech Stack:**

- Python
- Flask
- Jinja2
- SQLalchemy
- JavaScript
- PostgreSQL
- AJAX
- JSON
- HTML
- CSS
- Bootstrap
- Cloudinary API
- SendGrid API

## Features

Users can easily sign up and upload a picture for their profile.

![Sign Up ](/static/README-img/signup.png)


After sign up users are able to log in in their profile.

![Log In ](/static/README-img/login.jpg)


After  log in the user is redicted to their profile page and can see their name, email and user id. Also they can get a daily quote by clicking the button that says "Get a Quote".

![Profile Page](/static/README-img/profileReadMe.jpg)


Letter Be provides to the user some ideas to start the letter and if the user is still not sure on what to write, they can click the button "Surprise Me" and Letter Be will generate a subject for them to start writing. 

![Letter Ideas](/static/README-img/letter_ideas.jpg)


When the users are ready to move on and write a letter they simply scroll down the page and will find a form. The user will fill out the following boxes:

![Write a Letter](/static/README-img/letter_form.jpg)


- The letter body
- Letter title
- Creation Date
- Delivery Date
- Choose if they want to make the letter public or not.

After that, just click on Submit!


Users can check their past letters by clicking on the button that says Read Letter.

![Past Letters](/static/README-img/user_personal_letter.jpg)

Another interesting thing that Letter Be provides to the user experience is that the users can read letters from other user. If they choose the option make it public when they are creating the letter they can click on Public Letters and read past letters. 


![Public Letters](/static/README-img/read_public.jpg)


## Setup/Installation
#### Requirements:
- PostgreSQL
- Python 3.9
- Cloudinary and SendGrid API Keys

To have this app running on your local computer, please follow the steps bellow:
Clone repository:
```
$ git clone https://github.com/karineunderwood/letter-be.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies🔗:
``` 
$ pip install -r requirements.txt
```
Get your own secret keys🔑 for   [Cloudinary](https://cloudinary.com/users/register/free) and   [SendGrid](https://app.sendgrid.com/login). Save them to a file `secrets.sh`. Your file should look something like this:
```
export CLOUDINARY_KEY='xwy123'
export CLOUDINARY_SECRET='123abC'
export SENDGRID_API_KEY='abc123'
```
Create database 'letters'.
```
$ createbd letters
```
Create your database tables and seed🌱 example data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

