from aiogram.dispatcher.filters.state import StatesGroup, State

API = ""

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

