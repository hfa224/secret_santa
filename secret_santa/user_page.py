from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from secret_santa.auth import login_required
from secret_santa.db import get_db
from secret_santa.emails import send_email

from email.message import EmailMessage

# no url prefix parameter, so this is the default page
bp = Blueprint('user_page', __name__)

@bp.route('/')
def index():
    """
    This is the view that displays a user their info
    """
    db = get_db()
    if (g.user):
        user_info = get_user(g.user['id'])
    else:
        user_info = None
    return render_template('user_page/index.html', user_info=user_info)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    This is the view where the user can update their user info
    """
    user = get_user(id)

    if request.method == 'POST':
        address = request.form['address']
        dietary_info = request.form['dietary_info']
        error = None

        #if not title:
        #    error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET address = ?, dietary_info = ?'
                ' WHERE id = ?',
                (address, dietary_info, id)
            )
            db.commit()
            return redirect(url_for('user_page.index'))

    return render_template('user_page/update.html', user=user)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_user(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auth.logout'))

@bp.route('/<int:id>/sendinfo', methods=('POST',))
@login_required
def send_info(id):
    user = get_user(id)

    name = user['username']
    email = user['email']
    address = user['address']
    dietary_info = user['dietary_info']

    msg = EmailMessage()
    msg['Subject'] = 'This is my first Python email'
    #msg['From'] = EMAIL_ADDRESS 
    #msg['To'] = email 
    msg.set_content('Your address is ' + address + 'and your dietary info is ' + dietary_info + '.')

    message = """\
    Subject: Hi " + name  

    This message is sent from Python."""

    #send_email_defaults(email, message)
    port = current_app.config['MAIL_PORT']  # For SSL
    password = current_app.config['MAIL_PASSWORD']

    print(port)
    print(password)
    print(email)
    send_email(port, password, email, message)

    return render_template('user_page/index.html', user_info=user)

def get_user(id):
    """
    Get user information given the user id
    """
    user = get_db().execute(
        'SELECT u.id, username, email, address, dietary_info'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()

    if user is None:
        abort(404, f"User id {id} doesn't exist.")

    return user