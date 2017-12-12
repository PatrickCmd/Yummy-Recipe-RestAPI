import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json, abort
from flask.views import MethodView
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import RecipeCategory, Recipe, BlacklistToken
from api.auth.views import login_token_required

user_recipes_blueprint = Blueprint('user_recipes', __name__)

@login_token_required
def user_recipes_view(current_user):
    auth_header = request.headers['Authorization']
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""
    if auth_token:
        resp = current_user.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            '''Returns recipes of current logged in user'''
            recipes = Recipe.query.filter_by(user_id=current_user.id).all()
            # pagination
            limit = request.args.get('limit', 0)
            page = request.args.get('page', 1)
            if limit and page:
                    try:
                        limit = int(limit)
                        page = int(page)
                    except ValueError:
                        return make_response(jsonify({'message':
                            'limit and page query parameters should be integers'})), 400
                    # return an empty list if no recipe categories are found thus the False
                    recipes = Recipe.query.filter_by(user_id=\
                                         current_user.id).paginate(
                                             page, limit, False
                                        ).items
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

# add rules for the API endpoints /recipe_category/recipes or /recipe_category/recipes?page=<int: page>&limit=<int: limit>
user_recipes_blueprint.add_url_rule(
    '/recipe_category/recipes',
    view_func=user_recipes_view,
    methods=['GET']
)