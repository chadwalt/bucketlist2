""" This is going to contain the models for the application. Creating users, buckets and bucketitems"""

## Import the database.
from app import db

## This is for creating the users.
class Users(db.Model):
    """ This class represents the users table. """

    __tablename__ = 'users' ## Defining the table name.

    ## Creating the columns for the table.
    id = db.Column(db.Integer, primary_key = True, sequence(increment=1))
    first_name = db.Column(db.String(20))
    sur_name = db.Column(db.String(20))
    usename = db.Column(db.String(20))
    password = db.Column(db.String(100))
    email = db.Column(db.String(30))