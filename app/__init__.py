from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app.url_map.strict_slashes = False
app.debug = True

from app import models
