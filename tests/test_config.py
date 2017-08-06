""" This will test the configuration variables and methods. """

import unittest
import os
import json
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app import create_app, db

## Import the models.
from app.models import Users

class TestUserModel(unittest.TestCase):
        
    def test_encode_auth_token(self):
        user = Users(
            first_name = 'Timothy',
            sur_name = 'Kyadondo',
            username = 'chadwalt',
            password='test',
            email='test@test.com',            
        )
        user.save()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))


    def test_decode_auth_token(self):
        user = Users(
            first_name = 'Timothy',
            sur_name = 'Kyadondo',
            username = 'chadwalt',
            password='test',
            email='test@test.com',            
        )

        user.save()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(user.decode_auth_token(auth_token) == 1)


if __name__ == '__main__':
    unittest.main()