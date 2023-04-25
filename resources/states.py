from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    weather_city_input = State()
    first_currency = State()
    amount = State()
    second_currency = State()
    enter_question = State()
    enter_options = State()
    enter_group_id = State()
