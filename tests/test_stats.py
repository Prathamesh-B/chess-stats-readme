import unittest
import requests
from main import get_stats


class TestStats(unittest.TestCase):
    def test_api(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get("https://api.chess.com/pub/player/PrathamRex/stats", headers=headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_best_ratings(self):
        self.assertTrue(get_stats("PrathamRex", "best"))

    def test_last_ratings(self):
        self.assertTrue(get_stats("PrathamRex", "last"))
