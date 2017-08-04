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

                results = {
                    'id': bucket.id,
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'success': True, 
                    'msg': 'Bucket created successfully'}

                return jsonify(results)
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields', 'status_code': 404})
        elif request.method == 'GET': ## Return all buckets if the requet if a GET.
            ##user_id = request.form['user_id']
            #buckets = Buckets.query.filter_by(user_id=user_id)
            buckets = Buckets.get_all()
            results = []

            for bucket in buckets:
                obj = {
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'user_id': bucket.user_id
                }

                results.append(obj)

            return jsonify(results);

    ## This route is for creating a bucket.
    @app.route('/bucketlists/<int:id>', methods=['PUT', 'GET', 'DELETE'])
    def bucketlists_id(id):
        bucket = Buckets.query.filter_by(id=id)
        if not bucket:
            abort(404) ## Raise not found error.
        
        if request.method == 'DELETE': ## Save bucket if the request is a post.
            bucket.delete()
            
            return jsonify({'success': True, 'msg': 'Bucketlist {} deleted successfully'.format(bucket.id)})
        elif request.method == 'PUT': ## Save bucket if the request is a post.
            name = str(request.data.get('name', ''))
            bucket.name  = name
            bucket.save()
            
            results = {
                    'id': bucket.id,
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'success': True, 
                    'msg': 'Bucket created successfully'}

            return jsonify(results)
        elif request.method == 'GET': ## Return all buckets if the requet if a GET.
            result = {
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'user_id': bucket.user_id
            }

            return jsonify(result);


    ## This route is for creating, updating and deleting  a bucketlist item.
    @app.route('/bucketlists/<int:id>/items/', methods=['GET', 'POST'])
    def bucketlists_items(id):            
        if request.method == 'POST': ## Add bucket items if the request is a POST.
            name = request.form['name']
            description = request.form['description']
            bucket_id = request.form['bucket_id']

            if name and bucket_id:
                bucketitem = Bucketitems(name, description, bucket_id)

                result = {
                    'id': bucketitem.id,
                    'name': bucketitem.name,
                    'description': bucketitem.description,
                    'date_created': bucketitem.date_created,
                    'bucket_id': bucketitem.bucket_id
                }

                return jsonify(result)

        elif request.method == 'GET': ## Get bueckt items if the request if a GET
            bucketitems = Bucketitems.query.filter_by(bucket_id=id)

            if not bucketitems:
                abort(404) ## Raise not found error.

            results = []

            for bucketitem in bucketitems:                                        
                obj = {
                    'id': bucketitem.id,
                    'name': bucketitem.name,
                    'description': bucketitem.description,
                    'date_created': bucketitem.date_created,
                    'bucket_id': bucketitem.bucket_id
                }
                results.append(obj)

            return jsonify(results);

    ## This route is for creating a bucket.
    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def bucketitems_id(id, item_id):
        bucketitem = Bucketitems.query.filter_by(bucket_id=id, id=item_id)
        if not bucketitem:
            abort(404) ## Raise not found error.
        
        if request.method == 'DELETE': ## Delete bucket if the request is a DELETE.
            bucketitem.delete()
            
            return jsonify({'success': True, 'msg': 'Bucketlist {} deleted successfully'.format(bucketitem.id)})
        elif request.method == 'PUT': ## Save bucket if the request is a PUT.
            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))

            bucketitem.name  = name
            bucketitem.description = description
            bucketitem.bucket_id = id
            bucketitem.save()
            
            results = {
                'id': bucketitem.id,
                'name': bucketitem.name,
                'description': bucketitem.description,
                'date_created': bucketitem.date_created,
                'success': True, 
                'msg': 'Bucket created successfully'
                }

            return jsonify(results)    
    return app