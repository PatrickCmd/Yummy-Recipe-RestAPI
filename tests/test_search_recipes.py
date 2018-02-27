# tests/test_search_recipes_.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestSearchRecipeBlueprint(RegisterLogin):
    
    def test_search_user_recipes(self):
        """
        Test for searching all user recipes
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
        recipe = Recipe(
            name="Rolex for Lunch",
            cat_id=2,
            user_id=1,
            ingredients="oil, Onions, Tomatoes",
            description="How to make lunch rolex"            
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
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        response = self.client.get('/search_recipes?q=Rolex', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Breakfast', str(response.data))
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
        # get recipes in category with limit
        response = self.client.get('/search_recipes?limit=1&page=2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Breakfast', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
        # get recipes in category with limit=a&page=b
        response = self.client.get('/search_recipes?limit=a&page=b', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('limit and page query parameters should be integers', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
    
    def test_search_recipes_with_authorization_token(self):
        """
        Test for searching all user recipes
        """
        response = self.register_user(
            "Patrick", "Walukagga", 
            "pwalukagga@gmail.com", "telnetcmd123"
        )
        # registered user login
        rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
        # valid token
        headers=dict(
            Authorization='Bearer ' + '10'
        )
        response = self.client.get('/search_recipes?q=Rolex', 
                                    headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('fail', str(response.data))
        self.assertIn('Token is invalid, please login again', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
        # get recipes in category with limit

if __name__ == '__main__':
    unittest.main()
