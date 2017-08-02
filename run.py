""" This will be used to run the application."""

## Import the os module
import os

## Import the app => create_app function.
from app import create_app

## Get the application app_setting which is development.
config_name = os.getenv('APP_SETTINGS')

if __name__ == '__main__':
    app.run()