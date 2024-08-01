"""This script can be run to add an admin user to the database"""
import emails

port = 465  # For SSL
password = input("Type your password and press enter: ")

receiver_email = input("Type the email to send to and press enter: ")

message = """\
Subject: Hi there

This message is sent from Python."""

emails.send_email(port, password, receiver_email, message)
