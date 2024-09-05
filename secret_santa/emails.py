"""Encapsulates send email functionality"""

from flask import flash
from flask_mail import Message

def send_email(flask_mail, recipient_email):
    """
    Method that sends an email using flask_mail to recipient email
    """
    recipient = recipient_email
    msg = Message("Twilio SendGrid Test Email", recipients=[recipient])
    msg.body = "Congratulations! You have sent a test email with " "Twilio SendGrid!"
    msg.html = (
        "<h1>Twilio SendGrid Test Email</h1>"
        "<p>Congratulations! You have sent a test email with "
        "<b>Twilio SendGrid</b>!</p>"
    )
    flask_mail.send(msg)
    flash(f"A test message was sent to {recipient}.")
