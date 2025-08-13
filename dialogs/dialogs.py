import os
from aiogram_dialog import Dialog

from windows.calendar_window import calendar_window
from windows.join_channel_window import create_join_channel_window
from windows.language_window import lang_window
from windows.payment_window import create_bank_payment_window, create_revolut_payment_window, \
    create_paypal_payment_window, create_uk_bank_payment_window
from windows.recommendation_window import (create_four_digits_window, create_five_digits_window, create_six_digits_window)
from windows.subscribe_window import create_subscribe_window

# Get premium channel link from environment
PREMIUM_CHANNEL_LINK = os.getenv("PREMIUM_CHANNEL_LINK", "https://t.me/+76i6XCTJtXQxZjFk")

main_dialog = Dialog(lang_window, calendar_window)

four_digits_dialog = Dialog(*create_four_digits_window())
five_digits_dialog = Dialog(*create_five_digits_window())
six_digits_dialog = Dialog(*create_six_digits_window())

join_channel_dialog = Dialog(*create_join_channel_window())

subscribe_dialog = Dialog(create_subscribe_window(PREMIUM_CHANNEL_LINK))

# TODO: Remove "Other Payment" this feature
payment_dialog = Dialog(*create_bank_payment_window(), *create_revolut_payment_window(), *create_paypal_payment_window(), *create_uk_bank_payment_window())
