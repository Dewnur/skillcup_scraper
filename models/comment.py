from datetime import datetime
from typing import NamedTuple

from dateutil.relativedelta import relativedelta

from tools.text_preprocessor import lemmatize


class Comment(NamedTuple):
    id: int
    task_id: int
    person_id: int
    content: str
    overdue: bool
    create_datetime: datetime


def set_comment(comment: Comment):
    pass


def string_datetime_to_timestamp(date: str) -> int:
    """
    Парсит значения даты и времени.
    Т.к.
    """
    # comment_ct = '20.02.2023 2:45'
    date = lemmatize(date)
    comment_ct = datetime(
        year=int(date[2]), month=int(date[1]), day=int(date[0]),
        hour=int(date[3]), minute=int(date[4])
    )

    print(comment_ct)

    comment_ct = comment_ct + relativedelta(hours=-2)

    print(comment_ct)
    comment_ct = comment_ct.timestamp()
    return int(comment_ct)
