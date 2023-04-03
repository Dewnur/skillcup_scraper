from parser import start_parse
from models import *
from db_models_manager import *


def test_parse():
    save_path = 'results/home5.csv'
    start_parse(save_path, fetchone(Card, name='Монетизация', deadline='12.03.2023'))
