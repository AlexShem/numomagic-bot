import calendar

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

import users
import energy_dict
import energy
from keyboards import create_month_buttons, create_mode_buttons, create_analysis_button
from states import AnalysisState

router = Router()


@router.message(lambda message: message.text == "/start")
async def send_welcome(message: types.Message):
    if users.get(message.from_user.id) is None:
        users.add(message.from_user.id, message.from_user.username)
    await message.answer("Welcome to our bot! Please choose an option:", reply_markup=create_mode_buttons())


@router.callback_query(F.data == "pay")
async def pay(callback: types.CallbackQuery):
    user = users.get(callback.from_user.id)
    if user is None:
        await callback.message.answer("Please restart a bot")
    else:
        user.pay()
        await callback.message.answer("Subscription is successfully activated! Now you can analyze your energy level", reply_markup=create_analysis_button())


@router.callback_query(F.data == "trial")
async def start_trial(callback: types.CallbackQuery, state: FSMContext):
    user = users.get(callback.from_user.id)
    if user is None:
        await callback.message.answer("Please restart a bot")
    else:
        if user.start_trial() is True:
            await callback.message.answer("Trial started! Now you can analyze your energy level.",
                                          reply_markup=create_analysis_button())
        else:
            await callback.message.answer("You have already started a trial.",
                                          reply_markup=create_analysis_button())


@router.callback_query(F.data == "analyze")
async def analyze(callback: types.CallbackQuery, state: FSMContext):
    user = users.get(callback.from_user.id)
    if user.is_legal():
        await state.set_state(AnalysisState.year)
        await callback.message.answer("Please enter a year:")
    else:
        await callback.message.answer("Your trial period is expired or you have not started it yet.")


@router.message(AnalysisState.year)
async def process_year(message: types.Message, state: FSMContext):
    year = message.text.strip()
    try:
        year = int(year)
    except:
        return await message.answer("Invalid year please try again")
    if year < 1930:
        return await message.answer("Invalid year please try again")
    await state.update_data(year=year)
    await state.set_state(AnalysisState.month)
    await message.answer("Enter a month", reply_markup=create_month_buttons())


@router.callback_query(F.data.startswith("month"),
                       AnalysisState.month)
async def handle_month_callback(callback: types.CallbackQuery, state: FSMContext):
    month = callback.data[len("month_"):]
    month = list(calendar.month_name).index(month)
    await state.update_data(month=month)
    await state.set_state(AnalysisState.day)
    await callback.message.answer("Enter a day: ")


def prepare_user_energy_output(energy_levels):
    # Converts range strings like "1-5" or "5-10" to list
    def to_range(rng):
        if not "-" in rng:
            return list([int(rng)])
        start, end = map(int, rng.split("-"))
        range_object = range(start, end + 1)
        range_list = list(range_object)
        return range_list

    energy_level_dictionary = energy_dict.load(len(energy_levels))
    result = ""
    for i, (time_period, items) in enumerate(energy_level_dictionary.items()):
        for energy_value, description in items.items():
            if energy_levels[i] in to_range(energy_value):
                result += (f"Рекомендация в период времени: {time_period}\n"
                           f"{description}\n"
                           f"-------------------------------\n")
    return result


@router.message(AnalysisState.day)
async def process_day(message: types.Message, state: FSMContext):
    day = message.text.strip()
    try:
        day = int(day)
    except:
        return await message.answer("Invalid date, please try again")
    data = await state.get_data()
    year = data.get("year")
    month = data.get("month")
    _, days_num = calendar.monthrange(year, month)
    if day < 1 or day > days_num:
        return await message.answer("Invalid date, please try again")
    energy_levels = energy.get_energy_levels(year, month, day)
    answer = prepare_user_energy_output(energy_levels)
    await message.answer(answer, reply_markup=create_analysis_button())
