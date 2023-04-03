from datetime import datetime
from typing import NamedTuple


class Task(NamedTuple):
    id: int
    name: int
    card_id: int


class Card(NamedTuple):
    name: str
    deadline: str
    id: int = None
    deadline_datetime: int = None


class PersonCard(NamedTuple):
    person_id: int
    card_id: int
    total: int = None
    total_string: str = ''
    id: int = None


class Person(NamedTuple):
    id: int
    name: str
    rate: str
    tg_url: str
    tg_name: str


class Comment(NamedTuple):
    id: int
    task_id: int
    person_id: int
    content: str
    overdue: bool
    create_datetime: datetime
