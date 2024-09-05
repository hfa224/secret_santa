"""This page serves up the admin page"""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from secret_santa.auth import login_required
from secret_santa.db import get_db
from secret_santa.emails import send_email

from secret_santa.user_page import get_user

# no url prefix parameter, so this is the default page
bp = Blueprint("admin_page", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    """
    This is the view that lets an admin add an event
    """
    is_admin = g.user["isAdmin"]

    if g.user and is_admin == 1:
        # get existing events created by the user
        admin_info = get_user(g.user["id"])
        # event_list = get_events(g.user["id"])
    else:
        admin_info = None
        # event_list = None
    return render_template(
        "admin_page/index.html", admin_info=admin_info, event_list=None
    )


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(user_id):
    """
    This is the view where the user can update their user info
    """
    user = get_user(user_id)

    if request.method == "POST":
        address = request.form["address"]
        dietary_info = request.form["dietary_info"]
        error = None

        # if not title:
        #    error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE user SET address = ?, dietary_info = ?" " WHERE id = ?",
                (address, dietary_info, id),
            )
            db.commit()
            return redirect(url_for("user_page.index"))

    return render_template("user_page/update.html", user=user)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(user_id):
    """
    Delete the user
    """
    get_user(user_id)
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("auth.logout"))


@bp.route("/<int:id>/sendinfo", methods=("POST",))
@login_required
def send_info():
    """
    Send the user's info to their email address
    """

    return redirect(url_for("auth.logout"))


def get_events():
    """
    Get event information given the user id
    """
    event_info = get_db().execute("SELECT *" " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info


def add_event():
    """
    Add an event
    """
    event_info = get_db().execute("SELECT *" " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info
