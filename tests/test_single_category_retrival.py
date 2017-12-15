# tests/test_single_category_retrival.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory
from tests.register_login import RegisterLogin


class TestRetriveSingleCategoriesBlueprint(RegisterLogin):
    
    
    def test_user_retrieve_single_recipe_category(self):
        """
        Test for user retrieves single recipe category
        """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
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
            response = self.client.get('/recipe_category/2', 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('How to make lunchfast', 
                        str(response.data))
            self.assertNotIn('How to make breakfast', 
                        str(response.data))
    
    def test_user_retrieve_single_recipe_category_id_not_number(self):
        """
        Test for user retrieves single recipe category with id not number
        """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
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
            response = self.client.get('/recipe_category/a', 
                                        headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Category ID must be an integer', 
                        str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_user_retrieves_single_recipe_category_not_in_database(self):
        """
        Test for user retrieves single recipe category which does not exist
        """
        with self.client:
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
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            
            response = self.create_category("Lunchfast", 
                                            "How to make lunchfast", 
                                            headers)
            response = self.client.get('/recipe_category/5', 
                                        headers=headers)
            self.assertEqual(response.status_code, 404)
            self.assertIn('No category found', str(response.data))
            self.assertNotIn('How to make breakfast', 
                             str(response.data))

if __name__ == '__main__':
    unittest.main()
