""" This will be used to run the application """

## Import the os module
import os
from app import Auth, Bucket, Bucketlist_item
from app.manage import *

## Get the application app_setting which is development.
config_name = os.getenv('APP_SETTINGS')

if __name__ == '__main__':
    app.run()
