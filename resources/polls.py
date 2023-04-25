from handlers import dp


async def send_poll(chat_id: int, question: str, options: list[str]):
    poll = await dp.bot.send_poll(
        chat_id=chat_id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False
    )
    return poll

