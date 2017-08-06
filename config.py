""" Define configurations for the application. """

# Define the application directory
import os

# Statement for enabling the development environment
DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "hs@kdkDke3%@dkl-/"

# Secret key for signing cookies
SECRET_KEY = "@ksd-??2dd()1`f3323"
