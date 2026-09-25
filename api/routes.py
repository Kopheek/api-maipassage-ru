from flask import Blueprint, jsonify, request
from . import quotes
from .auth import require_api_key

bp = Blueprint("api", __name__)

# == for MAI.STEN == #
@bp.get("/health")
def health():
    """Проверка состояния API
    ---
    tags:
      - система
    responses:
      200:
        description: API работает
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            version:
              type: string
              example: 2.1.0
            quotes_count:
              type: integer
              example: 3
    """
    return jsonify({"status": "ok", "version": "2.1.1", "quotes_count": len(quotes.get_all())})


@bp.get("/quotes")
def list_quotes():
    """Список цитат с фильтрами
    ---
    tags:
      - цитаты
      - mai.sten
    parameters:
      - in: query
        name: q
        type: string
        required: false
        description: Поиск по тексту цитаты (регистронезависимый)
      - in: query
        name: author
        type: string
        required: false
        description: Фильтр по автору (подстрока)
      - in: query
        name: subject
        type: string
        required: false
        description: Точное совпадение по предмету
      - in: query
        name: limit
        type: integer
        required: false
        default: 50
        description: Максимум результатов
    responses:
      200:
        description: Список цитат
        schema:
          type: object
          properties:
            count:
              type: integer
            results:
              type: array
              items:
                $ref: '#/definitions/Quote'
    """
    q = request.args.get("q")
    author = request.args.get("author")
    subject = request.args.get("subject")
    limit = int(request.args.get("limit", 50))
    results = quotes.search(query=q, author=author, subject=subject, limit=limit)
    return jsonify({"count": len(results), "results": results})


@bp.get("/quotes/<int:quote_id>")
def get_quote(quote_id):
    """Одна цитата по ID
    ---
    tags:
      - цитаты
      - mai.sten
    parameters:
      - in: path
        name: quote_id
        type: integer
        required: true
    responses:
      200:
        description: Цитата
        schema:
          $ref: '#/definitions/Quote'
      404:
        description: Цитата не найдена
    """
    quote = quotes.get_by_id(quote_id)
    if not quote:
        return jsonify({"error": "quote not found"}), 404
    return jsonify(quote)


@bp.get("/quotes/random")
def random_quote():
    """Случайная цитата
    ---
    tags:
      - цитаты
      - mai.sten
    responses:
      200:
        description: Случайная цитата
        schema:
          $ref: '#/definitions/Quote'
      404:
        description: Цитат нет
    """
    import random
    all_q = quotes.get_all()
    if not all_q:
        return jsonify({"error": "no quotes available"}), 404
    return jsonify(random.choice(all_q))


@bp.get("/subjects")
def list_subjects():
    """Список предметов
    ---
    tags:
      - данные
      - mai.sten
    responses:
      200:
        description: Уникальные предметы
        schema:
          type: object
          properties:
            subjects:
              type: array
              items:
                type: string
    """
    return jsonify({"subjects": quotes.get_subjects()})


@bp.get("/authors")
def list_authors():
    """Список авторов
    ---
    tags:
      - данные
      - mai.sten
    responses:
      200:
        description: Уникальные авторы
        schema:
          type: object
          properties:
            authors:
              type: array
              items:
                type: string
    """
    return jsonify({"authors": quotes.get_authors()})


@bp.post("/admin/reload")
#@require_api_key
def reload_quotes():
    """Перечитать файл с цитатами (только для админа)
    ---
    tags:
      - админ
      - mai.sten
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Файл перечитан
        schema:
          type: object
          properties:
            status:
              type: string
              example: reloaded
            count:
              type: integer
      401:
        description: Неверный или отсутствующий API-ключ
    """
    quotes.reload()
    return jsonify({"status": "reloaded", "count": len(quotes.get_all())})