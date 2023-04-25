from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

weather = InlineKeyboardButton(text='Погода', callback_data='weather')
exchange = InlineKeyboardButton(text='Конвертер валют', callback_data='exchange')
random_pic = InlineKeyboardButton(text='Картинка', callback_data='random_pic')

menu = InlineKeyboardMarkup(row_width=1).add(weather, exchange, random_pic)


provide_location_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
provide_location_button.insert(KeyboardButton(text='Отправить геопозицию', request_location=True))
