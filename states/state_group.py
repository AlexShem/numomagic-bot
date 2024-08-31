from aiogram.fsm.state import State, StatesGroup


class DialogSG(StatesGroup):
    MAIN = State()
    CALENDAR = State()


class FourDigitsStates(StatesGroup):
    PERIOD1 = State()
    PERIOD2 = State()
    PERIOD3 = State()
    PERIOD4 = State()


class FiveDigitsStates(StatesGroup):
    PERIOD1 = State()
    PERIOD2 = State()
    PERIOD3 = State()
    PERIOD4 = State()
    PERIOD5 = State()


class SixDigitsStates(StatesGroup):
    PERIOD1 = State()
    PERIOD2 = State()
    PERIOD3 = State()
    PERIOD4 = State()
    PERIOD5 = State()
    PERIOD6 = State()


class JoinChannelStatesGroup(StatesGroup):
    MAIN = State()
