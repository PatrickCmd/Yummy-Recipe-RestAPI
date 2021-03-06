# tests/test_auth_login.py

import unittest
import json
import time

from tests.register_login import RegisterLogin


class TestAuthLoginBlueprint(RegisterLogin):

    def test_registered_user_login(self):
        """ Test for login of registered user """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga",
                "pwalukagga@gmail.com", "telnetcmd123"
            )
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

    def test_registered_user_login_email_as_number(self):
        """ Test for login of email as number """
        with self.client:
            response = self.register_user(
                "Patrick", "Walukagga",
                "pwalukagga@gmail.com", "telnetcmd123"
            )
            # registered user login
            registered_user = json.dumps({
                "email": 1233445677,
                "password": "telnetcmd123"
            })
            response = self.client.post(
                'auth/login', data=registered_user,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn('Bad request, body field must be of type string',
                          str(response.data))

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
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123"
            })
            rep_login = self.client.post(
                '/auth/login', data=registered_user,
                content_type='application/json'
            )
            # valid token logout
            headers = dict(
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
            # registered user login
            registered_user = json.dumps({
                "email": "pwalukagga@gmail.com",
                "password": "telnetcmd123"
            })
            rep_login = self.client.post(
                '/auth/login', data=registered_user,
                content_type='application/json'
            )
            # Invalid token logout
            time.sleep(61)
            headers = dict(
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
