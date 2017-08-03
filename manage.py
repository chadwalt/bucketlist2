""" This will manage the migrations of the database. """

import os
from flask_script import Manager ## manages a set of commands.
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app # Import the database and the create app method.
from app import models ## Import the models

app = create_app(config_name = os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()