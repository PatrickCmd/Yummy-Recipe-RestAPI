import os

from flask import Flask

from api.config import app_config

app = Flask(__name__)

config_name = os.environ['APP_SETTINGS']
app.config.from_object(app_config[config_name])
