# Bucketlist API

[![Build Status](https://travis-ci.org/chadwalt/bucketlist2.svg?branch=master)](https://travis-ci.org/chadwalt/bucketlist2) [![Coverage Status](https://coveralls.io/repos/github/chadwalt/bucketlist2/badge.svg?branch=master)](https://coveralls.io/github/chadwalt/bucketlist2?branch=master)

This is an Bucketlist API, which you provide data to, to store things you want to do before you die..

### How to install the API.

Go to [GitHub: Bucketlist2](https://github.com/chadwalt/bucketlist2 "Buketlist2") and clone the Repository

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

View the API Documentation on Heroku. [API Documentation](https://mybucketlist-api.herokuapp.com/apidocs/)
