import json
import os
import tempfile
from threading import Lock
from datetime import datetime, timezone

STATS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "stats.json"
)

_lock = Lock()

def _empty():
    return {"total": 0, "endpoints": {}, "first_seen": None, "last_seen": None}

def _load():
    if not os.path.exists(STATS_FILE):
        return _empty()
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("total", 0)
        data.setdefault("endpoints", {})
        data.setdefault("first_seen", None)
        data.setdefault("last_seen", None)
        return data
    except (json.JSONDecodeError, OSError):
        return _empty()

def _save(data):
    dir_ = os.path.dirname(STATS_FILE)
    os.makedirs(dir_, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".stats-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, STATS_FILE)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

def track(endpoint):
    now = datetime.now(timezone.utc).isoformat()
    with _lock:
        data = _load()
        data["total"] += 1
        data["endpoints"][endpoint] = data["endpoints"].get(endpoint, 0) + 1
        if data["first_seen"] is None:
            data["first_seen"] = now
        data["last_seen"] = now
        _save(data)

def get_stats():
    with _lock:
        return _load()

def reset_stats():
    with _lock:
        _save(_empty())