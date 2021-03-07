import os

from flask import Flask, g, redirect, url_for
from flask_babel import Babel
from config import Config

babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
    app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]

    babel.init_app(app)

    @app.route("/")
    def index():
        return redirect(url_for("main.index", lang_code=g.get("lang_code", "uk")))

    from kyivmural.main import bp as main_bp
    from kyivmural.errors import bp as errors_bp

    @main_bp.url_defaults
    @errors_bp.url_defaults
    def add_language_code(endpoint, values):
        values.setdefault("lang_code", g.get("lang_code", "uk"))

    @main_bp.url_value_preprocessor
    @errors_bp.url_value_preprocessor
    def pull_lang_code(endpoint, values):
        g.lang_code = values.pop("lang_code", "uk")

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app


@babel.localeselector
def get_locale():
    return g.get("lang_code", "uk")
