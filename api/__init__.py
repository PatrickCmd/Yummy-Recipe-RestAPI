import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from api.config import app_config

db = SQLAlchemy()

app = Flask(__name__)

config_name = os.environ['APP_SETTINGS']
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)
db.init_app(app)


from api.auth.views import auth_blueprint
from api.categories.views import category_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(category_blueprint)