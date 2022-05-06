import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import crud

# def a function to send email to user
# use a crud function to query data from database
# do some logic

def send_letter_to_user_by_email():

    letter_content = crud.get_all_letter_by_delivery_date()

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("karineunderwood23@gmail.com")  # changed to my verified sender
    to_email = To("letterbe9@gmail.com")  # the recipient that I want to send the email
    subject = "Letter to Your Future Self"
    content = Content("text/plain", letter_content)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)