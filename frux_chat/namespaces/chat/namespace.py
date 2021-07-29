"""User namespace module."""

from flask_restx import Namespace, Resource

from frux_chat.services import notifications
from frux_chat.services.authorization import requires_api_key
from frux_chat.services.database import database

from .models import chat_parser

ns = Namespace("Chat", description="Private chat operations",)


@ns.route('/<project_id>', endpoint='chat')
@ns.doc(
    params={
        'project_id': 'Project ID',
    }
)
class ChatResource(Resource):
    """Chat resource"""

    # @ns.doc('chat', security='apikey')
    # @ns.response(401, "Unauthorized")
    # @requires_api_key
    @ns.expect(chat_parser)
    def post(self, project_id):
        """Ask or reply to a question"""
        data = ns.payload
        replyto_user = database.get_user(data['replyto_id'])
        is_question = data['question']
        body = data['body']

        title = "Your question was replied!"
        if (is_question): title = "Someone asked you a question!"

        notification_data = {'project_id':project_id, 'chat': True}
        database.insert_notification(data['replyto_id'], title, body, project_id, True)
        notifications.notify_device(replyto_user['token'], title, body, notification_data)
        return {'status': 'ok'}
