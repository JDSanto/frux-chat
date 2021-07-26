from flask_restx import reqparse

# TODO: Find a better way to map notification message and parameters
# without writing N routes for each notification
notification_parser = reqparse.RequestParser()
notification_parser.add_argument(
    "project", type=str, location="json", help="The project to send in the notification"
)
notification_parser.add_argument(
    "state", type=str, location="json", help="The state to send in the notification"
)
notification_parser.add_argument(
    "stage_number",
    type=str,
    location="json",
    help="The stage number to send in the notification",
)
notification_parser.add_argument(
    "username",
    type=str,
    location="json",
    help="The username to send in the notification",
)
