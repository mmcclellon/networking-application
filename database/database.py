import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sold.db')


def get_connection():
    # Open a new connection every time. sqlite3 connections should not be shared
    # between threads, and the server runs one thread per client.
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # lets us read columns by name
    return connection


def init_db():
    # Create the tables if they don't exist yet. Safe to call every time the server starts.
    connection = get_connection()
    try:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt          TEXT NOT NULL,
                created_at    TEXT NOT NULL
            )
        ''')
        connection.commit()
    finally:
        connection.close()


def create_user(username, password_hash, salt):
    # Returns True if the account was created, False if the username is already taken
    connection = get_connection()
    try:
        connection.execute(
            'INSERT INTO users (username, password_hash, salt, created_at) VALUES (?, ?, ?, ?)',
            (username, password_hash, salt, datetime.now(timezone.utc).isoformat())
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        # Raised by the UNIQUE rule on username
        return False
    finally:
        connection.close()


def get_user(username):
    # Returns the user's row, or None if no account has that username
    connection = get_connection()
    try:
        return connection.execute(
            'SELECT id, username, password_hash, salt FROM users WHERE username = ?',
            (username,)
        ).fetchone()
    finally:
        connection.close()
