from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo
from aiogram_dialog.widgets.text import Format, Case, Const
from magic_filter import MagicFilter

from handlers.handlers import close_recommendation_dialog, on_join_channel
from lang import Lang
from states.state_group import PaymentStatesGroup


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


def get_localized_learn_more_button(F: MagicFilter):
    return [Button(
        Case(
            {
                Lang.ENG: Const("Learn more"),
                Lang.RUS: Const("Узнать больше"),
                Lang.ESP: Const("Aprender más"),
                Lang.DEU: Const("Mehr erfahren"),
                Lang.FRA: Const("En savoir plus"),
                Lang.ARA: Const("تعلم أكثر"),
                Lang.CHI: Const("了解更多"),
                Lang.HIN: Const("और जानें"),
                Lang.JPN: Const("もっと知る")
            },
            selector=F["start_data"]["lang"]
        ),
        id="join_channel", on_click=on_join_channel
    )]
def create_payment_buttons_group(F: MagicFilter):
    button_group = Group(
        SwitchTo(Const("Revolut"), id="revolut_btn", state=PaymentStatesGroup.REVOLUT),
        SwitchTo(Const("Paypal"), id="paypal_btn", state=PaymentStatesGroup.PAYPAL),
        SwitchTo(Const("Bank transfer"), id="bank_transfer_btn", state=PaymentStatesGroup.BANK),
        *get_localized_close_button(F),
        width=2
    )
    return [button_group]