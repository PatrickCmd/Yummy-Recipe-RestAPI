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
    
    # helper function to create recipe category
    def create_category(self, name, description, headers):
        category_data = json.dumps({"name": name, 
                                     "description": description})
        return self.client.post('/recipe_category', 
                                headers=headers,
                                data=category_data)

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
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
            
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
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
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
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make lunchfast', 
                        str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
    
    def test_user_retrieve_single_recipe_category(self):
        """
        Test for user retrieves single recipe category
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
            response = self.client.get('/recipe_category/2', 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make lunchfast', 
                        str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
    
    def test_user_retrieves_single_recipe_category_not_in_database(self):
        """
        Test for user retrieves single recipe category which does not exist
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
            response = self.client.get('/recipe_category/3', 
                                        headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn('No category found', str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
    
    def test_update_single_recipe_category(self):
        """
        Test for update single recipe category
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
            # valid token
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            category_data = json.dumps({"name": "Lunchfast", 
                                     "description": 
                                     "How to make lunchfast"})
            response = self.client.put('/recipe_category/1', 
                                        headers=headers,
                                        data=category_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Recipe Category updated', 
                        str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
            # update recipe category not in database
            response = self.client.put('/recipe_category/3', 
                                        headers=headers,
                                        data=category_data)
            self.assertEqual(response.status_code, 404)
            self.assertIn('No category found', 
                        str(response.data))
            self.assertNotIn('How to make lunchfast', 
                        str(response.data))
    
    def test_delete_single_recipe_category(self):
        """
        Test for delete single recipe category
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
            # valid token
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            cresponse = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            
            response = self.create_category("Lunchfast", 
                                            "How to make lunchfast", 
                                            headers)
            response = self.client.delete('/recipe_category/1', 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Recipe category deleted', 
                        str(response.data))
            # delete recipe category not in database
            response = self.client.delete('/recipe_category/3', 
                                        headers=headers, )
            self.assertEqual(response.status_code, 404)
            self.assertIn('No category found', 
                        str(response.data))

    def test_crud_category_when_logged_in(self):
        """
        Test for crud recipe category when not logged in
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
            # invalid token
            headers=dict(Authorization='Bearer ')
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token is missing', str(response.data))
            category_data = json.dumps({"name": "Lunchfast", 
                                     "description": 
                                     "How to make lunchfast"})
            response = self.client.put('/recipe_category/1', 
                                        headers=headers,
                                        data=category_data)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token is missing', str(response.data))
            response = self.client.delete('/recipe_category/1', 
                                        headers=headers, 
                                        data=category_data)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token is missing', str(response.data))
            # delete recipe category not in database
            response = self.client.delete('/recipe_category/3', 
                                        headers=headers, 
                                        data=category_data)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token is missing', str(response.data))
