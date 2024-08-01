"""This module creates and runs a secret santa app"""
import os
from flask import Flask
from . import db, auth, user_page, admin_page


def create_app(test_config=None):
    """
    Create the flask app.

    Keyword arguments:
    test_config -- test config, None by default
    """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        MAIL_SERVER="smtp.sendgrid.net",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME="apikey",
        MAIL_PASSWORD=os.environ.get("SENDGRID_API_KEY"),
        MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        print("loading from pyfile")
        app.config.from_pyfile("config.py", silent=False)
        print(app.config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(user_page.bp)
    app.register_blueprint(admin_page.bp)

    # the user_page blueprint does not have a url prefix,
    # so it's the main view
    app.add_url_rule("/", endpoint="index")

    return app
