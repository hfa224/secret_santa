from flask import current_app, g
from flask_mailman import Mail

def init_app(app):
    if 'mail' not in g:
        g.mail = Mail(app)

def get_mail():
    return g.mail
