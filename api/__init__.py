import os

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flasgger import Swagger

from api.config import app_config

db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

config_name = os.environ['APP_SETTINGS']
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')
# swagger configuration
app.config['SWAGGER'] = {
    'title': 'Yummy Recipes',
        'description': "This project is part of the [Andela Fellowship](https://andela.com/)\
    Bootcamp.\n\nYummy recipes app is an application that allows users to create, save and share\
    meeting the needs of keeping track of awesome food recipes. \nThis is a REST API built in python using\
    Flask.\
    \n\nThe host is 'https://https://yummy-recipe-api.herokuapp.com/'\
    \n\nThe Github repo at 'https://https://github.com/PatrickCmd/Yummy-Recipe-RestAPI",
        'basePath': '/',
        'version': '1.0.0',
        'contact': {
                    'responsibleOrganization': 'Andela',
                    'responsibleDeveloper': 'WALUKAGGA PATRICK',
                    'email': 'patrick.walukagga@andela.com',
                    'url': 'https://andela.com/',
                    },
        'schemes': [
                        'http',
                        'https'
                    ],
        'license': {
            'name': 'MIT',
            'url': 'https://github.com/PatrickCmd/Yummy-Recipe-RestAPI/blob/master/LICENSE'
        },
        'tags': [
            {
                'name': 'Recipe category',
                'description': 'A category of recipes of similar food'
            },
            {
                'name': 'Recipe',
                'description': 'A recipe of a kind of food'
            },            
            {
                'name': 'User_Authentication',
                'description': 'Register, login/authenticate user, reset password and logout user'
            },
        ],
        'specs_route': '/apidocs/'    
}

bcrypt = Bcrypt(app)
db.init_app(app)
swagger = Swagger(app)

# index route
@app.route('/')
@app.route('/index')
def index():
    """
    Redirect to the root of the swagger docs
    """
    return redirect('/apidocs/')


from api.auth.views import auth_blueprint
from api.categories.categories_views import category_blueprint
from api.categories.single_category_views import single_category_blueprint
from api.recipes.recipes_view import recipes_blueprint
from api.recipes.user_recipes_view import user_recipes_blueprint
from api.recipes.single_recipes_view import single_recipe_blueprint
from api.recipes.search_user_recipes import search_recipes_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(single_category_blueprint)
app.register_blueprint(recipes_blueprint)
app.register_blueprint(user_recipes_blueprint)
app.register_blueprint(single_recipe_blueprint)
app.register_blueprint(search_recipes_blueprint)
