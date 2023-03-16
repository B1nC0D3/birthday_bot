from discord.ext.commands.context import Context
from config import FEMALE_ROLE_ID
from utils.date_utils import validate_date, get_today_date
from utils.jinja_utils import get_birthday_message, get_paste_message
from db import create, get_users_by_date
from typing import Generator
from discord import Member


async def add_user_birthday(birth_date: str, user: Member) -> str:
    gender = 'M'
    if user.get_role(FEMALE_ROLE_ID):
        gender = 'F'
    try:
        created = create(user.id, birth_date, gender)
    except Exception as e:
        print(e)
        return '<@237542033697406986> твоя хуйня опять развалилась'
    if created:
        return f'День рождения для <@{user.id}> добавлен'
    return f'День рождения для <@{user.id}> уже добавлен'


async def get_paste(user: Member) -> str:
    message = get_paste_message(user.id)
    return message


def create_msg_for_birthday_boys() -> Generator:
    today_date = get_today_date()
    users = get_users_by_date(today_date)
    for user in users:
        yield get_birthday_message(user['user_id'], user['gender'])
