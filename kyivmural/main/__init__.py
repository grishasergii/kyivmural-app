"""Main routes"""
from flask import Blueprint

bp = Blueprint("main", __name__, url_prefix="/<lang_code>")

from kyivmural.main import routes  # pylint: disable=wrong-import-position
