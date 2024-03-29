import datetime
import re


def replace_string(text: str) -> str:
    pattern = r'(\d+\.\d+\.\d+)?\s+.*\s+(\d+:\d+)?'
    replacement = r'\1 \2'
    result = re.sub(pattern, replacement, text)
    return result


def string_to_timestamp(date_string: str, date_format: str = "%d.%m.%Y") -> int:
    date_string = replace_string(date_string)
    date_object = datetime.datetime.strptime(date_string, date_format)
    timestamp = int(datetime.datetime.timestamp(date_object))
    return timestamp


def timestamp_to_string(timestamp: float, date_format: str = "%d.%m.%Y") -> str:
    date_object = datetime.datetime.fromtimestamp(timestamp)
    date_string = date_object.strftime(date_format)
    return date_string


def remove_duplicates(lst):
    result = []
    for item in lst:
        if item not in result:
            result.append(item)
    return result
