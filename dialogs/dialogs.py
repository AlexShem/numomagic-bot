from aiogram_dialog import Dialog

from windows.windows import (user_option_window, energy_analysis_window, calendar_window,
                             create_four_digits_window, create_five_digits_window, create_six_digits_window)

main_dialog = Dialog(user_option_window, energy_analysis_window, calendar_window)

four_digits_dialog = Dialog(*create_four_digits_window())
five_digits_dialog = Dialog(*create_five_digits_window())
six_digits_dialog = Dialog(*create_six_digits_window())
