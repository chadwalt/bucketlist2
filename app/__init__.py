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

    ## This route is for registering a user.
    @app.route('/auth/register', methods=['POST'])
    def register():
        if request.method == 'POST':
            first_name = request.form['first_name']
            sur_name = request.form['sur_name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            if first_name and sur_name and username and password: ## Confirm that the required fields are provided.
                user = Users(first_name, sur_name, username, password, email)
                user.save() ## Save the user.

                return jsonify({'success': True, 'msg': 'User created successfully'})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields', 'status_code': 404})

    ## This is the route for user login.
    @app.route('/auth/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username and password:
                ## Get all the users.
                users = Users.get_all()
                
                ## Loop through to get all the users to get this username and password.
                for user in users:
                    if user.username == username and user.password == password:
                        return jsonify({'success': True, 'msg': 'User Logined successfully'})
                else:
                    return jsonify({'success': False, 'msg': 'User not found'})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'})

    ## This is the route for user login.
    @app.route('/auth/logout', methods=['POST'])
    def logout():
        if request.method == 'POST':            
            return jsonify({'success': True, 'msg': 'User logged out successfully'})

    ## This is the route for user resetting password.
    @app.route('/auth/reset-password', methods=['POST'])
    def resetPassword():
        if request.method == 'POST':            
            email = request.form['email']
            password = request.form['password']

            ## Get the user with this email
            user = Users.query.filter_by(email=email).first()

            if not user:
                abort(404) ## Raise the not found status.

            if email and password:               
                user.password = password
                user.save()
                return jsonify({'success': True, 'msg': 'User Password reset successfully'})                
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'})
    
    ## This route is for creating a bucket.
    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def buckets():
        if request.method == 'POST': ## Save bucket if the request is a post.
            name = request.form['name']
            user_id = request.form['user_id']            

            if name and user_id: ## Confirm that the required fields are provided.
                bucket = Buckets(name, user_id)
                bucket.save() ## Save the user.

                return jsonify({'success': True, 'msg': 'Bucket created successfully'})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields', 'status_code': 404})
        elif request.method == 'GET': ## Return all buckets if the requet if a GET.
            user_id = request.form['user_id']

            results = Buckets.query.filter_by(user_id=user_id)
            return jsonify(results);
            
    return app