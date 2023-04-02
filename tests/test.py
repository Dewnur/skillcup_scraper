from models.person import Person
from db_models_manager import *
from models.card import Card

def test_start():
    person_list = fetchall(Person, rate='ВИП')
    print(person_list)
    print(fetchone(Card, name='Монетизация', deadline='12.03.2023'))
