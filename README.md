# Bucketlist API

[![Build Status](https://travis-ci.org/chadwalt/bucketlist2.svg?branch=master)](https://travis-ci.org/chadwalt/bucketlist2) [![Coverage Status](https://coveralls.io/repos/github/chadwalt/bucketlist2/badge.svg?branch=master)](https://coveralls.io/github/chadwalt/bucketlist2?branch=master)

This is an Bucketlist API, which you provide data to, to store things you want to do before you die..

### How to install the API.

Go to [GitHub: Bucketlist2](https://github.com/chadwalt/bucketlist2 "Buketlist2") and clone the Repository make sure you have git installed.

```
git clone https://github.com/chadwalt/bucketlist2
```

Navigate to the installation folder or create a directory if you have not created one yet, like

```
mkdir bucketlist_api
```

Move to the created directory

```
$ cd bucketlist_api
```

Now clone the repository.

```
git clone https://github.com/chadwalt/bucketlist2
```

Make sure you have the lastest python installed. [Python.org](https://www.python.org/downloads/)

Download and install Postgressql if you dont have it. [Postgresql](https://www.postgresql.org/download/)

### Now Setup Virtual Environment

```
$ pip install virtualenv
```

```
$ pip install virtualenvwrapper
```

```
$ export WORKHOME=~/Envs
```

```
$ source /usr/local/bin/virtualenvwrapper.sh
```

```
$ mkvirtualenv bucketlistapi
```

```
$ workon bucketlistapi
```

**Run the .env to install application environment variable**

```
$ source .env
```

**Install the requirements**
```
$ pip install -r requirements.txt
```

**Create the databases, make sure you have Postgresql installed**
```
createdb bucketlist
createdb test_db
```

### Run the flask server

```
$ flask run
```

### API End Points.

| Request Method | End Point | Public Access | Description |
| --- | --- | ---| --- |
| POST | /auth/register | TRUE | User Registration |
| POST | /auth/login | TRUE | User Login |
| POST | /auth/logout | FALSE | User Logout |
| POST | /auth/reset-password | TRUE | Resetting User Password |
| POST | /buckets/ | FALSE | Creating Buckets |
| GET |  /buckets/ | FALSE | Get all Buckets |
| GET | /buckets/<id> | FALSE | Get a particular Bucket by its ID |
| PUT | /buckets/<id> | FALSE | Update a Bucket |
| DELETE | /buckets/<id> | FALSE | Delete a particular Bucket by its ID |
| POST | /bucketlists/<id>/items/ | FALSE | Create a Bucket List Item by its ID |
| PUT | /bucketlists/<id>/items/<item_id> | FALSE | Update a Bucket List Item by its ID|
| DELETE | /bucketlists/<id>/items/<item_id> | FALSE | Delete a Bucket List Item by its ID |


View the API Documentation on Heroku. [API Documentation](https://mybucketlist-api.herokuapp.com/apidocs/)
