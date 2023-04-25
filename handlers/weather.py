from aiogram import types
from aiogram.dispatcher import FSMContext

from config import dp
from resources.weather import Weather, get_weather_from_message
from resources.keyboards import menu, provide_location_button
from resources.replies import answer
from resources.states import States


@dp.callback_query_handler(text='weather')
async def weather_section(call: types.CallbackQuery) -> None:
    await dp.bot.send_message(chat_id=call.message.chat.id, text=answer['input_city_reply'],reply_markup=provide_location_button)
    await States.weather_city_input.set()
    await call.answer()


@dp.message_handler(state=States.weather_city_input)
async def weather_in_city(message: types.Message, state: FSMContext) -> None:
    try:
        weather: Weather = await get_weather_from_message(message.text)
        reply = answer['weather_reply'].format(weather.city, weather.info, weather.temp)
        await dp.bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=menu)
        await state.reset_state()
    except Exception:
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['error_fetch_weather'])
