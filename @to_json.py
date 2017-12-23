import json
import functools


def to_json(func):
    @functools.wraps(func)  # вместо wrapped будет название исходной функции
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result)
    return wrapped
