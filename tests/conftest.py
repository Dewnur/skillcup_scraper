import random

import pytest

from db_models_manager import *
from models import *


@pytest.fixture()
def get_random_person() -> Person:
    return random.choice(fetchall(Person))


@pytest.fixture()
def get_random_card() -> Card:
    return random.choice(fetchall(Card))


@pytest.fixture()
def get_random_personCard() -> PersonCard:
    return random.choice(fetchall(PersonCard))


@pytest.fixture()
def get_random_record():
    return _random_record


def _random_record(cls: Type[T]):
    return random.choice(fetchall(cls))
