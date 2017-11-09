# tests/test_auth.py

import unittest
import json
import uuid
import time

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
            response = self.client.post('/auth/register', data=user, 
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
            response = self.client.post('/auth/register', data=user, 
                                        content_type='application/json')
            self.assertEqual(response.status_code, 202)
            self.assertIn('User already exists', str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_registered_user_login(self):
        """ Test for login of registered user """
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            response = self.client.post('/auth/register', data=user, 
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            response = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Successfully logged in', 
                            str(response.data))
            self.assertIn('success', str(response.data))
    
    def test_non_registered_user_login(self):
        """ Test for login of registered user """
        with self.client:
            non_registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            response = self.client.post(
                '/auth/login', data=non_registered_user, 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist, please register', 
                            str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_registered_user_login_with_wrong_password(self):
        """ 
        Test for login of registered user with wrong password 
        """
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            response = self.client.post('/auth/register', data=user, 
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd1234" 
            })
            response = self.client.post(
                '/auth/login', data=registered_user, 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 401)
            self.assertIn('Incorrect password, try again', 
                            str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_valid_logout(self):
        """
        Test for logout before token expires
        """
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            rep_register = self.client.post(
                'auth/register', data=user, 
                content_type='application/json'
            )
            self.assertEqual(rep_register.status_code, 201)
            self.assertIn('Successfully registered', 
                          str(rep_register.data))
            self.assertIn('success', str(rep_register.data))
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                '/auth/login', data=registered_user, 
                content_type='application/json'
            )
            self.assertEqual(rep_login.status_code, 200)
            self.assertIn('Successfully logged in', 
                            str(rep_login.data))
            self.assertIn('success', str(rep_login.data))
            # valid token logout
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.client.post('/auth/logout', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('User has logged out successfully.', 
                           str(response.data))
    
    def test_invalid_logout(self):
        """
        Test for logout after token expires
        """
        with self.client:
            user = json.dumps({"first_name": "Patrick",
                                "last_name": "Walukagga",
                                "email": "pwalukagga@gmail.com",
                                "password": "telnetcmd123"})
            rep_register = self.client.post(
                'auth/register', data=user, 
                content_type='application/json'
            )
            self.assertEqual(rep_register.status_code, 201)
            self.assertIn('Successfully registered', 
                          str(rep_register.data))
            self.assertIn('success', str(rep_register.data))
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            rep_login = self.client.post(
                '/auth/login', data=registered_user, 
                content_type='application/json'
            )
            self.assertEqual(rep_login.status_code, 200)
            self.assertIn('Successfully logged in', 
                            str(rep_login.data))
            self.assertIn('success', str(rep_login.data))
            # Invalid token logout
            time.sleep(301)
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.client.post('/auth/logout', headers=headers)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Token is invalid', 
                           str(response.data))
            self.assertIn('fail', str(response.data))



if __name__ == '__main__':
    unittest.main()
