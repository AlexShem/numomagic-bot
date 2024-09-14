from logger.logger import get_logger
from datetime import date

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from lang import Lang
import energy
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates, JoinChannelStatesGroup, \
    PaymentStatesGroup

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


# Common close button handler -----------------------------------------------

async def on_close_dialog(callback: CallbackQuery, button, manager: DialogManager):
    await manager.done()