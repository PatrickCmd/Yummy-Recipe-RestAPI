# api/categories/views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json
from flask.views import MethodView

from api import app, bcrypt, db
from api.models import RecipeCategory, BlacklistToken
from api.auth.views import login_token_required

category_blueprint = Blueprint('category', __name__)

class RecipeCategoryAPI(MethodView):
    """
    Recipe Category Resource
    """

    decorators = [login_token_required]

    def post(self, current_user):
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                data = request.get_json(force=True)
                if data:
                    if data['name'] == "" or data["description"] == "":
                        responseObject = {
                            'status': 'fail',
                            'message': 'field names not provided'
                        }
                        return make_response(
                            jsonify(responseObject)), 200
                    if RecipeCategory.query.filter_by(
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

# define the API resources
category_view = RecipeCategoryAPI.as_view('recipe_category_api')

# add Rules for API Endpoints
category_blueprint.add_url_rule(
    '/recipe_category',
    view_func=category_view,
    methods=['POST']
)