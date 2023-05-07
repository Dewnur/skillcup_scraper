import pytest

from tools.date_preprocessor import *
from tools.text_preprocessor import comment_tokens


@pytest.mark.parametrize('text, result', [
    ('12.03.2023', '12.03.2023'),
    ('12.03.2023 в 21:29', '12.03.2023 21:29'),
    ('12.03.2023 d 21:29', '12.03.2023 21:29')
])
def test_replace_string(text, result):
    assert replace_string(text) == result


@pytest.mark.parametrize('date, date_format, result_type', [
    ('12.03.2023', '%d.%m.%Y', float),
    ('12.03.2023 в 21:29', '%d.%m.%Y %H:%M', float),
    ('12.03.2023 d 21:29', '%d.%m.%Y %H:%M', float)
])
def test_string_to_timestamp(date, date_format, result_type):
    assert type(string_to_timestamp(date, date_format)) == result_type


def test_comment_tokens():
    assert comment_tokens(
        "https://t.me/vlezvxs/27 Цель поста: привлечение подписчиков. Формула: новость"
    ) == [
               ('', 0),
               ('https://t.me/vlezvxs/27', 1),
               (' Цель поста: привлечение подписчиков. Формула: новость', 0)
           ]
    assert comment_tokens(
        "Цель поста: привлечение подписчиков. Формула: новость https://t.me/vlezvxs/27 Формула: новость"
    ) == [
               ('Цель поста: привлечение подписчиков. Формула: новость ', 0),
               ('https://t.me/vlezvxs/27', 1),
               (' Формула: новость', 0)
           ]
