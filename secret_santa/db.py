"""
Contains db functionality
"""
import sqlite3

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


@click.command("init-db")
def init_db_command():
    """
    Creates the cli 'init-db' command
    Clear the existing data and create new tables
    """

    init_db()
    click.echo("Initialized the database.")


@click.command("add-admin")
def add_admin_command():
    """
    Creates the cli 'add-admin' command
    Add admin user to the database.
    """

    add_admin()
    click.echo("Added the admin user.")


def init_app(app):
    """
    Returns the database, will create the database if
    it's not already present in the global flask object

    Keyword arguments:
    app -- the flask app
    """

    # Call the close_db function when cleaning up
    app.teardown_appcontext(close_db)

    # Add the defined cli command to the flask app
    app.cli.add_command(init_db_command)

    app.cli.add_command(add_admin_command)


def init_db():
    """
    Initialises the db using the schema file. Will
    clear the existing data and create new tables.
    """
    db = get_db()

    # resource location relative to the package
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def add_admin():
    """
    Initialises the db using the schema file. Will
    clear the existing data and create new tables.
    """
    db = get_db()

    password = "password"  # obviously a bad idea, for testing

    db.execute(
        "INSERT INTO user (username, password, email, isAdmin) VALUES (?, ?, ?, ?)",
        ("admin", generate_password_hash(password), "helenffionadams@gmail.com", True),
    )
    db.commit()


def get_db():
    """
    Returns the database, will create the database if
    it's not already present in the global flask object
    """

    if "db" not in g:
        # create a connection to the datanase
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    """
    If the connection was created, close it
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
