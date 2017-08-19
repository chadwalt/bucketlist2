""" Setting up the application """

# Import flask_api
from flask_api import FlaskAPI

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

## Import the config file in the instance folder.
from instance.config import app_config, ITEMS_PER_PAGE

from flask import request, jsonify, abort,render_template

from flask_bcrypt import Bcrypt ## Import the encryption module for flask.

## Import flasgger for API documentation.
from flasgger import Swagger

## Importing flask_cors to enable cross_origin.
from flask_cors import CORS, cross_origin

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    ## Import the models
    from app.models import Users, Buckets, Bucketitems, BlacklistToken

    app = FlaskAPI(__name__, instance_relative_config=True)
    swagger = Swagger(app) ## Adding swagger.
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    CORS(app) ## Enable Cross Site Origin.
    app.config['CORS_HEADERS'] = 'Content-Type'

    @app.route('/', methods=['POST', 'GET'])
    def index():
        """ Home page (Documentation Page.)
        This page has the Documentation for the API... Using the flassger documentation
        """
        return render_template("index.html")

    ## This route is for registering a user.
    @app.route('/auth/register', methods=['POST'])
    def register():
        """ Registering a user.
        Please provide all the required fields.
        ---
        tags:
         - User Account
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: first_name
            in: formData
            type: string
            description: First Name E.g Timothy
            required: true
         -  name: sur_name
            in: formData
            type: string
            description: SurName E.g Kyadondo
            required: true
         -  name: username
            in: formData
            type: string
            description: Username E.g chadalt
            required: true
         -  name: password
            in: formData
            type: string
            required: true
         -  name: email
            in: formData
            type: string
            description: E.g example@example.com
            required: false
        responses:
            200:
                description: User has been created successfully
        """
        if request.method == 'POST':
            first_name = request.form['first_name']
            sur_name = request.form['sur_name']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            if first_name and sur_name and username and password: ## Confirm that the required fields are provided.
                ## Check if the user already exists.
                user = Users.query.filter_by(username=username).first();
                if not user:
                    user = Users(first_name, sur_name, username, password, email)
                    user.save() ## Save the user.

                    response_obj = {
                        'success': True,
                        'msg': 'User created successfully'
                    }

                    return jsonify(response_obj)
                else:
                    return jsonify({'success': False, 'msg': 'User already exists'})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields', 'status_code': 404})

    ## This is the route for user login.
    @app.route('/auth/login', methods=['POST'])
    @cross_origin()
    def login():
        """ Logining a user.
        Please provide all the required fields.
        ---
        tags:
         - User Account
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: username
            in: formData
            type: string
            description: Username E.g chadalt
            required: true
         -  name: password
            in: formData
            type: string
            required: true
        responses:
            200:
                description: User logined successfully
        """
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username and password: ## Check if the username and password have been specified.
                ## Get all the user.
                user = Users.query.filter_by(username=username).first();

                #if user and user.password == password:
                ##if user.valid_password(password):
                if user and user.valid_password(password):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        response_obj = {
                            'success': True,
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token
                        }

                        return jsonify(response_obj)
                else:
                   response_obj = {
                            'success': False,
                            'message': 'User does not exist.'
                        }
                   return jsonify(response_obj)
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'})

    ## This is the route for user login.
    @app.route('/auth/logout', methods=['POST'])
    def logout():
        """ logging out a user.
        Please provide all the required fields.
        ---
        tags:
         - User Account
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
        responses:
            200:
                description: User has been logged out successfully
        """

        # get auth token
        auth_header = request.headers['Authorization']
        if auth_header:
            auth_token = auth_header
        else:
            auth_token = ''
        if auth_token:
            resp = Users.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    blacklist_token.save()

                    response_obj = {
                        'success': True,
                        'msg': 'Successfully logged out.'
                    }
                    return jsonify(response_obj)
                except Exception as e:
                    response_obj = {
                        'success': False,
                        'msg': 'Failed to logout.'
                    }
                    return jsonify(response_obj)
            else:
                response_obj = {
                    'success': False,
                    'msg': resp
                }
                return jsonify(response_obj)
        else:
            response_obj = {
                'success': False,
                'msg': 'Provide a valid auth token.'
            }
            return jsonify(response_obj)

    ## This is the route for user resetting password.
    @app.route('/auth/reset-password', methods=['POST'])
    def resetPassword():
        """ Resetting a user password.
        Please provide all the required fields.
        ---
        tags:
         - User Account
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: email
            in: formData
            type: string
            description: E.g example@example.com
            required: true
         -  name: password
            in: formData
            type: string
            required: true
        responses:
            200:
                description: User password has been reset successfully
        """
        if request.method == 'POST':
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            email = request.form['email']
            password = request.form['password']

            if email and password:
                ## Get the user with this email
                user = Users.query.filter_by(email=email).first()

                if not user:
                    #abort(404) ## Raise the not found status.
                    return jsonify({'success': False, 'msg': 'User with the specified email does not exist.'})

                #user.password = password
                user.password = Bcrypt().generate_password_hash(password).decode()
                user.save()
                return jsonify({'success': True, 'msg': 'User Password reset successfully'})
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'})

    ## This route is for creating a bucket.
    @app.route('/bucketlists/', methods=['POST'])
    def add_buckets():
        """ Add Buckets.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: name
            in: formData
            type: string
            description: E.g Climbing the Mountain
            required: true
        responses:
            200:
                description: Bucket added successfully
        """
        if request.method == 'POST': ## Save bucket if the request is a post.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            name = request.form['name']

            # Check if the bucket exists.
            bucket_exists = Buckets.query.filter_by(name=name).first()
            if bucket_exists:
                return jsonify({'success': False, 'msg': 'Bucket Already exists'})

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

    ## This route is for getting all buckets.
    @app.route('/bucketlists/', methods=['GET'])
    def get_buckets():
        """ Get all Buckets.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: q
            in: formData
            type: string
            required: false
         -  name: page
            in: formData
            type: integer
            required: false
         -  name: rows
            in: formData
            type: integer
            required: false
        responses:
            200:
                description: All buckets.
        """
        if request.method == 'GET': ## Return all buckets if the requet if a GET.

            ## Get the authentication token from the header.
            token = request.headers['Authorization']
            
            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            #user_id = int(request.args.get('user_id'))
            search = str(request.args.get('q'))
            page = int(request.args.get('page'))
            rows = int(request.args.get('rows'))

            if not page:
                page = 1
            if not rows:
                rows = ITEMS_PER_PAGE

            if search != 'None': ## Search by name
                buckets = Buckets.query.filter(Buckets.name.like('%' + search + '%')).filter_by(user_id=user_id).paginate(page, rows, False).items
            else:
                buckets = Buckets.query.filter_by(user_id=user_id).paginate(page, rows, False).items

            results = []

            for bucket in buckets:
                obj = {
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'user_id': bucket.user_id
                }

                results.append(obj)

            return jsonify(results)

    ## This route is for deleting a bucket item.
    @app.route('/bucketlists/<int:id>', methods=['DELETE'])
    def delete_bucketlists_id(id):
        """ Delete Bucketlist.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            description: E.g ID of the bucket
            required: true
        responses:
            200:
                description: Bucketlist deleted successfully
        """
        ## Get the authentication token from the header.
        token = request.headers['Authorization']

        if token:
            ## Decode the token to get the user_id
            user_id = Users.decode_auth_token(token)
            if isinstance(user_id, str):
                return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

        bucket = Buckets.query.get(id)
        if not bucket:
            return jsonify({'success': False, 'msg': 'Bucketlist with id {} does not exist'.format(id)})

        if request.method == 'DELETE': ## Save bucket if the request is a post.
            #user_id = int(request.args.get('user_id'))
            bucket.delete()

            return jsonify({'success': True, 'msg': 'Bucketlist {} deleted successfully'.format(bucket.id)})

    ## This route is for creating a bucket.
    @app.route('/bucketlists/<int:id>', methods=['PUT'])
    def update_bucketlists_id(id):
        """ Update Bucketlist.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            description: E.g ID of the bucket
            required: true
         -  name: name
            in: formData
            description: The name of the bucket.
            type: string
            required: true
        responses:
            200:
                description: Bucketlist updated successfully
        """
        ## Get the authentication token from the header.
        token = request.headers['Authorization']

        if token:
            ## Decode the token to get the user_id
            user_id = Users.decode_auth_token(token)
            if isinstance(user_id, str):
                return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

        bucket = Buckets.query.get(id)
        if not bucket:
            return jsonify({'success': False, 'msg': 'Bucketlist with id {} does not exist'.format(id)})

        if request.method == 'PUT': ## Save bucket if the request is a post.
            name = str(request.args.get('name'))
            bucket.name  = name
            bucket.save()

            results = {
                    'id': bucket.id,
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'success': True,
                    'msg': 'Bucket created successfully'}

            return jsonify(results)

    ## This route is for creating a bucket.
    @app.route('/bucketlists/<int:id>', methods=['GET'])
    def bucketlists_id(id):
        """ Get Bucketlist.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            description: E.g ID of the bucket
            required: true
        responses:
            200:
                description: Get the Bucketlist
        """
        ## Get the authentication token from the header.
        token = request.headers['Authorization']

        if token:
            ## Decode the token to get the user_id
            user_id = Users.decode_auth_token(token)
            if isinstance(user_id, str):
                return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

        bucket = Buckets.query.get(id)
        if not bucket:
            return jsonify({'success': False, 'msg': 'Bucketlist with id {} does not exist'.format(id)})

        if request.method == 'GET': ## Return all buckets if the requet if a GET.
            result = {
                'id': bucket.id,
                'name': bucket.name,
                'date_created': bucket.date_created,
                'user_id': bucket.user_id
            }

            return jsonify(result);


    ## This route is for creating a bucketlist item.
    @app.route('/bucketlists/<int:id>/items/', methods=['POST'])
    def add_bucketlists_items(id, page=1):
        """ Add Buckets Items.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist Items
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: name
            in: formData
            type: string
            description: Name of the bucket item
            required: true
         -  name: description
            in: formData
            type: string
            description: Detail about the item
            required: true
         -  name: bucket_id
            in: formData
            type: integer
            description: The ID of the bucket
            required: true
        responses:
            200:
                description: Bucket Item added successfully.
        """
        if request.method == 'POST': ## Add bucket items if the request is a POST.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            name = request.form['name']
            description = request.form['description']
            bucket_id = request.form['bucket_id']

            if name and bucket_id:
                bucketitem = Bucketitems(name, description, bucket_id)
                bucketitem.save()

                result = {
                    'id': bucketitem.id,
                    'name': bucketitem.name,
                    'description': bucketitem.description,
                    'date_created': bucketitem.date_created,
                    'bucket_id': bucketitem.bucket_id
                }

                return jsonify(result)

    ## This route is for getting bucketlist items.
    @app.route('/bucketlists/<int:id>/items/', methods=['GET'])
    def get_bucketlists_items(id):
        """ Get all Buckets Items.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist Items
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            description: ID of the Bucketlist
            required: true
         -  name: page
            in: formData
            type: integer
            description: The page to view
            required: false
         -  name: rows
            in: formData
            type: integer
            description: Number of records/rows to return.
            required: false
        responses:
            200:
                description: All Bucket items.
        """
        if request.method == 'GET': ## Get bueckt items if the request if a GET
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            if not request.args.get('page'):
                page = 1
            else:
                page = int(request.args.get('page'))

            rows = ITEMS_PER_PAGE

            bucketitems = Bucketitems.query.filter_by(bucket_id=id).paginate(page, rows, False).items

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

    ## This route is for Updating a bucket.
    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
    def update_bucketitems_id(id, item_id = None):
        """ Edit Bucket.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist Items
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            required: true
         -  name: item_id
            in: path
            type: integer
            required: true
         -  name: name
            in: formData
            type: string
            required: true
         -  name: description
            in: formData
            type: string
            required: true
        """
        if request.method == 'PUT': ## Save bucket if the request is a PUT.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            bucketitem = Bucketitems.query.get(item_id)
            name = str(request.form['name'])
            description = str(request.form['description'])

            bucketitem.name  = name
            bucketitem.description = description
            bucketitem.save()

            results = {
                'id': bucketitem.id,
                'name': bucketitem.name,
                'description': bucketitem.description,
                'date_created': bucketitem.date_created,
                'success': True,
                'msg': 'Bucketitem updated successfully'
                }

            return jsonify(results)

    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
    def bucketitems_id(id, item_id = None):
        """ Delete Bucket item.
        Please provide all the required fields.
        ---
        tags:
         - Bucketlist Items
        consumes:
         - "application/x-www-form-urlencoded"
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: id
            in: path
            type: integer
            required: true
         -  name: item_id
            in: path
            type: integer
            required: true
        """
        if request.method == 'DELETE': ## Delete bucket if the request is a DELETE.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']

            if token:
                ## Decode the token to get the user_id
                user_id = Users.decode_auth_token(token)
                if isinstance(user_id, str):
                    return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

            bucketitem = Bucketitems.query.get(item_id)
            if not bucketitem:
                return jsonify({'success': False, 'msg': 'Bucketlist item with id {} does not exist'.format(item_id)})
            bucketitem.delete()

            return jsonify({'success': True, 'msg': 'Bucketlist {} deleted successfully'.format(bucketitem.id)})

    return app
