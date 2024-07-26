from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row
from aiogram_dialog.widgets.text import Const

from handlers import on_premium, on_trial
from states.state_group import DialogSG

user_option_window = Window(
    Const("Welcome to our bot! Please choose an option:"),
    Row(
        Button(Const("Trial"), id="trial", on_click=on_trial),
        Button(Const("Premium"), id="premium", on_click=on_premium)),
    state=DialogSG.MAIN
)

energy_analysis_window = Window(
    Const("Press the button to start the energy analysis"),
    Button(Const("Energy analysis"), id="analysis"),
    state=DialogSG.ANALYSIS
)
