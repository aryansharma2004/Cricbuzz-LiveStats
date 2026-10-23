"""
Test suite executing all 25 SQL practice questions.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_connection import init_database
from services.stats_service import SQL_QUERIES, run_query


class TestSQLQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_database()

    def test_all_25_queries_execute(self):
        self.assertEqual(len(SQL_QUERIES), 25, "Expected 25 SQL queries in catalog.")

        for qid in range(1, 26):
            with self.subTest(query_id=qid):
                try:
                    df, info = run_query(qid)
                    self.assertIsNotNone(df, f"Query {qid} returned None")
                    # Assert no exception was thrown during SQL execution
                except Exception as e:
                    self.fail(f"Query {qid} ({SQL_QUERIES[qid]['title']}) raised exception: {e}")


if __name__ == '__main__':
    unittest.main()
