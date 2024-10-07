from flask import render_template, session
from functools import wraps


def need_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'yandex_token' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)

    return wrapper
