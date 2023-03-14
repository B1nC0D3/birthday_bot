from discord.ext.commands.context import Context
from config import FEMALE_ROLE_ID
from utils.discord_utils import validate_discord_user
from utils.date_utils import validate_date, get_today_date
from utils.jinja_utils import get_birthday_message, get_paste_message
from db import create, get_users_by_date
from typing import Generator


async def add_user_birthday(context: Context, raw_birth_date: str, raw_user_id: str) -> str:
    birth_date = validate_date(raw_birth_date)
    if not birth_date:
        return 'Инвалидная дата, хватит ломать бота'

    user = await validate_discord_user(context, raw_user_id)
    if not user:
        return 'Юзер не найден'
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


async def get_paste(context: Context, raw_user_id: str):
    user = await validate_discord_user(context, raw_user_id)
    if not user:
        return 'Юзер не найден'
    message = get_paste_message(user.id)
    return message


def create_msg_for_birthday_boys() -> Generator:
    today_date = get_today_date()
    users = get_users_by_date(today_date)
    for user in users:
        yield get_birthday_message(user['user_id'], user['gender'])
