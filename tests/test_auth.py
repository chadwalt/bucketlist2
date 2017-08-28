"""
This file will test the user authentication from login, registration, forgotPassword, logout
"""

import unittest
import os
import json
import sys
import re
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app import create_app, db

""" This class will test the users """
class AuthTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.
        self.app = create_app(config_name='testing');
        self.client = self.app.test_client
        self.user = {'first_name': 'Timothy', 'sur_name' : 'Kyadondo', 'username': 'chadwalt', 'password': '123', 'email': 'chadwalt@outlook.com'}
        self.form_data = {'username': 'chadwalt', 'password': '123'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_page_not_handler(self):
        """ This will test if the page does not exist."""

        resp = self.client().post('/auth/reg')
        self.assertEqual(resp.status_code, 404)

    def test_index_page_loads(self):
        """ This will test if the index page loads successfully. """
        resp = self.client().post('/')
        self.assertEqual(resp.status_code, 200) ## Check if the page successfully loads

    def test_valid_inputs(self):
        """ Test if first_name or sur_name can allow numbers."""

        data = {'first_name': '123kyaodndo',
            'sur_name' : '73883',
            'username': 'chadwalt',
            'password': '1234',
            'email': 'chadwalt@outlook.com'
            }

        resp = self.client().post('/auth/register', data = data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Numbers not allowed', str(resp.data))

    def test_account_create(self):
        """ Test user account registration using the POST request. """
        resp = self.client().post('/auth/register', data = self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data)) ## Searches for kyadondo in the users string.

    def test_register_empty_fields(self):
        """ Test if the required fields are field. """

        user = {'first_name': 'Timothy',
            'sur_name' : '',
            'username': 'chadwalt',
            'password': '',
            'email': 'chadwalt@outlook.com'}

        resp = self.client().post('/auth/register', data = user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data)) ## Searches for kyadondo in the users string.

    def test_user_already_exists(self):
        """ Test if the user already exists. (Registration)"""

        resp = self.client().post('/auth/register', data = self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))  ## Return false cause the account has already been created.

        resp = self.client().post('/auth/register', data = self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data))  ## Return false cause the account has already been created.

    def test_user_login(self):
        """ Test user login using the POST request. """

        resp = self.client().post('/auth/register', data = self.user) ## First register the user.
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))  ## Return false cause the account has already been created.

        form_data = {'username': 'chadwalt', 'password': '123'}
        resp = self.client().post('/auth/login', data = self.form_data) ## Check if the user login details are valid.
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data)) ## Searches for chadwalt in the users string.

    def test_user_not_exist(self):
        """ Test is the user exists.. """

        resp = self.client().post('/auth/register', data = self.user) ## First create the user.
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data)) ## Searches for kyadondo in the users string.

        form_data = {'username': 'chadtims', 'password': '123'}
        resp = self.client().post('/auth/login', data = form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data)) ## Now check if the user exists.

    def test_login_empty_fields(self):
        """ Test user login using the POST request. """

        form_data = {'username': 'chadwalt', 'password': ''}
        resp = self.client().post('/auth/login', data = form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data)) ## Searches for chadwalt in the users string.

    def test_user_logout(self):
        """ Test user logout using the POST request. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/auth/logout',headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))

    def test_user_reset_password(self):
        """ Test user reset password using the POST request. """

        resp = self.client().post('/auth/register', data = self.user) ## First create the user.
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        form_data = {'email': 'chadwalt@outlook.com', 'password': '2342'}
        resp = self.client().post('/auth/reset-password', data = form_data, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))

    def test_user_reset_password_validate_email(self):
        """ Test if the user with the specified email exists.. """

        resp = self.client().post('/auth/register', data = self.user) ## First create the user.
        self.assertEqual(resp.status_code, 200)
        self.assertIn('true', str(resp.data))

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        form_data = {'email': 'chadwalt@gmail.com', 'password': '2342'}
        resp = self.client().post('/auth/reset-password', data = form_data, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data))

    def test_user_reset_password_required_fields(self):
        """ Test if all the required fields have been specified """

        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        form_data = {'email': '', 'password': '2342'}
        resp = self.client().post('/auth/reset-password', data = form_data, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('false', str(resp.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
