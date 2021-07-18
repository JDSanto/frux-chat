def new_seeder(seeder, project):
    return f"""{seeder} has started funding {project}!"""


def change_state(project, stage):
    if stage == "FUNDING":
        return f"""{project} is looking for new seeders!"""
    if stage == "IN_PROGRESS":
        return f"""{project} has started development!"""
    if stage == "COMPLETE":
        return f"""{project} has finished development!"""


def new_stage_non_creator(project, stage_number):
    return f"""{project} has started developing their Stage #{stage_number}!"""


def new_stage_creator(name, project, stage_number):
    return f"""{name} has released the funds for Stage #{stage_number} of {project}!"""


def new_seer_creator(name, project):
    return f"""{name} has been assigned as the {project} supervisor!"""


def new_seer_seer(project):
    return f"""You've been assigned to supervise {project}!"""


### Chats -> No tiene que ver con suscripcion
def new_question(name):
    return f"""{name} has a new question for you!"""


def new_reply(name):
    return f"""{name} has replied to your question!"""
