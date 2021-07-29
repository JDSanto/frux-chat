"""API module."""
import logging

from flask_restx import Api

from frux_chat.namespaces import (
    default_namespace,
    subscription_namespace,
    user_namespace,
    chat_namespace,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

authorizations = {'apikey': {'type': 'apiKey', 'in': 'header', 'name': 'X-API-KEY'}}

api = Api(
    validate=True,
    title='Frux Chat API',
    description='Frux chat and notification API',
    authorizations=authorizations,
)

api.add_namespace(user_namespace, path='/user')
api.add_namespace(subscription_namespace, path='/subscription')
api.add_namespace(chat_namespace, path='/chat')
api.add_namespace(default_namespace, path='/health')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)
