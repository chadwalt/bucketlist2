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

    ## Create an object representation.
    def __rep__(self):
        return "<User: {}>".format(self.username)

""" This is for the buckets """
class Buckets(db.Model):
    """ This represents the buckets table """

    __tablename__ = "buckets"

    ## Creating the columns for the table.
    id = db.Column(db.Integer, primary_key = True, sequence(increment=1))
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    ## Initializing it.
    def __init__(self, name, date_created):
        self.name = name
        self.date_created = date_created

    ## Save the bucket.
    def save(self):
        db.session.add(self)
        db.session.commit()

    ## Get all the buckets.
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
class Bucketitems():
    """ This represents the buckets table """

    __tablename__ = "bucketitems"

    ## Creating the columns for the table.
    id = db.Column(db.Integer, primary_key = True, sequence(increment=1))
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    bucket_id = db.Column(db.Integer,db.ForeignKey('buckets.id'))

    ## Initializing it.
    def __init__(self, name, description, date_created, bucket_id):
        self.name = name
        self.description = description
        self.date_created = date_created
        self.bucket_id = bucket_id        

    ## Save the bucket.
    def save(self):
        db.session.add(self)
        db.session.commit()

    ## Get all the buckets.
    def get_all():
        return Bucketsitems.query.all()

    ## Delete the bucket.
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    ## Create an object representation.
    def __rep__(self):
        return "<Bucketitems: {}>".format(self.name)

