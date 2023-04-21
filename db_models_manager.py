from typing import List, TypeVar, Type, NamedTuple, Any

import db

T = TypeVar('T', bound=NamedTuple)


def fetchall(cls: Type[T], **kwargs) -> List[T] | None:
    condition = []
    objects_list = []
    for key, value in kwargs.items():
        condition.append((key, value))
    fields = [field for field in cls._fields]
    table_name = cls.__name__
    records = db.fetchall(table_name, fields, condition)
    if records:
        for record in records:
            obj = cls(**record)
            objects_list.append(obj)
        return objects_list
    else:
        return None


def fetchone(cls: Type[T], **kwargs) -> Any | None:
    condition = []
    for key, value in kwargs.items():
        condition.append((key, value))
    fields = [field for field in cls._fields]
    table_name = cls.__name__
    record = db.fetchone(table_name, fields, condition)
    if record:
        obj = cls(**record)
        return obj
    else:
        return None


def insert(obj: T) -> None:
    table_name = type(obj).__name__
    db.insert(table_name, obj._asdict())


def update(obj: T, **kwargs: dict == {}) -> None:
    table_name = type(obj).__name__
    db.update(table_name, obj.id, kwargs)


def delete(obj: T) -> None:
    table_name = type(obj).__name__
    db.delete(table_name, obj.id)


def check_record_exists(obj: T) -> bool:
    try:
        obj_asdict = obj._asdict()
        record = fetchone(type(obj), **obj_asdict)
        if record:
            return True
        return False
    except AttributeError:
        return False
