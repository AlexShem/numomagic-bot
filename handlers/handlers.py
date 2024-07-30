from datetime import date

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

import users
import energy
from states.state_group import DialogSG, FiveDigitsStates, FourDigitsStates, SixDigitsStates


def prepare_user_energy_output(energy_levels):
    # Converts range strings like "1-5" or "5-10" to list
    def to_range(rng):
        if not "-" in rng:
            return list([int(rng)])
        start, end = map(int, rng.split("-"))
        range_object = range(start, end + 1)
        range_list = list(range_object)
        return range_list

    energy_level_dictionary = energy.load(len(energy_levels))
    result = list()
    for i, (time_period, items) in enumerate(energy_level_dictionary.items()):
        for energy_value, description in items.items():
            if energy_levels[i] in to_range(energy_value):
                result.append(f"Рекомендация в период времени: {time_period}\n"
                              f"{description}")
    return result


async def start(message: Message, dialog_manager: DialogManager):
    if users.get(message.from_user.id) is None:
        users.add(message.from_user.id, message.from_user.username)
    await dialog_manager.start(DialogSG.MAIN, mode=StartMode.RESET_STACK)


async def on_trial(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    user = users.get(callback.from_user.id)
    if user is None:
        await callback.message.answer("Please restart a bot")
    else:
        user.start_trial()
        await manager.switch_to(DialogSG.ANALYSIS)


async def on_premium(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    user = users.get(callback.from_user.id)
    if user is None:
        await callback.message.answer("Please restart a bot")
    else:
        user.pay()
        await manager.switch_to(DialogSG.ANALYSIS)


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    manager.dialog_data["name"] = selected_date
    energy_levels = energy.get_energy_levels(selected_date.year, selected_date.month, selected_date.day)
    prepared_answer = prepare_user_energy_output(energy_levels)
    dialog_data = {f"period_{i + 1}": text for i, text in enumerate(prepared_answer)}
    if len(prepared_answer) == 4:
        await manager.start(FourDigitsStates.PERIOD1, data=dialog_data)
    elif len(prepared_answer) == 5:
        await manager.start(FiveDigitsStates.PERIOD1, data=dialog_data)
    else:
        await manager.start(SixDigitsStates.PERIOD1, data=dialog_data)


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
