from datetime import datetime
import json


def add_date_to_json(date, user):
    birthday_date = string_to_date(date)
    if not birthday_date:
        return 'Невалидная дата, попробуйте снова.'

    with open('db.json', encoding='utf8') as db:
        data = json.load(db)
    node = {'date': date, 'user': user}
    birth_monthname = birthday_date.strftime('%B')
    data[birth_monthname].append(node)
    with open('db.json', 'w', encoding='utf8') as db:
        json.dump(data, db)
    return f'День рождения для {user} добавлен!'


def string_to_date(date):
    try:
        date = datetime.strptime(date, '%d.%m')
    except ValueError:
        return False
    return date


def check_today_birthdays():
    today_timestamp = datetime.now()
    today_date = today_timestamp.strftime('%d.%m')
    today_monthname = today_timestamp.strftime('%B')

    with open('db.json', encoding='utf8') as db:
        data = json.load(db)

    month_birthdays = data[today_monthname]
    if not month_birthdays:
        return

    today_birthdays = set()
    for month_birthday in month_birthdays:
        if month_birthday['date'] == today_date:
            today_birthdays.add(month_birthday['user'])
    return today_birthdays
