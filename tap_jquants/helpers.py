"""Helper functions for tap-jquants."""

import re
import typing as t
from datetime import datetime, timedelta, timezone


def convert_key(name: str) -> str:
    """Converts a CamelCased word to snake case."""
    name = re.sub(r"\(", "_", name)
    name = re.sub(r"\)", "", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def convert_obj(obj: object) -> object:
    """Convert keys in the given object from camel case to snake case."""
    if isinstance(obj, dict):
        return convert_json(obj)
    if isinstance(obj, list):
        return convert_array(obj)
    return obj


def convert_array(arr: t.List) -> t.List:
    """Convert keys in json array from camel case to snake case."""
    return [convert_obj(elem) for elem in arr]


def convert_json(data: t.Dict) -> t.Dict:
    """Convert keys in the given object from camel case to snake case."""
    return {convert_key(key): convert_obj(value) for key, value in data.items()}


def get_next_date(date: str) -> t.Optional[str]:
    """Returns the next date."""
    jst = timezone(timedelta(hours=9))
    dt = datetime.strptime(date, "%Y-%m-%d").astimezone(tz=jst)
    new_dt = dt + timedelta(days=1)
    if new_dt > datetime.now(tz=jst):
        return None
    return new_dt.strftime("%Y-%m-%d")
