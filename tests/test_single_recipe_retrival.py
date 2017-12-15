# tests/test_single_recipe_retrival.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestRetriveSingleRecipeBlueprint(RegisterLogin):

    
    def test_get_single_recipe_in_category(self):
        """
        Test for getting single recipe in category
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
            "Mix and boil",
            headers
        )
        response = self.client.get('/recipe_category/2/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rolex for Lunch', str(response.data))
        self.assertNotIn('Mix and boil', str(response.data))
        # get recipe not yet in database
        response = self.client.get('/recipe_category/2/recipes/4', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Recipe not found', str(response.data))
        # get recipe in category not yet in database
        response = self.client.get('/recipe_category/3/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found in database', 
                      str(response.data))

    def test_get_single_recipe_in_category_catid_not_number(self):
        """
        Test for getting single recipe in category cat_id and 
        recipe_id not number
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
            "Mix and boil",
            headers
        )
        response = self.client.get('/recipe_category/a/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Category ID must be an integer', str(response.data))
        self.assertIn('fail', str(response.data))
        # recipe id not number
        response = self.client.get('/recipe_category/2/recipes/a', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Recipe ID must be an integer', str(response.data))
        self.assertIn('fail', str(response.data))
    
    def test_recipe_crud_when_not_logged_in(self):
        """
        Test for recipe crud when not logged in
        """
        response = self.register_user(
            "Patrick", "Walukagga", 
            "pwalukagga@gmail.com", "telnetcmd123"
        )
        
        headers=dict(Authorization='Bearer ')
        category = RecipeCategory(
            name="Breakfast",
            description="How to make breakfast",
            user_id=1
        )
        category.save()
        response = self.create_category("LunchBuffe", 
                                        "How to make lunch buffe", 
                                        headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))
        recipe = Recipe(
            name="Rolex for breakfast",
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
        response = self.client.delete('/recipe_category/2/recipes/2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))
        # delete recipe not yet in database
        response = self.client.delete('/recipe_category/2/recipes/4', 
                                    headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))
        # delete recipe in category not yet in database
        response = self.client.delete('/recipe_category/3/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))

if __name__ == '__main__':
    unittest.main()