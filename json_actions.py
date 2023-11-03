import json
import os


def read_json(path_to_json: str):
    if not os.path.exists(path_to_json):
        write_json(path_to_json, {})
    with open(path_to_json, 'r') as f:
        data = json.load(f)
    return data


def write_json(path_to_json: str, data):
    with open(path_to_json, 'w') as f:
        json.dump(data, f)