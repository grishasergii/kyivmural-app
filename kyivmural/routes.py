from kyivmural import app
from flask import render_template
from kyivmural.queries.queries import get_murals


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="KYIVMURAL")


@app.route("/murals")
def murals():
    murals = get_murals()
    return render_template("mural/all.html", murals=murals)
