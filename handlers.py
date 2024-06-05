import calendar
from datetime import datetime

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_marked_list

import db
import energy
from keyboards import create_month_buttons, create_mode_buttons, create_analysis_button
from states import Birthday

router = Router()


@router.message(lambda message: message.text == "/start")
async def send_welcome(message: types.Message):
    db.add_new_user(message.from_user.id)
    await message.answer("Welcome to our bot! Please choose an option:", reply_markup=create_mode_buttons())


@router.callback_query(F.data == "trial")
async def start_trial(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if user.trial_period_start is None:
        user.trial_period_start = datetime.now()
        await callback.message.answer("Trial started! Now you can analyze your energy level.",
                                      reply_markup=create_analysis_button())
    else:
        await callback.message.answer("You have already started a trial.")


@router.callback_query(F.data == "analyze")
async def analyze(callback: types.CallbackQuery, state: FSMContext):
    user = db.get_user(callback.from_user.id)
    if user.is_legal():
        await state.set_state(Birthday.year)
        await callback.message.answer("Please enter your birth year:")
    else:
        await callback.message.answer("Your trial period is expired or you have not started it yet.")


@router.message(Birthday.year)
async def process_name(message: types.Message, state: FSMContext):
    year = message.text.strip()
    user = db.get_user(message.from_user.id)
    try:
        year = int(year)
    except:
        return await message.answer("Invalid year please try again")
    if year < 1930 or year > 2020:
        return await message.answer("Invalid year please try again")
    user.year = year
    await message.answer("Please enter your birth month", reply_markup=create_month_buttons())


@router.callback_query(F.data.startswith("month"))
async def handle_month_callback(callback: types.CallbackQuery, state: FSMContext):
    user = db.get_user(callback.from_user.id)
    month = callback.data[len("month_"):]
    print(month)
    print(list(calendar.month_name))
    month = list(calendar.month_name).index(month)
    user.month = month
    await state.set_state(Birthday.day)
    await callback.message.answer("Please enter your birth day: ")


@router.message(Birthday.day)
async def process_birthday(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    day = message.text.strip()
    try:
        day = int(day)
    except:
        return await message.answer("Invalid date, please try again")
    _, days_num = calendar.monthrange(user.year, user.month)
    if day < 1 or day > days_num:
        return await message.answer("Invalid date, please try again")
    user.day = day
    nrg = energy.calc_energy(user)
    answer = energy.create_string_from_energy_chart(nrg)
    await message.answer(answer, parse_mode=ParseMode.HTML)


