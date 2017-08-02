""" Setting up the application """
# Import flask and template operators
from flask import Flask
import os

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask_api
from flask.ext.api import FlaskAPI


# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app