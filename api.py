import requests

from exceptions import GitHubApiError
from models import GitHubRepo


def create_query(languages, min_stars=50000):
    query = f"stars:>{min_stars} " + \
            " ".join(f"language:{language.strip()}" for language in languages)
    return query


def repos_with_most_stars(languages, sort="stars", order="desc"):
    query = create_query(languages)

    gh_api_repo_search_url = "https://api.github.com/search/repositories"

    params = {"q": query, "sort": sort, "order": order}
    response = requests.get(gh_api_repo_search_url, params)

    status_code = response.status_code
    if status_code != 200:
        raise GitHubApiError(status_code)

    items = response.json()["items"]
    return [GitHubRepo(item["name"], item["language"], item["stargazers_count"])
            for item in items]
