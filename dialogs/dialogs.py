from aiogram_dialog import Dialog

from windows.windows import (energy_analysis_window, calendar_window,
                             create_four_digits_window, create_five_digits_window, create_six_digits_window,
                             lang_window, join_channel_window)

main_dialog = Dialog(energy_analysis_window, calendar_window, lang_window)

four_digits_dialog = Dialog(*create_four_digits_window())
five_digits_dialog = Dialog(*create_five_digits_window())
six_digits_dialog = Dialog(*create_six_digits_window())

join_channel_dialog = Dialog(join_channel_window)
