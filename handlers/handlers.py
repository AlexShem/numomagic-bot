from action import Action
from logger.logger import get_logger, get_csv_logger
from datetime import date

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from lang import Lang
import energy
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates, JoinChannelStatesGroup, \
    PaymentStatesGroup, SubscribeStatesGroup

logger = get_logger(__name__)
action_logger = get_csv_logger()


# This function is called when the user starts the bot.
async def start(message: Message, dialog_manager: DialogManager):
    logger.warning(f"User {message.from_user.username} started the bot")
    action_logger.info(Action("start", message.from_user))
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)


# This function is called when the user selects a language.
async def on_lang_selected(callback: CallbackQuery, button: Button, manager: DialogManager):
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

    selected_language = manager.dialog_data["lang"]
    logger.warning(f"User {callback.from_user.username} selected language {selected_language}")
    action_logger.info(Action("on_lang_selected", callback.from_user, extra=selected_language.value))
    await manager.switch_to(DialogSG.CALENDAR)


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
    action_logger.info(Action("on_date_selected", callback.from_user, extra=str(selected_date)))

    if len(prepared_answer) == 4:
        await manager.start(FourDigitsStates.PERIOD1, data=dialog_data)
    elif len(prepared_answer) == 5:
        await manager.start(FiveDigitsStates.PERIOD1, data=dialog_data)
    else:
        await manager.start(SixDigitsStates.PERIOD1, data=dialog_data)


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
    await manager.start(JoinChannelStatesGroup.MAIN, data=manager.start_data)

# TODO: Remove "Other Payment" this feature
async def on_another_payment_button(callback: CallbackQuery, button, manager: DialogManager):
    logger.warning(f"User {callback.from_user.username} selected another payment method")
    await manager.start(PaymentStatesGroup.BANK, data=manager.start_data)



# Subscribe dialog handler ------------------------------------------------

async def on_subscribe_command(message: Message, dialog_manager: DialogManager):
    """Handle /subscribe command and start the subscribe dialog"""
    # Get user language from their Telegram settings or default to English
    user_lang = Lang.ENG
    if hasattr(message.from_user, 'language_code') and message.from_user.language_code:
        lang_code = message.from_user.language_code.lower()
        lang_mapping = {
            'en': Lang.ENG, 'ru': Lang.RUS, 'de': Lang.DEU, 'es': Lang.ESP,
            'fr': Lang.FRA, 'ar': Lang.ARA, 'zh': Lang.CHI, 'hi': Lang.HIN, 'ja': Lang.JPN
        }
        user_lang = lang_mapping.get(lang_code, Lang.ENG)
        # Try prefix match for codes like 'en-US'
        if user_lang == Lang.ENG and lang_code not in lang_mapping:
            for code, lang in lang_mapping.items():
                if lang_code.startswith(code):
                    user_lang = lang
                    break

    logger.info(f"User {message.from_user.id} requested subscription in language {user_lang.value}")
    await dialog_manager.start(SubscribeStatesGroup.MAIN, data={"lang": user_lang})


# Common close button handler -----------------------------------------------

async def on_close_dialog(callback: CallbackQuery, button, manager: DialogManager):
    await manager.done()
