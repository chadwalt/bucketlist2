""" This will manage the migrations of the database. """

import os
from flask_script import Manager ## manages a set of commands.
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app # Import the database and the create app method.
from app import models ## Import the models