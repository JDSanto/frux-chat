from flask_restx import Model, fields, reqparse

user_model = Model(
    "User model",
    {"token": fields.String(required=True, description="The Expo session token")},
)

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    "token", type=str, location="json", help="The Expo session token"
)

notification_model = Model(
    "Notification model",
    {
        "created_at": fields.DateTime(
            required=True, description="The notification creation date"
        ),
        "user_id": fields.Integer(required=True, description="The user id"),
        "title": fields.String(required=True, description="The notification title"),
        "body": fields.String(required=True, description="The notification body"),
        "project_id": fields.String(
            required=True, description="The project the notification relates to"
        ),
        "chat_id": fields.String(
            required=False,
            description="The conversation id of the notification (question + reply). If the notification is not a chat, this is None",
        ),
        "commenter_id": fields.String(
            required=False,
            description="The id of the commenter. If the notification is not a chat, this is None",
        ),
    },
)


notification_parser = reqparse.RequestParser()
notification_parser.add_argument(
    "title", type=str, location="json", help="The notification title"
)
notification_parser.add_argument(
    "body", type=str, location="json", help="The notification body"
)
