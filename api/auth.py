import os
import secrets
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    """Проверяет заголовок X-API-Key. Ключ берётся из ADMIN_API_KEY."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        expected = os.getenv("ADMIN_API_KEY")
        if not expected:
            # Если ключ не задан — не даём доступ, а не открываем всем
            return jsonify({"error": "server misconfigured: ADMIN_API_KEY is not set"}), 500

        provided = request.headers.get("X-API-Key", "")
        if not secrets.compare_digest(provided, expected):
            return jsonify({"error": "unauthorized"}), 401

        return f(*args, **kwargs)
    return wrapper