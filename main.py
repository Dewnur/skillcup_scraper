from db_models_manager import *
from homework_scraper import start_scraping_homework
from models import *
from word_report_generator import WordReportGenerator
from homework_scraper import driver
# TODO: Перед запуском новой партии обновить даты и ts у карточек

if __name__ == "__main__":
    # start_scraping_homework(fetchone(Card, name='Активное продвижение', deadline_date='05.03.2023'))

    persons = fetchall(Person)
    for person in persons:
        wrp = WordReportGenerator(f'results/{person.name}.docx')
        wrp.generate_report(person)

    driver.close()
    driver.quit()