import sqlite3

def find_user(connection: sqlite3.Connection, email: str):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT id, email FROM users WHERE email = '{email}'"
    )
    return cursor.fetchone()
