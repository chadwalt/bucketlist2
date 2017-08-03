""" This will test the users from creation, updating, deletion. """

import unittest
import os
import json
from app import create_app, db

class UsersTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defien teh test variables and initialize the appliction.

        self.app = create_app(config_name='testing');
        self.client = self.app.test_client
        self.user = {'first_name': 'Timothy', 'sur_name' : 'Kyadondo', 'username': 'chadwalt', 'password': '123', 'email': 'chadwalt@outlook.com'}

        ## Binds the app to the current context.
        
