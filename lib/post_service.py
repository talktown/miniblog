from typing import List

from lib.db import get_connection
from lib.utils import get_now


def add_post(title, content, enabled):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO posts (title, content, enabled, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                   (title, content, enabled, get_now(), get_now()))
    last_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return last_id


def get_post(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts where id = ?", (id, ))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row


def get_posts(page, page_size) -> (List, int):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM posts order by id desc limit ?, ?", (offset, page_size))
    rows = cursor.fetchall()

    cursor.execute("SELECT count(*) as total FROM posts")
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return rows, total


def get_enabled_posts(page, page_size) -> (List, int):
    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size
    cursor.execute("SELECT * FROM posts where enabled = 1 order by id desc limit ?, ?", (offset, page_size))
    rows = cursor.fetchall()

    cursor.execute("SELECT count(*) as total FROM posts where enabled = 1")
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return rows, total


def update_post(id, title, content, enabled):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE posts SET title=?, content=?, enabled=?, updated_at=? WHERE id=?",
                   (title, content, enabled, get_now(), id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_post(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM posts WHERE id=?", (id,))

    conn.commit()
    cursor.close()
    conn.close()
