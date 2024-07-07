from dataclasses import dataclass, asdict
from typing import List

from app import db


@dataclass
class Repository:
    id: int
    name: str
    stars: int
    owner: str
    description: str
    forks_url: str
    languages: List[str]
    number_of_forks: int
    topics: List[str]


class RepositoriesCollection:
    @staticmethod
    def insert_new_document(repository: Repository):
        if db.repositories.find_one({'name': repository.name}) is None:
            db.repositories.insert_one(asdict(repository))
