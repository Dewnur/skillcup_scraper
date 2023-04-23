import pytest

from tools.date_preprocessor import *


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
