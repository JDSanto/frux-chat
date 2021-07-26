"""User namespace module."""

from flask_restx import Namespace, Resource, fields

from frux_chat.services.database import database
from frux_chat.services import notifications
from .models import (
    user_model,
    user_parser,
    notification_parser,
    notification_model
)

ns = Namespace("User", description="User operations", )

ns.models[user_model.name] = user_model
ns.models[notification_model.name] = notification_model

@ns.route('/<id>', endpoint='user')
@ns.doc(params={'id': 'User ID'})
class UserResource(Resource):

    @ns.doc('put_user')
    @ns.marshal_with(user_model)
    @ns.expect(user_parser)
    def put(self, id):
        """Save or update a user given by the ID"""
        data = ns.payload
        user = database.insert_user(int(id), data['token'])
        return user


    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Get a user token by ID"""
        user = database.get_user(int(id))
        return user


@ns.route('/<id>/notifications', endpoint='notifications')
@ns.doc(params={'id': 'User ID'})
class NotificationsResource(Resource):

    @ns.doc('post_user_notification')
    @ns.marshal_with(notification_model)
    @ns.expect(notification_parser)
    def post(self, id):
        """Send new notification to the user"""
        data = ns.payload
        notification = database.insert_notification(
            int(id),
            data['title'],
            data['body']
        )
        user = database.get_user(int(id))
        notifications.notify_device(user['token'], data['title'], data['body'])
        return notification

    @ns.doc('get_user_notifications')
    @ns.marshal_with(notification_model)
    # @ns.response(200, "successfully fetched user notifications", fields.List(fields.Nested(notification_model)))
    def get(self, id):
        """Get all the user's notifications"""
        user_notifications = database.get_notifications(int(id))
        return user_notifications
