# tests/test_categories_retrival.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory
from tests.register_login import RegisterLogin


class TestRetriveCategoriesBlueprint(RegisterLogin):

    def test_user_retrieves_recipe_categories(self):
        """
        Test for user retrieves recipe categories
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

if __name__ == '__main__':
    unittest.main()