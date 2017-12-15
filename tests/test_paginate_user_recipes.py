# tests/test_user_recipes.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestUserRecipeBlueprint(RegisterLogin):


    def test_paginate_user_recipes(self):
        """
        Test for paginate all user recipes
        """
        response = self.register_user(
            "Patrick", "Walukagga", 
            "pwalukagga@gmail.com", "telnetcmd123"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', str(response.data))
        self.assertIn('success', str(response.data))
        # registered user login
        rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
        self.assertEqual(rep_login.status_code, 200)
        self.assertIn('Successfully logged in', 
                        str(rep_login.data))
        self.assertIn('success', str(rep_login.data))
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
        recipe = Recipe(
            name="Rolex for Lunch",
            cat_id=2,
            user_id=1,
            ingredients="oil, Onions, Tomatoes",
            description="How to make breakfast rolex"            
        )
        recipe.save()
        recipe = Recipe(
            name="Rolex for Breakfast",
            cat_id=1,
            user_id=1,
            ingredients="oil, Onions, Tomatoes",
            description="How to make breakfast rolex"            
        )
        recipe.save()
        response = self.create_recipe_in_category(2, 
            "Chicken Lunch Buffe",
            "oil, Onions,Tomatoes",
            "Mix and boil",
            headers
        )
        response = self.client.get('/recipes?page=1&limit=2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Breakfast', str(response.data))
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertNotIn('Chicken Lunch Buffe', str(response.data))
        # paginate with non integer values
        response = self.client.get('/recipes?page=a&limit=b', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('limit and page query parameters should be integers', 
                      str(response.data))

if __name__ == '__main__':
    unittest.main()
        