"""
This is for the decorator functions.
"""

from functools import wraps
from flask import request, jsonify


def auth_token_required(f):
    @wraps(f)
    def token_required(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return jsonify({'success': False, 'msg': 'Invalid authentication token. Please login again.'}), 401
    return token_required
