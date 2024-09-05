"""
Simple script to use emails file to send an email, for testing
"""
from secret_santa.emails import send_email

PORT = 465  # For SSL
password = input("Type your password and press enter: ")

receiver_email = input("Type the email to send to and press enter: ")

MESSAGE = """\
Subject: Hi there

This message is sent from Python."""

send_email(PORT, password, receiver_email, MESSAGE)
