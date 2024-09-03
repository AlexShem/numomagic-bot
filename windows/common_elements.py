from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Case, Const
from magic_filter import MagicFilter

from handlers.handlers import close_recommendation_dialog
from lang import Lang


def get_localized_close_button(F: MagicFilter):
    return [Button(
        Case(
            {
                Lang.ENG: Const("Close"),
                Lang.RUS: Const("Закрыть"),
                Lang.ESP: Const("Cerrar"),
                Lang.DEU: Const("Schließen"),
                Lang.FRA: Const("Fermer"),
                Lang.ARA: Const("إغلاق"),
                Lang.CHI: Const("关闭"),
                Lang.HIN: Const("बंद करे"),
                Lang.JPN: Const("閉じる")
            },
            selector=F["start_data"]["lang"]
        ),
        id="button_close_recommendation", on_click=close_recommendation_dialog
    )]