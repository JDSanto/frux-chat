
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_restful_swagger import swagger

from ..services.notifications import notify_device

parser = reqparse.RequestParser()
parser.add_argument("token", type=str)
parser.add_argument("message", type=str)

class Notification(Resource):
    # Recibe el proyecto y el nombre de la notificacion a enviar y los parametros de esa notificacion (nombres de usuarios, nombres de proyecto, etc)
    # Recorre todas las suscripciones de ese proyecto y para las suscripciones correspondientes a la notif recibida, las envia
    # Tambien guarda la notificacion en la db, para despues poder darsela al usuario y mostrarla en la app en si

    # Hay distintos tipos de notificaciones, y algunas tienen subtipos (donde solo cambia el body segun el receptor)
    # Los bodys estan en notifications.py
    # NewSeederNotification -> X fundeo tu proyecto
    # NewStageNotification_noncreator -> El proyecto entro en tal stage
    # NewStageNotification_creator -> El veedor te dio los funds para tal stage
    # FinishStageNotification_noncreator -> El proyecto termino tal stage
    # FinishStageNotification_seeder -> El creador marco como completado el desarrollo de un stage
    # NewSeer_creator -> Se asigno un veedor a tu proyecto
    # NewSeer_seer -> Se te asigno un proyecto para que seas el seer
    # ChangeStateNotification -> El proyecto entro en funding, el proyecto entro en inprogress, el proyecto se completo

    # Como se envia una notif?
    # PushClient().publish(PushMessage(to=token, body=message))

    def post(self):
        args = parser.parse_args()
        token = args.get("token")
        message = args.get("message")
        notify_device(token, message)
        return {'status': 'ok'}
