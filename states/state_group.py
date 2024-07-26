from aiogram.fsm.state import State, StatesGroup


class DialogSG(StatesGroup):
    MAIN = State()
    ANALYSIS = State()
    CALENDAR = State()
    RESULT = State()