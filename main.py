import os
import sys
from github import Github, GithubException
import re
import base64
import requests

GH_TOKEN = os.getenv("INPUT_GH_TOKEN")
CHESS_USERNAME = os.getenv("INPUT_CHESS_USERNAME")
REPOSITORY = os.getenv("INPUT_REPOSITORY")
RATING_TYPE = os.getenv("INPUT_RATING_TYPE")
print(f"Env: {GH_TOKEN}, {CHESS_USERNAME}, {REPOSITORY}, {RATING_TYPE}")


START_COMMENT = "<!--START_SECTION:Chess-->"
END_COMMENT = "<!--END_SECTION:Chess-->"
listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"


def decode_readme(data: str) -> str:
    """Decode the contents of old readme"""
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, "utf-8")


def get_stats(username: str, type: str) -> str:
    """Get player stats"""
    url = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        print(f"API Response: {response.status_code}")
        print(f"API Content: {response.content}")
        if response.status_code == 200:
            stats_list = ["chess_rapid", "chess_blitz", "chess_bullet"]
            ratings = {}
            string = "**♟️ My Chess.com Stats** \n\n"
            for i in stats_list:
                query = f'response.json()["{i}"]["{type}"]["rating"]'
                ratings[i] = eval(query)
            string += f"> ⏲️ Rapid: {ratings['chess_rapid']}\n>\n"
            string += f"> ⚡ Blitz: {ratings['chess_blitz']}\n>\n"
            string += f"> 💣 Bullet: {ratings['chess_bullet']}\n>\n"
            print(string)
            return string
        else:
            # Handle non-200 response code
            print(f"API error: {response}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        sys.exit(1)


def generate_new_readme(stats: str, readme: str) -> str:
    """Generate a new Readme.md"""
    stats_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
    return re.sub(listReg, stats_in_readme, readme)


if __name__ == "__main__":
    g = Github(GH_TOKEN)
    try:
        repo = g.get_repo(REPOSITORY)
        print("Repo",repo)
    except GithubException:
        print("Authentication Error. Try saving a GitHub Token in your Repo Secrets or Use the GitHub Actions Token, which is automatically used by the action.")
        sys.exit(1)
    contents = repo.get_readme()
    chess_stats = get_stats(CHESS_USERNAME, RATING_TYPE)
    rdmd = decode_readme(contents.content)
    new_readme = generate_new_readme(stats=chess_stats, readme=rdmd)
    if new_readme != rdmd:
        repo.update_file(
            path=contents.path,
            message="Update readme chess stats",
            content=new_readme,
            sha=contents.sha,
        )
        print("Success")
    else:
        print("No change")
