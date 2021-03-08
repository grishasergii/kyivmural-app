import os

from flask import Flask, g, redirect, url_for, current_app
from flask_babel import Babel
from config import Config

babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
    app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]
    app.config["DEFAULT_LANG_CODE"] = os.environ["DEFAULT_LANG_CODE"]

    babel.init_app(app)
    app.jinja_env.globals.update(get_locale=get_locale)

    @app.route("/")
    def index():
        return redirect(url_for("main.index", lang_code=g.get("lang_code", current_app.config["DEFAULT_LANG_CODE"])))

    from kyivmural.main import bp as main_bp
    from kyivmural.errors import bp as errors_bp

    @main_bp.url_defaults
    @errors_bp.url_defaults
    def add_language_code(endpoint, values):
        values.setdefault("lang_code", get_locale())

    @main_bp.url_value_preprocessor
    @errors_bp.url_value_preprocessor
    def pull_lang_code(endpoint, values):
        lang_code = values.pop("lang_code", current_app.config["DEFAULT_LANG_CODE"])
        if lang_code not in current_app.config["LANGUAGES"]:
            lang_code = current_app.config["DEFAULT_LANG_CODE"]
        g.lang_code = lang_code

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app


@babel.localeselector
def get_locale():
    return g.get("lang_code", current_app.config["LANGUAGES"])
