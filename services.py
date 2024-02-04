from config import FEMALE_ROLE_ID
from utils.jinja_utils import get_birthday_message, get_paste_message, get_gay_joke_message
from db import create, get_users_by_date, delete
from typing import Generator
from discord import Member


class BirthdayService:

    def __init__(self, user: Member):
        self.user = user

    @property
    def gender(self):
        gender = 'M'
        if self.user.get_role(FEMALE_ROLE_ID):
            gender = 'F'
        return gender

    def add_user_birthday(self, birth_date: str) -> str:
        try:
            created = create(self.user.id, birth_date, self.gender)
        except Exception as e:
            print(e)
            return '<@237542033697406986> твоя хуйня опять развалилась'
        if created:
            return f'День рождения для <@{self.user.id}> добавлен'
        return f'День рождения для <@{self.user.id}> уже добавлен'

    def delete_user_birthday(self):
        deleted = delete(self.user.id)
        if deleted:
            return f'День рождения для <@{self.user.id}> удален'
        return f'День рождения для <@{self.user.id}> не был добавлен'

    @classmethod
    def create_msg_for_birthday_boys(cls, today_date) -> Generator:
        # TODO fix dependency of db
        users = get_users_by_date(today_date)
        for user in users:
            yield get_birthday_message(user['user_id'], user['gender'])


class PasteService:

    @staticmethod
    def get_paste(paste_name: str, users: list[Member]) -> str:
        users_id = [user.id for user in users]
        message = get_paste_message(paste_name, users_id)
        return message

    @staticmethod
    def get_gay_joke(users: list[Member]):
        users_id = [user.id for user in users]
        message = get_gay_joke_message(users_id)
        return message
