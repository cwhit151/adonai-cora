import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_NAME = "cora.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Initializes the database with tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    # Posts Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            platform TEXT NOT NULL,
            scheduled_at TEXT,
            caption TEXT,
            hashtags TEXT,
            media_path TEXT,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Media Assets Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS media_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_path TEXT NOT NULL,
            source TEXT NOT NULL,
            tags TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Publish Logs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS publish_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            attempted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            result TEXT,
            message TEXT,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    ''')

    conn.commit()
    conn.close()

def run_query(query, params=()):
    """Executes a query and returns the results as a DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"Error running query: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def execute_command(command, params=()):
    """Executes a command (INSERT, UPDATE, DELETE)."""
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute(command, params)
        conn.commit()
        last_row_id = c.lastrowid
        return last_row_id
    except Exception as e:
        print(f"Error executing command: {e}")
        return None
    finally:
        conn.close()
