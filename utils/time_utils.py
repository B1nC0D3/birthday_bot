import datetime
from config import HOUR, MIN


def get_today_date() -> str:
    today_date = datetime.datetime.now().strftime('%d.%m')
    return today_date


def get_task_start_time():
    utc = datetime.timezone.utc
    time = datetime.time(hour=HOUR, minute=MIN, tzinfo=utc)
    return time
