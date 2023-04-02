from typing import List, NamedTuple, Optional

import db


class Task(NamedTuple):
    id: int
    name: int
    card_id: int


class Card(NamedTuple):
    id: int
    name: str
    deadline: str
    deadline_datetime: int = None


def get_one(**kwargs) -> Card:
    """Возвращает первую найденную запись"""
    condition = []
    for key, value in kwargs.items():
        condition.append((key, value))
    card = db.fetchall('Card', ['id', 'name', 'deadline', 'deadline_datetime'], condition)[0]
    return Card(
        id=card['id'],
        name=card['name'],
        deadline=card['deadline'],
        deadline_datetime=card['deadline_datetime']
    )


def get_tasks_by_card(card_id: int):
    tasks = db.fetchall('Task', ['id', 'name', 'card_id'], [('card_id', card_id)])
    task_list = []
    for t in tasks:
        task_list.append(
            Task(
                id=t['id'],
                name=t['name'],
                card_id=t['card_id']
            )
        )
    return task_list


def string_to_timestemp(datetime: str) -> int:
    pass
