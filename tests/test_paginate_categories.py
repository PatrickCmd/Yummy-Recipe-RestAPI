# tests/test_categories.py

import unittest
import json
import uuid
import time

from flask import request

from api import db
from api.models import User, RecipeCategory
from tests.base import BaseTestCase
from tests.register_login import RegisterLogin


class TestPaginateCategories(RegisterLogin):
    
    def test_get_paginated_categories(self):
        """
        Test for pagination of categories
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
        # create categories
        category = RecipeCategory(
            name="Breakfast",
            description="How to make breakfast",
            user_id=1
        )
        category.save()
        category = RecipeCategory(
            name="Lunch",
            description="How to make Lunch",
            user_id=1
        )
        category.save()
        category = RecipeCategory(
            name="Dinner",
            description="How to make Dinner",
            user_id=1
        )
        category.save()
        category = RecipeCategory(
            name="Chapati Fried",
            description="How to make fried chapatis",
            user_id=1
        )
        category.save()
        category = RecipeCategory(
            name="Luwombo",
            description="How to make Luwombo",
            user_id=1
        )
        category.save()
        response = self.client.get('/recipe_category?limit=2&page=1', 
                                        headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('How to make breakfast', 
                    str(response.data))
        self.assertIn('How to make Lunch', 
                    str(response.data))
        self.assertNotIn('How to make Dinner', 
                        str(response.data))
        response = self.client.get('/recipe_category?limit=2&page=2', 
                                        headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('How to make breakfast', 
                    str(response.data))
        self.assertNotIn('How to make lunchfast', 
                    str(response.data))
        self.assertIn('How to make Dinner', 
                        str(response.data))
        response = self.client.get('/recipe_category?limit=a&page=b', 
                                        headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('limit and page query parameters should be integers', 
                    str(response.data))
        
if __name__ == '__main__':
    unittest.main()
