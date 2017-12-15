# tests/test_auth_register.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User
from tests.register_login import RegisterLogin


class TestAuthRegisterBlueprint(RegisterLogin):
    
    
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
        user = json.dumps({"first_name": "Patrick@&*%",
                           "last_name": "Walukagga@#$%$!^@&",
                           "email": "pwalukagga@gmail.com",
                           "password": "telnet123"})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name contains special character', 
                      str(response.data))
    
    def test_user_registration_fails_with_name_having_numbers(self):
        '''Test register user with name having numbers'''
        user = json.dumps({"first_name": "Patrick1233647",
                           "last_name": "Walukagga364748",
                           "email": "pwalukagga@gmail.com",
                           "password": "telnet123"})
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name field can not contain numbers', 
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


if __name__ == '__main__':
    unittest.main()
