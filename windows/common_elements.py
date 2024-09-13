from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo, Url
from aiogram_dialog.widgets.text import Format, Case, Const, Text
from magic_filter import MagicFilter

from handlers.handlers import on_join_channel, on_close_dialog
from lang import Lang
from states.state_group import PaymentStatesGroup


def get_localized_close_button(F: MagicFilter):
    return [Button(
        Case(
            {
                Lang.ENG: Const("Close"),    #TODO: Make referense to payment description
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
        id="button_close_recommendation", on_click=on_close_dialog
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

def get_channel_url(F: MagicFilter):
    return [Url(
        Case(
            {
                Lang.ENG: Const("Join Channel"),
                Lang.RUS: Const("Подключиться к каналу"),
                Lang.ESP: Const("Unirse al canal"),
                Lang.DEU: Const("Kanal beitreten"),
                Lang.FRA: Const("Rejoindre le canal"),
                Lang.ARA: Const("انضم إلى القناة"),
                Lang.CHI: Const("加入频道"),
                Lang.HIN: Const("चैनल से जुड़ें"),
                Lang.JPN: Const("チャンネルに参加"),
                ...: Const("Not implemented language"),
            },
            selector=F["start_data"]["lang"]
        ),
        Case(
            {
                Lang.ENG: Const("https://t.me/+1cEaSbrrGshmNzlk"),
                Lang.RUS: Const("https://t.me/+9t7ylcITlJdmYTk0"),
                Lang.ESP: Const("https://t.me/+9l-JYRXy2CA2YzU0"),
                Lang.DEU: Const("https://t.me/+sZ_KGJI5L5hhZWM0"),
                Lang.FRA: Const("https://t.me/+6u5KXd2hUXhiMGM8"),
                Lang.ARA: Const("https://t.me/+9_BfGfHMQrM0MmNk"),
                Lang.CHI: Const("https://t.me/+HsIGO3-8dZ45ODBk"),
                Lang.HIN: Const("https://t.me/+RAalShGyKscyOGU0"),
                Lang.JPN: Const("https://t.me/+q723Uy3pLaw1YzJk"),
                ...: Const("https://t.me/+1cEaSbrrGshmNzlk")
            },
            selector=F["start_data"]["lang"]
        )
    )]

def get_localized_more_methods_button(F: MagicFilter):
    return [Button(
        Case(
            {
                Lang.ENG: Const("More methods available soon"),
                Lang.RUS: Const("Больше методов скоро"),
                Lang.ESP: Const("Más métodos disponibles pronto"),
                Lang.DEU: Const("Weitere Methoden bald verfügbar"),
                Lang.FRA: Const("Plus de méthodes bientôt disponibles"),
                Lang.ARA: Const("المزيد من الطرق قريبًا"),
                Lang.CHI: Const("更多方法即将推出"),
                Lang.HIN: Const("जल्द ही और अधिक विधियाँ उपलब्ध होगी"),
                Lang.JPN: Const("もっと多くの方法が間もなく利用可能になります"),
                ...: Const("Not implemented language")
            },
            selector=F["start_data"]["lang"]
        ),
        id="more_methods"
    )]

def create_payment_buttons_group(F: MagicFilter):
    button_group = Group(
        # SwitchTo(Const("💳 Revolut"), id="revolut_btn", state=PaymentStatesGroup.REVOLUT), # Not implemented
        SwitchTo(Const("🅿️ PayPal"), id="paypal_btn", state=PaymentStatesGroup.PAYPAL),
        SwitchTo(
            Case(
                {
                    Lang.ENG: Const("🏦 Bank Transfer"),
                    Lang.RUS: Const("🏦 Банковский перевод"),
                    Lang.ESP: Const("🏦 Transferencia bancaria"),
                    Lang.DEU: Const("🏦 Bank Transfer"),
                    Lang.FRA: Const("🏦 Virement bancaire"),
                    Lang.ARA: Const("🏦 تحويل بنكي"),
                    Lang.CHI: Const("🏦 银行转账"),
                    Lang.HIN: Const("🏦 बैंक ट्रांसफर"),
                    Lang.JPN: Const("🏦 銀行振込")
                },
                selector=F["start_data"]["lang"]
            ),
            id="bank_transfer_btn", state=PaymentStatesGroup.BANK
        ),
        SwitchTo(Const("🇬🇧🏦 UK Bank Transfer"), id="uk_bank_transfer_btn", state=PaymentStatesGroup.UK_BANK),
        # SwitchTo(Const("🔐 Crypto"), id="crypto_btn", state=PaymentStatesGroup.CRYPTO), # Not implemented
        *get_channel_url(F),
        # *get_localized_more_methods_button(F), # Remove "More methods available soon" button until new methods are being developed
        *get_localized_close_button(F),
        width=2
    )
    return [button_group]
