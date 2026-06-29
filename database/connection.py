import sqlite3

DB_NAME = "chat_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)