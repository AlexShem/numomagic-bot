import json


def load(periods):
    file = f"dicts/{periods}-digits.json"
    with open(file, "r") as f:
        description = json.load(f)
    return description
