from flask import render_template, request

from kyivmural.main import bp
from kyivmural.queries.queries import get_mural, get_all_murals, get_murals, get_artist, get_artists, get_murals_by_artist


@bp.route("/index")
def index():
    murals = get_all_murals()
    return render_template("index.html", title="KYIVMURAL", murals=murals)


@bp.route("/murals")
def murals():
    next_token = request.args.get("next_token")
    murals, next_token = get_murals(9, next_token)
    return render_template("mural/all.html", murals=murals, next_token=next_token)


@bp.route("/mural/<uuid:mural_id>/<artist_name_en>")
def mural(mural_id, artist_name_en):
    mural = get_mural(mural_id, artist_name_en)
    return render_template("mural/detail_view.html", mural=mural)


@bp.route("/artists")
def artists():
    artists = get_artists()
    return render_template("artist/all.html", artists=artists)


@bp.route("/artists/<artist_name_en>")
def artist(artist_name_en):
    artist = get_artist(artist_name_en)
    murals = get_murals_by_artist(artist_name_en)
    return render_template("artist/detail_view.html", artist=artist, murals=murals)
