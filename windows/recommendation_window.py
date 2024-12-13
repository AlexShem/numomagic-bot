from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Calendar, Group, Url
from aiogram_dialog.widgets.text import Const, Format, Case
from magic_filter import F

from handlers.handlers import (
    on_4_1, on_4_2, on_4_3, on_4_4,
    on_5_1, on_5_2, on_5_3, on_5_4, on_5_5,
    on_6_1, on_6_2, on_6_3, on_6_4, on_6_5, on_6_6,
)
from states.state_group import FiveDigitsStates, FourDigitsStates, SixDigitsStates
from .common_elements import get_localized_close_button, get_localized_learn_more_button

# Recommendation windows -------------------------------------------------------

async def get_period_1(dialog_manager: DialogManager, **kwargs):
    return {"period_1": dialog_manager.start_data.get("period_1")}


async def get_period_2(dialog_manager: DialogManager, **kwargs):
    return {"period_2": dialog_manager.start_data.get("period_2")}


async def get_period_3(dialog_manager: DialogManager, **kwargs):
    return {"period_3": dialog_manager.start_data.get("period_3")}


async def get_period_4(dialog_manager: DialogManager, **kwargs):
    return {"period_4": dialog_manager.start_data.get("period_4")}


async def get_period_5(dialog_manager: DialogManager, **kwargs):
    return {"period_5": dialog_manager.start_data.get("period_5")}


async def get_period_6(dialog_manager: DialogManager, **kwargs):
    return {"period_6": dialog_manager.start_data.get("period_6")}


def create_four_digits_window():
    button_group = Group(
        Button(Const("00:00-06:00"), id="b_4_1", on_click=on_4_1),
        Button(Const("06:00-12:00"), id="b_4_2", on_click=on_4_2),
        Button(Const("12:00-18:00"), id="b_4_3", on_click=on_4_3),
        Button(Const("18:00-24:00"), id="b_4_4", on_click=on_4_4),
        *get_localized_close_button(F),
        # *get_localized_learn_more_button(F),
        width=2
    )
    windows = [
        Window(Format("{period_1}"),
               button_group,
               state=FourDigitsStates.PERIOD1,
               getter=get_period_1),
        Window(Format("{period_2}"),
               button_group,
               state=FourDigitsStates.PERIOD2,
               getter=get_period_2),
        Window(Format("{period_3}"),
               button_group,
               state=FourDigitsStates.PERIOD3,
               getter=get_period_3),
        Window(Format("{period_4}"),
               button_group,
               state=FourDigitsStates.PERIOD4,
               getter=get_period_4),
    ]
    return windows


def create_five_digits_window():
    button_group = Group(
        Button(Const("00:00-04:48"), id="b_5_1", on_click=on_5_1),
        Button(Const("04:48-9:36"), id="b_5_2", on_click=on_5_2),
        Button(Const("9:36-14:24"), id="b_5_3", on_click=on_5_3),
        Button(Const("14:24-19:12"), id="b_5_4", on_click=on_5_4),
        Button(Const("19:12-24:00"), id="b_5_5", on_click=on_5_5),
        *get_localized_close_button(F),
        # *get_localized_learn_more_button(F),
        width=2
    )

    windows = [
        Window(Format("{period_1}"),
               button_group,
               state=FiveDigitsStates.PERIOD1,
               getter=get_period_1),
        Window(Format("{period_2}"),
               button_group,
               state=FiveDigitsStates.PERIOD2,
               getter=get_period_2),
        Window(Format("{period_3}"),
               button_group,
               state=FiveDigitsStates.PERIOD3,
               getter=get_period_3),
        Window(Format("{period_4}"),
               button_group,
               state=FiveDigitsStates.PERIOD4,
               getter=get_period_4),
        Window(Format("{period_5}"),
               button_group,
               state=FiveDigitsStates.PERIOD5,
               getter=get_period_5),
    ]
    return windows


def create_six_digits_window():
    button_group = Group(
        Button(Const("00:00-04:00"), id="b_6_1", on_click=on_6_1),
        Button(Const("04:00-08:00"), id="b_6_2", on_click=on_6_2),
        Button(Const("08:00-12:00"), id="b_6_3", on_click=on_6_3),
        Button(Const("12:00-16:00"), id="b_6_4", on_click=on_6_4),
        Button(Const("16:00-20:00"), id="b_6_5", on_click=on_6_5),
        Button(Const("20:00-24:00"), id="b_6_6", on_click=on_6_6),
        *get_localized_close_button(F),
        # *get_localized_learn_more_button(F),
        width=2
    )
    windows = [
        Window(Format("{period_1}"),
               button_group,
               state=SixDigitsStates.PERIOD1,
               getter=get_period_1),
        Window(Format("{period_2}"),
               button_group,
               state=SixDigitsStates.PERIOD2,
               getter=get_period_2),
        Window(Format("{period_3}"),
               button_group,
               state=SixDigitsStates.PERIOD3,
               getter=get_period_3),
        Window(Format("{period_4}"),
               button_group,
               state=SixDigitsStates.PERIOD4,
               getter=get_period_4),
        Window(Format("{period_5}"),
               button_group,
               state=SixDigitsStates.PERIOD5,
               getter=get_period_5),
        Window(Format("{period_6}"),
               button_group,
               state=SixDigitsStates.PERIOD6,
               getter=get_period_6),
    ]
    return windows
