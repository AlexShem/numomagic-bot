from random import random

from db import User
import emoji


def calc_energy(user: User):
    formula = user.year + user.month + user.day
    energy_chart = {'0-4': int(random() * formula),
                    '4-12': int(random() * formula),
                    '12-19': int(random() * formula),
                    '19-24': int(random() * formula)}
    return energy_chart


def create_string_from_energy_chart(energy_chart):
    emoji_key = emoji.emojize(':mantelpiece_clock:')
    emoji_value = emoji.emojize(':battery:')
    string = ''
    for key, value in energy_chart.items():
        string += (f"{emoji_key}<b>In time period: </b>{key}\n"
                   f"{emoji_value}<b>Energy level: </b>{value}\n")
    return string
