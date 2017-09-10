""" This will test the bucketlist from creation, updating, deletion. """

import unittest
import os
import json
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app.manage import app, db

""" This class will test the users """
class BucketsTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = app
        self.client = self.app.test_client
        self.user = {'first_name': 'Timothy', 'sur_name' : 'Kyadondo', 'username': 'chadwalt', 'password': '123', 'email': 'chadwalt@outlook.com'}
        self.bucket = {'name': 'Climbing', 'user_id': '1'}
        self.headers = {'Authorization': 'this is authozized.'}
        self.form_data = {'username': 'chadwalt', 'password': '123'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucket_creation(self):
        """ Test Buckets creation using the POST request. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp_bucket = self.client().post('/bucketlists/', data = self.bucket,
        headers=dict(Authorization=token)) ## Place the token in the header.
        self.assertEqual(resp_bucket.status_code, 201)
        self.assertIn('Climbing', str(resp_bucket.data)) ## Searches for climbing.

        resp_bucket = self.client().post('/bucketlists/', data = {"name": "", "user_id": ""},
        headers=dict(Authorization=token)) ## Place the token in the header.
        self.assertIn("Please provide all fields", str(resp_bucket.data))
        self.assertEqual(resp_bucket.status_code, 400)


    def test_get_all_buckets(self):
        """ This will test get all the buckets using the GET request."""
        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))

        form_obj = {
            'user_id': '1',
            'page': '1',
            'rows': '20'
        }
        resp = self.client().get('/bucketlists/', query_string = form_obj, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('Climbing', str(resp.data))

    def test_get_bucket_by_id(self):
        """ This will test if the bucket can be gotten by the id. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Save a bucket.
        self.assertEqual(resp.status_code, 201)
        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))

        result = self.client().get('/bucketlists/{}'.format(json_result.get('id')), headers=dict(Authorization=token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Climbing', str(resp.data))

    def test_bucket_editing(self):
        """ Test if the bucket can be edited. Using the PUT request. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(resp.status_code, 201)

        data = {"name": "Mountain Climbing"}
        results = self.client().put('/bucketlists/{}'.format(json_result.get('id')), data = data, headers=dict(Authorization=token))
        self.assertIn('true', str(results.data))
        self.assertEqual(results.status_code, 201)

    def test_bucket_deletion(self):
        """ Test if the bucket can be deleted. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating a user

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Creating a bucket.
        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(resp.status_code, 201)

        res = self.client().delete('/bucketlists/{}'.format(json_result.get('id')), headers=dict(Authorization=token))
        self.assertEqual(res.status_code, 201)

    def test_none_exist_bucket_id(self):
        """ Test if the bucket can be deleted. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating a user

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Creating a bucket.
        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(resp.status_code, 201)

        res = self.client().put('/bucketlists/6', headers=dict(Authorization=token))
        self.assertEqual(res.status_code, 404)
        self.assertIn("Bucketlist with id 6 does not exist", str(res.data))

        res = self.client().get('/bucketlists/6', headers=dict(Authorization=token))
        self.assertEqual(res.status_code, 404)
        self.assertIn("Bucketlist with id 6 does not exist", str(res.data))

        res = self.client().delete('/bucketlists/6', headers=dict(Authorization=token))
        self.assertEqual(res.status_code, 404)
        self.assertIn("Bucketlist with id 6 does not exist", str(res.data))


    def test_duplicate_bucket(self):
        """ Test to check if the bucket already exists."""

        resp = self.client().post('/auth/register', data = self.user) ## Creating a user

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Creating a bucket.
        self.assertEqual(resp.status_code, 201)

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Creating a bucket.
        self.assertEqual(resp.status_code, 409)
        self.assertIn('Bucket Already exists', str(resp.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
