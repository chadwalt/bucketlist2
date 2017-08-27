"""
Initializing the database for the application
"""
import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config, ITEMS_PER_PAGE
from flasgger import Swagger
from flask_cors import CORS, cross_origin

## Import the models
from app.models import Users, Buckets, Bucketitems, BlacklistToken

# initialize sql-alchemy
db = SQLAlchemy()

config_name = os.getenv('APP_SETTINGS')

app = FlaskAPI(__name__, instance_relative_config=True)
swagger = Swagger(app) ## Adding swagger.
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app) ## Enable Cross Site Origin.
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)
