import os

from flask import Flask, request, current_app
from flask_babel import Babel
from config import Config

babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
    app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]

    babel.init_app(app)

    from kyivmural.main import bp as main_bp
    app.register_blueprint(main_bp)

    from kyivmural.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app


@babel.localeselector
def get_locale():
    return "en"
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
