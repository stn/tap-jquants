import os
import re
from typing import Dict, List

import singer

LOGGER = singer.get_logger()


def get_abs_path(path: str):
    """Returns absolute path for URL."""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def convert(name):
    """Converts a CamelCased word to snake case."""
    name = re.sub(r"\(", "_", name)
    name = re.sub(r"\)", "", name)
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


# Convert keys in json array
def convert_array(arr: List):
    """Converts all the CamelCased dict Keys in a list to snake case Iterated
    through each object recursively and if the object is dict type then
    converts its key to snake case."""
    new_arr = []
    for element in arr:
        if isinstance(element, list):
            new_arr.append(convert_array(element))
        elif isinstance(element, dict):
            new_arr.append(convert_json(element))
        else:
            new_arr.append(element)
    return new_arr


# Convert keys in json
def convert_json(data_object: Dict):
    """Converts all the CamelCased Keys in a nested dictionary object to snake
    case."""
    out = {}
    for key in data_object:
        new_key = convert(key)
        if isinstance(data_object[key], dict):
            out[new_key] = convert_json(data_object[key])
        elif isinstance(data_object[key], list):
            out[new_key] = convert_array(data_object[key])
        else:
            out[new_key] = data_object[key]
    return out
