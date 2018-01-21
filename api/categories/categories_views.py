# api/categories/categories_views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json, abort
from flask.views import MethodView
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import RecipeCategory, BlacklistToken
from api.auth.decorators import login_token_required
from api.auth.helpers import (
    is_valid, category_key_missing_in_body, key_is_not_string
)

category_blueprint = Blueprint('categories', __name__)

class RecipeCategoryAPI(MethodView):
    """
    Recipe Category Resource
    """

    decorators = [login_token_required]

    @swag_from('swagger_docs/categories_post.yaml', methods=['POST'])
    def post(self, current_user):
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
                if data:
                    category_key_missing_in_body(data)
                    if key_is_not_string(data):
                        response_object = {
                            'error': 'Bad request, body field must be of type string'
                        }
                        return jsonify(response_object), 400
                    if data['name'] == "" or data["description"] == "":
                        responseObject = {
                            'status': 'fail',
                            'message': 'field names not provided'
                        }
                        return make_response(
                            jsonify(responseObject)), 200
                    if RecipeCategory.query.filter_by(
                        user_id=current_user.id, 
                        name=data['name']).first():
                        responseObject = {
                            'status': 'fail',
                            'message': 'Category already exists'
                        }
                        return make_response(
                            jsonify(responseObject)), 200
                    category = RecipeCategory(
                        name=data['name'], 
                        description=data['description'], 
                        user_id=current_user.id
                    )
                    category.save()
                    responseObject = {
                        'status': 'success',
                        'message': 'New recipe category created!'
                    }
                    return make_response(jsonify(responseObject)), 201
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'New recipe category not created!'
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
    
    @swag_from('swagger_docs/categories.yaml', methods=['GET'])
    def get(self, current_user):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                categories = RecipeCategory.query.\
                                         filter_by(user_id=\
                                         current_user.id).all()
                # pagination
                limit = request.args.get('limit', 0)
                page = request.args.get('page', 1)
                search = str(request.args.get('q', "")).lower()
                '''if limit:
                    limit = int(limit)
                    # offset = int(request.args.get('offset', 0))
                    categories = RecipeCategory.get_all_limit_offset(
                                                current_user.id, limit)'''
                if limit and page:
                    try:
                        limit = int(limit)
                        page = int(page)
                    except ValueError:
                        return make_response(jsonify({'message':
                            'limit and page query parameters should be integers'})), 400
                    # return an empty list if no recipe categories are found thus the False
                    categories = RecipeCategory.query.filter_by(user_id=\
                                         current_user.id).paginate(
                                             page, limit, False
                                        ).items
                if search:
                    categories = [category for category in categories if 
                                  search in str(category.name).lower()]
                category_list = []
                for category in categories:
                    category_data = {}
                    category_data['id'] = category.id
                    category_data['name'] = category.name
                    category_data['description'] = category.description
                    category_list.append(category_data)
                responseObject = {
                    'status': 'success',
                    'recipe categories': category_list
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
category_view = RecipeCategoryAPI.as_view('recipe_category_api')

# add Rules for API Endpoints
category_blueprint.add_url_rule(
    '/recipe_category',
    view_func=category_view,
    methods=['POST', 'GET']
)
