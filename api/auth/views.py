# api/auth/views.py

import uuid
import jwt
import re

from flask import Blueprint, request, make_response, jsonify, json, abort
from flask.views import MethodView
from validate_email import validate_email
from flasgger import swag_from

from api import app, bcrypt, db
from api.models import User, BlacklistToken
from api.auth.helpers import (
    is_valid, is_valid_email, key_missing_in_body, key_is_not_string
)
from api.auth.decorators import (
    login_token_required
)
from api.auth import errors

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    
    @swag_from('swagger_docs/register.yaml', methods=['POST'])
    def post(self):
        """get post data"""
        if not request.get_json(force=True):
            abort(400)
        data = request.get_json(force=True)
        if data:
            key_missing_in_body(data)
            if key_is_not_string(data):
                response_object = {
                    'error': 'Bad request, body field must be of type string'
                }
                return jsonify(response_object), 400
            if is_valid(data['first_name']) or \
                        is_valid(data['last_name']):
                return jsonify({'message': 
                               'Name contains special characters'}),200
            if data['email'] == "" or data['password'] == "" or \
                data['first_name'] == "" or data['last_name'] == "":
                return jsonify({'message': 
                                'All fields must be filled'}), 200
            if not validate_email(is_valid_email(data['email'])):
                return jsonify({'Error': 'Invalid Email'}), 200
            if len(data['password']) < 6:
                return jsonify({'Error': 'Password is too short'}), 200
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

    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        # get post data
        data = request.get_json(force=True)
        try:
            # fetching user data
            user = User.query.filter_by(email=data['email']).first()
            if user:
                if bcrypt.check_password_hash(
                    user.password, 
                    data['password']
                ):
                    auth_token = user.encode_auth_token(user.id, 
                                                        user.public_id)
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
                            'message': 'Try again',
                        }
                        return make_response(jsonify(responseObject)), 500
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Incorrect password, try again',
                    }
                    return make_response(jsonify(responseObject)), 401
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

class PasswordResetAPI(MethodView):
    """
    Password Reset Resource
    """

    decorators = [login_token_required]
    
    @swag_from('swagger_docs/reset_password.yaml', methods=['POST'])
    def post(self, current_user):
        # get post data
        data = request.get_json(force=True)
        try:
            # fetching user data
            user = User.query.filter_by(email=data['email']).first()
            if user:
                if bcrypt.check_password_hash(
                    user.password, 
                    data['old_password']
                ):
                    user.password = user.change_password(
                        data['old_password'],
                        data['new_password']
                    )
                    user.update()
                    responseObject = {
                        'status': 'success',
                        'message': 'Password has been reset'
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Incorrect password, try again',
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Wrong email provided, please try again!',
                }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Try again',
            }
            return make_response(jsonify(responseObject)), 500



class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    decorators = [login_token_required]

    @swag_from('swagger_docs/logout.yaml', methods=['POST'])
    def post(self, current_user):
        """
        get auth token
        """
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = current_user.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'User has logged out successfully.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
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
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')
password_reset_view = PasswordResetAPI.as_view('passwordreset_api')

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

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/password_reset',
    view_func=password_reset_view,
    methods=['POST']
)
