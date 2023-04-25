from aiogram import executor
from resources.on_startup import set_up
from handlers import dp


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_up)
