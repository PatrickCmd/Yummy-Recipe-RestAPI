# tests/test_categories.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory
from tests.base import BaseTestCase


class TestCategoriesBlueprint(BaseTestCase):
    
    # helper function to register user
    def register_user(self, first_name, last_name, email, password):
        user = json.dumps({"first_name": first_name,
                                "last_name": last_name,
                                "email": email,
                                "password": password})
        return self.client.post('/auth/register', data=user, 
                                 content_type='application/json')    

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
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
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
            category_data = json.dumps({"name": "Breakfast", 
                                     "description": 
                                     "How to make breakfast"})
            response = self.client.post('/recipe_category', 
                                        headers=headers,
                                        data=category_data)
            self.assertEqual(response.status_code, 201)
            self.assertIn('New recipe category created!', 
                        str(response.data))
            # creation with empty fields
            category_data = json.dumps({"name": "", 
                                     "description": ""})
            response = self.client.post('/recipe_category', 
                                        headers=headers,
                                        data=category_data)
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
            category_data = json.dumps({"name": "Breakfast", 
                                     "description": 
                                     "How to make breakfast"})
            response = self.client.post('/recipe_category', 
                                        headers=headers,
                                        data=category_data)
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
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
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
            category_data = json.dumps({"name": "Breakfast", 
                                     "description": 
                                     "How to make breakfast"})
            response = self.client.post('/recipe_category', 
                                        headers=headers,
                                        data=category_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category already exists', 
                        str(response.data))
            self.assertIn('fail', str(response.data))
