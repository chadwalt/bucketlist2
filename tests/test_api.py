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
class ApiTestCase(unittest.TestCase):
    ## Set it up.
    def setUp(self):
        ## Defining test variables and initialize the appliction.

        self.app = create_app(config_name='testing');
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

    def test_index_page_loads(self):
        """ This will test if the index page loads successfully. """
        resp = self.client().post('/')
        self.assertEqual(resp.status_code, 200) ## Check if the page successfully loads

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
        resp = self.client().post('/auth/login', data = form_data) ## Check if the user login details are valid.
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

    def test_bucket_creation(self):
        """ Test Buckets creation using the POST request. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp_bucket = self.client().post('/bucketlists/', data = self.bucket,
        headers=dict(Authorization=token)) ## Place the token in the header.

        # res = self.client().post(
        #     '/bucketlists/',
        #     HTTP_AUTHORIZATION="access_token",
        #     data=self.bucketlist)

        self.assertEqual(resp_bucket.status_code, 200)
        self.assertIn('Climbing', str(resp_bucket.data)) ## Searches for climbing.

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
        self.assertEqual(resp.status_code, 200)
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
        self.assertEqual(resp.status_code, 200)

        data = {"name": "Mountain Climbing"}
        results = self.client().put('/bucketlists/{}'.format(json_result.get('id')), data = data, headers=dict(Authorization=token))
        self.assertIn('true', str(results.data))

    def test_bucket_deletion(self):
        """ Test if the bucket can be deleted. """
        resp = self.client().post('/auth/register', data = self.user) ## Creating a user

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token)) ## Creating a bucket.
        json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(resp.status_code, 200)

        ## Then test if the user exists. should return 404
        res = self.client().delete('/bucketlists/{}'.format(json_result.get('id')), headers=dict(Authorization=token))
        self.assertEqual(res.status_code, 200)

    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     with self.app.app_context():
    #         # drop all tables
    #         db.session.remove()
    #         db.drop_all()


# """ This will test the bucketlist Items """
# class BucketitemsTestCase(unittest.TestCase):
    ## Set it up.
    # def setUp(self):
    #     ## Defining test variables and initialize the appliction.

    #     self.app = create_app(config_name='testing');
    #     self.client = self.app.test_client
    #     self.bucketitems = {'name': 'Climbing More', 'description': 'Touching the clouds', 'bucket_id': '1'}

    #     ## Binds the app to the current context.
    #     with self.app.app_context():
    #         # create all tables
    #         db.create_all()

    def test_bucketitems_creation(self):
        """ Test Bucketitems creation using the POST request. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Climbing', str(resp.data)) ## Searches for climbing in the users string.

    def test_get_all_bucketitems(self):
        """ This will test get all the bucketitems using the GET request."""

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data, ) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)

        resp = self.client().get('/bucketlists/1/items/', headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200) ## Test if the response is successfully loaded.
        self.assertIn('Climbing', str(resp.data))

    # def test_get_bucketitems_by_id(self):
    #     """ This will test if the user can be gotten by the id. """
    #     resp = self.client().post('/bucketlists/<int:id>/items/<int:item_id>', data = self.bucketitems)
    #     self.assertEqual(resp.status_code, 201)

    #     json_result = json.loads(resp.data.decode('utf-8').replace("'", "\""))
    #     result = self.client().get('/bucketitems/{}'.format(json_result['id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('climbing', str(resp.data))

    def test_bucketitems_can_be_edited(self):
        """ Test if the bucketitems can be edited. Using the PUT request. """

        resp = self.client().post('/auth/register', data = self.user)

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().post('/bucketlists/', data = self.bucket, headers=dict(Authorization=token))
        resp = self.client().post('/bucketlists/1/items/', data = self.bucketitems, headers=dict(Authorization=token)) ## Create the item.

        form_data = {'name': 'walking on the moon', 'description': 'Go by the space craft'}
        resp = self.client().put('/bucketlists/1/items/1', data = form_data, headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)

        self.assertIn('true', str(resp.data))

    def test_bucketitems_deletion(self):
        """ Test if the bucketitems can be deleted. """

        resp = self.client().post('/auth/register', data = self.user) ## Creating an account.

        resp_login = self.client().post('/auth/login', data = self.form_data) ## Login the user.
        token = json.loads(resp_login.data.decode())['auth_token'] ## Get the authentication token.

        resp = self.client().delete('/bucketlists/1/items/1', headers=dict(Authorization=token))
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
