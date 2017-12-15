# tests/test_auth_reset_password.py

import unittest
import json
import uuid
import time

from api import db
from api.models import User
from tests.register_login import RegisterLogin


class TestAuthResetPasswordBlueprint(RegisterLogin):

    def test_user_resets_password(self):
        """
        Test for user resets passwords
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
