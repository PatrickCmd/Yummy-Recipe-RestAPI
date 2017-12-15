# tests/test_single_recipe_update.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestUpdateSingleRecipeBlueprint(RegisterLogin):

    def test_update_recipe_in_category(self):
        """
        Test for editing recipe in category
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
        recipe_data = json.dumps({"name": "Chicken Lunch Buffes", 
                                  "ingredients": "oil, Onions",
                                  "description": "Mix and boil"})
        response = self.client.put('/recipe_category/2/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recipe has been updated', str(response.data))
        response = self.client.get('/recipe_category/2/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chicken Lunch Buffes', str(response.data))
        self.assertNotIn('Tomatoes', str(response.data))
        # update recipe not yet in database
        response = self.client.put('/recipe_category/2/recipes/4', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Recipe not found', str(response.data))
        # update recipe in category not yet in database
        response = self.client.put('/recipe_category/3/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found in database', 
                      str(response.data))

    def test_update_recipe_in_category_catid_recipeid_not_number(self):
        """
        Test for editing recipe in category
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
        recipe_data = json.dumps({"name": "Chicken Lunch Buffes", 
                                  "ingredients": "oil, Onions",
                                  "description": "Mix and boil"})
        response = self.client.put('/recipe_category/a/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Category ID must be an integer', str(response.data))
        self.assertIn('fail', str(response.data))
        # recipe id not number
        response = self.client.put('/recipe_category/2/recipes/a', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Recipe ID must be an integer', str(response.data))
        self.assertIn('fail', str(response.data))

    def test_update_recipe_in_category_with_one_field(self):
        """
        Test for editing recipe in category with one field
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
        recipe_data = json.dumps({"name": "Chicken Lunch Buffes"})
        response = self.client.put('/recipe_category/2/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recipe has been updated', str(response.data))
        response = self.client.get('/recipe_category/2/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chicken Lunch Buffes', str(response.data))

        recipe_data = json.dumps({"ingredients": "oil, Onions"})
        response = self.client.put('/recipe_category/2/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recipe has been updated', str(response.data))

        recipe_data = json.dumps({"description": "Mix and boils"})
        response = self.client.put('/recipe_category/2/recipes/1', 
                                    headers=headers,
                                    data=recipe_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recipe has been updated', str(response.data))

if __name__ == '__main__':
    unittest.main()
