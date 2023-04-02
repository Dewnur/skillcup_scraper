import db
import csv
from models import card

def load_person(path):
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            db.insert(
                'Person',
                {
                    'name': row['name'],
                    'rate': row['rate'],
                    'tg_url': row['tg_url'],
                    'tg_name': row['tg_name']
                }
            )

def load_card_tasks(path):
    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
        card_name_list, deadline_list, task_list = [], [], []
        for row in reader:
            card_name_list.append(row['card_name'])
            deadline_list.append(row['deadline'])
            task_list.append(row['task'])
        card_name = list(filter(None, card_name_list))[0]
        deadline = list(filter(None, deadline_list))[0]
        TASK_LIST = list(filter(None, task_list))
        db.insert('Card', {'name': card_name, 'deadline': deadline})
        card_id = card.get_one(name=card_name, deadline=deadline).id
        for t in TASK_LIST:
            db.insert('Task', {'card_id': card_id, 'name': t})

