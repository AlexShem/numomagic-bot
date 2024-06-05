# Keyboards
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar


def create_mode_buttons():
    buttons = [[InlineKeyboardButton(text='Trial', callback_data="trial"),
                InlineKeyboardButton(text='Pay', callback_data="pay")]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_analysis_button():
    button = InlineKeyboardButton(text="Energy Analysis", callback_data="analyze")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return markup


def create_month_buttons():
    month_names = list(calendar.month_name)[1:]
    buttons = [[None for i in range(4)] for i in range(3)]
    for i, month in enumerate(month_names):
        buttons[int(i / 4)][int(i % 4)] = InlineKeyboardButton(text=month, callback_data=f"month_{month}")
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
