from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Url, Button
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from handlers.handlers import on_another_payment_button
from lang import Lang
from states.state_group import JoinChannelStatesGroup
from windows.common_elements import get_localized_close_button

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
        Lang.ENG: {"stars": "⭐ Telegram stars", "other": "💸 Other payment"},
        Lang.RUS: {"stars": "⭐ Telegram stars", "other": "💸 Другой способ оплаты"},
        Lang.ESP: {"stars": "⭐ Telegram stars", "other": "💸 Otro pago"},
        Lang.DEU: {"stars": "⭐ Telegram stars", "other": "💸 Andere Zahlung"},
        Lang.FRA: {"stars": "⭐ Telegram stars", "other": "💸 Autre paiement"},
        Lang.ARA: {"stars": "⭐ Telegram stars", "other": "💸 دفع آخر"},
        Lang.CHI: {"stars": "⭐ Telegram stars", "other": "💸 其他付款"},
        Lang.HIN: {"stars": "⭐ Telegram stars", "other": "💸 अन्य भुगतान"},
        Lang.JPN: {"stars": "⭐ Telegram stars", "other": "💸 その他の支払い"}
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"join_channel_buttons": lang_messages.get(selected_lang, {"stars": "Telegram stars", "other": "Other payment"})}


async def get_join_channel_star_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_star_link": "https://t.me/+0-JREGcV0KBiOTM0"}
    return {"join_channel_star_link": "https://t.me/+zTjKEuObGCw2NWFk"}



def create_join_channel_window():
    window = [
        Window(
            Format("{join_channel_message}"),
            Url(Format("{join_channel_buttons[stars]}"), Format("{join_channel_star_link}")),
            Button(Format("{join_channel_buttons[other]}"), id="another_payment_button", on_click=on_another_payment_button),
            *get_localized_close_button(F),
            getter=[get_join_channel_message, get_join_channel_buttons, get_join_channel_star_link],
            state=JoinChannelStatesGroup.MAIN
        )]
    return window