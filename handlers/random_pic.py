from aiogram import types

from config import dp
from resources.keyboards import menu
from resources.random_pic import get_random_pic
from resources.replies import answer


@dp.callback_query_handler(text='random_pic')
async def random_pic_send(call: types.CallbackQuery) -> None:
    try:
        await dp.bot.send_photo(chat_id=call.message.chat.id, photo=(await get_random_pic()), reply_markup=menu)
        await call.answer()
    except Exception:
        await dp.bot.send_message(chat_id=call.from_user.id, text=answer['error_fetch_pic'], reply_markup=menu)
