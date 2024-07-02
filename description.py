import json

with open("description.json", "r") as f:
    description = json.load(f)


def get_description():
    return description
