from aiogram import types
from resources.replies import answer
from aiogram.dispatcher import FSMContext

from config import dp
from resources.weather import get_weather_from_location
from resources.keyboards import menu
from resources.states import States


@dp.message_handler(content_types='location', state="*")
async def handle_location(message: types.Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    try:
        weather: Weather = await get_weather_from_location(latitude=latitude, longitude=longitude)
        reply = answer['location_reply'].format(weather.info, weather.temp)
        await dp.bot.send_message(chat_id=message.from_user.id, text=reply, reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state()
    except Exception:
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['error_fetch_weather_by_location'], reply_markup=menu)
        await state.reset_state()



