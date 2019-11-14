from flask import session, redirect, url_for
from functools import wraps


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('logins.login'))

    return check_login
