from flask import Blueprint

bp = Blueprint("errors", __name__)


from kyivmural.errors import handlers  # pylint: disable=wrong-import-position
