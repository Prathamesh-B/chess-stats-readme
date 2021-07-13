import os
from github import Github, GithubException
import re
import requests

GH_TOKEN = os.getenv("INPUT_GH_TOKEN")
CHESS_USERNAME = os.getenv("INPUT_CHESS_USERNAME")
