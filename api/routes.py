from flask import Blueprint, jsonify, request
from . import quotes
from .auth import require_api_key

bp = Blueprint("api", __name__)

@bp.get("/health")
def health():
    return jsonify({"status": "ok", "quotes_count": len(quotes.get_all())})

@bp.get("/quotes")
def list_quotes():
    """Список цитат с фильтрами.
    Query params: q, author, subject, limit
    """
    q = request.args.get("q")
    author = request.args.get("author")
    subject = request.args.get("subject")
    limit = int(request.args.get("limit", 50))

    results = quotes.search(query=q, author=author, subject=subject, limit=limit)
    return jsonify({"count": len(results), "results": results})

@bp.get("/quotes/<int:quote_id>")
def get_quote(quote_id):
    quote = quotes.get_by_id(quote_id)
    if not quote:
        return jsonify({"error": "quote not found"}), 404
    return jsonify(quote)

@bp.get("/quotes/random")
def random_quote():
    import random
    all_q = quotes.get_all()
    if not all_q:
        return jsonify({"error": "no quotes available"}), 404
    return jsonify(random.choice(all_q))

@bp.get("/subjects")
def list_subjects():
    return jsonify({"subjects": quotes.get_subjects()})

@bp.get("/authors")
def list_authors():
    return jsonify({"authors": quotes.get_authors()})

@bp.post("/admin/reload")
#@require_api_key
def reload_quotes():
    quotes.reload()
    return jsonify({"status": "reloaded", "count": len(quotes.get_all())})