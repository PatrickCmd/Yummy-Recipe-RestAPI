# tests/test_categories_creation.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User, RecipeCategory
from tests.register_login import RegisterLogin


class TestCreateCategoriesBlueprint(RegisterLogin):
    

    def test_category_creation(self):
        """
        Test for category creation
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
            response = self.create_category("Breakfast", 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Category already exists', 
                        str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_category_creation_with_name_having_numbers(self):
        """
        Test for category creation with name having numbers
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
            response = self.create_category(12344575, 
                                            "How to make breakfast", 
                                            headers)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Bad request, body field must be of type string', 
                        str(response.data))

if __name__ == '__main__':
    unittest.main()
