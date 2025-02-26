"""create and configure flask app"""

import os
from datetime import datetime

from flask import Flask, current_app, g, redirect, url_for
from flask_babel import Babel

from config import Config

babel = Babel()


def get_locale():
    """Returns app language code"""
    return g.get("lang_code", current_app.config["DEFAULT_LANG_CODE"])


def create_app(config_class=Config):
    """Create an instance of an app"""
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
    app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]
    app.config["DEFAULT_LANG_CODE"] = os.environ["DEFAULT_LANG_CODE"]

    babel.init_app(app, locale_selector=get_locale)
    app.jinja_env.globals.update(get_locale=get_locale)  # pylint: disable=no-member
    app.jinja_env.globals.update(  # pylint: disable=no-member
        GOOGLE_MAPS_API_KEY=os.environ["GOOGLE_MAPS_API_KEY"]
    )
    app.jinja_env.globals.update(  # pylint: disable=no-member
        GOOGLE_ANALYTICS_ID=os.environ["GOOGLE_ANALYTICS_ID"]
    )

    @app.route("/")
    def index():  # pylint: disable=unused-variable
        return redirect(
            url_for(
                "main.index",
                lang_code=g.get("lang_code", current_app.config["DEFAULT_LANG_CODE"]),
            )
        )

    # isort: off
    from kyivmural.errors import (  # pylint: disable=import-outside-toplevel
        bp as errors_bp,
    )

    # isort: on
    from kyivmural.main import bp as main_bp  # pylint: disable=import-outside-toplevel

    @main_bp.url_defaults
    @errors_bp.url_defaults
    def add_language_code(_, values):  # pylint: disable=unused-variable
        values.setdefault("lang_code", get_locale())

    @main_bp.url_value_preprocessor
    @errors_bp.url_value_preprocessor
    def pull_lang_code(_, values):  # pylint: disable=unused-variable
        lang_code = values.pop("lang_code", current_app.config["DEFAULT_LANG_CODE"])
        if lang_code not in current_app.config["LANGUAGES"]:
            lang_code = current_app.config["DEFAULT_LANG_CODE"]
        g.lang_code = lang_code  # pylint: disable=assigning-non-slot

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    @app.context_processor
    def inject_now():  # pylint: disable=unused-variable
        return {"now": datetime.utcnow()}

    return app
