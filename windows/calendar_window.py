from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Case, Const
from magic_filter import F

from handlers.handlers import on_date_selected
from lang import Lang
from states.state_group import DialogSG

calendar_window = Window(
    Case(
        {
            Lang.ENG: Const("Choose a date to get your recommendations."),
            Lang.RUS: Const("Выберите дату, чтобы получить рекомендации."),
            Lang.ESP: Const("Elija una fecha para obtener sus recomendaciones."),
            Lang.DEU: Const("Wählen Sie ein Datum, um Ihre Empfehlungen zu erhalten."),
            Lang.FRA: Const("Choisissez une date pour obtenir vos recommandations."),
            Lang.ARA: Const("اختر تاريخًا للحصول على توصياتك."),
            Lang.CHI: Const("选择日期以获取您的建议。"),
            Lang.HIN: Const("अपनी सिफारिशों प्राप्त करने के लिए एक तारीख चुनें।"),
            Lang.JPN: Const("お勧めを取得するための日付を選択してください。")
        },
        selector=F["dialog_data"]["lang"],
    ),
    Calendar(id='calendar', on_click=on_date_selected),
    state=DialogSG.CALENDAR
)
