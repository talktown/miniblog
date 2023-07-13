import time
from datetime import datetime
import markdown


def get_now():
    return int(time.time())


def format_timestamp(timestamp: int):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime('%d %b %Y')


def parse_markdown(text: str):
    return markdown.markdown(text)
