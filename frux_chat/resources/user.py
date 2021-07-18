
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_restful_swagger import swagger

from ..services.database import database

@swagger.model
class UserResponseFields():
    resource_fields = {
        'id': fields.Integer,
        'token': fields.String
    }

@swagger.model
class UserRequestFields():
    resource_fields = {
        'token': fields.String
    }


parser = reqparse.RequestParser()
parser.add_argument("token", type=str)


class User(Resource):
    # Recibe user_id y token -> Lo guarda en la db
    # Also se fija si el token es distinto y lo actualiza en la db (o lo agrega como extra? pensar en multiples dispositivos?)

    @swagger.operation(
        notes='Add a new user to the database',
        parameters=[
            {
                "name": "body",
                "description": "A User item",
                "required": True,
                "allowMultiple": False,
                "dataType": UserRequestFields.__name__,
                "paramType": "body",
            }
        ],
        responseClass=UserResponseFields
    )
    def put(self, id):
        args = parser.parse_args()
        user = database.insert_user(id, args['token'])
        return {
            'id': user.inserted_id,
            'token': args['token']
        }

    @swagger.operation(
        notes='Get a user from the database',
        responseClass=UserResponseFields
    )
    def get(self, id):
        return database.get_user(id)
