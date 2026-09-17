from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.json.ensure_ascii = False   # чтобы кириллица не экранировалась в \uXXXX

    CORS(app)

    from .routes import bp
    app.register_blueprint(bp, url_prefix="/v2")

    return app