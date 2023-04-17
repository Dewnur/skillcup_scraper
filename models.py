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
    ts_deadline: float = None


class PersonCard(NamedTuple):
    person_id: int
    card_id: int
    is_done: int = 0
    total_done: str = '0'
    id: int = None


class Person(NamedTuple):
    name: str
    id: int = None
    rate: str = ''
    tg_url: str = ''
    tg_name: str = ''


class Comment(NamedTuple):
    task_id: int
    person_id: int
    content: str
    overdue: bool
    ts_create: float
    id: int = None
