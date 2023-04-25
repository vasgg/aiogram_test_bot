from aiogram import types
from aiogram.dispatcher.filters import Command

from config import dp
from resources.keyboards import menu
from resources.replies import answer
from resources.states import States


@dp.message_handler(Command('start'))
async def start_command(message: types.Message) -> None:
    await message.answer(text=answer['start_reply'], reply_markup=menu)

