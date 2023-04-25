from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import ChatNotFound

from config import dp
from resources.poll import send_poll
from resources.replies import answer
from resources.states import States


@dp.message_handler(Command('poll'))
async def start_command(message: types.Message) -> None:
    await message.answer(text=answer['poll_question_reply'])
    await States.enter_question.set()


@dp.message_handler(state=States.enter_question)
async def get_question(message: types.Message, state: FSMContext) -> None:
    question = message.text
    # check poll question lenght limitation
    if len(question) <= 300:
        await state.update_data(question=question)
        await message.answer(text=answer['poll_answers_reply'])
        await States.enter_options.set()
    else:
        await message.answer(text=answer['poll_question_error_reply'])


@dp.message_handler(state=States.enter_options)
async def get_options(message: types.Message, state: FSMContext) -> None:
    options = message.text.strip(",").split(",")
    options = [option.strip() for option in options]
    # check poll options limitation
    if len(options) == 1 or len(options) > 10 or '' in options or any(len(option) > 100 for option in options):
        await message.answer(text=answer['poll_answers_error_reply'])
    else:
        await state.update_data(options=options)
        # in private chat we need to ask group id
        if message.chat.type != types.ChatType.PRIVATE:
            chat_id = message.chat.id
            async with state.proxy() as data:
                question = data["question"]
                options = data["options"]
            poll = await send_poll(chat_id, question, options)
            chat = await dp.bot.get_chat(chat_id)
            await dp.bot.send_message(chat_id=message.from_user.id, text=answer['poll_sent_reply'].format(question, chat.title, chat_id))
            await state.reset_state(with_data=True)
        else:
            await dp.bot.send_message(chat_id=message.from_user.id, text=answer['poll_select_group_reply'])
            await States.enter_group_id.set()


@dp.message_handler(state=States.enter_group_id)
async def get_chat_id(message: types.Message, state: FSMContext) -> None:
    # group id always starts with minus
    chat_id = message.text if message.text.startswith('-') else '-' + str(message.text)
    async with state.proxy() as data:
        question = data["question"]
        options = data["options"]
    try:
        poll = await send_poll(chat_id, question, options)
        chat = await dp.bot.get_chat(chat_id)
        await dp.bot.send_message(chat_id=message.from_user.id, text=answer['poll_sent_reply'].format(question, chat.title, chat_id))
        await state.reset_state(with_data=True)
    except ChatNotFound:
        await message.answer(text=answer['send_poll_error_reply'])
