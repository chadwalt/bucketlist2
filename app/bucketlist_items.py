from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import re
from instance.config import app_config, ITEMS_PER_PAGE
from flask import request, jsonify, abort,render_template
from flask_bcrypt import Bcrypt

# initialize sql-alchemy
db = SQLAlchemy()
## Import the db configuration
from app.manage import app, Users, Buckets, Bucketitems
from decorators import auth_token_required

class Bucketlist_item:

    ## This will handle the routes if he route does not exist, it will return the 404 errors.
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'Page not found.'}), 404

    ## This route is for creating a bucketlist item.
    @app.route('/bucketlists/<int:id>/items/', methods=['POST'])
    @auth_token_required
    def add_bucketlists_items(id):
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
         -  name: id
            in: path
            type: integer
            description: E.g ID of the bucket
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
        responses:
            200:
                description: Bucket Item added successfully.
        """
        if request.method == 'POST': ## Add bucket items if the request is a POST.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']
            user_id = Users.decode_auth_token(token)
            name = request.form['name']
            description = request.form['description']
            bucket_id = id

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

                return jsonify(result), 201

    ## This route is for getting bucketlist items.
    @app.route('/bucketlists/<int:id>/items/', methods=['GET'])
    @auth_token_required
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
            in: query
            type: integer
            description: The page to view
            required: false
         -  name: rows
            in: query
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
            user_id = Users.decode_auth_token(token)

            if not request.args.get('page'):
                page = 1
            else:
                page = int(request.args.get('page'))

            if not request.args.get('rows'):
                rows = ITEMS_PER_PAGE
            else:
                rows = int(request.args.get('rows'))

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

            return jsonify(results), 200

    ## This route is for Updating a bucket.
    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
    @auth_token_required
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
            description: The ID of the bucket
         -  name: item_id
            in: path
            type: integer
            required: true
            description: The ID of the bucketlist item
         -  name: name
            in: formData
            type: string
            required: true
            description: The name of the bucketlist item
         -  name: description
            in: formData
            type: string
            required: true
            description: A breif description of the bucketlist item.
        """
        if request.method == 'PUT': ## Save bucket if the request is a PUT.
            ## Get the authentication token from the header.
            token = request.headers['Authorization']
            user_id = Users.decode_auth_token(token)
            
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

            return jsonify(results), 201

    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
    @auth_token_required
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
            user_id = Users.decode_auth_token(token)

            bucketitem = Bucketitems.query.get(item_id)
            if not bucketitem:
                return jsonify({'success': False, 'msg': 'Bucketlist item with id {} does not exist'.format(item_id)}), 404
            bucketitem.delete()

            return jsonify({'success': True, 'msg': 'Bucketlist {} deleted successfully'.format(bucketitem.id)}), 201
