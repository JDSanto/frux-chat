from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)

from frux_chat.services.database import database


def notify_device(token, title='', body='New event!'):
    # TODO: Logging
    print(f'NEW MESSAGE -- {token} -- {title} -- {body}')
    try:
        PushClient().publish(PushMessage(to=token, title=title, body=body))
    except (ValueError, DeviceNotRegisteredError, PushServerError, PushTicketError):
        pass


def set_tag_and_project(tag, project_id):
    '''Mix the tag and the project to store in the database'''
    return f'{tag}_{project_id}'


def notify_tag(tag, project_id, params):
    # TODO: Bulk notifications/inserts
    title, body = TAG_MAPPER[tag](params)
    users = database.get_subscriptions_users(set_tag_and_project(tag, project_id))
    for user in users:
        notify_device(user['token'], title, body)
        database.insert_notification(user['_id'], title, body)


# TODO: usar todo esto
# TODO: dividir en titulo/descripcion


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


def finish_stage_non_creator(data):
    project = data['project']
    stage_number = data['stage_number']
    return (
        'Stage finished!',
        f'{project} has finished developing their Stage #{stage_number}!',
    )


def finish_stage_seer(data):
    project = data['project']
    stage_number = data['stage_number']
    return (
        'Stage finished!',
        f'{project} has finished developing their Stage #{stage_number}! Check if everything is in place!',
    )


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


# app-server -> frux-chat
# NewSeederNotification -> X fundeo tu proyecto

# app-server -> frux-chat
# NewStageNotification_noncreator -> El proyecto entro en tal stage (similar a la de abajo)

# app-server -> frux-chat
# NewStageNotification_creator -> El veedor te dio los funds para tal stage

# app-server -> frux-chat
# NewSeer_creator -> Se asigno un veedor a tu proyecto

# app-server -> frux-chat
# NewSeer_seer -> Se te asigno un proyecto para que seas el seer

# app-server -> frux-chat
# ChangeStateNotification -> El proyecto entro en funding, el proyecto entro en inprogress, el proyecto se completo

# Como se envia una notif?
# PushClient().publish(PushMessage(to=token, body=message))


TAG_MAPPER = {
    'NewSeederNotification': new_seeder,
    'NewStageNotification_noncreator': new_stage_non_creator,
    'NewStageNotification_creator': new_stage_creator,
    'NewSeer_creator': new_seer_creator,
    'NewSeer_seer': new_seer_seer,
    'ChangeStateNotification': change_state,
}


# Chats -> No tiene que ver con suscripcion
def new_question(name):
    return f"""{name} has a new question for you!"""


def new_reply(name):
    return f"""{name} has replied to your question!"""
