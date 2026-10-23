"""
API client and fallback tests.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.cricbuzz_client import CricbuzzClient


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = CricbuzzClient()

    def test_client_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.max_retries, 3)

    def test_mock_matches_fallback(self):
        data = self.client._get_mock_matches()
        self.assertIn("typeMatches", data)
        self.assertIsInstance(data["typeMatches"], list)
        self.assertGreater(len(data["typeMatches"]), 0)


if __name__ == '__main__':
    unittest.main()
