from db_models_manager import *
from homework_scraper import start_scraping_homework
from models import *
from tools.date_preprocessor import string_to_timestamp
from tools.db_loader import load_person, load_cards
from word_report_generator import WordReportGenerator

# TODO: Перед запуском новой партии обновить даты и ts у карточек

if __name__ == "__main__":
    scraping = True
    report = True
    loader = False
    card_scraping = fetchone(Card, name='Домашнее задание', deadline_date='07.05.2023')
    if card_scraping is None:
        raise Exception("Карточка не найдена")
    if scraping:
        start_scraping_homework(card_scraping)
    if report:
        persons = fetchall(Person)
        for person in persons:
            cards = [
                (fetchone(Card, name='Домашнее задание', deadline_date='23.04.2023')),
                (fetchone(Card, name='Домашнее задание', deadline_date='30.04.2023')),
                (fetchone(Card, name='Домашнее задание', deadline_date='07.05.2023')),
            ]
            wrp = WordReportGenerator(f'results/', cards=cards)
            wrp.generate_report(person)
    if loader:
        load_person('template/persons-4.csv')
        load_cards('template/cards-4.csv')

    # cards = fetchall(Card)
    # for c in cards:
    #     datatime = c.deadline_date + ' ' + c.deadline_time
    #     update(c, ts_deadline=string_to_timestamp(datatime, "%d.%m.%Y %H:%M"))