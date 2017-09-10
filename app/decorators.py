"""
This is for the decorator functions.
"""

from functools import wraps
from flask import request, jsonify
from manage import Users


def auth_token_required(f): ## The f represents the function called after the decorator.
    @wraps(f)
    def token_required(*args, **kwargs):
        ## Get the authentication token from the header.
        token = request.headers['Authorization']

        if token:
            ## Decode the token to get the user_id
            user_id = Users.decode_auth_token(token)
            if isinstance(user_id, str):
                return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'})

        return f(*args, **kwargs)
    return token_required