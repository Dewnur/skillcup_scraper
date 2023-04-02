import csv
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from db_models_manager import *
from models import *

URL_LOGIN = 'https://oauth-vamvtg.skillcup.ru/login'

URL_DASHBOARD = 'https://vamvtg.skillcup.ru/dashboard'

options = webdriver.ChromeOptions()

# options.add_argument(fake_useragent.UserAgent().random)
options.add_argument("--headless")

driver = webdriver.Chrome(
    executable_path=r'Users\Dewnur\Desktop\skill_pars\chromedriver\chromedriver.exe',
    options=options
)


def write_row_csv(doc: dict, path: str):
    with open(path, 'a', errors='ignore', newline='') as file:
        fieldnames = list(doc.keys())
        writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames)
        writer.writerow(doc)


def write_html_file(driver: webdriver):
    pageSource = driver.page_source
    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(pageSource)
    fileToWrite.close()


def login(driver: webdriver):
    """Авторизация"""
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys('evddkv@gmail.com')
    password_input = driver.find_element(By.NAME, 'password')
    password_input.send_keys('qBXCgXhE')
    driver.find_element(By.CLASS_NAME, 'button').click()


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
        if td_name == card.name and td_deadline == card.deadline:
            tr.find_element(By.CSS_SELECTOR, 'td').click()
            break


def task_parse(driver: webdriver):
    """Достает комментарии из задания. Возвращает список комментариев"""
    print("Парсинг комментов")
    comments_element = driver.find_elements(By.CSS_SELECTOR, "[class='comment-list']")
    if bool(len(comments_element)):
        comments_list = comments_element[0].find_elements(By.CSS_SELECTOR, "[class='comment-list__comment']")
        comments = []
        for com in comments_list:
            comments.append(com.find_element(By.CSS_SELECTOR, "[class='comment-list__text']").text)
        comments.reverse()
        return comments
    else:
        pass


# def comment_parse(driver: webdriver) -> Comment:
#     print("Парсинг комментов")
#     comments_element = driver.find_elements(By.CSS_SELECTOR, "[class='comment-list']")
#     if bool(len(comments_element)):
#         comments_list = comments_element[0].find_elements(By.CSS_SELECTOR, "[class='comment-list__comment']")
#         comments = []
#         datetime_list = []
#         for com in comments_list:
#             comments.append(com.find_element(By.CSS_SELECTOR, "[class='comment-list__text']").text)
#             datetime_list.append(com.find_element(By.CSS_SELECTOR, "[class='comment-list__date']").text)
#         comments.reverse()
#         content = ''.join(list(set(comments)))
#         create_datetime = comment.string_datetime_to_timestamp(datetime_list[0])
#         overdue = 0
#         total = 0
#         total_string = ''
#         return comments
#     else:
#         pass


def get_row_dict(current_person: str, task_name_list: list) -> dict:
    temp = ['person']
    temp.extend(task_name_list)
    row_dict = {i: '' for i in temp}
    row_dict['person'] = current_person
    return row_dict


def set_row_dict_total(row_dict: dict, task_list):
    total = 0
    for task in task_list:
        if row_dict[task] != '':
            total += 1
    row_dict['total'] = total
    if total == 0:
        row_dict['total_name'] = 0
    elif total == len(task_list):
        row_dict['total_name'] = 1
    else:
        row_dict['total_name'] = f'{total}из{len(task_list)}'
    return row_dict


def card_parse(row_dict: dict, card_id: int, person_id: int) -> dict:
    """
    Проходит циклом по всем выполненным вопросам в карточке.
    """
    selector_table_tr = "[class='userstatistics-table__tr userstatistics-table__tr--clickable']"
    table_tbody = driver.find_elements(By.CSS_SELECTOR, "[class='userstatistics-table__tbody']")[2]
    table_tr_size = len(table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr))
    person_card = PersonCard(person_id=person_id, card_id=card_id)

    print("Парсинг задания")
    for i in range(table_tr_size):
        tr = table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr)
        content_name = tr[i].find_element(
            By.CSS_SELECTOR,
            "[class='userstatistics-table__td userstatistics-table__td--content-name']"
        ).text
        tr[i].find_element(By.CSS_SELECTOR, 'td').click()
        sleep_while(True, "[class='comment-list']")

        # time.sleep(4)

        comments_list = task_parse(driver)
        try:
            for x in comments_list:
                if comments_list.count(x) > 1:
                    comments_list.remove(x)
        except IndexError:
            raise Exception("Ошибка в цикле парсинга карточки")
        row_dict[content_name] = ''.join(comments_list)

        tr = table_tbody.find_elements(By.CSS_SELECTOR, selector_table_tr)
        tr[i].find_element(By.CSS_SELECTOR, 'td').click()
    print('Возврат строки')
    return row_dict


def sleep_while(exist: bool, css_selector: str, time_sleep=1, upper_node=None) -> None:
    """
    Создает задержку для прогрузки элементов страницы
    :param exist: True - Ждать пока элемент не существует, False - Ждать пока элемент существует
    :param css_selector:
    :param time_sleep:
    :param upper_node:
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


def start_parse(save_path: str, crd: Card):  # Передавать карточку
    try:
        driver.get(url=URL_LOGIN)
        time.sleep(4)
        login(driver)
        time.sleep(4)
        person_list = fetchall(Person)
        tasks_by_card = [c.name for c in fetchall(Task, card_id=crd.id)]
        for psn in person_list:
            driver.get(url=URL_DASHBOARD)  # Открыть дашборд
            sleep_while(False, "[class='sc-preloader']")  # Экран загрузки "Авторизация"
            sleep_while(True, "[class='sc-input sc-input--empty']")  # Элемент поиска
            filter = driver.find_element(By.CLASS_NAME, 'filter')
            sc_input = filter.find_element(By.CSS_SELECTOR, 'input')
            sc_input.send_keys(psn.name)  # Ввод Имя Фамилия
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
            open_card(crd)
            time.sleep(1)
            print(psn.name)
            row_dict = get_row_dict(psn.name, tasks_by_card)  # Сюда передать карточку

            if not check_open_card():  # Поиск в `Задано`
                click_dropdown(0)
                open_card(crd)
                time.sleep(1)
            if not check_open_card():  # Поиск в `Просрочено`
                click_dropdown(1)
                open_card(crd)
                time.sleep(1)
            if not check_open_card():  # Нет ответа не на одно задание
                write_row_csv(set_row_dict_total(row_dict, tasks_by_card), save_path)

                continue
            time.sleep(1)
            row_dict = card_parse(row_dict, crd.id, psn.id)
            write_row = set_row_dict_total(row_dict, tasks_by_card)
            write_row_csv(write_row, save_path)

        time.sleep(10)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def click_dropdown(item_index: int) -> None:
    safe_click("[class='sc-dropdown__button sc-dropdown__button--hidden']", num_retries=3)
    time.sleep(1)
    dropdown = driver.find_element(By.CSS_SELECTOR,
                                   "[class='sc-dropdown__list sc-dropdown__list--visible']")
    time.sleep(1)
    dropdown.find_elements(By.CSS_SELECTOR, "[class='sc-dropdown__item']")[item_index].click()
    time.sleep(1)
