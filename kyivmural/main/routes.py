"""Describes main routes"""

import random

from flask import render_template, request

from kyivmural.main import bp
from kyivmural.queries.queries import (
    get_all_murals,
    get_artist,
    get_artists,
    get_mural,
    get_murals,
    get_murals_by_artist,
)


@bp.route("/index")
def index():
    """Landing page"""
    _murals = get_all_murals()
    random_murals = random.choices(_murals, k=4)
    murals_count = len(_murals)
    _artists = set()
    for _mural in _murals:
        _artists.add(_mural["artist_name_en"])
    _artists.discard("unknown")
    artists_count = len(_artists)
    return render_template(
        "index.html",
        title="KYIVMURAL",
        murals=_murals,
        random_murals=random_murals,
        murals_count=murals_count,
        artists_count=artists_count,
    )


@bp.route("/murals")
def murals():
    """Murals page"""
    next_token = request.args.get("next_token")
    _murals, next_token = get_murals(9, next_token)
    return render_template("mural/all.html", murals=_murals, next_token=next_token)


@bp.route("/mural/<uuid:mural_id>/<artist_name_en>")
def mural(mural_id, artist_name_en):
    """Mural page"""
    _mural = get_mural(mural_id, artist_name_en)
    return render_template("mural/detail_view.html", mural=_mural)


@bp.route("/artists")
def artists():
    """Artists page"""
    _artists = get_artists()
    return render_template("artist/all.html", artists=_artists)


@bp.route("/artists/<artist_name_en>")
def artist(artist_name_en):
    """Artist page"""
    _artist = get_artist(artist_name_en)
    _murals = get_murals_by_artist(artist_name_en)
    return render_template("artist/detail_view.html", artist=_artist, murals=_murals)


@bp.route("/about")
def about():
    """About page"""
    return render_template("about.html")


@bp.route("/support-ukraine")
def support_ukraine():
    """About page"""
    return render_template("support-ukraine.html")
