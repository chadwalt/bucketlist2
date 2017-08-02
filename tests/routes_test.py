""" Testing the routes of the application. """
#import json
import unittest
from app import app

class testApplicatinRoutes(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        # Test to see if the login page can be loaded.
    def test_login_status_code(self):
        response = self.app.get('/', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")

    # Test if the signup page can be loaded.
    def test_signup_status_code(self):
        response = self.app.get('/signup', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")
                
    # Test if the forgot password page can be loaded.
    def test_forgotPassword_status_code(self):
        response = self.app.get('/forgotPassword', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")

    # Test if dashboard loads successfully
    def test_dashboard_status_code(self):
        response = self.app.get('/dashboard', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")

    def test_bucket_status_code(self):
        response = self.app.get('/bucket', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")

    def test_bucketItem_status_code(self):
        response = self.app.get('/bucket_items', content_type="html/text")
        self.assertEqual(response.status_code, 200,
                         msg="Request was unsuccessful")

if __name__ == '__main__':
    unittest.main()
