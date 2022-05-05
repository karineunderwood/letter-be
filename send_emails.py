import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email("karineunderwood23@gmail.com")  # changed to my verified sender
to_email = To("letterbe9@gmail.com")  # the recipient that I want to send the email
subject = "Letter to Your Future Self"
content = Content("text/plain", "If you are receiving this email. It is because I nailed it!")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)



# TO DO:
# query data from database user's email, letter title, letter body
# creation date and delivery date
# def a function
# store data  / create a html template so I can use as a content
# 
# 
# 
