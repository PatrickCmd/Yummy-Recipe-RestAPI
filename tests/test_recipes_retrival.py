# tests/test_recipes_retrival.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestRetriveRecipeBlueprint(RegisterLogin):

    def test_get_recipes_in_category(self):
        """
        Test for getting recipes in category
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
        self.assertEqual(response.status_code, 201)
        self.assertIn('New recipe added to category', 
                       str(response.data))
        response = self.client.get('/recipe_category/2/recipes', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertIn('Mix and boil', str(response.data))
        # get recipes in category with limit
        response = self.client.get('/recipe_category/2/recipes?limit=1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
        # get recipes in category which doesnot exit
        response = self.client.get('/recipe_category/3/recipes', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found in database', 
                       str(response.data))
    
    def test_get_user_recipes(self):
        """
        Test for getting all user recipes
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
            "Fresh chicken",
            "Mix and boil",
            headers
        )
        response = self.client.get('/recipes', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Breakfast', str(response.data))
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertIn('Mix and boil', str(response.data))
        # get recipes in category with limit
        response = self.client.get('/recipes?limit=1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))

if __name__ == '__main__':
    unittest.main()
