"""
Sending emails methods
"""
import smtplib
import ssl

from flask import current_app


def send_email_defaults(reciever_email, message):
    """
    Send email with default parameters
    """
    port = current_app.config["MAIL_PORT"]  # For SSL
    password = current_app.config["MAIL_PASSWORD"]

    print(port)
    print(password)

    print("Sending email to: " + reciever_email)

    send_email(port, password, reciever_email, message)


def send_email(port, password, receiver_email, message):
    """
    Send email
    """
    # Create a secure SSL context
    context = ssl.create_default_context()
    #smtp_server = "smtp.gmail.com"
    sender_email = "testingsanta3@gmail.com"  # Enter your address

    print("Calling smtplib")

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("testingsanta3@gmail.com", password)
        server.set_debuglevel(1)
        print(server.sendmail(sender_email, receiver_email, message))
