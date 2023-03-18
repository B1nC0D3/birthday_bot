from jinja2 import Environment, FileSystemLoader
from random import choice
from config import PATH_TO_TEMPLATES

BIRTHDAY_TEMPLATES_NAMES = ('1.txt', '2.txt', '3.txt', '4.txt')
GAY_JOKES_TEMPLATES_NAMES = ('1.txt', '2.txt')
KEYS = ('first_user_id', 'second_user_id')
env = Environment(loader=FileSystemLoader(PATH_TO_TEMPLATES))


def get_birthday_message(user_id: int, gender: str):
    chosen_template = choice(BIRTHDAY_TEMPLATES_NAMES)
    template = env.get_template(f'birthday_templates/{chosen_template}')
    message = template.render(user_id=user_id, gender=gender)
    return message


def get_paste_message(paste_name: str, users_id: list[int]):
    users_for_template = zip(KEYS, users_id)
    paste_path = f'{paste_name}.txt'

    template = env.get_template(f'paste_templates/{paste_path}')
    message = template.render(dict(users_for_template))
    return message


def get_gay_joke_message(users_id: list[int]):
    users_for_template = zip(KEYS, users_id)
    chosen_template = choice(GAY_JOKES_TEMPLATES_NAMES)
    template = env.get_template(f'gay_jokes_templates/{chosen_template}')
    message = template.render(dict(users_for_template))
    return message
