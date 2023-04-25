import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
weather_apikey = os.getenv("OPEN_WEATHER_TOKEN")
exchange_apikey = os.getenv("EXCHANGERATE_API_TOKEN")
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&lang=ru&units=metric'
RANDOM_PIC_URL = 'https://random-d.uk/api/random'
EXCHANGE_RATE_URL = 'https://v6.exchangerate-api.com/v6/{}/pair/{}/{}/{}'
