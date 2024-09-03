from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from lang import Lang
from states.state_group import PaymentStatesGroup
from windows.common_elements import create_payment_buttons_group, get_localized_close_button


async def get_bank_payment_description(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"description": "Оплата по платежной системе на русском"}
    elif selected_lang == Lang.ENG:
        return {"description": "Payment via payment system in English"}

async def get_revolut_payment_description(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"description": "Оплата по Revolut на русском"}
    elif selected_lang == Lang.ENG:
        return {"description": "Payment via Revolut in English"}

async def get_paypal_payment_description(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"description": "Оплата по Paypal на русском"}
    elif selected_lang == Lang.ENG:
        return {"description": "Payment via Paypal in English"}

def create_bank_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_bank_payment_description,
               state=PaymentStatesGroup.BANK)
    ]

def create_revolut_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_revolut_payment_description,
               state=PaymentStatesGroup.REVOLUT)
    ]

def create_paypal_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_paypal_payment_description,
               state=PaymentStatesGroup.PAYPAL)
    ]