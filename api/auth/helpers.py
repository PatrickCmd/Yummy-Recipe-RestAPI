# api/auth/helpers.py
import re

from flask import abort, jsonify

# method to check for special characters and validate a name
def is_valid(name_string):
    special_character = "~!@#$%^&*()_={}|\[]<>?/,;:"
    return any(char in special_character for char in name_string)

# method to check whether email is valid
def is_valid_email(email):
    match=re.search(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)",
        email
    )
    if match:
        return email
    else:
        return 'Invalid email'

# method to check whether key is missing in request
def key_missing_in_body(data):
    # check if key is present in data
    keys = ('first_name', 'last_name', 'email', 'password')
    for key in keys:
        if key not in data:
            abort(400)

def key_is_not_string(data):
    "check if key is string"
    for key in data:
        if not isinstance(data[key], str):
            return True
