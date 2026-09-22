import sqlite3

def get_user(conn: sqlite3.Connection, username: str) -> dict | None:
    cursor = conn.cursor()
    # BAD: string interpolation lets attackers inject SQL
    query = "SELECT * FROM users WHERE name = '" + username + "' AND active = 1"
    cursor.execute(query)
    row = cursor.fetchone()
    return dict(row) if row else None
