from typing import List, NamedTuple, Optional

import db


class Person(NamedTuple):
    id: int
    name: str
    rate: str
    tg_url: str
    tg_name: str


class PersonCard(NamedTuple):
    person_id: int
    card_id: int
    total: int = None
    total_string: str = ''
    id: int = None


def get_all() -> List[Person]:
    persons = db.fetchall(
        'Person',
        [
            'id',
            'name',
            'rate',
            'tg_url',
            'tg_name'
        ]
    )
    persons_list = []
    for p in persons:
        persons_list.append(
            Person(
                id=p['id'],
                name=p['name'],
                rate=p['rate'],
                tg_url=p['tg_url'],
                tg_name=p['tg_name']
            )
        )
    return persons_list
