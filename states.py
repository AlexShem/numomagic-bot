from aiogram.fsm.state import StatesGroup, State


class AnalysisState(StatesGroup):
    year = State()
    month = State()
    day = State()