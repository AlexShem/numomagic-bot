from logger.logger import get_logger
from datetime import date

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from lang import Lang
import energy
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates, JoinChannelStatesGroup

logger = get_logger(__name__)


# This function is called when the user starts the bot.
async def start(message: Message, dialog_manager: DialogManager):
    logger.warning(f"User {message.from_user.username} started a bot")
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)


# This function is called when the user selects a language.
async def on_lang_selected(callback: CallbackQuery, button: Button, manager: DialogManager):
    """
    Handles the event when a language is selected by the user.

    Args:
        callback (CallbackQuery): The callback query from the user interaction.
        button (Button): The button that was pressed to select the language.
        manager (DialogManager): The dialog manager handling the current dialog state.

    This function sets the selected language in the dialog data based on the button pressed.
    It then switches the dialog state to the calendar view and logs the selected language.
    """
    if button.widget_id == Lang.ESP.value:
        manager.dialog_data["lang"] = Lang.ESP
    elif button.widget_id == Lang.RUS.value:
        manager.dialog_data["lang"] = Lang.RUS
    elif button.widget_id == Lang.DEU.value:
        manager.dialog_data["lang"] = Lang.DEU
    elif button.widget_id == Lang.FRA.value:
        manager.dialog_data["lang"] = Lang.FRA
    elif button.widget_id == Lang.ARA.value:
        manager.dialog_data["lang"] = Lang.ARA
    elif button.widget_id == Lang.CHI.value:
        manager.dialog_data["lang"] = Lang.CHI
    elif button.widget_id == Lang.HIN.value:
        manager.dialog_data["lang"] = Lang.HIN
    elif button.widget_id == Lang.JPN.value:
        manager.dialog_data["lang"] = Lang.JPN
    else:
        manager.dialog_data["lang"] = Lang.ENG

    await manager.switch_to(DialogSG.CALENDAR)
    logger.warning(f"User {callback.from_user.username} selected language {manager.dialog_data['lang']}")


def prepare_user_energy_output(energy_levels, lang: Lang, selected_date: date):
    # Converts range strings like "1-5" or "5-10" to list
    def to_range(rng):
        if not "-" in rng:
            return list([int(rng)])
        range_start, range_end = map(int, rng.split("-"))
        range_object = range(range_start, range_end + 1)
        range_list = list(range_object)
        return range_list

    energy_level_dictionary = energy.load(len(energy_levels), lang)
    lang_messages = {
        Lang.RUS: {
            "date": "Дата",
            "time": "Время",
            "recommendation": "Рекомендация"
        },
        Lang.ENG: {
            "date": "Date",
            "time": "Time",
            "recommendation": "Recommendation"
        },
        Lang.ESP: {
            "date": "Fecha",
            "time": "Hora",
            "recommendation": "Recomendación"
        },
        Lang.DEU: {
            "date": "Datum",
            "time": "Zeit",
            "recommendation": "Empfehlung"
        },
        Lang.FRA: {
            "date": "Date",
            "time": "Heure",
            "recommendation": "Recommandation"
        },
        Lang.ARA: {
            "date": "تاريخ",
            "time": "وقت",
            "recommendation": "توصية"
        },
        Lang.CHI: {
            "date": "日期",
            "time": "时间",
            "recommendation": "建议"
        },
        Lang.HIN: {
            "date": "तारीख",
            "time": "समय",
            "recommendation": "सिफारिश"
        },
        Lang.JPN: {
            "date": "日付",
            "time": "時間",
            "recommendation": "推奨事項"
        }
    }

    result = list()
    for i, (time_period, items) in enumerate(energy_level_dictionary.items()):
        for energy_value, description in items.items():
            if energy_levels[i] in to_range(energy_value):
                messages = lang_messages.get(lang, lang_messages[Lang.ENG])
                result.append(f"🗓 {messages['date']}: {selected_date}\n🕒 {messages['time']}: {time_period}\n\n📌 {messages['recommendation']}:\n{description}")
    return result


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    energy_levels = energy.get_energy_levels(selected_date.year, selected_date.month, selected_date.day)
    lang = manager.dialog_data.get("lang", Lang.ENG)
    prepared_answer = prepare_user_energy_output(energy_levels, lang, selected_date)
    dialog_data = {f"period_{i + 1}": text for i, text in enumerate(prepared_answer)}
    dialog_data["lang"] = lang

    logger.warning(f"User {callback.from_user.username} selected date {selected_date}, energy levels: {energy_levels}")
    logger.warning(f"The dialog data is: {dialog_data}")

    if len(prepared_answer) == 4:
        await manager.start(FourDigitsStates.PERIOD1, data=dialog_data)
    elif len(prepared_answer) == 5:
        await manager.start(FiveDigitsStates.PERIOD1, data=dialog_data)
    else:
        await manager.start(SixDigitsStates.PERIOD1, data=dialog_data)
    logger.warning(f"User {callback.from_user.username} selected date {selected_date}, energy levels: {energy_levels}")


# When the user selects the "Close" recommendation button, display the calendar view.
async def close_recommendation_dialog(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.done()


async def on_4_1(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FourDigitsStates.PERIOD1)


async def on_4_2(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FourDigitsStates.PERIOD2)


async def on_4_3(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FourDigitsStates.PERIOD3)


async def on_4_4(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FourDigitsStates.PERIOD4)


async def on_5_1(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FiveDigitsStates.PERIOD1)


async def on_5_2(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FiveDigitsStates.PERIOD2)


async def on_5_3(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FiveDigitsStates.PERIOD3)


async def on_5_4(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FiveDigitsStates.PERIOD4)


async def on_5_5(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(FiveDigitsStates.PERIOD5)


async def on_6_1(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD1)


async def on_6_2(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD2)


async def on_6_3(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD3)


async def on_6_4(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD4)


async def on_6_5(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD5)


async def on_6_6(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(SixDigitsStates.PERIOD6)


# Join channel dialog handlers ------------------------------------------------

async def on_join_channel(callback: CallbackQuery, button, manager: DialogManager):
    logger.warning(f"User {callback.from_user.username} selected to join the channel")
    logger.warning(f"The dialog data is: {manager.start_data}")
    await manager.start(JoinChannelStatesGroup.MAIN, data=manager.start_data)


async def close_join_channel_dialog(callback: CallbackQuery, button, manager: DialogManager):
    await manager.done()


async def get_join_channel_message(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        Lang.ENG: "You can learn more about numerology on our Telegram channel. "
                        "To get access to the channel, you can pay in Telegram Stars or send a join request and pay using a bank transfer. "
                        "Click the buttons below to get access to the channel.",
        Lang.RUS: "Вы можете узнать больше о нумерологии на нашем Telegram-канале. "
                        "Чтобы получить доступ к каналу, вы можете оплатить в Telegram Stars или отправить запрос на вступление и оплатить банковским переводом. "
                        "Нажмите на кнопки ниже, чтобы получить доступ к каналу.",
        Lang.ESP: "Puede obtener más información sobre numerología en nuestro canal de Telegram. "
                        "Para acceder al canal, puede pagar en Telegram Stars o enviar una solicitud de unirse y pagar mediante una transferencia bancaria. "
                        "Haga clic en los botones a continuación para acceder al canal.",
        Lang.DEU: "Sie können mehr über Numerologie auf unserem Telegram-Kanal erfahren. "
                        "Um Zugriff auf den Kanal zu erhalten, können Sie in Telegram Stars bezahlen oder eine Beitrittsanfrage senden und per Banküberweisung bezahlen. "
                        "Klicken Sie auf die Schaltflächen unten, um Zugriff auf den Kanal zu erhalten.",
        Lang.FRA: "Vous pouvez en apprendre plus sur la numérologie sur notre chaîne Telegram. "
                        "Pour accéder à la chaîne, vous pouvez payer en étoiles Telegram ou envoyer une demande de rejoindre et payer par virement bancaire. "
                        "Cliquez sur les boutons ci-dessous pour accéder à la chaîne.",
        Lang.ARA: "يمكنك معرفة المزيد حول علم الأعداد على قناتنا على تطبيق تليجرام. "
                        "للوصول إلى القناة، يمكنك الدفع بنجوم تليجرام أو إرسال طلب انضمام والدفع عبر التحويل المصرفي. "
                        "انقر على الأزرار أدناه للوصول إلى القناة.",
        Lang.CHI: "您可以在我们的Telegram频道上了解更多关于数字学的信息。 "
                        "要访问频道，您可以使用Telegram Stars支付或发送加入请求并通过银行转账支付。 "
                        "单击下面的按钮以访问频道。",
        Lang.HIN: "आप हमारे टेलीग्राम चैनल पर अंकशास्त्र के बारे में अधिक जान सकते हैं। "
                        "चैनल तक पहुंचने के लिए, आप टेलीग्राम स्टार्स में भुगतान कर सकते हैं या ज्वाइन अनुरोध भेजकर बैंक ट्रांसफर के जरिए भुगतान कर सकते हैं। "
                        "चैनल तक पहुंचने के लिए नीचे दिए गए बटन पर क्लिक करें।",
        Lang.JPN: "当社のTelegramチャンネルで数秘術について詳しく知ることができます。 "
                        "チャンネルにアクセスするには、Telegram Starsで支払うか、参加リクエストを送信して銀行振込で支払うことができます。 "
                        "チャンネルにアクセスするには、以下のボタンをクリックしてください。"
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"join_channel_message": lang_messages.get(selected_lang, "You can learn more about numerology on our Telegram channel. "
                        "To get access to the channel, you can pay in Telegram Stars or send a join request and pay using a bank transfer. "
                        "Click the buttons below to get access to the channel.")}


async def get_join_channel_buttons(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        Lang.ENG: {"stars": "⭐Telegram stars", "other": "💸Other payment"},
        Lang.RUS: {"stars": "⭐Telegram stars", "other": "💸Другой способ оплаты"},
        Lang.ESP: {"stars": "⭐Telegram stars", "other": "💸Otro pago"},
        Lang.DEU: {"stars": "⭐Telegram stars", "other": "💸Andere Zahlung"},
        Lang.FRA: {"stars": "⭐Telegram stars", "other": "💸Autre paiement"},
        Lang.ARA: {"stars": "⭐Telegram stars", "other": "💸دفع آخر"},
        Lang.CHI: {"stars": "⭐Telegram stars", "other": "💸其他付款"},
        Lang.HIN: {"stars": "⭐Telegram stars", "other": "💸अन्य भुगतान"},
        Lang.JPN: {"stars": "⭐Telegram stars", "other": "💸その他の支払い"}
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"join_channel_buttons": lang_messages.get(selected_lang, {"stars": "Telegram stars", "other": "Other payment"})}


async def get_join_channel_star_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_star_link": "https://t.me/+0-JREGcV0KBiOTM0"}
    return {"join_channel_star_link": "https://t.me/+zTjKEuObGCw2NWFk"}


async def get_join_channel_request_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_request_link": "https://t.me/+9t7ylcITlJdmYTk0"}
    return {"join_channel_request_link": "https://t.me/+zTjKEuObGCw2NWFk"}
