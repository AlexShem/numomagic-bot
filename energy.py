import math
from datetime import datetime

from db import User
import emoji


def calc_energy(user: User):
    energy = {0: 0, 4: 1, 8: 4, 12: 5, 16: 7, 20: 2, 24: 8}
    formula = user.year * user.month * user.day
    num = len(str(formula))
    step = math.ceil(24 / num)
    result = ""
    for hour in range(0, 24, step):
        time = f"{hour}:00" + '-' + f"{hour + step}:00"
        prev, nxt = energy[hour], energy[hour + step]
        energy_chart = F"{prev} - {nxt}"
        emoji_alarm = emoji.emojize(":alarm_clock:")
        result += (f"In time period {emoji_alarm} {time}\n"
                   f"Energy level: {energy_chart}\n"
                   f"-------------------------------\n")
    return result
