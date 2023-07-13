from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR.joinpath("data")
DB_PATH = DATA_DIR.joinpath('db.sqlite3')

PAGE_SIZE = 10
