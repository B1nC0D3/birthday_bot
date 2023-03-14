from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from random import choice
from config import PATH_TO_TEMPLATES


TEMPLATES_NAMES = ('1.txt',)
env = Environment(loader=FileSystemLoader(PATH_TO_TEMPLATES))


def string_to_date(date):
    try:
        date = datetime.strptime(date, '%d.%m')
    except ValueError:
        return False
    return date.strftime('%d.%m')


def get_today_date() -> str:
    today_date = datetime.now().strftime('%d.%m')
    return today_date


def create_message(user_id: int, gender: str):
    template = env.get_template(choice(TEMPLATES_NAMES))
    message = template.render(user_id=user_id, gender=gender)
    return message


def get_exception_message(user_id: int):
    template = env.get_template('exception.txt')
    message = template.render(user_id=user_id)
    return message
