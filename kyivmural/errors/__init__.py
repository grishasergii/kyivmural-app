"""Error routes"""

# pylint: disable=cyclic-import
from flask import Blueprint

bp = Blueprint("errors", __name__, url_prefix="/<lang_code>")


from kyivmural.errors import handlers  # noqa pylint: disable=wrong-import-position
