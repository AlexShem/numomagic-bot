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
        Lang.RUS: "✨ Добро пожаловать в мир магии и нумерологии! ✨\n\n"
                  "Если вам нравится открывать и использовать прогнозирование в области эзотерики, обязательно посетите наш закрытый канал. "
                  "Вы откроете для себя ритуальную часть нумерологии через магию чисел и кодов.🔮\n\n"
                  "⭐️ Если у вас есть Telegram Premium, вы можете использовать 500 звезд в месяц для получения доступа к эксклюзивным материалам! Это простой и удобный способ приобщиться к тайным знаниям.\n\n"
                  "💸 Не хотите использовать звезды или нет Telegram Premium? Не проблема! Нажмите кнопку ниже, чтобы узнать, как еще можно оплатить доступ и стать частью нашего сообщества.",
        Lang.ENG: "✨ Welcome to the world of magic and numerology! ✨\n\n"
                  "If you enjoy exploring and utilizing predictions in the realm of esotericism, be sure to visit our private channel. "
                  "You will discover the ritualistic side of numerology through the magic of numbers and codes.🔮\n\n"
                  "⭐️ If you have Telegram Premium, you can use 500 stars per month to gain access to exclusive materials! It's a simple and convenient way to tap into secret knowledge.\n\n"
                  "💸 Prefer not to use stars or don’t have Telegram Premium? No problem! Click the button below to learn about other payment methods and join our community.",
        Lang.ESP: "✨ ¡Bienvenido al mundo de la magia y la numerología! ✨\n\n"
                  "Si disfrutas explorando y utilizando predicciones en el ámbito de la esoteria, asegúrate de visitar nuestro canal privado. "
                  "Descubrirás el lado ritual de la numerología a través de la magia de los números y códigos.🔮\n\n"
                  "⭐️ Si tienes Telegram Premium, puedes usar 500 estrellas al mes para acceder a materiales exclusivos. ¡Es una forma sencilla y conveniente de acceder a conocimientos secretos!\n\n"
                  "💸 ¿Prefieres no usar estrellas o no tienes Telegram Premium? ¡No hay problema! Haz clic en el botón de abajo para conocer otros métodos de pago y unirte a nuestra comunidad.",
        Lang.DEU: "✨ Willkommen in der Welt der Magie und Numerologie! ✨\n\n"
                  "Wenn Sie es genießen, Vorhersagen im Bereich der Esoterik zu erforschen und zu nutzen, sollten Sie unbedingt unserem privaten Kanal beitreten. "
                  "Sie werden die rituelle Seite der Numerologie durch die Magie der Zahlen und Codes entdecken.🔮\n\n"
                  "⭐️ Wenn Sie Telegram Premium haben, können Sie 500 Sterne pro Monat verwenden, um Zugang zu exklusiven Materialien zu erhalten! Es ist ein einfacher und bequemer Weg, geheimes Wissen zu erlangen.\n\n"
                  "💸 Möchten Sie keine Sterne verwenden oder haben Sie kein Telegram Premium? Kein Problem! Klicken Sie unten auf die Schaltfläche, um mehr über andere Zahlungsmethoden zu erfahren und unserem Kanal beizutreten.",
        Lang.FRA: "✨ Bienvenue dans le monde de la magie et de la numérologie ! ✨\n\n"
                  "Si vous aimez explorer et utiliser les prédictions dans le domaine de l'ésotérisme, assurez-vous de visiter notre canal privé. "
                  "Vous découvrirez le côté rituel de la numérologie à travers la magie des chiffres et des codes.🔮\n\n"
                  "⭐️ Si vous avez Telegram Premium, vous pouvez utiliser 500 étoiles par mois pour accéder à des matériaux exclusifs ! C'est un moyen simple et pratique d'accéder à des connaissances secrètes.\n\n"
                  "💸 Vous préférez ne pas utiliser d'étoiles ou vous n'avez pas Telegram Premium ? Pas de problème ! Cliquez sur le bouton ci-dessous pour en savoir plus sur les autres méthodes de paiement et rejoindre notre communauté.",
        Lang.ARA: "✨ مرحبًا بكم في عالم السحر والتنجيم! ✨\n\n"
                  "إذا كنت تستمتع باستكشاف واستخدام التنبؤات في مجال الروحانيات، فلا تنسَ زيارة قناتنا المغلقة. "
                  "ستكتشف الجانب الطقوسي من علم الأرقام من خلال سحر الأرقام والرموز.🔮\n\n"
                  "⭐️ إذا كان لديك Telegram Premium، يمكنك استخدام 500 نجمة شهريًا للوصول إلى مواد حصرية! إنه وسيلة بسيطة ومريحة للوصول إلى المعرفة السرية.\n\n"
                  "💸 تفضل عدم استخدام النجوم أو ليس لديك Telegram Premium؟ لا مشكلة! اضغط على الزر أدناه لتتعرف على طرق الدفع الأخرى والانضمام إلى قناتنا.",
        Lang.CHI: "✨ 欢迎来到魔法和数字学的世界！✨\n\n"
                  "如果你喜欢探索和运用神秘学领域的预测，务必访问我们的私密频道。"
                  "你将通过数字和代码的魔力，发现数字学的仪式部分。🔮\n\n"
                  "⭐️ 如果你有 Telegram Premium，你可以每月使用 500 星来获得独家内容的访问权限！这是一种简单便捷的方式，接触到秘密知识。\n\n"
                  "💸 不想使用星星或没有 Telegram Premium？没问题！点击下方按钮了解其他支付方式并加入我们的频道。",
        Lang.HIN: "✨ जादू और अंकशास्त्र की दुनिया में आपका स्वागत है! ✨\n\n"
                  "यदि आपको गूढ़ विद्या के क्षेत्र में भविष्यवाणियों का उपयोग और अन्वेषण करना पसंद है, तो हमारे निजी चैनल का दौरा अवश्य करें। "
                  "आप अंकों और कोड्स के जादू के माध्यम से अंकशास्त्र के अनुष्ठानिक भाग की खोज करेंगे।🔮\n\n"
                  "⭐️ यदि आपके पास Telegram Premium है, तो आप 500 स्टार्स प्रति माह का उपयोग करके विशेष सामग्री प्राप्त कर सकते हैं! यह गुप्त ज्ञान का हिस्सा बनने का एक सरल और सुविधाजनक तरीका है।\n\n"
                  "💸 स्टार्स का उपयोग नहीं करना चाहते या आपके पास Telegram Premium नहीं है? कोई समस्या नहीं! नीचे दिए गए बटन पर क्लिक करें और अन्य भुगतान विधियों के बारे में जानें और हमारे चैनल का हिस्सा बनें।",
        Lang.JPN: "✨ 魔法と数秘術の世界へようこそ！✨\n\n"
                  "占いの分野で予測を探求し、活用することが好きなら、ぜひ私たちの非公開チャンネルを訪れてください。 "
                  "あなたは、数字とコードの魔法を通じて、数秘術の儀式的な側面を発見するでしょう。🔮\n\n"
                  "⭐️ Telegram Premiumをお持ちの方は、月額500スターを利用して独占コンテンツにアクセスできます！ 秘密の知識に触れるための簡単で便利な方法です。\n\n"
                  "💸 スターを利用したくない、またはTelegram Premiumをお持ちでない方は？ 問題ありません！他の支払い方法について確認し、コミュニティに参加するには、下のボタンをクリックしてください。"
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