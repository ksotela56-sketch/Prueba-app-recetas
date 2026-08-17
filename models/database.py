import sqlite3

import config


def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None, schema_path=None):
    conn = get_connection(db_path)
    with open(schema_path or config.SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
