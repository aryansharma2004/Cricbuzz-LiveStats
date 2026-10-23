"""
Database connection handler for Cricbuzz LiveStats.
Provides centralized SQLite connection management and query execution.
"""

import sqlite3
import os
import pandas as pd
from config import DB_PATH


def get_connection():
    """Create and return a database connection with foreign key support."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database with schema and seed data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

    seed_path = os.path.join(base_dir, 'database', 'seed_data.sql')
    if os.path.exists(seed_path):
        with open(seed_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

    conn.commit()
    conn.close()


def execute_query(query, params=None):
    """Execute a SELECT query and return results as a pandas DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params or [])
        return df
    except Exception as e:
        raise e
    finally:
        conn.close()


def execute_insert(query, params=None):
    """Execute an INSERT query and return the new row ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_update(query, params=None):
    """Execute an UPDATE or DELETE query and return rows affected."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
