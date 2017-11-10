# api/recipes/views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json
from flask.views import MethodView

from api import app, bcrypt, db
from api.models import RecipeCategory, Recipe, BlacklistToken
from api.auth.views import login_token_required

recipe_blueprint = Blueprint('recipe', __name__)


class RecipeAPI(MethodView):
    """
    Recipe Resource
    """

    decorators = [login_token_required]

    def post(self, current_user, cat_id):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'Category not found in database'
                    }
                    return make_response(jsonify(responseObject)), 404
                data = request.get_json(force=True)
                if data:
                    if data['name'] == "" or data["description"] == "" \
                       or data['ingredients'] == "":
                        responseObject = {
                            'status': 'fail',
                            'message': 'field names not provided'
                        }
                        return make_response(
                            jsonify(responseObject)), 200
                    if Recipe.query.filter_by(name=data['name'], 
                                      user_id=current_user.id).\
                                      first():
                        responseObject = {
                            'status': 'fail',
                            'message': 'Recipe already exists'
                        }
                        return make_response(
                            jsonify(responseObject)), 200
                    recipe = Recipe(name=data['name'], 
                            cat_id=cat_id, 
                            user_id=current_user.id,
                            ingredients=data['ingredients'],
                            description=data['description'])
                    recipe.save()
                    responseObject = {
                        'status': 'success',
                        'message': 'New recipe added to category'
                    }
                    return make_response(jsonify(responseObject)), 201
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'New recipe not created!'
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                        'status': 'fail',
                        'message': resp
                    }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
    
    def get(self, current_user, cat_id):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'Category not found in database'
                    }
                    return make_response(jsonify(responseObject)), 404
                '''Returns recipes of current logged in user'''
                recipes = Recipe.query.filter_by(cat_id=cat_id, user_id=\
                                                current_user.id).all()
                recipe_list = []
                for recipe in recipes:
                    recipe_data = {}
                    recipe_data['id'] = recipe.id
                    recipe_data['cat_id'] = recipe.cat_id
                    recipe_data['user_id'] = recipe.user_id
                    recipe_data['name'] = recipe.name
                    recipe_data['ingredients'] = recipe.ingredients
                    recipe_data['description'] = recipe.description
                    recipe_list.append(recipe_data)
                responseObject = {
                    'status': 'sucess',
                    'recipes in category': recipe_list
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
    


# define the API resources
recipe_view = RecipeAPI.as_view('recipe_api')

# add rules for the API endpoints
recipe_blueprint.add_url_rule(
    '/recipe_category/<cat_id>/recipes',
    view_func=recipe_view,
    methods=['GET', 'POST']
)
