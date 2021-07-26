"""API module."""
import logging

from flask_restx import Api

from frux_chat.namespaces import user_namespace, subscription_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api = Api(validate=True, title='Frux Chat API', description='Frux chat and notification API')

api.add_namespace(user_namespace, path='/user')
api.add_namespace(subscription_namespace, path='/subscription')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)
