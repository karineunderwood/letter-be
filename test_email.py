
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase


port = 465
smtp_server = "smtp.gmail.com"
sender_email = "letterbe9@gmail.com"
receiver_email = "letterbe9@gmail.com"
password = input("type your password and press enter: ")
message = """\
    Subject: Hi there!
    
    This is just a test....."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

