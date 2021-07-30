from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)

from frux_chat.services.database import database


def notify_device(token, title='', body='New event!', notification_data={}):
    # TODO: Logging
    print(f'NEW MESSAGE -- {token} -- {title} -- {body}')
    try:
        PushClient().publish(PushMessage(to=token, title=title, body=body, data=notification_data))
    except (ValueError, DeviceNotRegisteredError, PushServerError, PushTicketError):
        pass


def set_tag_and_project(tag, project_id):
    '''Mix the tag and the project to store in the database'''
    return f'{tag}_{project_id}'


def notify_tag(tag, project_id, params):
    # TODO: Bulk notifications/inserts
    title, body = TAG_MAPPER[tag](params)
    users = database.get_subscriptions_users(set_tag_and_project(tag, project_id))
    notification_data = {'project_id':project_id}
    for user in users:
        notify_device(user['token'], title, body, notification_data)
        database.insert_notification(user['_id'], title, body, project_id)


# Notifications Specccc
# NewSeederNotification -> X fundeo tu proyecto
# NewStageNotification_noncreator -> El proyecto entro en tal stage (similar a la de abajo)
# NewStageNotification_creator -> El veedor te dio los funds para tal stage
# NewSeer_creator -> Se asigno un veedor a tu proyecto
# NewSeer_seer -> Se te asigno un proyecto para que seas el seer
# ChangeStateNotification -> El proyecto entro en funding, el proyecto entro en inprogress, el proyecto se completo

def new_seeder(data):
    project = data['project']
    username = data['username']
    return ('New seeder!', f'{username} has started funding {project}!')


def change_state(data):
    project = data['project']
    state = data['state']
    if state == "FUNDING":
        body = f'{project} is looking for new seeders!'
    if state == "IN_PROGRESS":
        body = f'{project} has started development!'
    if state == "COMPLETE":
        body = f'{project} has finished development!'
    return ('New progress!', body)



def new_stage_non_creator(data):
    project = data['project']
    stage_number = data['stage_number']
    return (
        'Stage finished!',
        f'{project} has started developing their Stage #{stage_number}!',
    )


def new_stage_creator(data):
    project = data['project']
    stage_number = data['stage_number']
    name = data['username']
    return (
        'Stage funds released!',
        f'{name} has released the funds for Stage #{stage_number} of {project}!',
    )


def new_seer_creator(data):
    project = data['project']
    name = data['username']
    return ('Seer assigned!', f'{name} has been assigned as the {project} supervisor!')


def new_seer_seer(data):
    project = data['project']
    return ('Project assigned!', f'You\'ve been assigned to supervise {project}!')


TAG_MAPPER = {
    'NewSeederNotification': new_seeder,
    'NewStageNotification_noncreator': new_stage_non_creator,
    'NewStageNotification_creator': new_stage_creator,
    'NewSeer_creator': new_seer_creator,
    'NewSeer_seer': new_seer_seer,
    'ChangeStateNotification': change_state,
}


# Role Specccc
# ProjectCreator
#   - Quien se suscribe? el creador de un proyecto al crearlo
#   - Que notificaciones recibe? NewSeederNotification, NewStageNotification_creator, NewSeer_creator, ChangeStateNotification,
# ProjectWatcher
#   - Quien se suscribe? los que dieron like
#   - Que notificaciones recibe? ChangeStateNotification,
# ProjectSeer
#   - Quien se suscribe? el veedor de un proyecto
#   - Que notificaciones recibe? NewSeederNotification, NewSeer_seer, ChangeStateNotification
# ProjectSeeder
#   - Quien se suscribe? los que invirtieron en el proyecto
#   - Que notificaciones recibe? NewStageNotification_noncreator
# El chat NO se maneja por suscripciones


ROLE_MAPPER = {
    'ProjectCreator': [
        'NewSeederNotification',
        'NewStageNotification_creator',
        'NewSeer_creator',
        'ChangeStateNotification',
    ],
    'ProjectWatcher': ['ChangeStateNotification'],
    'ProjectSeer': [
        'NewSeederNotification',
        'NewSeer_seer',
        'ChangeStateNotification',
    ],
    'ProjectSeeder': [
        'NewStageNotification_noncreator',
    ],
}
