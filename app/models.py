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
    def get_all():
        return Users.query.all()

    ## Delete the user.
    def delete(self):
        db.session.delete(self)
        db.session.commit()