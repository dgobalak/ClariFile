from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object('config')
Talisman(app, content_security_policy=None)

from src import views