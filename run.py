""" This will be used to run the application."""

## Import the os module
import os

## Import the app => create_app function.
from app import create_app

from app import app

if __name__ == '__main__':
    app.run()