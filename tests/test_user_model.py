# tests/test_user_model.py

import unittest
import uuid

from api import app, db
from api.models import User
from tests.base import BaseTestCase

class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            public_id=str(uuid.uuid4()),
            first_name = "Patrick",
            last_name = "Rickson",
            email = "patrick@andela.com",
            password = "test1234"
        )
        user.save()
        auth_token = user.encode_auth_token(user.id, user.public_id, user.email, 
                                            user.first_name, user.last_name)
        self.assertTrue(isinstance(auth_token, bytes))
    
    def test_decode_auth_token(self):
        user = User(
            public_id=str(uuid.uuid4()),
            first_name = "Patrick",
            last_name = "Rickson",
            email = "patrick@andela.com",
            password = "test1234"
        )
        user.save()
        auth_token = user.encode_auth_token(user.id, user.public_id, user.email,
                                            user.first_name, user.last_name)
        self.assertTrue(isinstance(auth_token, bytes))
        token_value = user.decode_auth_token(auth_token)
        self.assertEqual(token_value, 1)
        

if __name__ == "__main__":
    unittest.main()