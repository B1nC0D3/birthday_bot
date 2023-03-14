from tinydb import TinyDB, Query
from config import PATH_TO_DB

db = TinyDB(PATH_TO_DB)
User = Query()


def create(user_id: int, birth_date: str, gender: str) -> bool:
    if db.search(User.user_id == user_id):
        return False
    db.insert({'user_id': user_id,
               'birth_date': birth_date,
               'gender': gender})
    return True


def get_users_by_date(today_date: str) -> list[dict]:
    birthday_boys = db.search(User.birth_date == today_date)
    return birthday_boys
