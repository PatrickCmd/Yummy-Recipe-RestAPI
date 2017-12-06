# tests/test_recipes.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory, Recipe
from tests.base import BaseTestCase


class TestSingleRecipeBlueprint(BaseTestCase):

    # helper function to register user
    def register_user(self, first_name, last_name, email, password):
        user = json.dumps({"first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password": password})
        return self.client.post('/auth/register', data=user, 
                                 content_type='application/json')
    
    #helper function to login user
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
        category_data = json.dumps({"name": name, 
                                     "description": description})
        return self.client.post('/recipe_category', 
                                headers=headers,
                                data=category_data)
    
    # helper function to create recipe in category
    def create_recipe_in_category(self, cat_id, name, ingredients, description, headers):
        recipe_data = json.dumps({"name": name, 
                                  "ingredients": ingredients,
                                  "description": description
                                })
        return self.client.post('/recipe_category/'+str(cat_id)+'/recipes', 
                                headers=headers, 
                                data=recipe_data)
    
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
