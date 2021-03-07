from flask import render_template

from kyivmural import app
from kyivmural.queries.queries import get_mural, get_murals


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="KYIVMURAL")


@app.route("/murals")
def murals():
    murals = get_murals()
    return render_template("mural/all.html", murals=murals)


@app.route("/mural/<uuid:mural_id>/<artist_name_en>")
def mural(mural_id, artist_name_en):
    mural = get_mural(mural_id, artist_name_en)
    return render_template("mural/detail_view.html", mural=mural)
