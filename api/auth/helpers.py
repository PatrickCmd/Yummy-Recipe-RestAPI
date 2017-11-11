# api/auth/helpers.py

# method to check for special characters and validate a name
def is_valid(name_string):
    special_character = "~!@#$%^&*()_={}|\[]<>?/,;:"
    return any(char in special_character for char in name_string)
