import os

from flask import Flask

app = Flask(__name__)
app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]

from kyivmural import routes
