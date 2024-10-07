from flask import render_template, session
from functools import wraps
from typing import Callable, Dict, List, Any
import threading


def need_login(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор, требующий авторизацию через Яндекс для работы функции
    """
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'yandex_token' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)

    return wrapper


def cache(time: int = 60) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор, кеширующий результат выполнения функции на указанное количество времени

    time - время кеширования
    """
    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        cache: Dict[str, Any] = {}

        @wraps(f)
        def wrapper(*args: str, **kwargs: Any) -> Any:
            key: str = '-'.join([arg for arg in args if arg])
            if key in cache:
                return cache[key]
            data: List[Any] = f(*args, **kwargs)
            cache[key] = data

            def delete_cache():
                cache.pop(key, None)

            timer: threading.Timer = threading.Timer(time, delete_cache)
            timer.start()

            return data

        return wrapper

    return decorator
