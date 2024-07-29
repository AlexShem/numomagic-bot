from aiogram.fsm.state import State, StatesGroup, StatesGroupMeta


class DialogSG(StatesGroup):
    MAIN = State()
    ANALYSIS = State()
    CALENDAR = State()


class FourDigitsStates(StatesGroup):
    STATE1 = State()
    STATE2 = State()
    STATE3 = State()
    STATE4 = State()
