import json
import os
from threading import Lock

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "quotes.json")

_lock = Lock()
_cache = None

def _load():
    """Загружает цитаты из файла. Кэширует результат."""
    global _cache
    with _lock:
        if _cache is not None:
            return _cache
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _cache = data.get("quotes", [])
        return _cache

def reload():
    """Сбрасывает кэш — пригодится, если файл обновили без рестарта."""
    global _cache
    with _lock:
        _cache = None

def get_all():
    return _load()

def get_by_id(quote_id):
    for q in _load():
        if q["id"] == quote_id:
            return q
    return None

def search(query=None, author=None, subject=None, limit=50):
    """Простой поиск по тексту, автору и предмету (регистронезависимый)."""
    results = _load()

    if query:
        q_lower = query.lower()
        results = [x for x in results if q_lower in x.get("text", "").lower()]

    if author:
        a_lower = author.lower()
        results = [x for x in results if a_lower in x.get("author", "").lower()]

    if subject:
        s_lower = subject.lower()
        results = [x for x in results if s_lower == x.get("subject", "").lower()]

    return results[:limit]

def get_subjects():
    """Список уникальных предметов."""
    return sorted({q.get("subject") for q in _load() if q.get("subject")})

def get_authors():
    """Список уникальных авторов."""
    return sorted({q.get("author") for q in _load() if q.get("author")})