""" This is going to contain the models for the application. Creating users, buckets and bucketitems"""
# Import the datetime.
import datetime

## Import the database.
from app import db

## Import the JSON Web Token for authentication.
import jwt

import os

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
        self.password = password
        self.email = email
    
    ## Save the user.
    def save(self):
        db.session.add(self)
        db.session.commit()

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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
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

