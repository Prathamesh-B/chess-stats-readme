import unittest
import requests
from main import get_stats, decode_readme, generate_new_readme


class TestStats(unittest.TestCase):
    def test_api(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get("https://api.chess.com/pub/player/PrathamRex/stats", headers=headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_best_ratings(self):
        stats = get_stats("PrathamRex", "best")

        self.assertTrue(stats)

        self.assertIn("Rapid", stats)
        self.assertIn("Blitz", stats)
        self.assertIn("Bullet", stats)

    def test_last_ratings(self):
        stats = get_stats("PrathamRex", "last")

        self.assertTrue(stats)

        self.assertIn("Rapid", stats)
        self.assertIn("Blitz", stats)
        self.assertIn("Bullet", stats)

    def test_decode_readme(self):
        result = decode_readme("SGVsbG8gd29ybGQh\n")
        self.assertEqual(result, "Hello world!")

    def test_generate_new_readme(self):
        stats = "**♟️ My Chess.com Stats** \n\n> ⏲️ Rapid: 1500\n>\n> ⚡ Blitz: 1500\n>\n> 💣 Bullet: 1500\n>\n"
        old_readme = "Hello world!\n<!--START_SECTION:Chess-->\nPrevious chess stats\n<!--END_SECTION:Chess-->\n"
        
        result = generate_new_readme(stats, old_readme)
        
        expected_result = "Hello world!\n<!--START_SECTION:Chess-->\n**♟️ My Chess.com Stats** \n\n> ⏲️ Rapid: 1500\n>\n> ⚡ Blitz: 1500\n>\n> 💣 Bullet: 1500\n>\n\n<!--END_SECTION:Chess-->\n"
        
        print("Actual Result:")
        print(result)
        print("Expected Result:")
        print(expected_result)

        self.assertEqual(result, expected_result)

    def test_generate_new_readme_no_changes(self):
        stats = "**♟️ My Chess.com Stats** \n\n> ⏲️ Rapid: 1500\n>\n> ⚡ Blitz: 1500\n>\n> 💣 Bullet: 1500\n>\n"
        old_readme = "Hello world!\n<!--START_SECTION:Chess-->\n**♟️ My Chess.com Stats** \n\n> ⏲️ Rapid: 1500\n>\n> ⚡ Blitz: 1500\n>\n> 💣 Bullet: 1500\n>\n\n<!--END_SECTION:Chess-->\n"
        
        result = generate_new_readme(stats, old_readme)
        
        print("Actual Result:")
        print(result)
        print("Expected Result:")
        print(old_readme)

        self.assertEqual(result, old_readme)