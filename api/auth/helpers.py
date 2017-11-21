# api/auth/helpers.py
import re

# method to check for special characters and validate a name
def is_valid(name_string):
    special_character = "~!@#$%^&*()_={}|\[]<>?/,;:"
    return any(char in special_character for char in name_string)

# method to check whether email is valid
def is_valid_email(email):
    match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", email)
    if match:
        return email
    else:
        return 'Invalid email'
