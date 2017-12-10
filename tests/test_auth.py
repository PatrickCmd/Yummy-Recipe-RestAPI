# tests/test_auth.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User
from tests.register_login import RegisterLogin


class TestAuthBlueprint(RegisterLogin):
    
    
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered', str(response.data))
            self.assertIn('success', str(response.data))
    
    def test_register_user_with_empty_body(self):
        """ Test for user registration with empty body """
        user = json.dumps({})
        response = self.client.post('/auth/register', data=user, 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request json format data or request body or field is empty', 
            str(response.data)
        )
    
    def test_register_user_with_bad_json_format_body(self):
        """ Test for user registration with bad json format body """
        user = '"first_name", "last_name", "email", "password"'
        response = self.client.post('/auth/register', data=user, 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request json format data or request body or field is empty', 
            str(response.data)
        )
    
    def test_register_user_with_missing_body_field(self):
        """ Test for user registration with missing body field """
        user = json.dumps({
            "first_name": "Patrick",
            "email": "example@email.com",
            "password": "password1234"
        })
        response = self.client.post('/auth/register', data=user, 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request json format data or request body or field is empty', 
            str(response.data)
        )
    
    def test_register_user_with_body_field_not_string(self):
        """ Test for user registration with body field not string """
        user = json.dumps({
            "first_name": 7828290,
            "last_name": 12345,
            "email": "example@email.com",
            "password": "password1234"
        })
        response = self.client.post('/auth/register', data=user, 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Bad request, body field must be of type string', 
            str(response.data)
        )
    
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
            response = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
            )
            self.assertEqual(response.status_code, 202)
            self.assertIn('User already exists', str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_user_registration_fails_with_invalid_email(self):
        '''Test register user with invalid email'''
        user = json.dumps({"first_name": "Patrick",
                           "last_name": "Walukagga",
                           "email": "pwalukaggagmail.com",
                           "password": "telnetcmd123"})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Email', str(response.data))
    
    def test_user_registration_fails_with_name_having_special_characters(self):
        '''Test register user with name having special characters'''
        user = json.dumps({"first_name": "Patrick@34&*%",
                           "last_name": "Walukagga@#$%$!^@&",
                           "email": "pwalukagga@gmail.com",
                           "password": "telnet123"})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name contains special character', 
                      str(response.data))
    
    def test_user_registration_fails_with_short_password(self):
        '''Test register user with short password'''
        user = json.dumps({"first_name": "Patrick",
                           "last_name": "Walukagga",
                           "email": "pwalukagga@gmail.com",
                           "password": "teln"})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password is too short', str(response.data))
    
    def test_user_registration_fails_with_empty_credintials(self):
        '''Test register user with empty fields'''
        user = json.dumps({"first_name": "",
                           "last_name": "",
                           "email": "",
                           "password": ""})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('All fields must be filled', str(response.data))

    def test_registered_user_login(self):
        """ Test for login of registered user """
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
            response = self.client.post(
                'auth/login', data=registered_user, 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('Successfully logged in', 
                            str(response.data))
            self.assertIn('success', str(response.data))
    
    def test_non_registered_user_login(self):
        """ Test for login of non_registered user """
        with self.client:
            non_registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123" 
            })
            response = self.client.post(
                '/auth/login', data=non_registered_user, 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)
            self.assertIn('User does not exist, please register', 
                            str(response.data))
            self.assertIn('fail', str(response.data))
    
    def test_registered_user_login_with_wrong_password(self):
        """ 
        Test for login of registered user with wrong password 
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
            rep_register = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
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
            rep_register = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
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
            time.sleep(121)
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
    
    def test_user_resets_password(self):
        """
        Test for user resets passwords
        """
        with self.client:
            rep_register = self.register_user(
                "Patrick", "Walukagga", 
                "pwalukagga@gmail.com", "telnetcmd123"
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
            reset_password_data = json.dumps({
                "email": "pwalukagga@gmail.com",
                "old_password": "telnetcmd123",
                "new_password": "telnetcmd1234"
            })
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    rep_login.data.decode()
                )['auth_token']
            )
            response = self.client.post('/auth/password_reset',
                                        data=reset_password_data, 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Password has been reset', 
                           str(response.data))
            self.assertIn('success', str(response.data))
            # reseting password with wrong email
            reset_password_data = json.dumps({
                "email": "pwalukagga123@gmail.com",
                "old_password": "telnetcmd123",
                "new_password": "telnetcmd1234"
            })
            response = self.client.post('/auth/password_reset',
                                        data=reset_password_data, 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Wrong email provided, please try again!', 
                           str(response.data))
            self.assertIn('fail', str(response.data))
            # reseting password with wrong password
            reset_password_data = json.dumps({
                "email": "pwalukagga@gmail.com",
                "old_password": "telnetcmd122",
                "new_password": "telnetcmd1234"
            })
            response = self.client.post('/auth/password_reset',
                                        data=reset_password_data, 
                                        headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Incorrect password, try again', 
                           str(response.data))
            self.assertIn('fail', str(response.data))



if __name__ == '__main__':
    unittest.main()
