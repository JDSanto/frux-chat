from flask_restx import reqparse

chat_parser = reqparse.RequestParser()
chat_parser.add_argument(
    "user_id", type=int, location="json", help="The originator of the message"
)
chat_parser.add_argument(
    "body", type=str, location="json", help="The body of the conversation message"
)
chat_parser.add_argument(
    "question", type=bool, location="json", help="True if an user is asking a question, false if the creator is replying to a question"
)
chat_parser.add_argument(
    "replyto_id",
    type=str,
    location="json",
    help="The user to whom the user is replying. If the user is asking an initial question, it replies to the creator",
)
