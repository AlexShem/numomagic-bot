import math
from datetime import datetime

from db import User
import emoji


def get_energy_chart(year, month, day):
    value = str(year * month * day)
    energy_chart = []
    for i, digit in enumerate(value):
        energy_chart.append(int(digit))
    return energy_chart
    # result = ""
    # for hour in range(0, 24, step):
    #     time = f"{hour}:00" + '-' + f"{hour + step}:00"
    #     prev, nxt = energy_chart[hour], energy_chart[hour + step]
    #     energy_chart = F"{prev} - {nxt}"
    #     emoji_alarm = emoji.emojize(":alarm_clock:")
    #     result += (f"In time period {emoji_alarm} {time}\n"
    #                f"Energy level: {energy_chart}\n"
    #                f"-------------------------------\n")
    # return result
