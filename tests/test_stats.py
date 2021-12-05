import unittest
import requests
from main import get_stats

class TestStats(unittest.TestCase):
    def testAPI(self):
        response = requests.get("https://api.chess.com/pub/player/PrathamRex/stats")
        self.assertEqual(response.status_code, 200)
