import sqlite3


def db_connect():
    return sqlite3.connect("sql_convert_tool.db")


def create_table():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sql_convert_tool (
            id INTEGER PRIMARY KEY,
            sql TEXT NOT NULL,
            converted_sql TEXT NOT NULL,
            hash_map TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()