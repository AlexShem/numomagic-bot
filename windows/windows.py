from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, Calendar
from aiogram_dialog.widgets.text import Const

from handlers import on_premium, on_trial, on_date_selected
from states.state_group import DialogSG

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

result_window = Window(Const("Energy analysis result"),
                       state=DialogSG.RESULT)
