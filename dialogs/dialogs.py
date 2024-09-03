from aiogram_dialog import Dialog

from windows.payment_windows import create_bank_payment_window, create_revolut_payment_window, \
    create_paypal_payment_window
from windows.windows import (lang_window, calendar_window,
                             create_four_digits_window, create_five_digits_window, create_six_digits_window,
                             create_join_channel_window)

main_dialog = Dialog(lang_window, calendar_window)

four_digits_dialog = Dialog(*create_four_digits_window())
five_digits_dialog = Dialog(*create_five_digits_window())
six_digits_dialog = Dialog(*create_six_digits_window())

join_channel_dialog = Dialog(*create_join_channel_window())

payment_dialog = Dialog(*create_bank_payment_window(), *create_revolut_payment_window(), *create_paypal_payment_window())
