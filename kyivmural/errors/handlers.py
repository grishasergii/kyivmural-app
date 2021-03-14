"""Error routes"""
from flask import render_template

from kyivmural.errors import bp


@bp.app_errorhandler(404)
def not_found_error(_):
    """Not found error page"""
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(_):
    """Internal error page"""
    return render_template("errors/500.html"), 500
