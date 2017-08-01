
from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

app.secret_key = 'ecii22727271sf@kdkdk'

# Load the views
from app.mod_auth import controllers

# Load the config file
app.config.from_object('config')