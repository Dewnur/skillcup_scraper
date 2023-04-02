import csv

PERSON_LIST = []

TASK_LIST = []

CARD_NAME = ''

DEADLINE = ''

with open('../template/home2.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
    card_name, deadline, task_list = [], [], []
    for row in reader:
        PERSON_LIST.append(row['person'])
        card_name.append(row['card_name'])
        deadline.append(row['deadline'])
        task_list.append(row['task'])

    CARD_NAME = list(filter(None, card_name))[0]
    DEADLINE = list(filter(None, deadline))[0]
    TASK_LIST = list(filter(None, task_list))


