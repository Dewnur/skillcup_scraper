from db_models_manager import *
from models import *


def test_start():
    person_list = fetchall(Person, rate='ВИП')
    print(person_list)
    print(fetchone(Card, name='Монетизация', deadline='12.03.2023'))
    c = Card(name='TEST', deadline='11.11.1111')
    insert(c)
    c = fetchone(Card, name='TEST')
    update(c, name='TESTTT')
    c = fetchone(Card, deadline='11.11.1111')
    delete(c)