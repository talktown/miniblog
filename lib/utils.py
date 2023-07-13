import time
from datetime import datetime


def get_now():
    return int(time.time())


def timestamp_to_date(timestamp: int):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime('%d %b %Y')
