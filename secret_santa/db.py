import sqlite3

import click
from flask import current_app, g


@click.command('init-db')
def init_db_command():
    """
    Creates the cli 'init-db' command
    """
        
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

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

def init_db():
    """
    Initialises the db using the schema file. Will
    clear the existing data and create new tables.
    """
    db = get_db()

    # resource location relative to the package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_db():
    """
    Returns the database, will create the database if
    it's not already present in the global flask object
    """
        
    if 'db' not in g:
        # create a connection to the datanase
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    If the connection was created, close it
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()