""" This will test the users from creation, updating, deletion. """

import unittest
import os
import json
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app.manage import app, db

class ApiTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = app
        self.client = self.app.test_client
        self.user = {'first_name': 'Timothy', 'sur_name' : 'Kyadondo', 'username': 'chadwalt', 'password': '123', 'email': 'chadwalt@outlook.com'}
        self.bucketitems = {'name': 'Climbing More', 'description': 'Touching the clouds', 'bucket_id': '1'}
        self.bucket = {'name': 'Climbing', 'user_id': '1'}
        self.headers = {'Authorization': 'this is authozized.'}
        self.form_data = {'username': 'chadwalt', 'password': '123'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketitems_creation(self):
        """ Test Bucketitems creation using the POST request. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Climbing', str(resp.data)) ## Searches for climbing in the users string.

    def test_get_all_bucketitems(self):
        """ This will test get all the bucketitems using the GET request."""

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data, ) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 201)

        resp = self.client().get('/bucketlists/1/items/', headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('Climbing', str(resp.data))

    def test_bucketitems_can_be_edited(self):
        """ Test if the bucketitems can be edited. Using the PUT request. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token)) ## Create the item.

        form_data = {'name': 'walking on the moon', 'description': 'Go by the space craft'}
        resp = self.client().put('/bucketlists/1/items/1', data = form_data, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 201)

        self.assertIn('true', str(resp.data))

    def test_bucketitems_deletion(self):
        """ Test if the bucketitems can be deleted. """

        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        res = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token)) ## Create the item.
        result = self.client().delete('/bucketlists/1/items/1', headers=dict(Authorization=token))

        self.assertEqual(resp.status_code, 201)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
