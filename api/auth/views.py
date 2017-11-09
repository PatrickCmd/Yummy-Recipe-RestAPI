# api/auth/views.py

import uuid
import jwt

from flask import Blueprint, request, make_response, jsonify, json
from flask.views import MethodView
from functools import wraps

from api import app, bcrypt, db
from api.models import User, BlacklistToken

auth_blueprint = Blueprint('auth', __name__)

# decorator to prevent unauthenticated users from accessing
# the endpoints
def login_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = " "
        if auth_token:
            try:
                payload = jwt.decode(
                    auth_token, 
                    app.config['SECRET_KEY']
                )
                current_user = User.query.filter_by(
                    public_id=\
                    payload['public_id']).first()
            except:
                return jsonify({'message': 'Token is invalid',
                                'status': 'fail'}), 401
        else:
            return jsonify({'message': 'Token is missing'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


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


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    decorators = [login_token_required]

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
