from typing import List, TypeVar, Type, NamedTuple

import db

T = TypeVar('T', bound=NamedTuple)


def fetchall(cls: Type[T], **kwargs) -> List[T]:
    condition = []
    for key, value in kwargs.items():
        condition.append((key, value))
    fields = [field for field in cls._fields]
    table_name = cls.__name__
    records = db.fetchall(table_name, fields, condition)

    objects_list = []
    for record in records:
        obj = cls(**record)
        objects_list.append(obj)

    return objects_list


def fetchone(cls: Type[T], **kwargs) -> T:
    condition = []
    for key, value in kwargs.items():
        condition.append((key, value))
    fields = [field for field in cls._fields]
    table_name = cls.__name__
    record = db.fetchall(table_name, fields, condition)[0]
    obj = cls(**record)

    return obj
