from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    start = State()
    update_marks = State()
