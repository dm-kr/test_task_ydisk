from flask import render_template, session
from functools import wraps
from typing import Callable, Any
import threading


def need_login(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'yandex_token' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)

    return wrapper


def cache(f: Callable[..., Any], time=60) -> Callable[..., Any]:
    cache: dict = {}

    @wraps(f)
    def wrapper(*args: str, **kwargs: Any) -> Any:
        key: str = '-'.join([arg for arg in args if arg])
        if key in cache:
            return cache[key]
        data: list = f(*args, **kwargs)
        cache[key] = data

        def delete_cache():
            cache.pop(key)

        timer: threading.Timer = threading.Timer(time, delete_cache)
        timer.start()

        return data

    return wrapper
