from flask import jsonify

from api import app

@app.errorhandler(400)
def bad_request(error):
    """
    Handles bad request errors
    """
    response_object = {
        'error': 'Bad request json format data or request body is empty'
    }
    return jsonify(response_object), 400