import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content



def send_letter_to_user(email, letter_body):
    
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY2'))
    print("sg: ", sg)
    from_email = Email("karineunderwood23@gmail.com")  # changed to my verified sender
    to_email = To("letterbe9@gmail.com")  # the recipient that I want to send the email
    subject = "Letter to Your Future Self"
    content = Content("text/plain", letter_body)
    mail = Mail(from_email, to_email, subject, content)

   

# Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

# Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print("response: ", response)
    print("response.status_code: ", response.status_code)
    return response.status_code
    














