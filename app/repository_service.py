from typing import List

import requests

from app.repository_model import Repository, RepositoriesCollection


def get_repository_data(repository_name: str) -> Repository:
    url = f"https://api.github.com/search/repositories?q={repository_name}"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json().get('items', [])
        if len(repositories) > 0:
            repository_data = repositories[0]
            repository = _get_repository_from_data(repository_data)

            RepositoriesCollection.insert_new_document(repository)

            return repository
        else:
            raise LookupError(f"Repository with name {repository_name} not found.")
    else:
        raise Exception(f"Error while retrieving repository data {response.status_code}.")


def _get_repository_from_data(repository_data: dict) -> Repository:
    languages = _get_repository_languages(repository_data['languages_url'])

    repository = Repository(
        id=repository_data['id'],
        name=repository_data['name'],
        stars=repository_data['stargazers_count'],
        owner=repository_data['owner']['login'],
        description=repository_data['description'],
        forks_url=repository_data['forks_url'],
        languages=languages,
        number_of_forks=repository_data['forks_count'],
        topics=repository_data['topics'],
    )

    return repository


def _get_repository_languages(languages_url: str) -> List[str]:
    response = requests.get(languages_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error while retrieving repository data {response.status_code}.")
