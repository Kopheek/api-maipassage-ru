from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flasgger import Swagger

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.json.ensure_ascii = False   # чтобы кириллица не экранировалась в \uXXXX

    CORS(app)

        # Swagger / OpenAPI
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/v2/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/v2/docs",
    }
    swagger_template = {
        "info": {
            "title": "Маёвский цитатник | API",
            "description": "API для цитат. Публичные эндпоинты доступны без авторизации.",
            "version": "2.0.0",
            "contact": {"name": "t.me/maipassage"},
        },
        "basePath": "/",
        "schemes": ["https"],
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
                "description": "Админский ключ для защищённых эндпоинтов",
            }
        },
        "definitions": {
            "Quote": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "author": {"type": "string", "example": "Альберт Эйнштейн"},
                    "subject": {"type": "string", "example": "наука"},
                    "text": {"type": "string", "example": "Воображение важнее знания."},
                },
            }
        },
    }
    Swagger(app, config=swagger_config, template=swagger_template)

    from .routes import bp
    app.register_blueprint(bp, url_prefix="/v2")

    return app