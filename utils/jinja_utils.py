from jinja2 import Environment, FileSystemLoader
from random import choice
from config import PATH_TO_TEMPLATES

BIRTHDAY_TEMPLATES_NAMES = ('birthday_templates/1.txt',)
env = Environment(loader=FileSystemLoader(PATH_TO_TEMPLATES))


def get_birthday_message(user_id: int, gender: str):
    template = env.get_template(choice(BIRTHDAY_TEMPLATES_NAMES))
    message = template.render(user_id=user_id, gender=gender)
    return message


def get_paste_message(user_id: int):
    template = env.get_template('paste_templates/pain_paste.txt')
    message = template.render(user_id=user_id)
    return message
