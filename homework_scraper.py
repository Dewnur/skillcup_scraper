import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from db_models_manager import *
from models import *
from tools.date_preprocessor import *
from selenium.webdriver.chrome.service import Service

# TODO: Вынести в переменные окружения
URL_LOGIN = 'https://oauth-vamvtg.skillcup.ru/login'

URL_DASHBOARD = 'https://vamvtg.skillcup.ru/dashboard'

options = webdriver.ChromeOptions()

# options.add_argument(fake_useragent.UserAgent().random)
options.add_argument("--headless")
# TODO: Сделать отдельный модуль для инициализации driver
s = Service('Users\Dewnur\Desktop\skill_pars\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(
    service=s,
    options=options
)


def login():
    """Авторизация"""
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys('evddkv@gmail.com')
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys('99Yg6VrJ')
    driver.find_element(By.CLASS_NAME, 'button').click()


def start_scraping_homework(card: Card):  # Передавать карточку
    try:
        driver.get(url=URL_LOGIN)
        time.sleep(4)
        login()
        time.sleep(4)
        persons = fetchall(Person)
        for person in persons:
            driver.get(url=URL_DASHBOARD)  # Открыть дашборд
            sleep_while(False, "[class='sc-preloader']")  # Экран загрузки "Авторизация"
            sleep_while(True, "[class='sc-input sc-input--empty']")  # Элемент поиска
            filter = driver.find_element(By.CLASS_NAME, 'filter')
            sc_input = filter.find_element(By.CSS_SELECTOR, 'input')
            sc_input.send_keys(person.name)  # Ввод Имя Фамилия
            sleep_while(False, "[class='userstatistics userstatistics--is-loading']")
            userstat_content = driver.find_element(By.CLASS_NAME, 'userstatistics__content')
            sleep_while(False, "[class='sc-preloader']", upper_node=userstat_content)
            sleep_while(True, "td", upper_node=userstat_content)
            userstat_content.find_element(By.CSS_SELECTOR, 'td').click()
            time.sleep(1)
            driver.find_elements(By.CLASS_NAME, 'tabs__item')[6].click()  # Клик по закладке `Домашнее задание`
            details_container = driver.find_element(
                By.CSS_SELECTOR,
                "[class='details__container details__container--open']"
            )
            sleep_while(False, "[class='sc-preloader']", upper_node=details_container)
            open_card(card)
            time.sleep(1)
            print(person.name)
            person_card = {
                'person_id': person.id,
                'card_id': card.id,
            }
            if not fetchone(PersonCard, **person_card):
                insert(PersonCard(**person_card))
            if not check_open_card():  # Поиск в `Задано`
                click_dropdown(0)
                open_card(card)
                time.sleep(1)
            if not check_open_card():  # Поиск в `Просрочено`
                click_dropdown(1)
                open_card(card)
                time.sleep(1)
            if not check_open_card():  # Нет ответа не на одно задание
                continue
            time.sleep(1)
            person_card = fetchone(PersonCard, **person_card)
            extract_card(person_card)
            counting_completed_tasks(person_card)
        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def check_open_card() -> bool:
    """Проверяет, открыта ли карточка с заданиями"""
    check = driver.find_elements(By.CSS_SELECTOR, "[class='userstatistics__before-table-info']")
    if bool(check):
        details_container = driver.find_elements(By.CSS_SELECTOR,
                                                 "[class='details__container details__container--open']")[1]
        sleep_while(False, "[class='sc-preloader']", upper_node=details_container)
    return bool(len(check))


def open_card(card: Card):
    """Поиск и открытие карточки"""
    table_tbody = driver.find_elements(By.CLASS_NAME, 'userstatistics-table__tbody')
    check_table_empty = bool(len(table_tbody[1].find_elements(By.CSS_SELECTOR, "[class='empty']")))
    if check_table_empty:
        print('Карточек нет')
        return
    table_trs = table_tbody[1].find_elements(By.CSS_SELECTOR, 'tr')
    for tr in table_trs:
        td_name = tr.find_element(By.CSS_SELECTOR, "[class='userstatistics-table__td']").text
        td_deadline = tr.find_element(By.CLASS_NAME, 'userstatistics-table__td--date').text
        if td_name == card.name and td_deadline == card.deadline_date:
            tr.find_element(By.CSS_SELECTOR, 'td').click()
            break


def extract_card(person_card: PersonCard) -> None:
    """Проходит циклом по всем выполненным задачам в карточке."""
    selector_table_tr = "[class='userstatistics-table__tr userstatistics-table__tr--clickable']"
    table_tbody = driver.find_elements(By.CSS_SELECTOR, "[class='userstatistics-table__tbody']")[2]
    # Количество выполненных заданий
    range_completed_tasks = len(table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr))
    print("Парсинг задания")
    for i in range(range_completed_tasks):
        tr = table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr)
        # Получение названия задания
        task_name = tr[i].find_element(
            By.CSS_SELECTOR,
            "[class='userstatistics-table__td userstatistics-table__td--content-name']"
        ).text
        # Клик по заданию
        tr[i].find_element(By.CSS_SELECTOR, 'td').click()
        # Ожидание прогрузки окна комментариев
        sleep_while(True, "[class='comment-list']")
        extract_task(person_card, task_name)
        tr = table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr)
        tr[i].find_element(By.CSS_SELECTOR, 'td').click()
    print('Возврат строки')


def extract_task(person_card: PersonCard, task_name: str) -> None:
    """Извлекает комментарии из задания"""
    print("Парсинг комментов")
    task = fetchone(Task, name=task_name, card_id=person_card.card_id)
    if task is None:
        raise Exception('Задание не найдено')
    extract_comments(task, person_card)


def extract_comments(task: Task, person_card: PersonCard) -> None:
    card = fetchone(Card, id=person_card.card_id)
    ts_deadline = card.ts_deadline
    comments_element = driver.find_elements(By.CSS_SELECTOR, "[class='comment-list']")
    comments_blocks = comments_element[0].find_elements(By.CSS_SELECTOR, "[class='comment-list__comment']")
    comments_list = []
    for com in comments_blocks:
        comment_text = com.find_element(By.CSS_SELECTOR, "[class='comment-list__text']").text
        comment_date = com.find_element(By.CSS_SELECTOR, "[class='comment-list__date']").text
        comments_list.append((comment_text, comment_date))
    comments_list = list(set(comments_list))
    comments_list.reverse()
    for i, (content, date) in enumerate(comments_list):
        ts_create = string_to_timestamp(date, "%d.%m.%Y %H:%M")
        overdue = True if ts_create > ts_deadline else False
        new_comment_dict = {
            'person_id': person_card.person_id,
            'task_id': task.id,
            'content': content,
            'ts_create': ts_create,
            'overdue': overdue,
            'sequence_number': i,
        }
        new_comment = fetchone(Comment, **new_comment_dict)
        if new_comment is None:
            insert(Comment(**new_comment_dict))


def sleep_while(exist: bool, css_selector: str, time_sleep=1, upper_node=None) -> None:
    """
    Создает задержку для прогрузки элементов страницы
    exist: True - Ждать пока элемент не появится, False - Ждать пока элемент существует
    """
    while True:
        elem = None
        if upper_node is None:
            elem = driver.find_elements(By.CSS_SELECTOR, css_selector)
        else:
            elem = upper_node.find_elements(By.CSS_SELECTOR, css_selector)
        if bool(elem) == exist:
            time.sleep(time_sleep)
            break


def safe_click(css_selector: str, num_retries: int, time_sleep=1) -> None:
    for attempt_no in range(num_retries):
        try:
            driver.find_elements(By.CSS_SELECTOR, css_selector)[0].click()
            return
        except ElementClickInterceptedException:
            if attempt_no < (num_retries - 1):
                print("Error: element click intercepted")
                time.sleep(time_sleep)
            else:
                raise Exception('Ошибка клика')


def counting_completed_tasks(person_card: PersonCard):
    tasks = fetchall(Task, card_id=person_card.card_id)
    if tasks is None:
        raise TypeError
    card = fetchone(Card, id=person_card.card_id)
    comments = []
    for t in tasks:
        coms = fetchall(Comment, person_id=person_card.person_id, task_id=t.id)
        if coms:
            comments.extend(coms)
    count_person_tasks = len(list(set([com.task_id for com in comments if com.task_id is not None])))
    is_done = 1 if len(tasks) == count_person_tasks else 0
    total_done = card.sequence_number if len(tasks) == count_person_tasks else f'{count_person_tasks}из{len(tasks)}'
    update(
        person_card,
        is_done=is_done,
        total_done=total_done,
    )


def click_dropdown(item_index: int) -> None:
    safe_click("[class='sc-dropdown__button sc-dropdown__button--hidden']", num_retries=3)
    time.sleep(1)
    dropdown = driver.find_element(By.CSS_SELECTOR,
                                   "[class='sc-dropdown__list sc-dropdown__list--visible']")
    time.sleep(1)
    dropdown.find_elements(By.CSS_SELECTOR, "[class='sc-dropdown__item']")[item_index].click()
    time.sleep(1)
