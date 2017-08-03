""" This will test the users from creation, updating, deletion. """

import unittest
import os
import json
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

## Import the app from the app folder.
from app import create_app, db

""" This class will test the users """
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

    def test_get_all_users(self):
        """ This will test get all the users using the GET request."""
        resp = self.client().post('/user', data = self.user)
        self.assertEqual(resp.status_code, 201)

        resp = self.client().get('/users')
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('kyadondo', str(resp.data))

    def test_get_user_by_id(self):
        """ This will test if the user can be gotten by the id. """
        resp = self.client().post('/user', data = self.user)
        self.assertEqual(resp.status_code, 201)

        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/users/{}'.format(json_result['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('kyadondo', str(resp.data))

    def test_user_can_be_edited(self):
        """ Test if the user can be edited. Using the PUT request. """

        resp = self.client().post('/users/', self.user)
        self.assertEqual(resp.status_code, 201)

        data = {"first_name": "Waltor"}
        update = self.client().put('/users/1', data)
        results = self.client().get('/users/1')
        self.assertIn('Waltor', str(results.data))

    def test_user_deletion(self):
        """ Test if the user can be deleted. """
        resp = self.client().post('/users/', self.user)
        self.assertEqual(resp.status_code, 201)

        result = self.client().delete('/users/1')
        self.assertEqual(result.status_code, 200)

        ## Then test if the user exists. should return 404
        res = self.client().get('/users/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

""" This will test the bucketlist """
class BucketTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = create_app(config_name='testing');
        self.client = self.app.test_client
        self.bucket = {'name': 'Climbing', 'user_id': '1'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucket_creation(self):
        """ Test Buckets creation using the POST request. """
        resp = self.client().post('/buckets', data = self.bucket)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Climbing', str(resp.data)) ## Searches for kyadondo in the users string.

    def test_get_all_buckets(self):
        """ This will test get all the users using the GET request."""
        resp = self.client().post('/buckets', data = self.bucket)
        self.assertEqual(resp.status_code, 201)

        resp = self.client().get('/buckets')
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('Climbing', str(resp.data))

    def test_get_bucket_by_id(self):
        """ This will test if the user can be gotten by the id. """
        resp = self.client().post('/buckets', data = self.bucket)
        self.assertEqual(resp.status_code, 201)

        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/buckets/{}'.format(json_result['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('climbing', str(resp.data))

    def test_bucket_can_be_edited(self):
        """ Test if the bucket can be edited. Using the PUT request. """

        resp = self.client().post('/buckets/', self.bucket)
        self.assertEqual(resp.status_code, 201)

        data = {"name": "Mountain Climbing"}
        update = self.client().put('/buckets/1', data)
        results = self.client().get('/buckets/1')
        self.assertIn('Waltor', str(results.data))

    def test_bucket_deletion(self):
        """ Test if the bucket can be deleted. """
        resp = self.client().post('/buckets/', self.bucket)
        self.assertEqual(resp.status_code, 201)

        result = self.client().delete('/buckets/1')
        self.assertEqual(result.status_code, 200)

        ## Then test if the user exists. should return 404
        res = self.client().get('/buckets/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


""" This will test the bucketlist Items """
class BucketitemsTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = create_app(config_name='testing');
        self.client = self.app.test_client
        self.bucketitems = {'name': 'Climbing', 'user_id': '1'}

        ## Binds the app to the current context.
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_bucketitems_creation(self):
        """ Test Bucketitemsitems creation using the POST request. """
        resp = self.client().post('/bucketitems', data = self.bucketitems)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Climbing', str(resp.data)) ## Searches for kyadondo in the users string.

    def test_get_all_bucketitems(self):
        """ This will test get all the users using the GET request."""
        resp = self.client().post('/bucketitems', data = self.bucketitems)
        self.assertEqual(resp.status_code, 201)

        resp = self.client().get('/bucketitems')
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('Climbing', str(resp.data))

    def test_get_bucketitems_by_id(self):
        """ This will test if the user can be gotten by the id. """
        resp = self.client().post('/bucketitems', data = self.bucketitems)
        self.assertEqual(resp.status_code, 201)

        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/bucketitems/{}'.format(json_result['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('climbing', str(resp.data))

    def test_bucketitems_can_be_edited(self):
        """ Test if the bucketitems can be edited. Using the PUT request. """

        resp = self.client().post('/bucketitems/', self.bucketitems)
        self.assertEqual(resp.status_code, 201)

        data = {"name": "Mountain Climbing"}
        update = self.client().put('/bucketitems/1', data)
        results = self.client().get('/bucketitems/1')
        self.assertIn('Waltor', str(results.data))

    def test_bucketitems_deletion(self):
        """ Test if the bucketitems can be deleted. """
        resp = self.client().post('/bucketitems/', self.bucketitems)
        self.assertEqual(resp.status_code, 201)

        result = self.client().delete('/bucketitems/1')
        self.assertEqual(result.status_code, 200)

        ## Then test if the user exists. should return 404
        res = self.client().get('/bucketitems/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()