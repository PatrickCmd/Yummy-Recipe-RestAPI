# tests/test_auth.py

import unittest
import json
import uuid

from api import db
from api.models import User
from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            response = self.client.post('auth/register', data=user, 
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
    
    def test_registration_with_already_registered_user(self):
        """ 
        Test for user registration with already registered email 
        """
        new_user = User(
            public_id=str(uuid.uuid4()), 
            email="pwalukagga@gmail.com", 
            password="telnetcmd123", 
            first_name="Patrick", 
            last_name="Walukagga"
        )
        new_user.save()
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            response = self.client.post('auth/register', data=user, 
                                        content_type='application/json')
            self.assertEqual(response.status_code, 202)
            self.assertIn('User already exists', str(response.data))
            self.assertIn('fail', str(response.data))


if __name__ == '__main__':
    unittest.main()
