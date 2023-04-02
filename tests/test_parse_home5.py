from homework_parser import start_parse
from models import card


def test_parse():
    save_path = 'results/home5.csv'
    start_parse(save_path, card.get_one(name='Монетизация', deadline='12.03.2023'))
