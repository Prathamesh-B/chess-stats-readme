import unittest
import requests
from main import get_stats


class TestStats(unittest.TestCase):
    def test_api(self):
        response = requests.get("https://api.chess.com/pub/player/PrathamRex/stats")
        self.assertEqual(response.status_code, 200)

    def test_best_ratings(self):
        self.assertTrue(get_stats("PrathamRex", "best"))

    def test_last_ratings(self):
        self.assertTrue(get_stats("PrathamRex", "last"))
