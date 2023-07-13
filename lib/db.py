import sqlite3

from lib.config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    return conn


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        create table if not exists posts(
            id integer not null primary key default 0,
            title text not null default '',
            content text not null default '',
            created_at integer not null default 0,
            updated_at integer not null default 0
        )
    ''')
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_tables()