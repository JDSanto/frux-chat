"""User namespace module."""

from flask_restx import Namespace, Resource

from frux_chat.services import notifications
from frux_chat.services.authorization import requires_api_key
from frux_chat.services.database import database

from .models import notification_model, notification_parser, user_model, user_parser

ns = Namespace("User", description="User operations",)

ns.models[user_model.name] = user_model
ns.models[notification_model.name] = notification_model


@ns.route('/<user_id>', endpoint='user')
@ns.doc(params={'user_id': 'User ID'})
class UserResource(Resource):
    """User resource"""

    @ns.doc('put_user')
    @ns.marshal_with(user_model)
    @ns.expect(user_parser)
    def put(self, user_id):
        """Save or update a user given by the ID"""
        data = ns.payload
        user = database.insert_user(int(user_id), data['token'])
        return user

    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user token by ID"""
        user = database.get_user(int(user_id))
        return user


@ns.route('/<user_id>/notifications', endpoint='notifications')
@ns.doc(params={'user_id': 'User ID'})
class NotificationsResource(Resource):
    """Notifications resource"""

    @ns.doc('post_user_notification', security='apikey')
    @ns.response(401, "Unauthorized")
    @ns.marshal_with(notification_model)
    @ns.expect(notification_parser)
    @requires_api_key
    def post(self, user_id):
        """Send new notification to the user"""
        data = ns.payload
        notification = database.insert_notification(
            int(user_id), data['title'], data['body']
        )
        user = database.get_user(int(user_id))
        if user:
            notifications.notify_device(user['token'], data['title'], data['body'])
        return notification

    @ns.doc('get_user_notifications')
    @ns.marshal_with(notification_model)
    def get(self, user_id):
        """Get all the user's notifications"""
        user_notifications = database.get_notifications(int(user_id))
        return user_notifications
