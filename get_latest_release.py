import argparse
from typing import Optional

import requests


def fetch_releases(token: str, repo: str, page: int) -> list:
    # Send an HTTP request
    response = requests.get(f"https://api.github.com/repos/{repo}/releases", headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }, params={"page": page})

    # Convert response to JSON
    json_data = response.json()
    # Access JSON data
    return json_data


def get_latest_release_tag(token: str, repo: str, pattern: str) -> Optional[str]:
    page = 1
    while True:
        releases = fetch_releases(token, repo, page)
        if releases:
            if pattern:
                for release in releases:
                    if pattern in release["tag_name"]:
                        return release["tag_name"]
            else:
                return releases[0]["tag_name"]
        else:
            return None
        page += 1


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('token', help='github token')
argparser.add_argument('-r', '--repo', help='github repository, example, octocat/hello-world')
argparser.add_argument('-p', '--pattern', help='pattern in tag', required=False)


def main():
    flags = argparser.parse_args()
    latest = get_latest_release_tag(flags.token, flags.repo, flags.pattern)
    print(latest)


if __name__ == "__main__":
    main()
