import os.path
import shutil
import time
from datetime import datetime
import markdown

from lib.config import DB_EMPTY_PATH, DB_PATH
from lib.db import create_tables


def get_now():
    return int(time.time())


def format_timestamp(timestamp: int):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime('%d %b %Y')


def parse_markdown(text: str):
    return markdown.markdown(text)


def init_database():
    if not os.path.exists(DB_PATH):
        shutil.copy2(DB_EMPTY_PATH, DB_PATH)

    create_tables()
