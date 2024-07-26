from aiogram.fsm.state import State, StatesGroup


class DialogSG(StatesGroup):
    MAIN = State()
    ANALYSIS = State()
    YEAR = State()
    MONTH = State()
    DAY = State()