import os

from flask import request


def requires_api_key(method):
    def wrapper(*args, **kwargs):
        key = request.headers.get('x-api-key')
        if not key:
            return {'error': 'Missing x-api-key header'}, 401

        if key != os.environ.get('API_KEY'):
            return {'error': 'Invalid x-api-key header'}, 401

        return method(*args, **kwargs)

    return wrapper
