from aiogram.fsm.state import StatesGroup, State


class Birthday(StatesGroup):
    year = State()
    month = State()
    day = State()