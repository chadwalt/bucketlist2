# coding=utf-8

import re
from instance.config import app_config, ITEMS_PER_PAGE
from flask import request, jsonify, abort,render_template
from flask_bcrypt import Bcrypt
#from decorators import auth_token_required

## Import the db configuration
from manage import app
from app.models import Users, BlacklistToken

class Auth:

    ## This will handle the index route.
    @app.route('/', methods=['POST', 'GET'])
    def index():
        """ Home page (Documentation Page.)
        This page has the Documentation for the API... Using the flassger documentation
        """
        return render_template("index.html"), 200

    ## This will handle the routes if he route does not exist, it will return the 404 errors.
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'Page not found.'}), 404

    ## This route is for registering a user.
    @app.route('/auth/register', methods=['POST'])
    #@auth_token_required
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
                ## Check if valid inputs are provided
                valid_first_name = re.search(r'[0-9]+', first_name) ## Search for numbers in the first_name
                valid_sur_name = re.search(r'[0-9]+', sur_name) ## Search for numbers in the first_name

                if valid_sur_name or valid_first_name:
                    return jsonify({'success': False, 'msg': 'Numbers not allowed in the First Name or Last Name fields'}), 400

                ## Check if the user already exists.
                user = Users.query.filter_by(username=username).first();
                if not user:
                    user = Users(first_name, sur_name, username, password, email)
                    user.save() ## Save the user.

                    response_obj = {
                        'success': True,
                        'msg': 'User created successfully'
                    }

                    return jsonify(response_obj), 201
                else:
                    return jsonify({'success': False, 'msg': 'User already exists'}), 409
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'}), 400

    ## This is the route for user login.
    @app.route('/auth/login', methods=['POST'])
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

                        return jsonify(response_obj), 200
                else:
                   response_obj = {
                            'success': False,
                            'message': 'User does not exist.'
                        }
                   return jsonify(response_obj), 404
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'}), 400

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
                    return jsonify(response_obj), 200
                except Exception as e:
                    response_obj = {
                        'success': False,
                        'msg': 'Failed to logout.'
                    }
                    return jsonify(response_obj), 400
            else:
                response_obj = {
                    'success': False,
                    'msg': resp
                }
                return jsonify(response_obj), 400
        else:
            response_obj = {
                'success': False,
                'msg': 'Provide a valid auth token.'
            }
            return jsonify(response_obj), 401

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
                        
            email = request.form['email']
            password = request.form['password']

            if email and password:
                ## Get the user with this email
                user = Users.query.filter_by(email=email).first()

                if not user:
                    #abort(404) ## Raise the not found status.
                    return jsonify({'success': False, 'msg': 'User with the specified email does not exist.'}), 404

                #user.password = password
                user.password = Bcrypt().generate_password_hash(password).decode()
                user.save()
                return jsonify({'success': True, 'msg': 'User Password reset successfully'}), 201
            else:
                return jsonify({'success': False, 'msg': 'Please provide all fields'}), 400
