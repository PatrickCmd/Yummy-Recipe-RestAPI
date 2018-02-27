# tests/test_single_recipe_update.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.register_login import RegisterLogin


class TestDeleteSingleRecipeBlueprint(RegisterLogin):

    def test_delete_recipe_in_category(self):
        """
        Test for deleting recipe in category
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
        response = self.client.delete('/recipe_category/2/recipes/2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Recipe item deleted', str(response.data))
        response = self.client.get('/recipe_category/2/recipes/2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Recipe not found', str(response.data))
        # delete recipe not yet in database
        response = self.client.delete('/recipe_category/2/recipes/4', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Recipe not found', str(response.data))
        # delete recipe in category not yet in database
        response = self.client.delete('/recipe_category/3/recipes/1', 
                                    headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Category not found in database', 
                      str(response.data))
    
    def test_delete_recipe_in_category_catid_recipeid_not_number(self):
        """
        Test for deleting recipe in category
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
        response = self.client.delete('/recipe_category/a/recipes/2', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Category ID must be an integer', str(response.data))
        # recipe id not number
        response = self.client.delete('/recipe_category/2/recipes/a', 
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Recipe ID must be an integer', str(response.data))

if __name__ == '__main__':
    unittest.main()
