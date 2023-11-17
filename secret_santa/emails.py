import smtplib, ssl, os

from flask import current_app

def send_email(reciever_email, message):
    port = current_app.config['MAIL_PORT']  # For SSL
    password = current_app.config['MAIL_PASSWORD']

    send_email(port, password, reciever_email, message)

def send_email(port, password, receiver_email, message):

    # Create a secure SSL context
    context = ssl.create_default_context()
    smtp_server = "smtp.gmail.com"
    sender_email = "testingsanta3@gmail.com"  # Enter your address

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("testingsanta3@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message)