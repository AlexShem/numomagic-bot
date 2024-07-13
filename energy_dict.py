import json


def load(periods):
    file = f"{periods}-digits.json"
    with open(file, "r") as f:
        description = json.load(f)
    return description
