"""
Contains login functionality
"""
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from secret_santa.db import get_db

# create a blueprint called 'auth'
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    """
    Runs before any view is returned from a url, and
    sets the user in the global flask object
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


def login_required(view):
    """
    Decorator, runs for each view and checks that the user
    is logged in before displaying content
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Provides the log-in view
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        # save the user id in the session, to keep them logged in
        # and redirect them to index
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Provides the register view
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        # User can add other info, such as address, dietary info later
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or email {email} is already registered."
            else:
                # redirect user to log-in page after registering
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/logout")
def logout():
    """ Log out the currently logged in user"""
    session.clear()
    return redirect(url_for("index"))
