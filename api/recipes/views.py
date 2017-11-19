# api/recipes/views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json
from flask.views import MethodView
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import RecipeCategory, Recipe, BlacklistToken
from api.auth.views import login_token_required

recipe_blueprint = Blueprint('recipe', __name__)


class RecipeAPI(MethodView):
    """
    Recipe Resource
    """

    decorators = [login_token_required]

    @swag_from('swagger_docs/recipe_post.yaml', methods=['POST'])
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
    
    @swag_from('swagger_docs/recipes.yaml', methods=['GET'])
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
                # pagination
                limit = request.args.get('limit', 0)
                if limit:
                    limit = int(limit)
                    # offset = int(request.args.get('offset', 0))
                    recipes = Recipe.get_all_limit_offset(cat_id,
                                                        current_user.id, 
                                                        limit)
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
recipe_view = RecipeAPI.as_view('recipe_api')
singlerecipe_view = SingleRecipeAPI.as_view('singlerecipe_api')

# add rules for the API endpoints
recipe_blueprint.add_url_rule(
    '/recipe_category/<cat_id>/recipes',
    view_func=recipe_view,
    methods=['GET', 'POST']
)

recipe_blueprint.add_url_rule(
    '/recipe_category/<cat_id>/recipes/<recipe_id>',
    view_func=singlerecipe_view,
    methods=['GET', 'PUT', 'DELETE']
)
