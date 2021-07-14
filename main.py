import os
from github import Github, GithubException
import re
import requests

GH_TOKEN = os.getenv("INPUT_GH_TOKEN")
CHESS_USERNAME = os.getenv("INPUT_CHESS_USERNAME")


def get_stats():
    response = requests.get(f"https://api.chess.com/pub/player/{CHESS_USERNAME}/stats")
    if response.status_code == 200:
        print("Work")


if __name__ == "__main__":
    get_stats()
    print(CHESS_USERNAME)
