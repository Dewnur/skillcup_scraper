import os
from typing import Dict, List, Tuple, Any

import sqlite3

conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "db/database.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict) -> None:
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def update(table: str, row_id: int, column_values: Dict) -> None:
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values()) + (row_id,)
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.execute(
        f"UPDATE {table} "
        f"SET ({columns}) "
        f"= ({placeholders}) "
        f"WHERE id = ?",
        values)
    conn.commit()


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def fetchall(table: str, columns: List[str], values: List[Tuple] = None) -> List[Dict] | None:
    columns_joined = ", ".join(columns)
    if values:
        new_values = [(col, f"\'{val}\'") if type(val) == str else (col, val) for col, val in values]
        condition = [f"{col}={val}" if val is not None else f"{col} IS NULL" for col, val in new_values]
        condition = ' AND '.join(condition)
        cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {condition}")
    else:
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    if rows:
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result
    else:
        return None


def fetchone(table: str, columns: List[str], values: List[Tuple] = None) -> Dict | None:
    columns_joined = ", ".join(columns)
    if values:
        new_values = [(col, f"\'{val}\'") if type(val) == str else (col, val) for col, val in values]
        condition = [f"{col}={val}" if val is not None else f"{col} IS NULL" for col, val in new_values]
        condition = ' AND '.join(condition)
        cursor.execute(f"SELECT {columns_joined} FROM {table} WHERE {condition}")
    else:
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
    row = cursor.fetchone()
    if row:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        return dict_row
    else:
        return None


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("database.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='Person'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
