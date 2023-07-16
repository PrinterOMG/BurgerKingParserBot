from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()
