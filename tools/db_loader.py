import csv

from db_models_manager import *
from models import *
from tools.date_preprocessor import string_to_timestamp


def load_person(path: str) -> None:
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            person_dict = {
                'name': row['name'],
                'rate': row['rate'],
                'tg_url': row['tg_url'],
                'tg_name': row['tg_name'],
                'subscriber_count': row['subscriber_count'],
            }
            person = fetchone(Person, name=person_dict['name'])
            if person:
                update(person, **person_dict)
            else:
                insert(Person(**person_dict))


def load_cards(path: str) -> None:
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            card_dict = {
                'name': row['name'],
                'deadline_date': row['deadline_date'],
                'deadline_time': row['deadline_time'],
                'ts_deadline': string_to_timestamp(
                    f"{row['deadline_date']} {row['deadline_time']}",
                    date_format='%d.%m.%Y %H:%M'
                ),
                'sequence_number': row['sequence_number'],
            }
            cars = fetchone(Card, sequence_number=card_dict['sequence_number'])
            if cars:
                update(cars, **card_dict)
            else:
                insert(Card(**card_dict))
