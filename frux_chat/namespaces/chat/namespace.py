"""User namespace module."""

import uuid

from flask_restx import Namespace, Resource

from frux_chat.namespaces.user.models import notification_model
from frux_chat.services import notifications
from frux_chat.services.database import database

from .models import chat_parser

ns = Namespace("Chat", description="Private chat operations",)


@ns.route('/<project_id>', endpoint='chat')
@ns.doc(params={'project_id': 'Project ID'})
class ChatResource(Resource):
    """Chat resource"""

    @ns.doc('chat', security='apikey')
    @ns.expect(chat_parser)
    def post(self, project_id):
        """Ask or reply to a question"""
        data = ns.payload
        commenter_id = data['commenter_id']
        replyto_user = database.get_user(int(data['replyto_id']))
        is_reply = data.get('chat_id', False)
        body = data['body']

        chat_id = data['chat_id'] if is_reply else str(uuid.uuid1())
        title = (
            "Your question was replied!"
            if is_reply
            else "Someone asked you a question!"
        )

        notification_data = {
            'project_id': project_id,
            'chat_id': chat_id,
            'commenter_id': commenter_id,
        }
        database.insert_notification(
            data['replyto_id'], title, body, project_id, chat_id, commenter_id
        )
        if replyto_user:
            notifications.notify_device(
                replyto_user['token'], title, body, notification_data
            )
        return {'status': 'ok'}

    @ns.doc('get_chat', security='apikey')
    @ns.marshal_with(notification_model)
    def get(self, project_id):
        """Get all the project messages"""
        project_chat = database.get_chat(project_id)
        return project_chat
