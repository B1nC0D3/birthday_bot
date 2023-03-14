from datetime import datetime


def validate_date(date):
    if not date:
        return None
    try:
        date = datetime.strptime(date, '%d.%m')
    except ValueError:
        return None
    return date.strftime('%d.%m')


def get_today_date() -> str:
    today_date = datetime.now().strftime('%d.%m')
    return today_date
