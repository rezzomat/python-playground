import requests
from config import github_token
from config import github_owner
from config import github_repo

header = {'Authorization': 'token ' + github_token}
BASE_URL = 'https://api.github.com/'


def get_request(endpoint):
    return requests.get(BASE_URL + endpoint, headers=header)


def post_request(url, data):
    return requests.post(BASE_URL + url, json=data, headers=header)


if __name__ == '__main__':
    data = {
        "title": "Found a serious bug",
        "body": "I'm having a problem with this.",
        "labels": [
            "bug"
        ]
    }

    endpoint = "repos/{owner}/{repo}/issues".format(owner=github_owner, repo=github_repo)
    response = get_request(endpoint)
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code, response.content)
