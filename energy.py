import json
from lang import Lang


# Function returns digits of common energy level
# Example: for 01.01.2024 common energy level is
# 1 * 1 * 2024 = 2024 => 4 digits energy level
# so function returns [2, 0, 2, 4]
def get_energy_levels(year, month, day):
    common_value = str(year * month * day)
    energy_chart = []
    for i, digit in enumerate(common_value):
        energy_chart.append(int(digit))
    return energy_chart


# Function returns description from dict directory
def load(digits, lang: Lang):
    file = f"dicts/{digits}-digits-{lang.value}.json"
    with open(file, "r", encoding="utf-8") as f:
        description = json.load(f)
    return description
