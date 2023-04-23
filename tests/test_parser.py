from models import PersonCard
from db_models_manager import *
from homework_scraper import counting_completed_tasks


def test_set_person_card_done(get_random_record):
    person_cards = fetchall(PersonCard)
    for pc in person_cards:
        counting_completed_tasks(pc)
