"""
This is the view that lets an admin add an event
"""
from secret_santa.db import get_db
from secret_santa.user_page import get_user
from flask import Blueprint, g, render_template

# no url prefix parameter, so this is the default page
bp = Blueprint("admin_page", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    """
    This is the view that lets an admin add an event
    """
    #db = get_db()
    is_admin = g.user["isAdmin"]

    if g.user and is_admin == 1:
        # get existing events created by the user
        admin_info = get_user(g.user["id"])
        #event_list = get_events(g.user["id"])
    else:
        admin_info = None
        #event_list = None
    return render_template("admin_page/index.html", admin_info=admin_info, event_list=None)

def get_events():
    """
    Get user information given the user id
    """
    event_info = get_db().execute("SELECT *", " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info


def add_event():
    """
    Add an event
    """
    event_info = get_db().execute("SELECT *", " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info
