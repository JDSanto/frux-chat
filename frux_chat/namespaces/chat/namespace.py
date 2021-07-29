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
        creator = database.get_user(data['user_id'])
        replyto_user = database.get_user(data['replyto_id'])
        is_question = data['question']
        body = data['body']

        title = "Someone asked you a question!"
        if (is_question): title = "Your question was replied!"
        notifications.notify_device(replyto_user['token'], title, body)
        # Help guardando esto en la db
        # database.insert_notification(user['_id'], title, body)
        return {'status': 'ok'}
