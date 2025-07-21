from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    from .blueprints.api.routes import api_bp
    from .blueprints.main.routes import main_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)

    return app