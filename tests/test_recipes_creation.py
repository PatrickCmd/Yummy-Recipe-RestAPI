# tests/test_recipes_creation.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestCreateRecipeBlueprint(RegisterLogin):


    def test_recipe_creation_in_category(self):
        """
        Test for recipe creation in category
        """
        response = self.register_user(
            "Patrick", "Walukagga", 
            "pwalukagga@gmail.com", "telnetcmd123"
        )
        # registered user login
        rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
        # valid token
        headers=dict(
            Authorization='Bearer ' + json.loads(
                rep_login.data.decode()
            )['auth_token']
        )
        category = RecipeCategory(
            name="Breakfast",
            description="How to make breakfast",
            user_id=1
        )
        category.save()
        response = self.create_category("LunchBuffe", 
                                        "How to make lunch buffe", 
                                        headers)
        response = self.create_recipe_in_category(2, 
            "Chicken Lunch Buffe",
            "oil, Onions,Tomatoes",
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('New recipe added to category', 
                       str(response.data))
        # create recipe with same name
        response = self.create_recipe_in_category(2, 
            "Chicken Lunch Buffe",
            "oil, Onions,Tomatoes",
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        self.assertEqual(response.status_code, 202)
        self.assertIn('Recipe already exists', 
                       str(response.data))
        # create recipe in category which doesnot exit
        response = self.create_recipe_in_category(3, 
            "Chicken Lunch Buffe",
            "oil, Onions,Tomatoes",
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found in database', 
                       str(response.data))
        # create recipe with empty fields
        response = self.create_recipe_in_category(2, "", "", "", "", headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('field names not provided', 
                       str(response.data))

    def test_recipe_creation_with_name_has_numbers(self):
        """
        Test for recipe creation with name has numbers
        """
        response = self.register_user(
            "Patrick", "Walukagga", 
            "pwalukagga@gmail.com", "telnetcmd123"
        )
        # registered user login
        rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
        # valid token
        headers=dict(
            Authorization='Bearer ' + json.loads(
                rep_login.data.decode()
            )['auth_token']
        )
        category = RecipeCategory(
            name="Breakfast",
            description="How to make breakfast",
            user_id=1
        )
        category.save()
        response = self.create_category("LunchBuffe", 
                                        "How to make lunch buffe", 
                                        headers)
        response = self.create_recipe_in_category(2, 
            1273839393,
            "oil, Onions,Tomatoes",
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad request, body field must be of type string', 
                       str(response.data))

if __name__ == '__main__':
    unittest.main()
