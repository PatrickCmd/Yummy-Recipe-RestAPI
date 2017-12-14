# api/auth/helpers.py
import re

from flask import abort, jsonify

from api import app

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

# check if field contains number
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#check if names contain numbers
def name_has_numbers(data):
    keys = ('first_name', 'last_name')
    for key in keys:
        if hasNumbers(data[key]):
            return True

# string string to remove white spaces
def strip_clean(string):
    return string.strip()

# method to check whether key is missing in request
def key_missing_in_body(data):
    # check if key is present in data
    keys = ('first_name', 'last_name', 'email', 'password')
    for key in keys:
        if key not in data:
            abort(400)

def login_key_missing_in_body(data):
    # check if key is present in data
    keys = ('email', 'password')
    for key in keys:
        if key not in data:
            abort(400)

def category_key_missing_in_body(data):
    # check if key is present in data
    keys = ('name', 'description')
    for key in keys:
        if key not in data:
            abort(400)

def recipe_key_missing_in_body(data):
    # check if key is present in data
    keys = ('name', 'ingredients', 'description')
    for key in keys:
        if key not in data:
            abort(400)

def key_is_not_string(data):
    "check if key is string"
    for key in data:
        if not isinstance(data[key], str):
            return True


# check if endpoint url_rule is correct
'''def not_correct_urlrule(url):
    rules = app.url_map.iter_rules()
    rules = list(rules)
    rule_list = []
    for rule in rules:
        rule_list.append(str(rule))
    if url not in rule_list:
        return url'''
