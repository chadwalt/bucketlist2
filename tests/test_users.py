""" This will test the users from creation, updating, deletion. """

import unittest
import os
import json
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app import create_app, db

class UsersTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = create_app(config_name='testing');
        self.client = self.app.test_client
        self.user = {'first_name': 'Timothy', 'sur_name' : 'Kyadondo', 'username': 'chadwalt', 'password': '123', 'email': 'chadwalt@outlook.com'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """ Test user creation using the POST request. """
        resp = self.client().post('/user', data = self.user)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Kyadondo', str(resp.data)) ## Searches for kyadondo in the users string.

if __name__ == '__main__':
    unittest.main()