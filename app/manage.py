"""
Initializing the database for the application
"""
import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config, ITEMS_PER_PAGE

# initialize sql-alchemy
db = SQLAlchemy()

## Import the models
from app.models import Users, Buckets, Bucketitems, BlacklistToken
config_name = os.getenv('APP_SETTINGS')

app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
