from aiogram import types

from config import bot


async def set_up(dp):
    '''setting bot commands'''
    bot_commands = [
        types.BotCommand(command="/start", description="Initial command"),
        types.BotCommand(command="/poll", description="Create group poll")
    ]
    await bot.set_my_commands(bot_commands)
