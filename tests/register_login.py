import json

from tests.base import BaseTestCase


class RegisterLogin(BaseTestCase):
    # helper function to register user
    def register_user(self, first_name, last_name, email, password):
        user = json.dumps({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password})
        return self.client.post('/auth/register', data=user,
                                content_type='application/json')

    # helper function to login user
    def login_user(self, email, password):
        registered_user = json.dumps({
            "email": email,
            "password": password
        })
        return self.client.post(
            'auth/login', data=registered_user,
            content_type='application/json'
        )

    # helper function to create recipe category
    def create_category(self, name, description, headers):
        category_data = json.dumps({
            "name": name, "description": description})
        return self.client.post('/recipe_category',
                                headers=headers,
                                data=category_data)

    # helper function to create recipe in category
    def create_recipe_in_category(self,
                                  cat_id, name, ingredients,
                                  description, directions, headers):
        recipe_data = json.dumps({"name": name,
                                  "ingredients": ingredients,
                                  "description": description,
                                  "directions": directions})
        return self.client.post('/recipe_category/'+str(cat_id)+'/recipes',
                                headers=headers,
                                data=recipe_data)
