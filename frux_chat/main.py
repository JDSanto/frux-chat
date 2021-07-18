from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from flask import Flask, request
from flask_restful import Api, Resource
from requests.exceptions import ConnectionError, HTTPError

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


class Notification(Resource):
    # Recibe el proyecto y el nombre de la notificacion a enviar y los parametros de esa notificacion (nombres de usuarios, nombres de proyecto, etc)
    # Recorre todas las suscripciones de ese proyecto y para las suscripciones correspondientes a la notif recibida, las envia
    # Tambien guarda la notificacion en la db, para despues poder darsela al usuario y mostrarla en la app en si

    # Hay distintos tipos de notificaciones, y algunas tienen subtipos (donde solo cambia el body segun el receptor)
    # Los bodys estan en notifications.py
    # NewSeederNotification -> X fundeo tu proyecto
    # NewStageNotification_noncreator -> El proyecto entro en tal stage
    # NewStageNotification_creator -> El veedor te dio los funds para tal stage
    # NewSeer_creator -> Se asigno un veedor a tu proyecto
    # NewSeer_seer -> Se te asigno un proyecto para que seas el seer
    # ChangeStateNotification -> El proyecto entro en funding, el proyecto entro en inprogress, el proyecto se completo

    # Como se envia una notif?
    # PushClient().publish(PushMessage(to=token, body=message))

    def post(self):
        body = request.get_json()
        project_id = body.get("project_id")
        notification_name = body.get("notification_name")
        notification_data = body.get("notification_data")
        return {}


class User(Resource):
    # Recibe user_id y token -> Lo guarda en la db
    # Also se fija si el token es distinto y lo actualiza en la db (o lo agrega como extra? pensar en multiples dispositivos?)
    def post(self):
        body = request.get_json()
        user_id = body.get("user_id")
        token = body.get("token")
        return {}


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

    api = Api(app)
    api.add_resource(User, "/user")
    api.add_resource(Subscription, "/subscription")
    api.add_resource(Notification, "/notification")
    api.add_resource(Chat, "/user")

    return app
