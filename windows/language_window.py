from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const

from handlers.handlers import on_lang_selected
from lang import Lang
from states.state_group import DialogSG

lang_window = Window(
    Const("Welcome to NumoMagic bot! Please, choose your language"),
    Group(
        Button(Const("English 🇬🇧"), id=Lang.ENG.value, on_click=on_lang_selected),
        Button(Const("Russian 🇷🇺"), id=Lang.RUS.value, on_click=on_lang_selected),
        Button(Const("Deutsch 🇩🇪"), id=Lang.DEU.value, on_click=on_lang_selected),
        Button(Const("Spanish 🇪🇸"), id=Lang.ESP.value, on_click=on_lang_selected),
        Button(Const("French 🇫🇷"), id=Lang.FRA.value, on_click=on_lang_selected),
        Button(Const("Arabic 🇸🇦"), id=Lang.ARA.value, on_click=on_lang_selected),
        Button(Const("Chinese 🇨🇳"), id=Lang.CHI.value, on_click=on_lang_selected),
        Button(Const("Hindi 🇮🇳"), id=Lang.HIN.value, on_click=on_lang_selected),
        Button(Const("Japanese 🇯🇵"), id=Lang.JPN.value, on_click=on_lang_selected),
        width=2
    ),
    state=DialogSG.MAIN
)
