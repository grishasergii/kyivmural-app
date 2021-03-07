import os

from flask import Flask

app = Flask(__name__)
app.config["KYIVMURAL_API_ENDPOINT"] = os.environ["KYIVMURAL_API_ENDPOINT"]
app.config["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]

# import here as described in as described in
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
from kyivmural import routes  # pylint: disable=wrong-import-position
