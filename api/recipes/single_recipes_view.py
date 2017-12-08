# api/recipes/single_recipe_view.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json, abort
from flask.views import MethodView
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import RecipeCategory, Recipe, BlacklistToken
from api.auth.views import login_token_required

single_recipe_blueprint = Blueprint('single_recipe', __name__)


class SingleRecipeAPI(MethodView):
    """
    Single Recipe Resource
    """

    decorators = [login_token_required]

    @swag_from('swagger_docs/single_recipe.yaml', methods=['GET'])
    def get(self, current_user, cat_id, recipe_id):
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
                recipe = Recipe.query.filter_by(id=recipe_id,
                                        cat_id=cat_id, 
                                        user_id=current_user.id).\
                                        first()
                if not recipe:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Recipe not found'
                    }
                    return make_response(jsonify(responseObject)), 404
                recipe_data = {}
                recipe_data['id'] = recipe.id
                recipe_data['cat_id'] = recipe.cat_id
                recipe_data['user_id'] = recipe.user_id
                recipe_data['name'] = recipe.name
                recipe_data['ingredients'] = recipe.ingredients
                recipe_data['description'] = recipe.description
                responseObject = {
                    'status': 'sucess',
                    'recipe in category': recipe_data
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
    
    @swag_from('swagger_docs/single_recipe_put.yaml', methods=['PUT'])
    def put(self, current_user, cat_id, recipe_id):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                if not request.get_json(force=True):
                    abort(400)
                data = request.get_json(force=True)
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'Category not found in database'
                    }
                    return make_response(jsonify(responseObject)), 404
                recipe = Recipe.query.filter_by(id=recipe_id,
                                        cat_id=cat_id, 
                                        user_id=current_user.id).\
                                        first()
                if not recipe:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Recipe not found'
                    }
                    return make_response(jsonify(responseObject)), 404
                recipe.name = data['name']
                recipe.ingredients = data['ingredients']
                recipe.description = data['description']
                recipe.save()
                responseObject = {
                    'status': 'sucess',
                    'message': 'Recipe has been updated'
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
    
    @swag_from('swagger_docs/single_recipe_delete.yaml', methods=['DELETE'])
    def delete(self, current_user, cat_id, recipe_id):
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
                recipe = Recipe.query.filter_by(id=recipe_id,
                                        cat_id=cat_id, 
                                        user_id=current_user.id).\
                                        first()
                if not recipe:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Recipe not found'
                    }
                    return make_response(jsonify(responseObject)), 404
                recipe.delete()
                responseObject = {
                    'status': 'deleted',
                    'message': 'Recipe item deleted'
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
singlerecipe_view = SingleRecipeAPI.as_view('singlerecipe_api')

# add rules for the API endpoints
single_recipe_blueprint.add_url_rule(
    '/recipe_category/<cat_id>/recipes/<recipe_id>',
    view_func=singlerecipe_view,
    methods=['GET', 'PUT', 'DELETE']
)
