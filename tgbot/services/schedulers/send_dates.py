import logging
from pprint import pprint

import aioredis
from aiogram import Bot
from aiogram.dispatcher import FSMContext

from tgbot.config import Config
from tgbot.keyboards import inline_keyboards
from tgbot.services.bk_parser.parser import BurgerKingParser


async def send_dates(bot: Bot, bk_parser: BurgerKingParser, config: Config, state: FSMContext):
    restaurants = await bk_parser.parse_restaurants_dates()
    data = await state.get_data()
    for rest in restaurants:
        saved_dates = data.get(str(rest))
        if saved_dates is None:
            data[rest] = list()
            saved_dates = list()
        for date in restaurants[rest]['dates']:
            if date['disabled']:
                continue

            if saved_dates and date['date'] in saved_dates:
                continue

            data[rest].append(date['date'])

            for admin in config.bot.admin_ids:
                await bot.send_message(chat_id=admin, text=f'Проверка в ресторане {restaurants[rest]["name"]} на дату {date["date"]}')
        await state.set_data(data)
