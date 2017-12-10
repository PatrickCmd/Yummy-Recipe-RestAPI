import jwt

from flask import request, jsonify
from functools import wraps

from api import app, bcrypt, db
from api.models import User, BlacklistToken
# from api.auth.helpers import not_correct_urlrule

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

# decorator to prevent wrong endpoint url_rules
'''def correct_url_rule_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        url = request.url_rule
        if not not_correct_urlrule(url):
            message_obj = {
                "url": url, 
                "error": "Endpoint not found on this server"
            }
            return jsonify(message_obj), 404
        return f(url, *args, **kwargs)
    return decorated'''
