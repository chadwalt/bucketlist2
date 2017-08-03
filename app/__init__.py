""" Setting up the application """

# Import flask_api
from flask_api import FlaskAPI

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

## Import the config file in the instance folder.
from instance.config import app_config

from flask import request, jsonify, abort

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    ## Import the models
    from app.models import Users, Buckets, Bucketitems 

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register/', methods=['POST'])
    def register():
        if request.method == 'POST':
            first_name = request.form['first_name']
            sur_name = request.form['sur_name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            if first_name && sur_name && username && password: ## Confirm that the required fields are provided.
                user = Users(first_name, sur_name, username, password, email)
                user.save() ## Save the user.

                return jsonify({'success': True, 'msg': 'User created successfully', 'status_code': 201})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields', 'status_code': 404})


    return app