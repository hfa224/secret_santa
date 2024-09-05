from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

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
    #db = get_db()
    is_admin = g.user["isAdmin"]

    if g.user and is_admin == 1:
        # get existing events created by the user
        admin_info = get_user(g.user["id"])
        #event_list = get_events(g.user["id"])
    else:
        admin_info = None
        #event_list = None
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
                (address, dietary_info, user_id),
            )
            db.commit()
            return redirect(url_for("user_page.index"))

    return render_template("user_page/update.html", user=user)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(user_id):
    get_user(user_id)
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (user_id,))
    db.commit()
    return redirect(url_for("auth.logout"))


@bp.route("/<int:id>/sendinfo", methods=("POST",))
@login_required
def send_info(user_id):
    user = get_user(user_id)

    #name = user["username"]
    #email = user["email"]
    address = user["address"]
    dietary_info = user["dietary_info"]

    msg = EmailMessage()
    msg["Subject"] = "This is my first Python email"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(
        "Your address is " + address + "and your dietary info is " + dietary_info + "."
    )

    message = """\
    Subject: Hi " + name  

    This message is sent from Python."""

    send_email(user_email, message)

    return redirect(url_for("auth.logout"))


def get_events(user_id):
    """
    Get user information given the user id
    """
    event_info = get_db().execute("SELECT *" " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info


def add_event(user_id):
    """
    Add an event
    """
    event_info = get_db().execute("SELECT *" " FROM event_info;").fetchall()

    # if user is None:
    #    abort(404, f"User id {id} doesn't exist.")

    return event_info
