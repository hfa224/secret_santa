"""This page serves up the user page endpoints"""
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from werkzeug.exceptions import abort
from flask_mail import Mail, Message

from secret_santa.auth import login_required
from secret_santa.db import get_db
from secret_santa.emails import send_email

# no url prefix parameter, so this is the default page
bp = Blueprint("user_page", __name__)


@bp.route("/")
def index():
    """
    This is the view that displays a user their info
    """
    if g.user:
        user_info = get_user(g.user["id"])
    else:
        user_info = None
    return render_template("user_page/index.html", user_info=user_info)


@bp.route("/<int:user_id>/update", methods=("GET", "POST"))
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
                "UPDATE user SET address = ?, dietary_info = ? WHERE id = ?",
                (address, dietary_info, user_id),
            )
            db.commit()
            return redirect(url_for("user_page.index"))

    return render_template("user_page/update.html", user=user)


@bp.route("/<int:user_id>/delete", methods=("POST",))
@login_required
def delete(user_id):
    """
    Deletes the user
    """
    get_user(user_id)
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("auth.logout"))


@bp.route("/<int:user_id>/sendinfo", methods=("POST",))
@login_required
def send_info(user_id):
    """
    Sends the user's info to their email address
    """
    user = get_user(user_id)

    name = user["username"]
    email = user["email"]
    address = user["address"]
    dietary_info = user["dietary_info"]

    mail = Mail(current_app)

    recipient = email
    msg = Message("Twilio SendGrid Test Email", recipients=[recipient])
    msg.body = "Hello" + name + ", your address is " + address + ", and your dietary requirements are " + dietary_info + "."
    #msg.html = (
    #    "<h1>Twilio SendGrid Test Email</h1>"
    #    "<p>Congratulations! You have sent a test email with "
    #    "<b>Twilio SendGrid</b>!</p>"
    #)
    mail.send(msg)
    flash(f"A test message was sent to {recipient}.")

    #send_email(mail, email)

    return render_template("user_page/index.html", user_info=user)


def get_user(user_id):
    """
    Get user information given the user id
    """
    user = (
        get_db()
        .execute(
            "SELECT u.id, username, email, address, dietary_info"
            " FROM user u"
            " WHERE u.id = ?",
            (user_id,),
        )
        .fetchone()
    )

    if user is None:
        abort(404, f"User id {user_id} doesn't exist.")

    return user
