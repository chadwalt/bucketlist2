""" This is going to contain the models for the application. Creating users, buckets and bucketitems"""
# Import the datetime.
import datetime

## Import the database.
from manage import *

## Import the JSON Web Token for authentication.
import jwt

import os

from flask_bcrypt import Bcrypt ## Import the encryption module for flask.

## This is for creating the users.
class Users(db.Model):
    """ This class represents the users table. """

    __tablename__ = 'users' ## Defining the table name.

    ## Creating the columns for the table.
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    first_name = db.Column(db.String(20))
    sur_name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))
    email = db.Column(db.String(30))

    ## Initializing it.
    def __init__(self, first_name, sur_name, username, password, email):
        self.first_name = first_name
        self.sur_name = sur_name
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.email = email

    ## Save the user.
    def save(self):
        db.session.add(self)
        db.session.commit()

    ## Check for password validity.
    def valid_password(self, password):
        """ Checks if the password provided matches the one in the database. """

        return Bcrypt().check_password_hash(self.password, password)

    ## Get all the users.
    @staticmethod
    def get_all():
        return Users.query.all()

    ## Delete the user.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        """ Generates the Auth Token :return: string """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=300), ## Expire after 5 hrs.
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """ Decodes the auth token :param auth_token: :return: integer|string """
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    ## Create an object representation.
    def __rep__(self):
        return "<User: {}>".format(self.username)

""" This is for the buckets """
class Buckets(db.Model):
    """ This represents the buckets table """

    __tablename__ = "buckets"

    ## Creating the columns for the table.
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    ## Initializing it.
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    ## Save the bucket.
    def save(self):
        db.session.add(self)
        db.session.commit()

    ## Get all the buckets.
    @staticmethod
    def get_all():
        return Buckets.query.all()

    ## Delete the bucket.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    ## Create an object representation.
    def __rep__(self):
        return "<Bucket: {}>".format(self.name)

""" This is for the bucketitems """
class Bucketitems(db.Model):
    """ This represents the buckets table """

    __tablename__ = "bucketitems"

    ## Creating the columns for the table.
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    bucket_id = db.Column(db.Integer,db.ForeignKey('buckets.id'))

    ## Initializing it.
    def __init__(self, name, description, bucket_id):
        self.name = name
        self.description = description
        #self.date_created = date_created
        self.bucket_id = bucket_id

    ## Save the bucket.
    def save(self):
        db.session.add(self)
        db.session.commit()

    ## Get all the buckets.
    @staticmethod
    def get_all():
        return Bucketitems.query.all()

    ## Delete the bucket.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    ## Create an object representation.
    def __rep__(self):
        return "<Bucketitems: {}>".format(self.name)

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


    def __repr__(self):
        return '<id: token: {}'.format(self.token)
