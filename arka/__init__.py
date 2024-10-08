from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from .api import api_bp
    app.register_blueprint(api_bp)

    return app
