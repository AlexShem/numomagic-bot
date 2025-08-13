from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Case, Const
from magic_filter import F

from handlers.handlers import on_close_dialog
from lang import Lang
from states.state_group import SubscribeStatesGroup

def create_subscribe_window(premium_channel_link: str = "https://t.me/+76i6XCTJtXQxZjFk"):
    return Window(
        Case(
            {
                Lang.ENG: Const(
                    "🔐 Subscribe to unlock the bot\n\n"
                    f"Join our premium channel for 1000 Stars:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "After paying with Stars, you'll be added automatically and can use all bot features."
                ),
                Lang.RUS: Const(
                    "🔐 Подпишитесь, чтобы разблокировать бота\n\n"
                    f"Присоединяйтесь к нашему премиум каналу за 1000 звезд:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "После оплаты звездами вы будете автоматически добавлены и сможете использовать все функции бота."
                ),
                Lang.DEU: Const(
                    "🔐 Abonnieren Sie, um den Bot freizuschalten\n\n"
                    f"Treten Sie unserem Premium-Kanal für 1000 Sterne bei:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "Nach der Zahlung mit Sternen werden Sie automatisch hinzugefügt und können alle Bot-Funktionen nutzen."
                ),
                Lang.ESP: Const(
                    "🔐 Suscríbete para desbloquear el bot\n\n"
                    f"Únete a nuestro canal premium por 1000 estrellas:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "Después de pagar con estrellas, serás agregado automáticamente y podrás usar todas las funciones del bot."
                ),
                Lang.FRA: Const(
                    "🔐 Abonnez-vous pour débloquer le bot\n\n"
                    f"Rejoignez notre chaîne premium pour 1000 étoiles :\n"
                    f"💫 {premium_channel_link}\n\n"
                    "Après avoir payé avec des étoiles, vous serez ajouté automatiquement et pourrez utiliser toutes les fonctionnalités du bot."
                ),
                Lang.ARA: Const(
                    "🔐 اشترك لفتح البوت\n\n"
                    f"انضم إلى قناتنا المميزة مقابل 1000 نجمة:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "بعد الدفع بالنجوم، ستتم إضافتك تلقائياً ويمكنك استخدام جميع ميزات البوت."
                ),
                Lang.CHI: Const(
                    "🔐 订阅以解锁机器人\n\n"
                    f"加入我们的高级频道，需要1000颗星星:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "用星星支付后，您将自动添加并可以使用所有机器人功能。"
                ),
                Lang.HIN: Const(
                    "🔐 बॉट को अनलॉक करने के लिए सब्सक्राइब करें\n\n"
                    f"1000 स्टार्स के लिए हमारे प्रीमियम चैनल में शामिल हों:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "स्टार्स से भुगतान के बाद, आप स्वचालित रूप से जोड़े जाएंगे और सभी बॉट सुविधाओं का उपयोग कर सकेंगे।"
                ),
                Lang.JPN: Const(
                    "🔐 ボットのロックを解除するために購読してください\n\n"
                    f"1000スターでプレミアムチャンネルに参加:\n"
                    f"💫 {premium_channel_link}\n\n"
                    "スターで支払った後、自動的に追加され、すべてのボット機能を使用できます。"
                )
            },
            selector=F["start_data"]["lang"],  # Use start_data instead of dialog_data
        ),
        Button(
            Case(
                {
                    Lang.ENG: Const("❌ Close"),
                    Lang.RUS: Const("❌ Закрыть"),
                    Lang.DEU: Const("❌ Schließen"),
                    Lang.ESP: Const("❌ Cerrar"),
                    Lang.FRA: Const("❌ Fermer"),
                    Lang.ARA: Const("❌ إغلاق"),
                    Lang.CHI: Const("❌ 关闭"),
                    Lang.HIN: Const("❌ बंद करें"),
                    Lang.JPN: Const("❌ 閉じる")
                },
                selector=F["start_data"]["lang"],  # Use start_data instead of dialog_data
            ),
            id="close",
            on_click=on_close_dialog
        ),
        state=SubscribeStatesGroup.MAIN
    )

# For backward compatibility
subscribe_window = create_subscribe_window()
