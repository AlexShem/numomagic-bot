from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Url, Button, Row
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from handlers.handlers import on_another_payment_button
from lang import Lang
from states.state_group import JoinChannelStatesGroup
from windows.common_elements import get_localized_close_button

async def get_join_channel_message(dialog_manager: DialogManager, **kwargs):
    proof_contact = "@PremiumCenterLTD"

    lang_messages = {
        Lang.RUS: "✨ Добро пожаловать в мир магии и нумерологии! ✨\n\n"
                        "Если вам нравится открывать и использовать прогнозирование в области эзотерики, обязательно посетите наш закрытый канал. "
                        "Вы откроете для себя ритуальную часть нумерологии через магию чисел и кодов.🔮\n\n"
                        "⭐️ Если у вас есть Telegram Premium, вы можете использовать 500 звезд в месяц для получения доступа к эксклюзивным материалам! Это простой и удобный способ приобщиться к тайным знаниям.\n\n"
                        "💳 Чтобы оплатить картой, просто нажмите на кнопку подписки и следуйте инструкциям бота Tribute. Вам нужно будет разрешить боту отправлять вам сообщения для завершения платежа.\n\n"
                        f"❓ Есть вопросы? Не стесняйтесь обращаться в нашу службу поддержки по адресу {proof_contact}.",

        Lang.ENG: "✨ Welcome to the world of magic and numerology! ✨\n\n"
                        "If you enjoy exploring and utilizing predictions in the realm of esotericism, be sure to visit our private channel. "
                        "You will discover the ritualistic side of numerology through the magic of numbers and codes.🔮\n\n"
                        "⭐️ If you have Telegram Premium, you can use 500 stars per month to gain access to exclusive materials! It's a simple and convenient way to tap into secret knowledge.\n\n"
                        "💳 To pay with a card, simply click the subscription button and follow the Tribute bot’s instructions. You’ll need to allow the bot to send you messages to complete the payment.\n\n"
                        f"❓ Have questions? Feel free to reach out to our support team at {proof_contact}.",

        Lang.ESP: "✨ ¡Bienvenido al mundo de la magia y la numerología! ✨\n\n"
                        "Si disfrutas explorando y utilizando predicciones en el ámbito de la esoterismo, no olvides visitar nuestro canal privado. "
                        "Descubrirás el lado ritualista de la numerología a través de la magia de los números y los códigos.🔮\n\n"
                        "⭐️ Si tienes Telegram Premium, puedes usar 500 estrellas por mes para acceder a materiales exclusivos. ¡Es una forma simple y conveniente de acceder a conocimientos secretos!\n\n"
                        "💳 Para pagar con tarjeta, simplemente haz clic en el botón de suscripción y sigue las instrucciones del bot Tribute. Necesitarás permitir que el bot te envíe mensajes para completar el pago.\n\n"
                        f"❓ ¿Tienes preguntas? No dudes en ponerte en contacto con nuestro equipo de soporte en {proof_contact}.",

        Lang.DEU: "✨ Willkommen in der Welt der Magie und Numerologie! ✨\n\n"
                        "Wenn Sie es lieben, Vorhersagen in der Welt der Esoterik zu erkunden und zu nutzen, sollten Sie unbedingt unseren privaten Kanal besuchen. "
                        "Entdecken Sie die rituelle Seite der Numerologie durch die Magie der Zahlen und Codes.🔮\n\n"
                        "⭐️ Wenn Sie Telegram Premium haben, können Sie 500 Sterne pro Monat nutzen, um Zugang zu exklusiven Materialien zu erhalten! Es ist ein einfacher und bequemer Weg, geheimes Wissen zu nutzen.\n\n"
                        "💳 Um mit einer Karte zu bezahlen, klicken Sie einfach auf die Abonnement-Schaltfläche und folgen Sie den Anweisungen des Tribute-Bots. Sie müssen dem Bot erlauben, Ihnen Nachrichten zu senden, um die Zahlung abzuschließen.\n\n"
                        f"❓ Haben Sie Fragen? Zögern Sie nicht, sich an unser Support-Team unter {proof_contact} zu wenden.",

        Lang.FRA: "✨ Bienvenue dans le monde de la magie et de la numérologie ! ✨\n\n"
                        "Si vous aimez explorer et utiliser les prédictions dans le domaine de l'ésotérisme, n'oubliez pas de visiter notre chaîne privée. "
                        "Vous découvrirez le côté rituel de la numérologie à travers la magie des nombres et des codes.🔮\n\n"
                        "⭐️ Si vous avez Telegram Premium, vous pouvez utiliser 500 étoiles par mois pour accéder à des contenus exclusifs ! C'est un moyen simple et pratique de puiser dans des connaissances secrètes.\n\n"
                        "💳 Pour payer par carte, cliquez simplement sur le bouton d'abonnement et suivez les instructions du bot Tribute. Vous devrez autoriser le bot à vous envoyer des messages pour finaliser le paiement.\n\n"
                        f"❓ Vous avez des questions ? N'hésitez pas à contacter notre équipe de support à {proof_contact}.",

        Lang.ARA: "✨ مرحبًا بكم في عالم السحر وعلم الأرقام! ✨\n\n"
                        "إذا كنت تستمتع باستكشاف واستخدام التنبؤات في عالم الروحانيات، فلا تفوت زيارة قناتنا الخاصة. "
                        "ستكتشف الجانب الطقسي لعلم الأرقام من خلال سحر الأرقام والرموز.🔮\n\n"
                        "⭐️ إذا كان لديك Telegram Premium، يمكنك استخدام 500 نجمة شهريًا للوصول إلى المواد الحصرية! إنه وسيلة بسيطة ومريحة للوصول إلى المعرفة السرية.\n\n"
                        "💳 للدفع بالبطاقة، اضغط ببساطة على زر الاشتراك واتبع تعليمات البوت Tribute. ستحتاج إلى السماح للبوت بإرسال الرسائل إليك لإتمام الدفع.\n\n"
                        f"❓ هل لديك أسئلة؟ لا تتردد في الاتصال بفريق الدعم الخاص بنا على {proof_contact}.",

        Lang.CHI: "✨ 欢迎来到魔法与数字学的世界！ ✨\n\n"
                        "如果您喜欢探索和利用预测，务必访问我们的私人频道。"
                        "您将通过数字和代码的魔法发现数字学的仪式化一面。🔮\n\n"
                        "⭐️ 如果您有 Telegram Premium，您每月可以使用 500 星星来获得独家材料的访问权限！这是获取秘密知识的简单便捷方式。\n\n"
                        "💳 要使用银行卡支付，只需点击订阅按钮，并按照 Tribute 机器人的指示操作。您需要允许机器人向您发送消息以完成付款。\n\n"
                        f"❓ 有问题吗？请随时联系我们的支持团队 {proof_contact}。",

        Lang.HIN: "✨ जादू और अंक ज्योतिष की दुनिया में आपका स्वागत है! ✨\n\n"
                        "यदि आपको गूढ़शास्त्र की दुनिया में भविष्यवाणियों का पता लगाना और उनका उपयोग करना पसंद है, तो हमारे निजी चैनल की सदस्यता अवश्य लें। "
                        "आप संख्याओं और कोड की जादुई दुनिया के माध्यम से अंक ज्योतिष के अनुष्ठानिक पक्ष की खोज करेंगे।🔮\n\n"
                        "⭐️ यदि आपके पास Telegram Premium है, तो आप 500 सितारों का उपयोग करके विशेष सामग्री तक पहुंच सकते हैं! यह गुप्त ज्ञान तक पहुंचने का एक सरल और सुविधाजनक तरीका है।\n\n"
                        "💳 कार्ड से भुगतान करने के लिए, बस सब्सक्रिप्शन बटन पर क्लिक करें और Tribute बॉट के निर्देशों का पालन करें। आपको भुगतान पूरा करने के लिए बॉट को संदेश भेजने की अनुमति देनी होगी।\n\n"
                        f"❓ कोई सवाल है? कृपया {proof_contact} पर हमारी सहायता टीम से संपर्क करें।",

        Lang.JPN: "✨ 魔法と数秘術の世界へようこそ！ ✨\n\n"
                        "予言を探求し、活用するのが好きな方は、ぜひ私たちのプライベートチャンネルを訪れてください。 "
                        "数秘術の儀式的な側面を、数字とコードの魔法を通じて発見することができます。🔮\n\n"
                        "⭐️ Telegram Premiumをお持ちの方は、月に500スターを使って限定コンテンツにアクセスできます！ 秘密の知識に触れるためのシンプルで便利な方法です。\n\n"
                        "💳 カードで支払うには、サブスクリプションボタンをクリックして、Tributeボットの指示に従ってください。 支払いを完了するために、ボットにメッセージを送信する許可が必要です。\n\n"
                        f"❓ 質問がありますか？ サポートチームまでお気軽にお問い合わせください {proof_contact}。"
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"join_channel_message": lang_messages.get(selected_lang, "You can learn more about numerology on our Telegram channel. "
                        "To get access to the channel, you can pay in Telegram Stars or send a join request and pay using a bank transfer. "
                        "Click the buttons below to get access to the channel.")}


async def get_join_channel_buttons(dialog_manager: DialogManager, **kwargs):
    lang_messages = {
        Lang.ENG: {"stars": "⭐ Telegram stars", "card_monthly": "💳 Card (Monthly)", "card_yearly": "💳 Card (Yearly)", "other": "💸 Other payment"},
        Lang.RUS: {"stars": "⭐ Telegram stars", "card_monthly": "💳 Карта (Ежемесячно)", "card_yearly": "💳 Карта (Ежегодно)", "other": "💸 Другой способ оплаты"},
        Lang.ESP: {"stars": "⭐ Telegram stars", "card_monthly": "💳 Tarjeta (Mensual)", "card_yearly": "💳 Tarjeta (Anual)", "other": "💸 Otro pago"},
        Lang.DEU: {"stars": "⭐ Telegram stars", "card_monthly": "💳 Karte (Monatlich)", "card_yearly": "💳 Karte (Jährlich)", "other": "💸 Andere Zahlung"},
        Lang.FRA: {"stars": "⭐ Telegram stars", "card_monthly": "💳 Carte (Mensuel)", "card_yearly": "💳 Carte (Annuel)", "other": "💸 Autre paiement"},
        Lang.ARA: {"stars": "⭐ Telegram stars", "card_monthly": "💳 بطاقة (شهريًا)", "card_yearly": "💳 بطاقة (سنويًا)", "other": "💸 دفع آخر"},
        Lang.CHI: {"stars": "⭐ Telegram stars", "card_monthly": "💳 卡 (每月)", "card_yearly": "💳 卡 (每年)", "other": "💸 其他付款"},
        Lang.HIN: {"stars": "⭐ Telegram stars", "card_monthly": "💳 कार्ड (मासिक)", "card_yearly": "💳 कार्ड (वार्षिक)", "other": "💸 अन्य भुगतान"},
        Lang.JPN: {"stars": "⭐ Telegram stars", "card_monthly": "💳 カード (月額)", "card_yearly": "💳 カード (年額)", "other": "💸 その他の支払い"}
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"join_channel_buttons": lang_messages.get(selected_lang, {"stars": "Telegram stars", "other": "Other payment"})}


async def get_join_channel_star_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_star_link": "https://t.me/+9_OFSHP1TDkwZTE0"}
    elif selected_lang == Lang.ENG:
        return {"join_channel_star_link": "https://t.me/+fEHq8cfO_ZkyZTFk"}
    elif selected_lang == Lang.ESP:
        return {"join_channel_star_link": "https://t.me/+iLXGQeQ0cPUxZDdk"}
    elif selected_lang == Lang.DEU:
        return {"join_channel_star_link": "https://t.me/+w4Pwus6n3vNiY2I0"}
    elif selected_lang == Lang.FRA:
        return {"join_channel_star_link": "https://t.me/+Fsx6VOCQEKQ1N2Q0"}
    elif selected_lang == Lang.ARA:
        return {"join_channel_star_link": "https://t.me/+rLhCOAsX6qQ4OGU0"}
    elif selected_lang == Lang.CHI:
        return {"join_channel_star_link": "https://t.me/+CMlr-bBOw64yZjI0"}
    elif selected_lang == Lang.HIN:
        return {"join_channel_star_link": "https://t.me/+d9ABhsgKgvtkMDBk"}
    elif selected_lang == Lang.JPN:
        return {"join_channel_star_link": "https://t.me/+3nqJNbZqyZkyZDdk"}

    # Else, return the English link
    return {"join_channel_star_link": "https://t.me/+fEHq8cfO_ZkyZTFk"}


async def get_join_channel_card_monthly_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf8Y"}
    elif selected_lang == Lang.ENG:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf8R"}
    elif selected_lang == Lang.ESP:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf91"}
    elif selected_lang == Lang.DEU:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf97"}
    elif selected_lang == Lang.FRA:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf90"}
    elif selected_lang == Lang.ARA:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf94"}
    elif selected_lang == Lang.CHI:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf95"}
    elif selected_lang == Lang.HIN:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf92"}
    elif selected_lang == Lang.JPN:
        return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf96"}

    # Else, return the English link
    return {"join_channel_card_monthly_link": "https://t.me/tribute/app?startapp=sf8R"}


async def get_join_channel_card_yearly_link(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf8Z"}
    elif selected_lang == Lang.ENG:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf8S"}
    elif selected_lang == Lang.ESP:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9f"}
    elif selected_lang == Lang.DEU:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9c"}
    elif selected_lang == Lang.FRA:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9e"}
    elif selected_lang == Lang.ARA:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9h"}
    elif selected_lang == Lang.CHI:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9i"}
    elif selected_lang == Lang.HIN:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9g"}
    elif selected_lang == Lang.JPN:
        return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf9k"}

    # Else, return the English link
    return {"join_channel_card_yearly_link": "https://t.me/tribute/app?startapp=sf8Z"}


def create_join_channel_window():
    window = [
        Window(
            Format("{join_channel_message}"),
            Url(Format("{join_channel_buttons[stars]}"), Format("{join_channel_star_link}")),
            Row(
                Url(Format("{join_channel_buttons[card_monthly]}"), Format("{join_channel_card_monthly_link}")),
                Url(Format("{join_channel_buttons[card_yearly]}"), Format("{join_channel_card_yearly_link}")),
            ),
            # TODO: Remove "Other Payment" this feature
            # Button(Format("{join_channel_buttons[other]}"), id="another_payment_button", on_click=on_another_payment_button),
            *get_localized_close_button(F),
            getter=[get_join_channel_message, get_join_channel_buttons, get_join_channel_star_link, get_join_channel_card_monthly_link, get_join_channel_card_yearly_link], #TODO: Remove "Other Payment" this feature
            state=JoinChannelStatesGroup.MAIN
        )]
    return window