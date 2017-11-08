# api/auth/views.py

import uuid

from flask import Blueprint, request, make_response, jsonify, json
from flask.views import MethodView

from api import bcrypt, db
from api.models import User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        """get post data"""
        data = request.get_json(force=True)
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            try:
                new_user = User(public_id=str(uuid.uuid4()), 
                                email=data['email'], 
                                password=data['password'], 
                                first_name=data['first_name'], 
                                last_name=data['last_name'])
                new_user.save()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered',                    
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occured, please try again!'
                }
                return make_response(jsonify(responseObject)), 201
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists'
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """ 
    Login User Resource
    """
    def post(self):
        # get post data
        data = request.get_json(force=True)
        try:
            # fetching user data
            user = User.query.filter_by(email=data['email']).first()
            if user and bcrypt.check_password_hash(
                user.password, data['password']
            ):
                auth_token = user.encode_auth_token(user.id, user.public_id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in',
                        'auth_token': auth_token.decode('UTF-8')
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist, please register',
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Try again',
            }
            return make_response(jsonify(responseObject)), 500

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

