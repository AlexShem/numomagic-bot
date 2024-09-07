from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from lang import Lang
from states.state_group import PaymentStatesGroup
from windows.common_elements import create_payment_buttons_group, get_localized_close_button


async def get_bank_payment_description(dialog_manager: DialogManager, **kwargs):
    proof_contact = "@JelenaLahmane"
    amount_monthly = 12
    amount_yearly = 120

    lang_messages = {
        Lang.ENG: "✨ How to Get Access to Our Private Channel ✨\n\n"
                  "To join our private channel and access exclusive content, follow these easy steps:\n\n"
                  "1️⃣ Click the 'Join Channel' button below to request access.\n\n"
                  "2️⃣ Complete the payment using the Bank Transfer details below.\n\n"
                  "💳 Bank Transfer Details:\n"
                  "- Company Name: PREMIUM CENTER LTD\n"
                  "- Bank: Bank of Scotland\n"
                  "- Bank Address: 75 George St, Edinburgh EH2 3EW\n"
                  "- Company Address: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN: GB97BOFS80226017831966\n"
                  "- BIC: BOFSGBS1SDP\n\n"
                  "💡 Please make sure to include your Telegram username (e.g., @username) in the payment message.\n\n"
                  f"💶 The monthly subscription is {amount_monthly} EUR, and the one-year subscription is {amount_yearly} EUR.\n\n"
                  f"3️⃣ Important: After completing the payment, please send us a confirmation screenshot or payment receipt via chat with {proof_contact} so we can approve your access.\n\n"
                  "💡 Note: If you need help or have any questions, feel free to reach out!",
        Lang.RUS: "✨ Как получить доступ к нашему закрытому каналу ✨\n\n"
                  "Чтобы присоединиться к нашему закрытому каналу и получить доступ к эксклюзивным материалам, выполните следующие шаги:\n\n"
                  "1️⃣ Нажмите кнопку 'Подключиться к каналу' ниже, чтобы подать заявку на доступ.\n\n"
                  "2️⃣ Завершите оплату, используя следующие реквизиты для банковского перевода:\n\n"
                  "💳 Реквизиты банковского перевода:\n"
                  "- Название компании: PREMIUM CENTER LTD\n"
                  "- Банк: Bank of Scotland\n"
                  "- Адрес банка: 75 George St, Edinburgh EH2 3EW\n"
                  "- Адрес компании: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN: GB97BOFS80226017831966\n"
                  "- BIC: BOFSGBS1SDP\n\n"
                  "💡 Пожалуйста, обязательно укажите свой Telegram-логин (например, @username) в сообщении к платежу.\n\n"
                  f"💶 Месячная подписка составляет {amount_monthly} EUR, годовая подписка — {amount_yearly} EUR.\n\n"
                  f"3️⃣ Важно: После завершения оплаты отправьте нам подтверждение или квитанцию о платеже через чат с {proof_contact}, чтобы мы могли подтвердить ваш доступ.\n\n"
                  "💡 Примечание: Если у вас есть вопросы, не стесняйтесь обращаться к нам!",
        Lang.ESP: "✨ Cómo obtener acceso a nuestro canal privado ✨\n\n"
                  "Para unirte a nuestro canal privado y acceder a contenido exclusivo, sigue estos pasos:\n\n"
                  "1️⃣ Haz clic en el botón 'Unirse al canal' abajo para solicitar acceso.\n\n"
                  "2️⃣ Completa el pago utilizando los detalles de la transferencia bancaria a continuación:\n\n"
                  "💳 Detalles de la transferencia bancaria:\n"
                  "- Nombre de la compañía: PREMIUM CENTER LTD\n"
                  "- Banco: Bank of Scotland\n"
                  "- Dirección del banco: 75 George St, Edinburgh EH2 3EW\n"
                  "- Dirección de la compañía: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN: GB97BOFS80226017831966\n"
                  "- BIC: BOFSGBS1SDP\n\n"
                  "💡 Asegúrate de incluir tu nombre de usuario de Telegram (por ejemplo, @username) en el mensaje de pago.\n\n"
                  f"💶 La suscripción mensual es de {amount_monthly} EUR, y la suscripción anual es de {amount_yearly} EUR.\n\n"
                  f"3️⃣ Importante: Después de completar el pago, envíanos una captura de pantalla o recibo de confirmación a través del chat con {proof_contact} para que podamos aprobar tu acceso.\n\n"
                  "💡 Nota: Si necesitas ayuda o tienes alguna pregunta, no dudes en contactarnos!",
        Lang.DEU: "✨ Wie Sie Zugang zu unserem privaten Kanal erhalten ✨\n\n"
                  "Um unserem privaten Kanal beizutreten und exklusiven Zugang zu erhalten, befolgen Sie diese einfachen Schritte:\n\n"
                  "1️⃣ Klicken Sie unten auf die Schaltfläche 'Kanal beitreten', um den Zugang zu beantragen.\n\n"
                  "2️⃣ Schließen Sie die Zahlung mit den untenstehenden Banküberweisungsdaten ab:\n\n"
                  "💳 Banküberweisungsdetails:\n"
                  "- Firmenname: PREMIUM CENTER LTD\n"
                  "- Bank: Bank of Scotland\n"
                  "- Bankadresse: 75 George St, Edinburgh EH2 3EW\n"
                  "- Firmenadresse: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN: GB97BOFS80226017831966\n"
                  "- BIC: BOFSGBS1SDP\n\n"
                  "💡 Bitte geben Sie in der Zahlungsnachricht unbedingt Ihren Telegram-Benutzernamen an (z. B. @username).\n\n"
                  f"💶 Das monatliche Abonnement kostet {amount_monthly} EUR, das Jahresabonnement {amount_yearly} EUR.\n\n"
                  f"3️⃣ Wichtig: Nach Abschluss der Zahlung senden Sie uns bitte einen Bestätigungs-Screenshot oder die Zahlungsquittung über den Chat mit {proof_contact}, damit wir Ihren Zugang freischalten können.\n\n"
                  "💡 Hinweis: Wenn Sie Hilfe benötigen oder Fragen haben, zögern Sie nicht, uns zu kontaktieren!",
        Lang.FRA: "✨ Comment obtenir l'accès à notre chaîne privée ✨\n\n"
                  "Pour rejoindre notre chaîne privée et accéder à du contenu exclusif, suivez ces étapes simples :\n\n"
                  "1️⃣ Cliquez sur le bouton 'Rejoindre le canal' ci-dessous pour demander l'accès.\n\n"
                  "2️⃣ Complétez le paiement en utilisant les informations de virement bancaire ci-dessous :\n\n"
                  "💳 Détails du virement bancaire :\n"
                  "- Nom de l'entreprise : PREMIUM CENTER LTD\n"
                  "- Banque : Bank of Scotland\n"
                  "- Adresse de la banque : 75 George St, Edinburgh EH2 3EW\n"
                  "- Adresse de l'entreprise : 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN : GB97BOFS80226017831966\n"
                  "- BIC : BOFSGBS1SDP\n\n"
                  "💡 Assurez-vous d'indiquer votre nom d'utilisateur Telegram (par exemple, @username) dans le message de paiement.\n\n"
                  f"💶 L'abonnement mensuel est de {amount_monthly} EUR, et l'abonnement annuel est de {amount_yearly} EUR.\n\n"
                  f"3️⃣ Important : Après avoir effectué le paiement, envoyez-nous une capture d'écran de confirmation ou le reçu de paiement via le chat avec {proof_contact} afin que nous puissions approuver votre accès.\n\n"
                  "💡 Remarque : Si vous avez besoin d'aide ou si vous avez des questions, n'hésitez pas à nous contacter !",
        Lang.ARA: "✨ كيفية الحصول على الوصول إلى قناتنا الخاصة ✨\n\n"
                  "للانضمام إلى قناتنا الخاصة والحصول على محتوى حصري، اتبع هذه الخطوات البسيطة:\n\n"
                  "1️⃣ اضغط على زر 'انضم إلى القناة' أدناه لطلب الوصول.\n\n"
                  "2️⃣ أكمل الدفع باستخدام تفاصيل التحويل البنكي أدناه:\n\n"
                  "💳 تفاصيل التحويل البنكي:\n"
                  "- اسم الشركة: PREMIUM CENTER LTD\n"
                  "- البنك: Bank of Scotland\n"
                  "- عنوان البنك: 75 George St, Edinburgh EH2 3EW\n"
                  "- عنوان الشركة: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                  "- IBAN: GB97BOFS80226017831966\n"
                  "- BIC: BOFSGBS1SDP\n\n"
                  "💡 يرجى التأكد من تضمين اسم المستخدم الخاص بك على Telegram (على سبيل المثال، @username) في رسالة الدفع.\n\n"
                  f"💶 الاشتراك الشهري هو {amount_monthly} يورو، والاشتراك السنوي هو {amount_yearly} يورو.\n\n"
                  f"3️⃣ مهم: بعد إتمام الدفع، يرجى إرسال لقطة شاشة أو إيصال الدفع عبر الدردشة مع {proof_contact} حتى نتمكن من الموافقة على وصولك.\n\n"
                  "💡 ملاحظة: إذا كنت بحاجة إلى مساعدة أو لديك أي استفسارات، لا تتردد في الاتصال بنا!",
        Lang.CHI: "✨ 如何获取我们私密频道的访问权限 ✨\n\n"
                    "要加入我们的私密频道并访问独家内容，请按照以下简单步骤操作：\n\n"
                    "1️⃣ 点击下方的'加入频道'按钮申请访问权限。\n\n"
                    "2️⃣ 使用以下银行转账详细信息完成付款：\n\n"
                    "💳 银行转账详细信息：\n"
                    "- 公司名称：PREMIUM CENTER LTD\n"
                    "- 银行：Bank of Scotland\n"
                    "- 银行地址：75 George St, Edinburgh EH2 3EW\n"
                    "- 公司地址：3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                    "- IBAN：GB97BOFS80226017831966\n"
                    "- BIC：BOFSGBS1SDP\n\n"
                    "💡 请确保在付款信息中包含您的 Telegram 用户名（例如，@username）。\n\n"
                    f"💶 月度订阅费为 {amount_monthly} 欧元，年度订阅费为 {amount_yearly} 欧元。\n\n"
                    f"3️⃣ 重要提示：付款完成后，请通过与 {proof_contact} 的聊天发送确认截图或付款收据，以便我们批准您的访问权限。\n\n"
                    "💡 注意：如果您需要帮助或有任何问题，请随时联系我们！",
        Lang.HIN: "✨ हमारे निजी चैनल तक पहुंचने का तरीका ✨\n\n"
                    "हमारे निजी चैनल में शामिल होने और विशेष सामग्री तक पहुंचने के लिए, निम्नलिखित सरल कदमों का पालन करें:\n\n"
                    "1️⃣ नीचे 'चैनल से जुड़ें' बटन पर क्लिक करके पहुंच के लिए अनुरोध करें।\n\n"
                    "2️⃣ निम्नलिखित बैंक ट्रांसफर विवरण का उपयोग करके भुगतान पूरा करें:\n\n"
                    "💳 बैंक ट्रांसफर विवरण:\n"
                    "- कंपनी का नाम: PREMIUM CENTER LTD\n"
                    "- बैंक: Bank of Scotland\n"
                    "- बैंक का पता: 75 George St, Edinburgh EH2 3EW\n"
                    "- कंपनी का पता: 3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                    "- IBAN: GB97BOFS80226017831966\n"
                    "- BIC: BOFSGBS1SDP\n\n"
                    "💡 कृपया भुगतान संदेश में अपना Telegram उपयोगकर्ता नाम (उदाहरण के लिए, @username) शामिल करें।\n\n"
                    f"💶 मासिक सदस्यता {amount_monthly} यूरो है, और वार्षिक सदस्यता {amount_yearly} यूरो है।\n\n"
                    f"3️⃣ महत्वपूर्ण: भुगतान पूरा करने के बाद, कृपया हमें {proof_contact} के साथ चैट के माध्यम से पुष्टि स्क्रीनशॉट या भुगतान रसीद भेजें ताकि हम आपके पहुंच को स्वीकृत कर सकें।\n\n"
                    "💡 ध्यान दें: यदि आपको मदद चाहिए या कोई सवाल है, तो हमसे संपर्क करने में हिचकिचाएं नहीं!",
        Lang.JPN: "✨ 当社のプライベートチャンネルへのアクセス方法 ✨\n\n"
                    "当社のプライベートチャンネルに参加し、独占コンテンツにアクセスするには、次の簡単な手順に従ってください：\n\n"
                    "1️⃣ 下の「チャンネルに参加」ボタンをクリックしてアクセスをリクエストします。\n\n"
                    "2️⃣ 以下の銀行振込の詳細を使用して支払いを完了します：\n\n"
                    "💳 銀行振込の詳細：\n"
                    "- 会社名：PREMIUM CENTER LTD\n"
                    "- 銀行：Bank of Scotland\n"
                    "- 銀行の住所：75 George St, Edinburgh EH2 3EW\n"
                    "- 会社の住所：3/18 Hawkhill Close, Edinburgh, EH7 6FD\n"
                    "- IBAN：GB97BOFS80226017831966\n"
                    "- BIC：BOFSGBS1SDP\n\n"
                    "💡 支払いメッセージにTelegramユーザー名（例：@username）を必ず含めてください。\n\n"
                    f"💶 月額サブスクリプションは{amount_monthly}ユーロで、年間サブスクリプションは{amount_yearly}ユーロです。\n\n"
                    f"3️⃣ 重要：支払いを完了した後、{proof_contact} とのチャットで確認スクリーンショットまたは支払いレシートを送信していただくと、アクセスを承認できます。\n\n"
                    "💡 注意：お手伝いが必要な場合やご質問がある場合は、お気軽にお問い合わせください！"
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"description": lang_messages.get(selected_lang)}

async def get_revolut_payment_description(dialog_manager: DialogManager, **kwargs):
    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    if selected_lang == Lang.RUS:
        return {"description": "Оплата по Revolut на русском"}
    elif selected_lang == Lang.ENG:
        return {"description": "Payment via Revolut in English"}
    else:
        return {"description": "Payment via Revolut in English"}

async def get_paypal_payment_description(dialog_manager: DialogManager, **kwargs):
    proof_contact = "@JelenaLahmane"
    paypal_link = "https://www.paypal.com/paypalme/PremiumCenterLTD"
    paypal_email = "info@premiumctr.com"
    amount_monthly = 12
    amount_yearly = 120

    lang_messages = {
        Lang.ENG: "✨ How to Get Access to Our Private Channel via PayPal ✨\n\n"
                  "To join our private channel and access exclusive content, follow these steps:\n\n"
                  "1️⃣ Click the 'Join Channel' button below to request access.\n\n"
                  "2️⃣ Complete the payment via PayPal using one of the options below:\n\n"
                  "💳 PayPal Options:\n"
                  f"- Use this PayPal.Me link: {paypal_link}\n"
                  f"- Or manually send the payment to: {paypal_email}\n\n"
                  "💡 Make sure to include your Telegram username (e.g., @username) in the payment message.\n\n"
                  f"💶 The monthly subscription is {amount_monthly} EUR, and the one-year subscription is {amount_yearly} EUR.\n\n"
                  f"3️⃣ Important: After completing the payment, please send us a confirmation screenshot or payment receipt via chat with {proof_contact} so we can approve your access.\n\n"
                  "💡 Note: If you need help or have any questions, feel free to reach out!",
        Lang.RUS: "✨ Как получить доступ к нашему закрытому каналу через PayPal ✨\n\n"
                    "Чтобы присоединиться к нашему закрытому каналу и получить доступ к эксклюзивным материалам, выполните следующие шаги:\n\n"
                    "1️⃣ Нажмите кнопку 'Подключиться к каналу' ниже, чтобы подать заявку на доступ.\n\n"
                    "2️⃣ Завершите оплату через PayPal, используя один из вариантов ниже:\n\n"
                    "💳 Опции PayPal:\n"
                    f"- Используйте эту ссылку PayPal.Me: {paypal_link}\n"
                    f"- Или отправьте платеж вручную на: {paypal_email}\n\n"
                    "💡 Пожалуйста, обязательно укажите свой Telegram-логин (например, @username) в сообщении к платежу.\n\n"
                    f"💶 Месячная подписка составляет {amount_monthly} EUR, годовая подписка — {amount_yearly} EUR.\n\n"
                    f"3️⃣ Важно: После завершения оплаты отправьте нам подтверждение или квитанцию о платеже через чат с {proof_contact}, чтобы мы могли подтвердить ваш доступ.\n\n"
                    "💡 Примечание: Если у вас есть вопросы, не стесняйтесь обращаться к нам!",
        Lang.ESP: "✨ Cómo obtener acceso a nuestro canal privado a través de PayPal ✨\n\n"
                    "Para unirte a nuestro canal privado y acceder a contenido exclusivo, sigue estos pasos:\n\n"
                    "1️⃣ Haz clic en el botón 'Unirse al canal' abajo para solicitar acceso.\n\n"
                    "2️⃣ Completa el pago a través de PayPal utilizando una de las opciones a continuación:\n\n"
                    "💳 Opciones de PayPal:\n"
                    f"- Utiliza este enlace PayPal.Me: {paypal_link}\n"
                    f"- O envía manualmente el pago a: {paypal_email}\n\n"
                    "💡 Asegúrate de incluir tu nombre de usuario de Telegram (por ejemplo, @username) en el mensaje de pago.\n\n"
                    f"💶 La suscripción mensual es de {amount_monthly} EUR, y la suscripción anual es de {amount_yearly} EUR.\n\n"
                    f"3️⃣ Importante: Después de completar el pago, envíanos una captura de pantalla o recibo de confirmación a través del chat con {proof_contact} para que podamos aprobar tu acceso.\n\n"
                    "💡 Nota: Si necesitas ayuda o tienes alguna pregunta, no dudes en contactarnos!",
        Lang.DEU: "✨ Wie Sie Zugang zu unserem privaten Kanal über PayPal erhalten ✨\n\n"
                    "Um unserem privaten Kanal beizutreten und exklusiven Zugang zu erhalten, befolgen Sie diese Schritte:\n\n"
                    "1️⃣ Klicken Sie unten auf die Schaltfläche 'Kanal beitreten', um den Zugang zu beantragen.\n\n"
                    "2️⃣ Schließen Sie die Zahlung über PayPal mit einer der folgenden Optionen ab:\n\n"
                    "💳 PayPal-Optionen:\n"
                    f"- Verwenden Sie diesen PayPal.Me-Link: {paypal_link}\n"
                    f"- Oder senden Sie die Zahlung manuell an: {paypal_email}\n\n"
                    "💡 Bitte geben Sie in der Zahlungsnachricht unbedingt Ihren Telegram-Benutzernamen an (z. B. @username).\n\n"
                    f"💶 Das monatliche Abonnement kostet {amount_monthly} EUR, das Jahresabonnement {amount_yearly} EUR.\n\n"
                    f"3️⃣ Wichtig: Nach Abschluss der Zahlung senden Sie uns bitte einen Bestätigungs-Screenshot oder die Zahlungsquittung über den Chat mit {proof_contact}, damit wir Ihren Zugang freischalten können.\n\n"
                    "💡 Hinweis: Wenn Sie Hilfe benötigen oder Fragen haben, zögern Sie nicht, uns zu kontaktieren!",
        Lang.FRA: "✨ Comment obtenir l'accès à notre chaîne privée via PayPal ✨\n\n"
                    "Pour rejoindre notre chaîne privée et accéder à du contenu exclusif, suivez ces étapes :\n\n"
                    "1️⃣ Cliquez sur le bouton 'Rejoindre le canal' ci-dessous pour demander l'accès.\n\n"
                    "2️⃣ Complétez le paiement via PayPal en utilisant l'une des options ci-dessous :\n\n"
                    "💳 Options PayPal :\n"
                    f"- Utilisez ce lien PayPal.Me : {paypal_link}\n"
                    f"- Ou envoyez manuellement le paiement à : {paypal_email}\n\n"
                    "💡 Assurez-vous d'indiquer votre nom d'utilisateur Telegram (par exemple, @username) dans le message de paiement.\n\n"
                    f"💶 L'abonnement mensuel est de {amount_monthly} EUR, et l'abonnement annuel est de {amount_yearly} EUR.\n\n"
                    f"3️⃣ Important : Après avoir effectué le paiement, envoyez-nous une capture d'écran de confirmation ou le reçu de paiement via le chat avec {proof_contact} afin que nous puissions approuver votre accès.\n\n"
                    "💡 Remarque : Si vous avez besoin d'aide ou si vous avez des questions, n'hésitez pas à nous contacter !",
        Lang.ARA: "✨ كيفية الحصول على الوصول إلى قناتنا الخاصة عبر PayPal ✨\n\n"
                    "للانضمام إلى قناتنا الخاصة والحصول على محتوى حصري، اتبع هذه الخطوات:\n\n"
                    "1️⃣ اضغط على زر 'انضم إلى القناة' أدناه لطلب الوصول.\n\n"
                    "2️⃣ أكمل الدفع عبر PayPal باستخدام أحد الخيارات أدناه:\n\n"
                    "💳 خيارات PayPal:\n"
                    f"- استخدم هذا الرابط PayPal.Me: {paypal_link}\n"
                    f"- أو أرسل الدفع يدويًا إلى: {paypal_email}\n\n"
                    "💡 يرجى التأكد من تضمين اسم المستخدم الخاص بك على Telegram (على سبيل المثال، @username) في رسالة الدفع.\n\n"
                    f"💶 الاشتراك الشهري هو {amount_monthly} يورو، والاشتراك السنوي هو {amount_yearly} يورو.\n\n"
                    f"3️⃣ مهم: بعد إتمام الدفع، يرجى إرسال لقطة شاشة أو إيصال الدفع عبر الدردشة مع {proof_contact} حتى نتمكن من الموافقة على وصولك.\n\n"
                    "💡 ملاحظة: إذا كنت بحاجة إلى مساعدة أو لديك أي استفسارات، لا تتردد في الاتصال بنا!",
        Lang.CHI: "✨ 如何通过 PayPal 获取我们私密频道的访问权限 ✨\n\n"
                    "要加入我们的私密频道并访问独家内容，请按照以下简单步骤操作：\n\n"
                    "1️⃣ 点击下方的'加入频道'按钮申请访问权限。\n\n"
                    "2️⃣ 使用以下 PayPal 选项之一完成付款：\n\n"
                    "💳 PayPal 选项：\n"
                    f"- 使用此 PayPal.Me 链接：{paypal_link}\n"
                    f"- 或手动发送付款至：{paypal_email}\n\n"
                    "💡 请确保在付款信息中包含您的 Telegram 用户名（例如，@username）。\n\n"
                    f"💶 月度订阅费为 {amount_monthly} 欧元，年度订阅费为 {amount_yearly} 欧元。\n\n"
                    f"3️⃣ 重要提示：付款完成后，请通过与 {proof_contact} 的聊天发送确认截图或付款收据，以便我们批准您的访问权限。\n\n"
                    "💡 注意：如果您需要帮助或有任何问题，请随时联系我们！",
        Lang.HIN: "✨ PayPal के माध्यम से हमारे निजी चैनल तक पहुंचने का तरीका ✨\n\n"
                    "हमारे निजी चैनल में शामिल होने और विशेष सामग्री तक पहुंचने के लिए, निम्नलिखित सरल कदमों का पालन करें:\n\n"
                    "1️⃣ नीचे 'चैनल से जुड़ें' बटन पर क्लिक करके पहुंच के लिए अनुरोध करें।\n\n"
                    "2️⃣ निम्नलिखित PayPal विकल्प का उपयोग करके भुगतान पूरा करें:\n\n"
                    "💳 PayPal विकल्प:\n"
                    f"- इस PayPal.Me लिंक का उपयोग करें: {paypal_link}\n"
                    f"- या अपने भुगतान को मैन्युअल रूप से भेजें: {paypal_email}\n\n"
                    "💡 कृपया भुगतान संदेश में अपना Telegram उपयोगकर्ता नाम (उदाहरण के लिए, @username) शामिल करें।\n\n"
                    f"💶 मासिक सदस्यता {amount_monthly} यूरो है, और वार्षिक सदस्यता {amount_yearly} यूरो है।\n\n"
                    f"3️⃣ महत्वपूर्ण: भुगतान पूरा करने के बाद, कृपया हमें {proof_contact} के साथ चैट के माध्यम से पुष्टि स्क्रीनशॉट या भुगतान रसीद भेजें ताकि हम आपके पहुंच को स्वीकृत कर सकें।\n\n",
        Lang.JPN: "✨ PayPal を利用して当社のプライベートチャンネルにアクセスする方法 ✨\n\n"
                    "当社のプライベートチャンネルに参加し、独占コンテンツにアクセスするには、次の簡単な手順に従ってください：\n\n"
                    "1️⃣ 下の「チャンネルに参加」ボタンをクリックしてアクセスをリクエストします。\n\n"
                    "2️⃣ 以下の PayPal オプションのいずれかを使用して支払いを完了します：\n\n"
                    "💳 PayPal オプション：\n"
                    f"- この PayPal.Me リンクを使用する：{paypal_link}\n"
                    f"- または手動で支払いを送信する：{paypal_email}\n\n"
                    "💡 支払いメッセージにTelegramユーザー名（例：@username）を必ず含めてください。\n\n"
                    f"💶 月額サブスクリプションは{amount_monthly}ユーロで、年間サブスクリプションは{amount_yearly}ユーロです。\n\n"
                    f"3️⃣ 重要：支払いを完了した後、{proof_contact} とのチャットで確認スクリーンショットまたは支払いレシートを送信していただくと、アクセスを承認できます。\n\n"
                    "💡 注意：お手伝いが必要な場合やご質問がある場合は、お気軽にお問い合わせください！"
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"description": lang_messages.get(selected_lang)}

async def get_uk_bank_payment_description(dialog_manager: DialogManager, **kwargs):
    proof_contact = "@JelenaLahmane"
    amount_monthly = 12
    amount_yearly = 120

    lang_messages = {
        Lang.ENG: "✨ How to Get Access to Our Private Channel via UK Bank Transfer ✨\n\n"
                  "To join our private channel and access exclusive content, follow these steps:\n\n"
                  "1️⃣ Click the 'Join Channel' button below to request access.\n\n"
                  "2️⃣ Complete the payment using the UK Bank Transfer details below:\n\n"
                  "💳 UK Bank Transfer Details:\n"
                  "- Company Name: PREMIUM CENTER LTD\n"
                  "- Sort code: 80-22-60\n"
                  "- Account number: 17831966\n\n"
                  "💡 Make sure to include your Telegram username (e.g., @username) in the payment message.\n\n"
                  f"💶 The monthly subscription is {amount_monthly} EUR, and the one-year subscription is {amount_yearly} EUR.\n\n"
                  f"3️⃣ Important: After completing the payment, please send us a confirmation screenshot or payment receipt via chat with {proof_contact} so we can approve your access.\n\n"
                  "💡 Note: If you need help or have any questions, feel free to reach out!",
        Lang.RUS: "✨ Как получить доступ к нашему закрытому каналу через британский банковский перевод ✨\n\n"
                    "Чтобы присоединиться к нашему закрытому каналу и получить доступ к эксклюзивным материалам, выполните следующие шаги:\n\n"
                    "1️⃣ Нажмите кнопку 'Подключиться к каналу' ниже, чтобы подать заявку на доступ.\n\n"
                    "2️⃣ Завершите оплату, используя следующие данные для британского банковского перевода:\n\n"
                    "💳 Детали британского банковского перевода:\n"
                    "- Название компании: PREMIUM CENTER LTD\n"
                    "- Сортировочный код: 80-22-60\n"
                    "- Номер счета: 17831966\n\n"
                    "💡 Пожалуйста, обязательно укажите свой Telegram-логин (например, @username) в сообщении к платежу.\n\n"
                    f"💶 Месячная подписка составляет {amount_monthly} EUR, годовая подписка — {amount_yearly} EUR.\n\n"
                    f"3️⃣ Важно: После завершения оплаты отправьте нам подтверждение или квитанцию о платеже через чат с {proof_contact}, чтобы мы могли подтвердить ваш доступ.\n\n"
                    "💡 Примечание: Если у вас есть вопросы, не стесняйтесь обращаться к нам!",
        Lang.ESP: "✨ Cómo obtener acceso a nuestro canal privado a través de transferencia bancaria en el Reino Unido ✨\n\n"
                    "Para unirte a nuestro canal privado y acceder a contenido exclusivo, sigue estos pasos:\n\n"
                    "1️⃣ Haz clic en el botón 'Unirse al canal' abajo para solicitar acceso.\n\n"
                    "2️⃣ Completa el pago utilizando los detalles de la transferencia bancaria en el Reino Unido a continuación:\n\n"
                    "💳 Detalles de la transferencia bancaria en el Reino Unido:\n"
                    "- Nombre de la empresa: PREMIUM CENTER LTD\n"
                    "- Código de clasificación: 80-22-60\n"
                    "- Número de cuenta: 17831966\n\n"
                    "💡 Asegúrate de incluir tu nombre de usuario de Telegram (por ejemplo, @username) en el mensaje de pago.\n\n"
                    f"💶 La suscripción mensual es de {amount_monthly} EUR, y la suscripción anual es de {amount_yearly} EUR.\n\n"
                    f"3️⃣ Importante: Después de completar el pago, envíanos una captura de pantalla o recibo de confirmación a través del chat con {proof_contact} para que podamos aprobar tu acceso.\n\n"
                    "💡 Nota: Si necesitas ayuda o tienes alguna pregunta, no dudes en contactarnos!",
        Lang.DEU: "✨ Wie Sie Zugang zu unserem privaten Kanal über britische Banküberweisung erhalten ✨\n\n"
                    "Um unserem privaten Kanal beizutreten und exklusiven Zugang zu erhalten, befolgen Sie diese Schritte:\n\n"
                    "1️⃣ Klicken Sie unten auf die Schaltfläche 'Kanal beitreten', um den Zugang zu beantragen.\n\n"
                    "2️⃣ Schließen Sie die Zahlung mit den folgenden Daten für die britische Banküberweisung ab:\n\n"
                    "💳 Details der britischen Banküberweisung:\n"
                    "- Firmenname: PREMIUM CENTER LTD\n"
                    "- Sortiercode: 80-22-60\n"
                    "- Kontonummer: 17831966\n\n"
                    "💡 Bitte geben Sie in der Zahlungsnachricht unbedingt Ihren Telegram-Benutzernamen an (z. B. @username).\n\n"
                    f"💶 Das monatliche Abonnement kostet {amount_monthly} EUR, das Jahresabonnement {amount_yearly} EUR.\n\n"
                    f"3️⃣ Wichtig: Nach Abschluss der Zahlung senden Sie uns bitte einen Bestätigung-Screenshot oder die Zahlungsquittung über den Chat mit {proof_contact}, damit wir Ihren Zugang freischalten können.\n\n"
                    "💡 Hinweis: Wenn Sie Hilfe benötigen oder Fragen haben, zögern Sie nicht, uns zu kontaktieren!",
        Lang.FRA: "✨ Comment obtenir l'accès à notre chaîne privée via un virement bancaire au Royaume-Uni ✨\n\n"
                    "Pour rejoindre notre chaîne privée et accéder à du contenu exclusif, suivez ces étapes :\n\n"
                    "1️⃣ Cliquez sur le bouton 'Rejoindre le canal' ci-dessous pour demander l'accès.\n\n"
                    "2️⃣ Complétez le paiement en utilisant les détails du virement bancaire au Royaume-Uni ci-dessous :\n\n"
                    "💳 Détails du virement bancaire au Royaume-Uni :\n"
                    "- Nom de l'entreprise : PREMIUM CENTER LTD\n"
                    "- Code de tri : 80-22-60\n"
                    "- Numéro de compte : 17831966\n\n"
                    "💡 Assurez-vous d'indiquer votre nom d'utilisateur Telegram (par exemple, @username) dans le message de paiement.\n\n"
                    f"💶 L'abonnement mensuel est de {amount_monthly} EUR, et l'abonnement annuel est de {amount_yearly} EUR.\n\n"
                    f"3️⃣ Important : Après avoir effectué le paiement, envoyez-nous une capture d'écran de confirmation ou le reçu de paiement via le chat avec {proof_contact} afin que nous puissions approuver votre accès.\n\n"
                    "💡 Remarque : Si vous avez besoin d'aide ou si vous avez des questions, n'hésitez pas à nous contacter !",
        Lang.ARA: "✨ كيفية الحصول على الوصول إلى قناتنا الخاصة عبر تحويل بنكي في المملكة المتحدة ✨\n\n"
                    "للانضمام إلى قناتنا الخاصة والحصول على محتوى حصري، اتبع هذه الخطوات:\n\n"
                    "1️⃣ اضغط على زر 'انضم إلى القناة' أدناه لطلب الوصول.\n\n"
                    "2️⃣ أكمل الدفع باستخدام تفاصيل التحويل البنكي في المملكة المتحدة أدناه:\n\n"
                    "💳 تفاصيل التحويل البنكي في المملكة المتحدة:\n"
                    "- اسم الشركة: PREMIUM CENTER LTD\n"
                    "- رمز التصنيف: 80-22-60\n"
                    "- رقم الحساب: 17831966\n\n"
                    "💡 يرجى التأكد من تضمين اسم المستخدم الخاص بك على Telegram (على سبيل المثال، @username) في رسالة الدفع.\n\n"
                    f"💶 الاشتراك الشهري هو {amount_monthly} يورو، والاشتراك السنوي هو {amount_yearly} يورو.\n\n"
                    f"3️⃣ مهم: بعد إتمام الدفع، يرجى إرسال لقطة شاشة أو إيصال الدفع عبر الدردشة مع {proof_contact} حتى نتمكن من الموافقة على وصولك.\n\n"
                    "💡 ملاحظة: إذا كنت بحاجة إلى مساعدة أو لديك أي استفسارات، لا تتردد في الاتصال بنا !",
        Lang.CHI: "✨ 如何通过英国银行转账获取我们私密频道的访问权限 ✨\n\n"
                    "要加入我们的私密频道并访问独家内容，请按照以下简单步骤操作：\n\n"
                    "1️⃣ 点击下方的'加入频道'按钮申请访问权限。\n\n"
                    "2️⃣ 使用以下英国银行转账数据完成付款：\n\n"
                    "💳 英国银行转账数据：\n"
                    "- 公司名称：PREMIUM CENTER LTD\n"
                    "- 分类代码：80-22-60\n"
                    "- 账号：17831966\n\n"
                    "💡 请确保在付款信息中包含您的 Telegram 用户名（例如，@username）。\n\n"
                    f"💶 月度订阅费为 {amount_monthly} 欧元，年度订阅费为 {amount_yearly} 欧元。\n\n"
                    f"3️⃣ 重要提示：付款完成后，请通过与 {proof_contact} 的聊天发送确认截图或付款收据，以便我们批准您的访问权限。\n\n"
                    "💡 注意：如果您需要帮助或有任何问题，请随时联系我们！",
        Lang.HIN: "✨ यूके बैंक ट्रांसफर के माध्यम से हमारे निजी चैनल तक पहुंचने का तरीका ✨\n\n"
                    "हमारे निजी चैनल में शामिल होने और विशेष सामग्री तक पहुंचने के लिए, निम्नलिखित सरल कदमों का पालन करें:\n\n"
                    "1️⃣ नीचे 'चैनल से जुड़ें' बटन पर क्लिक करके पहुंच के लिए अनुरोध करें।\n\n"
                    "2️⃣ यूके बैंक ट्रांसफर विवरण का उपयोग करके भुगतान पूरा करें:\n\n"
                    "💳 यूके बैंक ट्रांसफर विवरण:\n"
                    "- कंपनी का नाम: PREMIUM CENTER LTD\n"
                    "- सॉर्ट कोड: 80-22-60\n"
                    "- खाता संख्या: 17831966\n\n"
                    "💡 कृपया भुगतान संदेश में अपना Telegram उपयोगकर्ता नाम (उदाहरण के लिए, @username) शामिल करें।\n\n"
                    f"💶 मासिक सदस्यता {amount_monthly} यूरो है, और वार्षिक सदस्यता {amount_yearly} यूरो है।\n\n"
                    f"3️⃣ महत्वपूर्ण: भुगतान पूरा करने के बाद, कृपया हमें {proof_contact} के साथ चैट के माध्यम से पुष्टि स्क्रीनशॉट या भुगतान रसीद भेजें ताकि हम आपके पहुंच को स्वीकृत कर सकें।\n\n",
        Lang.JPN: "✨ イギリスの銀行振込を利用して当社のプライベートチャンネルにアクセスする方法 ✨\n\n"
                    "当社のプライベートチャンネルに参加し、独占コンテンツにアクセスするには、次の簡単な手順に従ってください：\n\n"
                    "1️⃣ 下の「チャンネルに参加」ボタンをクリックしてアクセスをリクエストします。\n\n"
                    "2️⃣ 以下のイギリスの銀行振込詳細を使用して支払いを完了します：\n\n"
                    "💳 イギリスの銀行振込詳細：\n"
                    "- 会社名：PREMIUM CENTER LTD\n"
                    "- ソートコード：80-22-60\n"
                    "- アカウント番号：17831966\n\n"
                    "💡 支払いメッセージにTelegramユーザー名（例：@username）を必ず含めてください。\n\n"
                    f"💶 月額サブスクリプションは{amount_monthly}ユーロで、年間サブスクリプションは{amount_yearly}ユーロです。\n\n"
                    f"3️⃣ 重要：支払いを完了した後、{proof_contact} とのチャットで確認スクリーンショットまたは支払いレシートを送信していただくと、アクセスを承認できます。\n\n"
                    "💡 注意：お手伝いが必要な場合やご質問がある場合は、お気軽にお問い合わせください！"
    }

    selected_lang = dialog_manager.start_data.get("lang", Lang.ENG)
    return {"description": lang_messages.get(selected_lang)}


def create_bank_payment_window():
    return [
        Window(Format("{description}"),
            *create_payment_buttons_group(F),
            getter=get_bank_payment_description,
            state=PaymentStatesGroup.BANK)
    ]

def create_revolut_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_revolut_payment_description,
               state=PaymentStatesGroup.REVOLUT)
    ]

def create_paypal_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_paypal_payment_description,
               state=PaymentStatesGroup.PAYPAL)
    ]

def create_uk_bank_payment_window():
    return [
        Window(Format("{description}"),
               *create_payment_buttons_group(F),
               getter=get_uk_bank_payment_description,
               state=PaymentStatesGroup.UK_BANK)
    ]