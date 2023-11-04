import smtplib, ssl

#from flask import current_app

port = 465  # For SSL
#password = current_app.config['MAIL_PASSWORD']
password = input("Type your password and press enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

smtp_server = "smtp.gmail.com"
sender_email = "testingsanta3@gmail.com"  # Enter your address
receiver_email = "helenffionadams@gmail.com"  # Enter receiver address
message = """\
Subject: Hi there

This message is sent from Python."""

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("testingsanta3@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)