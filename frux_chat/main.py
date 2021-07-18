from flask import Flask, request
from flask_restful import Api, Resource

from requests.exceptions import ConnectionError, HTTPError

from flask_restful_swagger import swagger

from frux_chat.resources.user import User
from frux_chat.resources.notification import Notification

"""
pip install flask
pip install flask_restful
pip install exponent_server_sdk
python main.py -> Levanta server



Esto tiene mucha pinta -> https://medium.com/analytics-vidhya/flask-restful-api-with-heroku-da1ecf3e04b


Also, si hay ganas, se puede dividir en distintos archivos
Also, se puede agregar herencia/polimorfismo (en vez de un switch enorme?)
"""

class Chat(Resource):
    # Fede stuff, dont dar bola
    def post(self):
        pass


class Subscription(Resource):
    # Recibe un usuario, un proyecto, y el tipo de suscripcion
    # Tambien hay que hacer metodo de delete, para cuando un usuario da dislike

    # Tipos de suscripciones:
    # ProjectCreator
    #   - Quien se suscribe? el creador de un proyecto al crearlo
    #   - Que notificaciones recibe? NewSeederNotification, NewStageNotification_creator, NewSeer_creator, ChangeStateNotification
    # ProjectWatcher
    #   - Quien se suscribe? los que dieron like
    #   - Que notificaciones recibe? ChangeStateNotification
    # ProjectSeer
    #   - Quien se suscribe? el veedor de un proyecto
    #   - Que notificaciones recibe? NewSeederNotification, NewSeer_seer, ChangeStateNotification
    # ProjectSeeder
    #   - Quien se suscribe? los que invirtieron en el proyecto
    #   - Que notificaciones recibe? NewStageNotification_noncreator
    # El chat NO se maneja por suscripciones

    def post(self):
        body = request.get_json()
        user_id = body.get("user_id")
        project_id = body.get("project_id")
        subscription_name = body.get("subscription_name")
        return {}

# PushClient().publish(PushMessage(to='ExponentPushToken[EnXw1vGCBYEkgRnuQa-B4o]', body='hello'))

def create_app():

    app = Flask(__name__)

    api = swagger.docs(
        Api(app),
        apiVersion="0.1",
        basePath="http://localhost:5000",
        resourcePath="/",
        produces=["application/json", "text/html"],
        api_spec_url="/api/spec",
        description="frux-chat API",
    )
    api.add_resource(User, "/user/<int:id>", endpoint="user")
    api.add_resource(Subscription, "/subscription")
    api.add_resource(Notification, "/notification")
    api.add_resource(Chat, "/chat")

    return app
