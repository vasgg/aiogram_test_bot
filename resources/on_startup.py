from aiogram import types

from config import bot


async def set_up(dp):
    bot_commands = [
        types.BotCommand(command="/start", description="Let's begin with this command"),
        types.BotCommand(command="/poll", description="Create group poll")
    ]
    await bot.set_my_commands(bot_commands)
