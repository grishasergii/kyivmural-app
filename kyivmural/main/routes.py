from flask import render_template

from kyivmural.main import bp
from kyivmural.queries.queries import get_mural, get_murals


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html", title="KYIVMURAL")


@bp.route("/murals")
def murals():
    murals = get_murals()
    return render_template("mural/all.html", murals=murals)


@bp.route("/mural/<uuid:mural_id>/<artist_name_en>")
def mural(mural_id, artist_name_en):
    mural = get_mural(mural_id, artist_name_en)
    return render_template("mural/detail_view.html", mural=mural)
