from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Calendar, Group, Url
from aiogram_dialog.widgets.text import Const, Format

import lang

from handlers.handlers import (on_date_selected,
                               on_5_1, on_5_2, on_5_3, on_5_4, on_5_5, on_4_1, on_4_2, on_4_3, on_4_4, on_6_1,
                               on_6_2, on_6_3, on_6_4, on_6_5, on_6_6, close_join_channel_dialog, on_lang_selected,
                               on_join_channel)
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates, JoinChannelStatesGroup

energy_analysis_window = Window(
    Const("Press the button to open a calendar and start the energy analysis"),
    SwitchTo(Const("Calendar"), id="calendar", state=DialogSG.CALENDAR),
    state=DialogSG.ANALYSIS
)


async def get_select_date_message(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        lang.Lang.ENG: "Choose a date to get your recommendations.",
        lang.Lang.RUS: "Выберите дату, чтобы получить рекомендации.",
        lang.Lang.ESP: "Elija una fecha para obtener sus recomendaciones.",
        lang.Lang.DEU: "Wählen Sie ein Datum, um Ihre Empfehlungen zu erhalten.",
        lang.Lang.FRA: "Choisissez une date pour obtenir vos recommandations.",
        lang.Lang.ARA: "اختر تاريخًا للحصول على توصياتك.",
        lang.Lang.CHI: "选择一个日期以获取您的建议。",
        lang.Lang.HIN: "अपनी सिफारिशें प्राप्त करने के लिए एक तिथि चुनें।",
        lang.Lang.JPN: "推奨事項を取得する日付を選択してください。"
    }
    selected_lang = dialog_manager.dialog_data.get("lang", lang.Lang.ENG)
    return {"select_date_message": lang_messages.get(selected_lang, "Choose a date to get your recommendations.")}


calendar_window = Window(
    Format("{select_date_message}"),
    Calendar(id='calendar', on_click=on_date_selected),
    getter=get_select_date_message,
    state=DialogSG.CALENDAR)

lang_window = Window(Const("Welcome to NumoMagic bot! Please, choose your language"),
                     Group(
                         Button(Const("English 🇬🇧"), id=lang.Lang.ENG.value, on_click=on_lang_selected),
                         Button(Const("Russian 🇷🇺"), id=lang.Lang.RUS.value, on_click=on_lang_selected),
                         Button(Const("Deutsch 🇩🇪"), id=lang.Lang.DEU.value, on_click=on_lang_selected),
                         Button(Const("Spanish 🇪🇸"), id=lang.Lang.ESP.value, on_click=on_lang_selected),
                         Button(Const("French 🇫🇷"), id=lang.Lang.FRA.value, on_click=on_lang_selected),
                         Button(Const("Arabic 🇸🇦"), id=lang.Lang.ARA.value, on_click=on_lang_selected),
                         Button(Const("Chinese 🇨🇳"), id=lang.Lang.CHI.value, on_click=on_lang_selected),
                         Button(Const("Hindi 🇮🇳"), id=lang.Lang.HIN.value, on_click=on_lang_selected),
                         Button(Const("Japanese 🇯🇵"), id=lang.Lang.JPN.value, on_click=on_lang_selected),
                         width=2
                     ),
                     state=DialogSG.MAIN)


# -------------------------------------------------------------------------------

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
    button_group = Group(Button(Const("00:00-06:00"), id="b_4_1", on_click=on_4_1),
                         Button(Const("06:00-12:00"), id="b_4_2", on_click=on_4_2),
                         Button(Const("12:00-18:00"), id="b_4_3", on_click=on_4_3),
                         Button(Const("18:00-24:00"), id="b_4_4", on_click=on_4_4),
                         Button(Const("Close"), id="close", on_click=close_join_channel_dialog),
                         width=2)
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
        Button(Const("Close"), id="close", on_click=close_join_channel_dialog),
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
        Button(Const("Close"), id="close", on_click=close_join_channel_dialog),
               Button(Format("Узнать больше"), id="join_channel", on_click=on_join_channel),
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


async def get_join_channel_message(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        lang.Lang.ENG: "You can learn more about numerology on our Telegram channel. "
                        "To get access to the channel, you can pay in Telegram Stars or send a join request and pay using a bank transfer. "
                        "Click the buttons below to get access to the channel.",
        lang.Lang.RUS: "Вы можете узнать больше о нумерологии на нашем Telegram-канале. "
                        "Чтобы получить доступ к каналу, вы можете оплатить в Telegram Stars или отправить запрос на вступление и оплатить банковским переводом. "
                        "Нажмите на кнопки ниже, чтобы получить доступ к каналу.",
        lang.Lang.ESP: "Puede obtener más información sobre numerología en nuestro canal de Telegram. "
                        "Para acceder al canal, puede pagar en Telegram Stars o enviar una solicitud de unirse y pagar mediante una transferencia bancaria. "
                        "Haga clic en los botones a continuación para acceder al canal.",
        lang.Lang.DEU: "Sie können mehr über Numerologie auf unserem Telegram-Kanal erfahren. "
                        "Um Zugriff auf den Kanal zu erhalten, können Sie in Telegram Stars bezahlen oder eine Beitrittsanfrage senden und per Banküberweisung bezahlen. "
                        "Klicken Sie auf die Schaltflächen unten, um Zugriff auf den Kanal zu erhalten.",
        lang.Lang.FRA: "Vous pouvez en apprendre plus sur la numérologie sur notre chaîne Telegram. "
                        "Pour accéder à la chaîne, vous pouvez payer en étoiles Telegram ou envoyer une demande de rejoindre et payer par virement bancaire. "
                        "Cliquez sur les boutons ci-dessous pour accéder à la chaîne.",
        lang.Lang.ARA: "يمكنك معرفة المزيد حول علم الأعداد على قناتنا على تطبيق تليجرام. "
                        "للوصول إلى القناة، يمكنك الدفع بنجوم تليجرام أو إرسال طلب انضمام والدفع عبر التحويل المصرفي. "
                        "انقر على الأزرار أدناه للوصول إلى القناة.",
        lang.Lang.CHI: "您可以在我们的Telegram频道上了解更多关于数字学的信息。 "
                        "要访问频道，您可以使用Telegram Stars支付或发送加入请求并通过银行转账支付。 "
                        "单击下面的按钮以访问频道。",
        lang.Lang.HIN: "आप हमारे टेलीग्राम चैनल पर अंकशास्त्र के बारे में अधिक जान सकते हैं। "
                        "चैनल तक पहुंचने के लिए, आप टेलीग्राम स्टार्स में भुगतान कर सकते हैं या ज्वाइन अनुरोध भेजकर बैंक ट्रांसफर के जरिए भुगतान कर सकते हैं। "
                        "चैनल तक पहुंचने के लिए नीचे दिए गए बटन पर क्लिक करें।",
        lang.Lang.JPN: "当社のTelegramチャンネルで数秘術について詳しく知ることができます。 "
                        "チャンネルにアクセスするには、Telegram Starsで支払うか、参加リクエストを送信して銀行振込で支払うことができます。 "
                        "チャンネルにアクセスするには、以下のボタンをクリックしてください。"
    }

    selected_lang = dialog_manager.dialog_data.get("lang", lang.Lang.ENG)
    return {"join_channel_message": lang_messages.get(selected_lang, "You can learn more about numerology on our Telegram channel. "
                        "To get access to the channel, you can pay in Telegram Stars or send a join request and pay using a bank transfer. "
                        "Click the buttons below to get access to the channel.")}


async def get_join_channel_buttons(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        lang.Lang.ENG: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.RUS: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.ESP: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.DEU: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.FRA: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.ARA: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.CHI: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.HIN: {"stars": "Telegram stars", "other": "Other payment"},
        lang.Lang.JPN: {"stars": "Telegram stars", "other": "Other payment"}
    }

    selected_lang = dialog_manager.start_data.get("lang", lang.Lang.ENG)
    return {"join_channel_buttons": lang_messages.get(selected_lang, {"stars": "Telegram stars", "other": "Other payment"})}


async def get_join_channel_star_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", lang.Lang.ENG)
    if selected_lang == lang.Lang.RUS:
        return {"join_channel_star_link": "https://t.me/+0-JREGcV0KBiOTM0"}
    return {"join_channel_star_link": "https://t.me/+zTjKEuObGCw2NWFk"}


async def get_join_channel_request_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", lang.Lang.ENG)
    if selected_lang == lang.Lang.RUS:
        return {"join_channel_request_link": "https://t.me/+9t7ylcITlJdmYTk0"}
    return {"join_channel_request_link": "https://t.me/+zTjKEuObGCw2NWFk"}


join_channel_window = Window(
    Format("{join_channel_message}"),
    Url(Format("{join_channel_buttons[stars]}"), Format("{join_channel_star_link}")),
    Url(Format("{join_channel_buttons[other]}"), Format("{join_channel_request_link}")),
    Button(Const("Close"), id="close", on_click=close_join_channel_dialog),
    getter=[get_join_channel_message, get_join_channel_buttons, get_join_channel_star_link, get_join_channel_request_link],
    state=JoinChannelStatesGroup.MAIN
)
