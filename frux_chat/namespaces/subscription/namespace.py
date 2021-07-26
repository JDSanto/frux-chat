"""User namespace module."""

from flask_restx import Namespace, Resource

from frux_chat.services import notifications
from frux_chat.services.database import database

from .models import notification_parser

ns = Namespace("Subscription", description="Subscription operations",)


@ns.route('/<project_id>/<tag>/user/<user_id>', endpoint='subscription_user')
@ns.doc(
    params={'project_id': 'Project ID', 'tag': 'Subscription Tag', 'user_id': 'User ID'}
)
class SubscriptionResource(Resource):
    """Subscription resource"""

    @ns.doc('add_subscription')
    def post(self, project_id, tag, user_id):
        """Subscribe a user to the given tag and project"""
        tag = notifications.set_tag_and_project(tag, project_id)
        user = database.insert_subscription(tag, int(user_id))
        return user

    @ns.doc('remove_subscription')
    def delete(self, project_id, tag, user_id):
        """Unsubscribe a user to the given tag and project"""
        tag = notifications.set_tag_and_project(tag, project_id)
        user = database.remove_subscription(tag, int(user_id))
        return user


@ns.route('/<project_id>/<tag>', endpoint='subscription')
@ns.doc(params={'project_id': 'Project ID', 'tag': 'Subscription Tag'})
class SubscriptionNotifierResource(Resource):
    """Subscription notifier resource"""

    @ns.doc('subscription_notifier')
    @ns.expect(notification_parser)
    def post(self, project_id, tag):
        """Send a notification to a given tag and project"""
        data = ns.payload
        notifications.notify_tag(tag, project_id, data)
        return {'status': 'ok'}
