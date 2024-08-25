from datetime import date

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from lang import Lang
import energy
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates
import logging


logger = logging.getLogger(__name__)

def prepare_user_energy_output(energy_levels, lang: Lang, date: date):
    # Converts range strings like "1-5" or "5-10" to list
    def to_range(rng):
        if not "-" in rng:
            return list([int(rng)])
        start, end = map(int, rng.split("-"))
        range_object = range(start, end + 1)
        range_list = list(range_object)
        return range_list

    energy_level_dictionary = energy.load(len(energy_levels), lang)
    lang_messages = {
        Lang.RUS: "Рекомендация в период времени:",
        Lang.ENG: "Recommendation in the time period:",
        Lang.ESP: "Recomendación en el período de tiempo:",
        Lang.DEU: "Empfehlung im Zeitraum:",
        Lang.FRA: "Recommandation dans la période de temps:",
        Lang.ARA: "توصية في الفترة الزمنية:",
        Lang.CHI: "时间段内的建议:",
        Lang.HIN: "समय अवधि में सिफारिश:",
        Lang.JPN: "期間内の推奨:"
    }

    result = list()
    for i, (time_period, items) in enumerate(energy_level_dictionary.items()):
        for energy_value, description in items.items():
            if energy_levels[i] in to_range(energy_value):
                message = lang_messages.get(lang, "Recommendation in the time period:")
                result.append(f"{message} {time_period} | {date}\n{description}")
    return result


async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)
    logger.warning(f"User {message.from_user.username} started a bot")


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    energy_levels = energy.get_energy_levels(selected_date.year, selected_date.month, selected_date.day)
    lang = manager.dialog_data["lang"]
    prepared_answer = prepare_user_energy_output(energy_levels, lang, selected_date)
    dialog_data = {f"period_{i + 1}": text for i, text in enumerate(prepared_answer)}
    if len(prepared_answer) == 4:
        await manager.start(FourDigitsStates.PERIOD1, data=dialog_data)
    elif len(prepared_answer) == 5:
        await manager.start(FiveDigitsStates.PERIOD1, data=dialog_data)
    else:
        await manager.start(SixDigitsStates.PERIOD1, data=dialog_data)
    logger.warning(f"User {callback.from_user.username} selected date {selected_date} so his energy levels are {energy_levels}")


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
    await manager.switch_to(DialogSG.CALENDAR)
    logger.warning(f"User {callback.from_user.username} selected language {manager.dialog_data['lang']}")



async def close_result_dialog(callback: CallbackQuery, widget, manager: DialogManager):
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