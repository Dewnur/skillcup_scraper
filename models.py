from datetime import datetime
from typing import NamedTuple


class Task(NamedTuple):
    id: int
    name: int
    card_id: int
    sequence_number: int


class Card(NamedTuple):
    name: str
    deadline_date: str
    deadline_time: str = ''
    id: int = None
    ts_deadline: float = None
    sequence_number: int = 0


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
    subscriber_count: int = 0


class Comment(NamedTuple):
    task_id: int
    person_id: int
    sequence_number: int
    content: str = ''
    overdue: bool = False
    ts_create: float = 0
    id: int = None
