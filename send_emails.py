# import sendgrid
# import os
# from sendgrid.helpers.mail import Mail, Email, To, Content
# from model import connect_to_db, db
# import crud
# from flask import (Flask, render_template, redirect, session,
#                            request,)
# from jinja2 import StrictUndefined
# app = Flask(__name__)
# app.secret_key = "dev"
# app.jinja_env.undefined = StrictUndefined

# def send_letter_to_user(email, letter_body):
    
#     sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("karineunderwood23@gmail.com")  # changed to my verified sender
#     to_email = To(email)  # the recipient that I want to send the email
#     subject = "Letter to Your Future Self"
#     content = Content("text/plain", letter_body)
#     mail = Mail(from_email, to_email, subject, content)

# # Get a JSON-ready representation of the Mail object
#     mail_json = mail.get()

# # Send an HTTP POST request to /mail/send
#     response = sg.client.mail.send.post(request_body=mail_json)
#     print(response.status_code)
#     print(response.headers)















# if __name__ == "__main__":
#     connect_to_db(app)
#     app.run(host="0.0.0.0", debug=True)