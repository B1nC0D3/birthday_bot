from discord.ext.commands.context import Context
from config import FEMALE_ROLE_ID
from utils import string_to_date, get_today_date, create_message
from db import create, get_users_by_date
from typing import Generator


async def add_user_birthday(context: Context, raw_birth_date: str, user: str) -> str:
    try:
        user = await context.guild.fetch_member(int(user[2:-1]))
    except Exception:
        return 'Инвалидный юзернейм, <@291205539562651648> пидор'

    gender = 'M'
    if user.get_role(FEMALE_ROLE_ID):
        gender = 'F'

    birth_date = string_to_date(raw_birth_date)
    if not birth_date:
        return 'Инвалидная дата, хватит ломать бота'
    try:
        created = create(user.id, birth_date, gender)
    except Exception as e:
        print(e)
        return '<@237542033697406986> твоя хуйня опять развалилась'
    if created:
        return f'День рождения для <@{user.id}> добавлен'
    return f'День рождения для <@{user.id}> уже добавлен'


def create_msg_for_birthday_boys() -> Generator:
    today_date = get_today_date()
    users = get_users_by_date(today_date)
    for user in users:
        yield create_message(user['user_id'], user['gender'])
