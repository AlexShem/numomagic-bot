from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, Calendar, Group
from aiogram_dialog.widgets.text import Const, Format

from handlers import on_premium, on_trial, on_date_selected, on_b_4_1, on_b_4_2, on_b_4_3, on_b_4_4
from states.state_group import DialogSG, FourDigitsStates

user_option_window = Window(
    Const("Welcome to our bot! Please choose an option:"),
    Row(
        Button(Const("Trial"), id="trial", on_click=on_trial),
        Button(Const("Premium"), id="premium", on_click=on_premium)),
    state=DialogSG.MAIN
)

energy_analysis_window = Window(
    Const("Press the button to open a calendar and start the energy analysis"),
    SwitchTo(Const("Calendar"), id="calendar", state=DialogSG.CALENDAR),
    state=DialogSG.ANALYSIS
)

calendar_window = Window(
    Const("Select your energy date"),
    Calendar(id='calendar', on_click=on_date_selected),
    state=DialogSG.CALENDAR)


# -------------------------------------------------------------------------------

async def get_period_1(dialog_manager: DialogManager, **kwargs):
    return {"period_1": dialog_manager.start_data.get("period_1")}


async def get_period_2(dialog_manager: DialogManager, **kwargs):
    return {"period_2": dialog_manager.start_data.get("period_2")}


async def get_period_3(dialog_manager: DialogManager, **kwargs):
    return {"period_3": dialog_manager.start_data.get("period_3")}


async def get_period_4(dialog_manager: DialogManager, **kwargs):
    return {"period_4": dialog_manager.start_data.get("period_4")}


def create_four_digits_window():
    button_group = Group(Button(Const("00:00-06:00"), id="b_4_1", on_click=on_b_4_1),
                         Button(Const("06:00-12:00"), id="b_4_2", on_click=on_b_4_2),
                         Button(Const("12:00-18:00"), id="b_4_3", on_click=on_b_4_3),
                         Button(Const("18:00-24:00"), id="b_4_4", on_click=on_b_4_4))
    windows = [
        Window(Format("{period_1}"),
               button_group,
               state=FourDigitsStates.STATE1,
               getter=get_period_1),
        Window(Format("{period_2}"),
               button_group,
               state=FourDigitsStates.STATE2,
               getter=get_period_2),
        Window(Format("{period_3}"),
               button_group,
               state=FourDigitsStates.STATE3,
               getter=get_period_3),
        Window(Format("{period_4}"),
               button_group,
               state=FourDigitsStates.STATE4,
               getter=get_period_4),
    ]
    return windows
