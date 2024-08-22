from aiogram.dispatcher.filters.state import StatesGroup, State

API = "7326073877:AAHhgwb7n6mbZOLcUZeYhj2GxXwTT6DeZVM"

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

