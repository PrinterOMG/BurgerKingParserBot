import asyncio

import aioschedule
from aiogram import Bot

from tgbot.config import Config
from tgbot.services.schedulers.send_dates import send_dates


async def start_schedulers(bot: Bot, config: Config, bk_parser, state):
    aioschedule.every(300).seconds.do(send_dates, bot, bk_parser, config, state)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
