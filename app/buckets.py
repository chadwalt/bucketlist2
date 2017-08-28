from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import re
from instance.config import app_config, ITEMS_PER_PAGE
from flask import request, jsonify, abort,render_template
from flask_bcrypt import Bcrypt

# initialize sql-alchemy
db = SQLAlchemy()

class Bucket:
    ## Import the db configuration
    from manage import app

    ## This will handle the routes if he route does not exist, it will return the 404 errors.
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'Page not found.'}), 404


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
        produces:
         - "application/json"
        parameters:
         -  name: Authorization
            in: header
            type: string
            description: Auth Token
            required: true
         -  name: q
            in: query
            type: string
            required: false
         -  name: page
            in: query
            type: integer
            required: true
            default: 1
         -  name: rows
            in: query
            type: integer
            required: true
            default: 10
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

    ## This route is for Editing or Updating a bucket.
    @app.route('/bucketlists/<int:id>', methods=['PUT'])
    def update_bucketlists_id(id):
        """ Update/Edit Bucketlist.
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
            name = str(request.form.get('name'))
            bucket.name  = name
            bucket.save()

            results = {
                    'id': bucket.id,
                    'name': bucket.name,
                    'date_created': bucket.date_created,
                    'success': True,
                    'msg': 'Bucket updated successfully'}

            return jsonify(results)

    ## This route is for Getting a bucket.
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
