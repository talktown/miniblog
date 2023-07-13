from lib.db import get_connection


def get(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM setting where name = ?", (name,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row["value"]


def get_all():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM setting")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
