from flask import render_template, session
from functools import wraps
from typing import Callable, Any


def need_login(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'yandex_token' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)

    return wrapper
