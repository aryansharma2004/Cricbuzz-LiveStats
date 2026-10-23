"""
Database connection and schema tests.
"""

import unittest
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import get_connection, init_database, execute_query


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_database()

    def test_database_connection(self):
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_players_table_populated(self):
        df = execute_query("SELECT COUNT(*) AS count FROM players")
        self.assertFalse(df.empty)
        self.assertGreater(int(df['count'].iloc[0]), 0)

    def test_matches_table_populated(self):
        df = execute_query("SELECT COUNT(*) AS count FROM matches")
        self.assertFalse(df.empty)
        self.assertGreater(int(df['count'].iloc[0]), 0)

    def test_foreign_keys_enabled(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys;")
        res = cursor.fetchone()
        conn.close()
        self.assertEqual(res[0], 1)


if __name__ == '__main__':
    unittest.main()
