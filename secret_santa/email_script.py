import emails

PORT = 465  # For SSL
password = input("Type your password and press enter: ")

receiver_email = input("Type the email to send to and press enter: ")

MESSAGE = """\
Subject: Hi there

This message is sent from Python."""

emails.send_email(PORT, password, receiver_email, MESSAGE)
