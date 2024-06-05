from aiogram.fsm.state import StatesGroup, State


class AnalysisState(StatesGroup):
    start = State()
    year = State()
    month = State()
    day = State()