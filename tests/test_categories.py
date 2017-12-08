# tests/test_categories.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory
from tests.register_login import RegisterLogin


class TestCategoriesBlueprint(RegisterLogin):
    

    def test_category_creation(self):
        """
        Test for category creation
        """
        with self.client:
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
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 201)
            self.assertIn('New recipe category created!', 
                        str(response.data))
            # creation with empty fields
            response = self.create_category("", "", headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('field names not provided', 
                        str(response.data))
            self.assertIn('fail', str(response.data))
            # creation when logged out
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.client.post('/auth/logout', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('User has logged out successfully.', 
                           str(response.data))
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token blacklisted. Please log in again.', 
                        str(response.data))

    
    def test_category_creation_which_exists(self):
        """
        Test for category creation which already exists
        """
        with self.client:
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
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category already exists', 
                        str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_user_retrieves_recipe_categories(self):
        """
        Test for user retrieves recipe categories
        """
        with self.client:
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
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 201)
            self.assertIn('New recipe category created!', 
                        str(response.data))
            response = self.create_category("Lunchfast", 
                                            "How to make lunchfast", 
                                            headers)
            response = self.client.get('/recipe_category', 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make lunchfast', 
                        str(response.data))
            self.assertIn('How to make breakfast', 
                        str(response.data))
    
    def test_user_retrieves_recipe_categories_with_limit(self):
        """
        Test for user retrieves recipe categories with limit pagination
        """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
            # registered user login
            rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
            
            # valid token
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            category = RecipeCategory(
                name="Morningfast",
                description="How to make morningfast",
                user_id=1
            )
            category.save()
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)

            response = self.create_category("Lunchfast", 
                                            "How to make lunchfast", 
                                            headers)
            response = self.client.get('/recipe_category?limit=2', 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make morningfast', 
                        str(response.data))
            self.assertIn('How to make breakfast', 
                        str(response.data))
            self.assertNotIn('How to make lunchfast', 
                        str(response.data))
    
    def test_user_retrieves_recipe_categories_with_search(self):
        """
        Test for user retrieves recipe categories with search
        """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
            # registered user login
            rep_login = self.login_user("pwalukagga@gmail.com", "telnetcmd123")
            # valid token
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            
            response = self.create_category("Lunchfast", 
                                            "How to make lunchfast", 
                                            headers)
            response = self.client.get('/recipe_category?q=Lunchfast', 
                                        headers=headers)
            print(str(response.data))
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make lunchfast', 
                        str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
