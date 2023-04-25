from aiogram import types
from aiogram.dispatcher import FSMContext

from config import dp
from resources.currency_codes import curency_code
from resources.exchange import get_currency_code, get_exchange_rate_from_message
from resources.keyboards import menu
from resources.replies import answer
from resources.states import States


@dp.callback_query_handler(text='exchange')
async def currency_exchange(call: types.CallbackQuery) -> None:
    await dp.bot.send_message(chat_id=call.from_user.id, text=answer['exchange_code_reply'])
    await States.first_currency.set()
    await call.answer()


@dp.message_handler(state=States.first_currency)
async def first_code_check(message: types.Message, state: FSMContext) -> None:
    try:
        code = message.text.upper()
        first_code = await get_currency_code(code)
        await state.update_data(first_code=first_code)
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text=answer['exchange_amount_reply'].format(curency_code[first_code], first_code))
        await States.amount.set()
    except Exception:
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['exchange_code_error'])


@dp.message_handler(state=States.amount)
async def get_amount(message: types.Message, state: FSMContext) -> None:
    try:
        amount = float(message.text)
        async with state.proxy() as data:
            first_code = data["first_code"]
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['amount_reply'].format(amount, first_code))
        await state.update_data(amount=amount)
        await States.second_currency.set()
    except ValueError:
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['exchange_amount_error'])


@dp.message_handler(state=States.second_currency)
async def second_code_check(message: types.Message, state: FSMContext) -> None:
    try:
        code = message.text.upper()
        second_code = await get_currency_code(code)
        async with state.proxy() as data:
            first_code = data["first_code"]
            amount = data["amount"]
        result: ExchangeResult = await get_exchange_rate_from_message(first_code=first_code, second_code=second_code, amount=amount)
        response = answer['exchange_reply'].format(curency_code[result.first_code], curency_code[result.second_code], result.amount,
                                                   result.first_code, result.result_amount, second_code, result.first_code,
                                                   result.conversion_rate, second_code)
        await state.reset_state(with_data=True)
        await dp.bot.send_message(chat_id=message.from_user.id, text=response, reply_markup=menu)
    except Exception:
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['exchange_code_error'])
