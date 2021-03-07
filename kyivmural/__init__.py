import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
    app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]

    from kyivmural.main import bp as main_bp
    app.register_blueprint(main_bp)

    from kyivmural.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
