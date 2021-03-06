# api/categories/single_category_views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json, abort
from flask.views import MethodView
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import RecipeCategory, BlacklistToken
from api.auth.decorators import login_token_required

single_category_blueprint = Blueprint('single_category', __name__)


class SingleRecipeCategoryAPI(MethodView):
    """
    Single Recipe Category Resource
    """

    decorators = [login_token_required]

    @swag_from('swagger_docs/single_category.yaml', methods=['GET'])
    def get(self, current_user, cat_id):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                if not cat_id.isdigit():
                    responseObject = {
                        'error': 'Category ID must be an integer',
                        'status': "fail"
                    }
                    return make_response(jsonify(responseObject)), 400
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'No category found'
                    }
                    return make_response(jsonify(responseObject)), 404
                category_data = {}
                category_data['id'] = category.id
                category_data['name'] = category.name
                category_data['description'] = category.description
                responseObject = {
                    'status': 'success',
                    'recipe_category': category_data
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
    
    @swag_from('swagger_docs/single_category_put.yaml', methods=['PUT'])
    def put(self, current_user, cat_id):
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
                if not cat_id.isdigit():
                    responseObject = {
                        'error': 'Category ID must be an integer',
                        'status': "fail"
                    }
                    return make_response(jsonify(responseObject)), 400
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'No category found'
                    }
                    return make_response(jsonify(responseObject)), 404
                if "name" in data and "description" not in data:
                    category.name = data['name']
                elif "name" not in data and "description" in data:
                    category.description = data['description']
                else:
                    category.name = data['name']
                    category.description = data['description']
                category.save()
                responseObject = {
                    'status': 'success',
                    'message': 'Recipe Category updated'
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
    
    @swag_from('swagger_docs/single_category_delete.yaml', methods=['DELETE'])
    def delete(self, current_user, cat_id):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                if not cat_id.isdigit():
                    responseObject = {
                        'error': 'Category ID must be an integer',
                        'status': "fail"
                    }
                    return make_response(jsonify(responseObject)), 400
                category = RecipeCategory.query.filter_by(id=cat_id, 
                                                  user_id=\
                                                  current_user.id).\
                                                  first()
                if not category:
                    responseObject = {
                        'message': 'No category found'
                    }
                    return make_response(jsonify(responseObject)), 404
                category.delete()
                responseObject = {
                    'status': 'success',
                    'message': 'Recipe category deleted'
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
singlecategory_view = SingleRecipeCategoryAPI.as_view(
                        'single_recipe_category_api')

# add Rules for API Endpoints
single_category_blueprint.add_url_rule(
    '/recipe_category/<cat_id>',
    view_func=singlecategory_view,
    methods=['GET', 'PUT', 'DELETE']
)